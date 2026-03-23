#!/usr/bin/env bash
# validate-conflict-report.sh — PostToolUse hook for conflict-report.md
# Ensures all conflicts are RESOLVED with ADR references. No open items allowed.
# Called automatically after Write tool touches conflict-report.md.

set -euo pipefail

FILE="${1:-}"
[[ -z "$FILE" ]] && exit 0
[[ ! -f "$FILE" ]] && exit 0

# Only validate conflict-report.md files
[[ "$(basename "$FILE")" != "conflict-report.md" ]] && exit 0

ERRORS=()

# Count total conflict items
conflict_count=$(grep -ciE 'blocking|concerning|minor' "$FILE" || echo 0)
if (( conflict_count == 0 )); then
  exit 0  # No conflicts yet, skip validation
fi

# Check for unresolved items
unresolved=$(grep -ciE 'UNRESOLVED|OPEN|PENDING' "$FILE" || echo 0)
if (( unresolved > 0 )); then
  ERRORS+=("conflict-report.md has $unresolved UNRESOLVED items — spawn Resolver Agents to resolve them")
fi

# Check that RESOLVED items have ADR references
resolved_count=$(grep -ciE 'RESOLVED' "$FILE" || echo 0)
adr_refs=$(grep -coE 'ADR-[0-9]+' "$FILE" || echo 0)
if (( resolved_count > 0 && adr_refs == 0 )); then
  ERRORS+=("conflict-report.md has RESOLVED items but no ADR references — each resolution needs an ADR")
fi

# Check for Blocking items without MITIGATED status
blocking_count=$(grep -ciE 'blocking' "$FILE" || echo 0)
mitigated_count=$(grep -ciE 'MITIGATED|RESOLVED' "$FILE" || echo 0)
if (( blocking_count > mitigated_count )); then
  ERRORS+=("conflict-report.md has Blocking items without MITIGATED/RESOLVED status")
fi

# Report
if (( ${#ERRORS[@]} > 0 )); then
  echo ""
  echo "@@PROPOSE_HOOK_FEEDBACK_START@@"
  echo "conflict-report.md validation failed:"
  for err in "${ERRORS[@]}"; do
    echo "  - $err"
  done
  echo ""
  echo "Every conflict MUST be RESOLVED with an ADR reference."
  echo "Spawn Resolver Agents for remaining items before proceeding."
  echo "@@PROPOSE_HOOK_FEEDBACK_END@@"
  exit 1
fi
