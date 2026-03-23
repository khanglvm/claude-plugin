#!/usr/bin/env bash
# ideate-gate.sh — Phase gate validator
# Validates that a phase produced the required outputs before allowing next phase.
#
# Usage:
#   ideate-gate.sh <slug> <phase>
#
# Returns exit 0 if gate passes, exit 1 with details if it fails.

set -euo pipefail

IDEATION_DIR=".claude/ideation"
SLUG="${1:?Usage: ideate-gate.sh <slug> <phase>}"
PHASE="${2:?Usage: ideate-gate.sh <slug> <phase>}"
WORK_DIR="${IDEATION_DIR}/${SLUG}/working"
ERRORS=()

fail() { ERRORS+=("$1"); }

check_file_exists() {
  local path="$1"
  local desc="$2"
  if [[ ! -f "$path" ]]; then
    fail "Missing: ${desc} (${path})"
    return 1
  fi
  return 0
}

check_file_nonempty() {
  local path="$1"
  local desc="$2"
  if [[ ! -s "$path" ]]; then
    fail "Empty: ${desc} (${path})"
    return 1
  fi
  return 0
}

check_min_lines() {
  local path="$1"
  local min="$2"
  local desc="$3"
  if [[ -f "$path" ]]; then
    local lines
    lines=$(wc -l < "$path")
    if (( lines < min )); then
      fail "Too short: ${desc} has ${lines} lines, need at least ${min}"
    fi
  fi
}

# ─── Phase 0: Intake ───────────────────────────────────────────────
gate_phase_0() {
  echo "🔍 Checking Phase 0 (Intake) gate..."
  check_file_exists "${WORK_DIR}/idea-brief.md" "Idea brief"
  check_file_nonempty "${WORK_DIR}/idea-brief.md" "Idea brief"
  check_min_lines "${WORK_DIR}/idea-brief.md" 10 "Idea brief"

  # Verify required sections in idea brief
  if [[ -f "${WORK_DIR}/idea-brief.md" ]]; then
    for section in "Problem Statement" "Target User" "Success Metrics" "Constraints"; do
      if ! grep -qi "${section}" "${WORK_DIR}/idea-brief.md"; then
        fail "Idea brief missing section: ${section}"
      fi
    done
  fi
}

# ─── Phase 0.5: Research Grounding ─────────────────────────────────
gate_phase_05() {
  echo "🔍 Checking Phase 0.5 (Research) gate..."
  check_file_exists "${WORK_DIR}/research-market.md" "Market research output"
  check_file_exists "${WORK_DIR}/research-technical.md" "Technical research output"
  check_file_exists "${WORK_DIR}/research-dossier.md" "Merged research dossier"

  check_file_nonempty "${WORK_DIR}/research-dossier.md" "Research dossier"
  check_min_lines "${WORK_DIR}/research-dossier.md" 50 "Research dossier"

  # Check for actual URLs (evidence of real research)
  if [[ -f "${WORK_DIR}/research-dossier.md" ]]; then
    local url_count
    url_count=$(grep -cE 'https?://' "${WORK_DIR}/research-dossier.md" || echo 0)
    if (( url_count < 10 )); then
      fail "Research dossier has only ${url_count} URLs — need at least 10 (evidence of real research)"
    fi
    echo "   📊 Found ${url_count} URLs in research dossier"

    # Check for required sections
    for section in "Market" "Competitive" "Case Study\|Best Practice" "Technology"; do
      if ! grep -qiE "${section}" "${WORK_DIR}/research-dossier.md"; then
        fail "Research dossier missing section matching: ${section}"
      fi
    done
  fi
}

# ─── Phase 1: Divergent Expansion ──────────────────────────────────
gate_phase_1() {
  echo "🔍 Checking Phase 1 (Expansion) gate..."
  local agents=("pm" "ux" "eng" "biz" "redteam")
  local found=0

  for agent in "${agents[@]}"; do
    if check_file_exists "${WORK_DIR}/${agent}-analysis.md" "${agent} agent analysis"; then
      check_file_nonempty "${WORK_DIR}/${agent}-analysis.md" "${agent} analysis"
      check_min_lines "${WORK_DIR}/${agent}-analysis.md" 20 "${agent} analysis"
      ((found++))
    fi
  done

  if (( found < 5 )); then
    fail "Only ${found}/5 agent analyses found — all 5 required"
  fi

  # Check that agents cited sources (research-backed)
  for agent in "${agents[@]}"; do
    local file="${WORK_DIR}/${agent}-analysis.md"
    if [[ -f "$file" ]]; then
      local src_count
      src_count=$(grep -cE '\[[0-9]+\]|https?://' "$file" || echo 0)
      if (( src_count < 2 )); then
        fail "${agent} analysis has only ${src_count} citations/URLs — needs at least 2"
      fi
    fi
  done
}

