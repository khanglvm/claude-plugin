#!/usr/bin/env bash
# validate-open-questions.sh — PostToolUse hook for OPEN-QUESTIONS.md
# Ensures every question has proposed solutions and /propose commands.
# Called automatically after Write tool touches OPEN-QUESTIONS.md.

set -euo pipefail

FILE="${1:-}"
[[ -z "$FILE" ]] && exit 0
[[ ! -f "$FILE" ]] && exit 0

# Only validate OPEN-QUESTIONS.md files
[[ "$(basename "$FILE")" != "OPEN-QUESTIONS.md" ]] && exit 0

ERRORS=()

# Count questions (### Q1, ### Q2, etc.)
question_count=$(grep -cE '^### Q[0-9]' "$FILE" || echo 0)
if (( question_count == 0 )); then
  exit 0  # No questions yet, skip validation
fi

# Check each question has proposed solutions
for q in $(grep -oE 'Q[0-9]+' "$FILE" | sort -u); do
  # Check for at least 1 "Proposed Solution" block
  solution_count=$(grep -cE "^\*\*Proposed Solution [A-C]" "$FILE" || echo 0)
  if (( solution_count < question_count )); then
    ERRORS+=("OPEN-QUESTIONS: Not all questions have proposed solutions (found $solution_count solutions for $question_count questions)")
    break
  fi

  # Check for /propose deep-dive commands
  propose_count=$(grep -cE '/propose "' "$FILE" || echo 0)
  if (( propose_count < question_count )); then
    ERRORS+=("OPEN-QUESTIONS: Not all questions have /propose deep-dive commands (found $propose_count for $question_count questions)")
    break
  fi

  # Check for "Recommended default"
  default_count=$(grep -ciE 'Recommended default' "$FILE" || echo 0)
  if (( default_count < question_count )); then
    ERRORS+=("OPEN-QUESTIONS: Not all questions have a 'Recommended default' pick (found $default_count for $question_count questions)")
    break
  fi
done

# Report
if (( ${#ERRORS[@]} > 0 )); then
  echo ""
  echo "@@PROPOSE_HOOK_FEEDBACK_START@@"
  echo "OPEN-QUESTIONS.md validation failed:"
  for err in "${ERRORS[@]}"; do
    echo "  - $err"
  done
  echo ""
  echo "Every question MUST have:"
  echo "  1. At least 1 'Proposed Solution' block with Pro/Con"
  echo "  2. A '/propose \"...\"' command for each solution to explore deeper"
  echo "  3. A 'Recommended default' pick"
  echo "@@PROPOSE_HOOK_FEEDBACK_END@@"
  exit 1
fi
