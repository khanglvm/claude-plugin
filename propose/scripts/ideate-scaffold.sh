#!/usr/bin/env bash
# ideate-scaffold.sh — Create proposal output directory structure
#
# Usage:
#   ideate-scaffold.sh <slug> [output-dir]
#
# Creates the full directory tree for the proposal output.
# Default output: proposal-<slug>/

set -euo pipefail

SLUG="${1:?Usage: ideate-scaffold.sh <slug> [output-dir]}"
OUT_DIR="${2:-proposal-${SLUG}}"

echo "📁 Creating proposal scaffold: ${OUT_DIR}/"

mkdir -p \
  "${OUT_DIR}/core" \
  "${OUT_DIR}/research" \
  "${OUT_DIR}/personas" \
  "${OUT_DIR}/approaches" \
  "${OUT_DIR}/edge-cases" \
  "${OUT_DIR}/what-if" \
  "${OUT_DIR}/technical" \
  "${OUT_DIR}/decisions" \
  "${OUT_DIR}/meta"

# Create placeholder files so agents know what to fill
PLACEHOLDERS=(
  "INDEX.md|Navigation hub"
  "SUMMARY.md|Executive summary"
  "COMPARISON.md|Weighted scoring matrix"
  "core/PRD.md|Core product requirements"
  "core/OUTCOME.md|Desired outcome + metrics"
  "core/ASSUMPTIONS.md|Explicit assumptions"
  "research/INDEX.md|Research overview"
  "research/DOSSIER.md|Full research dossier"
  "research/FACT-CHECK.md|Claim verification report"
  "research/COMPETITIVE-LANDSCAPE.md|Competitor deep dive"
  "research/BENCHMARKS.md|Industry/tech benchmarks"
  "research/SOURCES.md|Master source registry"
  "personas/INDEX.md|Persona overview"
  "personas/PERSONA-MATRIX.md|Cross-persona priorities"
  "approaches/INDEX.md|Approach comparison"
  "approaches/approach-speed.md|Speed-optimized variant"
  "approaches/approach-recommended.md|Recommended approach"
  "approaches/approach-lean.md|Cost-optimized variant"
  "approaches/TRADEOFF-MATRIX.md|Tradeoff scores + sensitivity"
  "edge-cases/INDEX.md|Edge case inventory"
  "edge-cases/failure-modes.md|Red team failure modes"
  "edge-cases/scale-scenarios.md|Scale behavior"
  "edge-cases/security.md|Security analysis"
  "what-if/INDEX.md|What-if navigator"
  "what-if/budget-constrained.md|Budget reduction scenario"
  "what-if/timeline-compressed.md|Timeline pressure scenario"
  "what-if/scope-expanded.md|Scope expansion scenario"
  "technical/architecture.md|Architecture overview"
  "technical/data-model.md|Data model"
  "technical/integration-points.md|External dependencies"
  "technical/migration.md|Migration strategy"
  "decisions/INDEX.md|Decision log"
  "meta/OPEN-QUESTIONS.md|Unresolved items"
  "meta/GLOSSARY.md|Terms"
  "meta/GENERATION-LOG.md|Agent pipeline trace"
)

for entry in "${PLACEHOLDERS[@]}"; do
  local_path="${entry%%|*}"
  desc="${entry#*|}"
  if [[ ! -f "${OUT_DIR}/${local_path}" ]]; then
    echo "<!-- TODO: ${desc} -->" > "${OUT_DIR}/${local_path}"
  fi
done

# Count structure
file_count=$(find "${OUT_DIR}" -type f | wc -l)
dir_count=$(find "${OUT_DIR}" -type d | wc -l)

echo "✅ Scaffold created: ${file_count} files in ${dir_count} directories"
echo ""
echo "Directory tree:"
find "${OUT_DIR}" -type f | sort | sed 's|^|   |'