# ─── Phase 2: Structured Critique ──────────────────────────────────
gate_phase_2() {
  echo "🔍 Checking Phase 2 (Critique) gate..."
  local critique_files=0

  for f in "${WORK_DIR}"/critique-*.md; do
    [[ -f "$f" ]] && ((critique_files++))
  done

  if (( critique_files < 2 )); then
    fail "Only ${critique_files} critique files found — need at least 2 (cross-review + devil's advocate)"
  fi

  # Check devil's advocate exists specifically
  if ! ls "${WORK_DIR}"/critique-*devils* "${WORK_DIR}"/devils-advocate* 2>/dev/null | head -1 > /dev/null 2>&1; then
    # Also accept any file mentioning "devil" in content
    if ! grep -rlqi "devil\|dissent\|disagree" "${WORK_DIR}"/critique-*.md 2>/dev/null; then
      fail "No Devil's Advocate output found — mandatory for adversarial review"
    fi
  fi
}

# ─── Phase 2.5: Fact-Check ────────────────────────────────────────
gate_phase_25() {
  echo "🔍 Checking Phase 2.5 (Fact-Check) gate..."
  check_file_exists "${WORK_DIR}/fact-check-report.md" "Fact-check report"
  check_file_nonempty "${WORK_DIR}/fact-check-report.md" "Fact-check report"

  if [[ -f "${WORK_DIR}/fact-check-report.md" ]]; then
    # Count verified claims
    local verified
    verified=$(grep -ciE '✅|confirmed|verified|partially true|contradicted' \
      "${WORK_DIR}/fact-check-report.md" || echo 0)
    if (( verified < 5 )); then
      fail "Fact-check only verified ${verified} claims — need at least 5"
    fi
    echo "   📊 ${verified} claims checked in fact-check report"

    # Check for actual search evidence
    local url_count
    url_count=$(grep -cE 'https?://' "${WORK_DIR}/fact-check-report.md" || echo 0)
    if (( url_count < 5 )); then
      fail "Fact-check has only ${url_count} URLs — needs at least 5 (evidence of verification searches)"
    fi
  fi
}

# ─── Phase 3: Synthesis ───────────────────────────────────────────
gate_phase_3() {
  echo "🔍 Checking Phase 3 (Synthesis) gate..."
  check_file_exists "${WORK_DIR}/synthesis.md" "Synthesized proposal"
  check_file_nonempty "${WORK_DIR}/synthesis.md" "Synthesized proposal"
  check_min_lines "${WORK_DIR}/synthesis.md" 50 "Synthesis"

  if [[ -f "${WORK_DIR}/synthesis.md" ]]; then
    # Must have NEEDS_CLARIFICATION items
    if ! grep -qi "NEEDS_CLARIFICATION\|needs clarification\|open question\|unresolved" \
      "${WORK_DIR}/synthesis.md"; then
      fail "Synthesis has no NEEDS_CLARIFICATION items — the synthesizer is papering over uncertainty"
    fi

    # Must have dissenting views
    if ! grep -qi "dissent\|minority\|disagree\|overruled" "${WORK_DIR}/synthesis.md"; then
      fail "Synthesis has no dissenting views — mandatory for honest proposal"
    fi

    # Must have citations
    local cite_count
    cite_count=$(grep -cE '\[[0-9]+\]' "${WORK_DIR}/synthesis.md" || echo 0)
    if (( cite_count < 3 )); then
      fail "Synthesis has only ${cite_count} citations — need at least 3 for research-backed proposal"
    fi
  fi
}

# ─── Phase 4: Variant Generation ──────────────────────────────────
gate_phase_4() {
  echo "🔍 Checking Phase 4 (Variants) gate..."
  local variant_count=0

  for f in "${WORK_DIR}"/variant-*.md; do
    [[ -f "$f" ]] && ((variant_count++))
  done

  if (( variant_count < 3 )); then
    fail "Only ${variant_count} variant files — need exactly 3 (speed, excellence, lean)"
  fi

  # Each variant must have meaningful differences
  for f in "${WORK_DIR}"/variant-*.md; do
    if [[ -f "$f" ]]; then
      check_min_lines "$f" 20 "$(basename "$f")"
    fi
  done
}

# ─── Phase 5: Document Assembly ────────────────────────────────────
gate_phase_5() {
  echo "🔍 Checking Phase 5 (Assembly) gate..."
  # Delegate to the full quality check script
  if [[ -f "$(dirname "$0")/ideate-check-quality.sh" ]]; then
    bash "$(dirname "$0")/ideate-check-quality.sh" "${SLUG}"
    return $?
  fi
  echo "⚠️  ideate-check-quality.sh not found — skipping detailed checks"
}

# ─── Main dispatch ─────────────────────────────────────────────────
case "$PHASE" in
  0)   gate_phase_0 ;;
  0.5) gate_phase_05 ;;
  1)   gate_phase_1 ;;
  2)   gate_phase_2 ;;
  2.5) gate_phase_25 ;;
  3)   gate_phase_3 ;;
  4)   gate_phase_4 ;;
  5)   gate_phase_5 ;;
  *)   echo "Unknown phase: ${PHASE}"; exit 1 ;;
esac

# Report results
if (( ${#ERRORS[@]} > 0 )); then
  echo ""
  echo "❌ GATE FAILED for Phase ${PHASE} — ${#ERRORS[@]} issue(s):"
  for err in "${ERRORS[@]}"; do
    echo "   • ${err}"
  done
  exit 1
else
  echo "✅ Phase ${PHASE} gate PASSED."
  exit 0
fi
