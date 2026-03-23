#!/usr/bin/env bash
# ideate-check-quality.sh — Full quality validation for assembled proposal
#
# Usage:
#   ideate-check-quality.sh <slug> [proposal-dir]
#
# Checks: structure, links, citations, research quality, completeness.
# Returns exit 0 if all pass, exit 1 with report if failures.

set -euo pipefail

SLUG="${1:?Usage: ideate-check-quality.sh <slug> [proposal-dir]}"
PROPOSAL_DIR="${2:-proposal-${SLUG}}"

PASS=0
FAIL=0
WARN=0
REPORT=""

pass() { ((PASS++)); REPORT+="  ✅ $1\n"; }
fail() { ((FAIL++)); REPORT+="  ❌ $1\n"; }
warn() { ((WARN++)); REPORT+="  ⚠️  $1\n"; }

echo "═══════════════════════════════════════════════"
echo "  Quality Check: ${SLUG}"
echo "  Directory: ${PROPOSAL_DIR}/"
echo "═══════════════════════════════════════════════"

# ─── 1. STRUCTURAL CHECKS ──────────────────────────────────────────
echo ""
echo "📋 Structural Checks"

REQUIRED_FILES=(
  "INDEX.md"
  "SUMMARY.md"
  "COMPARISON.md"
  "core/PRD.md"
  "core/OUTCOME.md"
  "core/ASSUMPTIONS.md"
  "research/INDEX.md"
  "research/DOSSIER.md"
  "research/FACT-CHECK.md"
  "research/SOURCES.md"
  "personas/INDEX.md"
  "approaches/INDEX.md"
  "approaches/approach-recommended.md"
  "approaches/TRADEOFF-MATRIX.md"
  "edge-cases/INDEX.md"
  "edge-cases/failure-modes.md"
  "decisions/INDEX.md"
  "meta/OPEN-QUESTIONS.md"
  "meta/GENERATION-LOG.md"
)

for f in "${REQUIRED_FILES[@]}"; do
  if [[ -f "${PROPOSAL_DIR}/${f}" ]] && [[ -s "${PROPOSAL_DIR}/${f}" ]]; then
    pass "${f} exists and non-empty"
  elif [[ -f "${PROPOSAL_DIR}/${f}" ]]; then
    fail "${f} exists but is EMPTY"
  else
    fail "${f} MISSING"
  fi
done

# ─── 2. NAVIGATION CHECKS ──────────────────────────────────────────
echo ""
echo "🔗 Navigation Checks"

# Check breadcrumbs in all markdown files
breadcrumb_total=0
breadcrumb_found=0

while IFS= read -r -d '' mdfile; do
  ((breadcrumb_total++))
  basename_file=$(basename "$mdfile")
  # INDEX.md at root doesn't need a breadcrumb to itself
  if [[ "$basename_file" == "INDEX.md" ]] && [[ "$(dirname "$mdfile")" == "$PROPOSAL_DIR" ]]; then
    ((breadcrumb_found++))
    continue
  fi
  if grep -qE '←.*\[.*\]\(.*\)' "$mdfile" 2>/dev/null; then
    ((breadcrumb_found++))
  fi
done < <(find "${PROPOSAL_DIR}" -name '*.md' -not -name '*.bak' -print0)

if (( breadcrumb_found >= breadcrumb_total * 8 / 10 )); then
  pass "Breadcrumbs: ${breadcrumb_found}/${breadcrumb_total} files have navigation"
else
  fail "Breadcrumbs: only ${breadcrumb_found}/${breadcrumb_total} files have navigation (need 80%+)"
fi

# Check that INDEX.md links to key sections
if [[ -f "${PROPOSAL_DIR}/INDEX.md" ]]; then
  link_count=$(grep -cE '\[.*\]\(\./' "${PROPOSAL_DIR}/INDEX.md" || echo 0)
  if (( link_count >= 10 )); then
    pass "INDEX.md has ${link_count} internal links"
  else
    fail "INDEX.md has only ${link_count} links — should link to all major sections"
  fi
fi

# Check for broken internal links
broken_links=0
while IFS= read -r -d '' mdfile; do
  # Extract relative links like [text](./path/file.md)
  while IFS= read -r link; do
    # Resolve relative to the file's directory
    dir=$(dirname "$mdfile")
    target="${dir}/${link}"
    # Normalize path
    target=$(cd "$(dirname "$target")" 2>/dev/null && echo "$(pwd)/$(basename "$target")" || echo "")
    if [[ -n "$target" ]] && [[ ! -f "$target" ]] && [[ ! -d "$target" ]]; then
      ((broken_links++))
    fi
  done < <(grep -oE '\]\(\./[^)]+\)' "$mdfile" 2>/dev/null | sed 's/\](\.\///' | sed 's/)//' | head -50)
done < <(find "${PROPOSAL_DIR}" -name '*.md' -print0)

if (( broken_links == 0 )); then
  pass "No broken internal links found"
else
  fail "${broken_links} broken internal link(s) detected"
fi

# ─── 3. RESEARCH QUALITY CHECKS ────────────────────────────────────
echo ""
echo "🔬 Research Quality Checks"

# Count total URLs across all files
total_urls=$(grep -rhE 'https?://' "${PROPOSAL_DIR}/" 2>/dev/null | wc -l || echo 0)
if (( total_urls >= 15 )); then
  pass "Total URLs across proposal: ${total_urls} (target: 15+)"
else
  fail "Only ${total_urls} URLs total — proposal is under-researched (need 15+)"
fi

# Check SOURCES.md specifically
if [[ -f "${PROPOSAL_DIR}/research/SOURCES.md" ]]; then
  source_entries=$(grep -cE '^\|.*https?://' "${PROPOSAL_DIR}/research/SOURCES.md" || echo 0)
  if (( source_entries >= 10 )); then
    pass "SOURCES.md has ${source_entries} entries (target: 10+)"
  else
    fail "SOURCES.md has only ${source_entries} entries — need at least 10"
  fi
else
  fail "SOURCES.md missing — no master source registry"
fi

# Check research dossier quality
if [[ -f "${PROPOSAL_DIR}/research/DOSSIER.md" ]]; then
  dossier_lines=$(wc -l < "${PROPOSAL_DIR}/research/DOSSIER.md")
  if (( dossier_lines >= 80 )); then
    pass "Research dossier: ${dossier_lines} lines (substantive)"
  else
    warn "Research dossier only ${dossier_lines} lines — may be thin"
  fi
fi

# Check fact-check report
if [[ -f "${PROPOSAL_DIR}/research/FACT-CHECK.md" ]]; then
  claims_checked=$(grep -ciE '✅|confirmed|partially|contradicted' \
    "${PROPOSAL_DIR}/research/FACT-CHECK.md" || echo 0)
  if (( claims_checked >= 5 )); then
    pass "Fact-check: ${claims_checked} claims verified"
  else
    fail "Fact-check only verified ${claims_checked} claims — need at least 5"
  fi
fi

# Check for UNVERIFIED markers
unverified_count=$(grep -rci '⚠️ UNVERIFIED\|UNVERIFIED' "${PROPOSAL_DIR}/" 2>/dev/null | 
  awk -F: '{s+=$2} END{print s+0}')
if (( unverified_count > 0 )); then
  warn "${unverified_count} unverified claims remain — check they're not in SUMMARY.md"
  # Specifically check summary
  if [[ -f "${PROPOSAL_DIR}/SUMMARY.md" ]]; then
    summary_unverified=$(grep -ci '⚠️ UNVERIFIED\|UNVERIFIED' "${PROPOSAL_DIR}/SUMMARY.md" || echo 0)
    if (( summary_unverified > 0 )); then
      fail "SUMMARY.md contains ${summary_unverified} unverified claims — executive summary must be clean"
    else
      pass "SUMMARY.md is free of unverified claims"
    fi
  fi
fi

# Check inline citations in key files
for key_file in "core/PRD.md" "approaches/approach-recommended.md" "COMPARISON.md"; do
  if [[ -f "${PROPOSAL_DIR}/${key_file}" ]]; then
    cite_count=$(grep -cE '\[[0-9]+\]' "${PROPOSAL_DIR}/${key_file}" || echo 0)
    if (( cite_count >= 2 )); then
      pass "${key_file}: ${cite_count} inline citations"
    else
      fail "${key_file}: only ${cite_count} citations — key files need research backing"
    fi
  fi
done

# ─── 4. CONTENT QUALITY CHECKS ─────────────────────────────────────
echo ""
echo "📝 Content Quality Checks"

# OPEN-QUESTIONS must have substance
if [[ -f "${PROPOSAL_DIR}/meta/OPEN-QUESTIONS.md" ]]; then
  question_count=$(grep -ciE '^### Q[0-9]|^###.*\?' "${PROPOSAL_DIR}/meta/OPEN-QUESTIONS.md" || echo 0)
  if (( question_count >= 3 )); then
    pass "OPEN-QUESTIONS: ${question_count} questions (Red Team did its job)"
  else
    fail "OPEN-QUESTIONS has only ${question_count} items — need at least 3"
  fi
fi

# failure-modes must be non-trivial
if [[ -f "${PROPOSAL_DIR}/edge-cases/failure-modes.md" ]]; then
  fm_lines=$(wc -l < "${PROPOSAL_DIR}/edge-cases/failure-modes.md")
  if (( fm_lines >= 30 )); then
    pass "failure-modes.md: ${fm_lines} lines (substantive)"
  else
    fail "failure-modes.md only ${fm_lines} lines — Red Team output too thin"
  fi
fi

# Check for at least 1 ADR
adr_count=$(find "${PROPOSAL_DIR}/decisions" -name 'ADR-*' -type f 2>/dev/null | wc -l)
if (( adr_count >= 2 )); then
  pass "Decision records: ${adr_count} ADRs"
elif (( adr_count >= 1 )); then
  warn "Only ${adr_count} ADR — recommend at least 2"
else
  fail "No Architecture Decision Records found"
fi

# Check variant count
variant_count=$(find "${PROPOSAL_DIR}/approaches" -name 'approach-*.md' -type f 2>/dev/null | wc -l)
if (( variant_count >= 3 )); then
  pass "Approach variants: ${variant_count}"
else
  fail "Only ${variant_count} approach variants — need at least 3"
fi

# ─── 5. TODO/PLACEHOLDER CHECK ─────────────────────────────────────
echo ""
echo "🚧 Placeholder Check"

todo_count=$(grep -rci 'TODO\|{{.*}}' "${PROPOSAL_DIR}/" 2>/dev/null | 
  awk -F: '{s+=$2} END{print s+0}')
if (( todo_count == 0 )); then
  pass "No TODO or {{placeholder}} markers found"
else
  fail "${todo_count} TODO/placeholder markers remain — proposal not fully assembled"
fi

# ─── FINAL REPORT ──────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════════"
echo "  Results: ✅ ${PASS} passed | ❌ ${FAIL} failed | ⚠️  ${WARN} warnings"
echo "═══════════════════════════════════════════════"
echo ""
echo -e "$REPORT"

if (( FAIL > 0 )); then
  echo "❌ QUALITY CHECK FAILED — fix ${FAIL} issue(s) before presenting."
  exit 1
else
  echo "✅ QUALITY CHECK PASSED."
  exit 0
fi
