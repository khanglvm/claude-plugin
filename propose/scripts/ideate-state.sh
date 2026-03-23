#!/usr/bin/env bash
# ideate-state.sh — Pipeline state tracker
# Enforces phase ordering: 0 → 0.5 → 1 → 2 → 2.5 → 3 → 4 → 5
#
# Usage:
#   ideate-state.sh init <slug>         Initialize pipeline for a feature
#   ideate-state.sh status <slug>       Show current pipeline state
#   ideate-state.sh check <slug> <phase> Check if a phase is ready to run
#   ideate-state.sh complete <slug> <phase> Mark a phase as complete
#   ideate-state.sh reset <slug>        Reset pipeline to start

set -euo pipefail

IDEATION_DIR=".claude/ideation"
PHASES=("0" "0.5" "1" "2" "2.5" "3" "4" "5")
PHASE_NAMES=(
  "0:Intake & Clarification"
  "0.5:Research Grounding"
  "1:Divergent Expansion"
  "2:Structured Critique"
  "2.5:Fact-Check & Research Deepening"
  "3:Synthesis"
  "4:Variant Generation"
  "5:Document Assembly"
)

# Prerequisites: which phase must be complete before each phase can run
declare -A PREREQS=(
  ["0"]=""
  ["0.5"]="0"
  ["1"]="0.5"
  ["2"]="1"
  ["2.5"]="2"
  ["3"]="2.5"
  ["4"]="3"
  ["5"]="4"
)

get_state_file() {
  echo "${IDEATION_DIR}/$1/pipeline-state.json"
}

cmd_init() {
  local slug="$1"
  local dir="${IDEATION_DIR}/${slug}"
  mkdir -p "${dir}/branches" "${dir}/working"

  cat > "$(get_state_file "$slug")" <<EOF
{
  "slug": "${slug}",
  "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "phases": {
    "0":   { "status": "pending", "started": null, "completed": null },
    "0.5": { "status": "pending", "started": null, "completed": null },
    "1":   { "status": "pending", "started": null, "completed": null },
    "2":   { "status": "pending", "started": null, "completed": null },
    "2.5": { "status": "pending", "started": null, "completed": null },
    "3":   { "status": "pending", "started": null, "completed": null },
    "4":   { "status": "pending", "started": null, "completed": null },
    "5":   { "status": "pending", "started": null, "completed": null }
  },
  "research_stats": {
    "total_searches": 0,
    "total_sources": 0,
    "claims_verified": 0
  },
  "agent_runs": []
}
EOF
  echo "✅ Pipeline initialized: ${dir}"
  echo "   State file: $(get_state_file "$slug")"
}

cmd_status() {
  local slug="$1"
  local state_file
  state_file="$(get_state_file "$slug")"

  if [[ ! -f "$state_file" ]]; then
    echo "❌ No pipeline found for '${slug}'. Run: ideate-state.sh init ${slug}"
    exit 1
  fi

  echo "═══════════════════════════════════════════════"
  echo "  Pipeline: ${slug}"
  echo "═══════════════════════════════════════════════"

  for entry in "${PHASE_NAMES[@]}"; do
    local phase="${entry%%:*}"
    local name="${entry#*:}"
    local status
    status=$(python3 -c "
import json, sys
with open('${state_file}') as f:
    d = json.load(f)
print(d['phases']['${phase}']['status'])
" 2>/dev/null || echo "unknown")

    local icon="⬜"
    case "$status" in
      complete) icon="✅" ;;
      running)  icon="🔄" ;;
      failed)   icon="❌" ;;
      pending)  icon="⬜" ;;
    esac
    printf "  %s Phase %-4s %s\n" "$icon" "$phase" "$name"
  done

  echo "───────────────────────────────────────────────"
  python3 -c "
import json
with open('${state_file}') as f:
    d = json.load(f)
rs = d.get('research_stats', {})
print(f\"  Research: {rs.get('total_searches',0)} searches, {rs.get('total_sources',0)} sources, {rs.get('claims_verified',0)} claims verified\")
print(f\"  Agent runs: {len(d.get('agent_runs',[]))}\")
" 2>/dev/null
  echo "═══════════════════════════════════════════════"
}

cmd_check() {
  local slug="$1"
  local phase="$2"
  local state_file
  state_file="$(get_state_file "$slug")"

  if [[ ! -f "$state_file" ]]; then
    echo "❌ No pipeline for '${slug}'."
    exit 1
  fi

  local prereq="${PREREQS[$phase]:-}"

  if [[ -n "$prereq" ]]; then
    local prereq_status
    prereq_status=$(python3 -c "
import json
with open('${state_file}') as f:
    d = json.load(f)
print(d['phases']['${prereq}']['status'])
" 2>/dev/null)

    if [[ "$prereq_status" != "complete" ]]; then
      echo "❌ BLOCKED: Phase ${phase} requires Phase ${prereq} to be complete (currently: ${prereq_status})"
      exit 1
    fi
  fi

  echo "✅ Phase ${phase} is ready to run."
}

cmd_complete() {
  local slug="$1"
  local phase="$2"
  local state_file
  state_file="$(get_state_file "$slug")"

  python3 -c "
import json
from datetime import datetime, timezone

with open('${state_file}') as f:
    d = json.load(f)

d['phases']['${phase}']['status'] = 'complete'
d['phases']['${phase}']['completed'] = datetime.now(timezone.utc).isoformat()

with open('${state_file}', 'w') as f:
    json.dump(d, f, indent=2)
"
  echo "✅ Phase ${phase} marked complete."
}

cmd_start() {
  local slug="$1"
  local phase="$2"
  local state_file
  state_file="$(get_state_file "$slug")"

  python3 -c "
import json
from datetime import datetime, timezone

with open('${state_file}') as f:
    d = json.load(f)

d['phases']['${phase}']['status'] = 'running'
d['phases']['${phase}']['started'] = datetime.now(timezone.utc).isoformat()

with open('${state_file}', 'w') as f:
    json.dump(d, f, indent=2)
"
  echo "🔄 Phase ${phase} started."
}

cmd_log_agent() {
  local slug="$1"
  local agent_name="$2"
  local phase="$3"
  local state_file
  state_file="$(get_state_file "$slug")"

  python3 -c "
import json
from datetime import datetime, timezone

with open('${state_file}') as f:
    d = json.load(f)

d['agent_runs'].append({
    'agent': '${agent_name}',
    'phase': '${phase}',
    'timestamp': datetime.now(timezone.utc).isoformat()
})

with open('${state_file}', 'w') as f:
    json.dump(d, f, indent=2)
"
}

cmd_update_research() {
  local slug="$1"
  local searches="${2:-0}"
  local sources="${3:-0}"
  local claims="${4:-0}"
  local state_file
  state_file="$(get_state_file "$slug")"

  python3 -c "
import json

with open('${state_file}') as f:
    d = json.load(f)

rs = d.setdefault('research_stats', {})
rs['total_searches'] = rs.get('total_searches', 0) + ${searches}
rs['total_sources'] = rs.get('total_sources', 0) + ${sources}
rs['claims_verified'] = rs.get('claims_verified', 0) + ${claims}

with open('${state_file}', 'w') as f:
    json.dump(d, f, indent=2)
"
}

cmd_reset() {
  local slug="$1"
  echo "⚠️  Resetting pipeline for '${slug}'..."
  cmd_init "$slug"
  echo "   Pipeline reset to initial state."
}

# Main dispatch
case "${1:-help}" in
  init)            cmd_init "${2:?slug required}" ;;
  status)          cmd_status "${2:?slug required}" ;;
  check)           cmd_check "${2:?slug required}" "${3:?phase required}" ;;
  complete)        cmd_complete "${2:?slug required}" "${3:?phase required}" ;;
  start)           cmd_start "${2:?slug required}" "${3:?phase required}" ;;
  log-agent)       cmd_log_agent "${2:?slug}" "${3:?agent}" "${4:?phase}" ;;
  update-research) cmd_update_research "${2:?slug}" "${3:-0}" "${4:-0}" "${5:-0}" ;;
  reset)           cmd_reset "${2:?slug required}" ;;
  *)
    echo "Usage: ideate-state.sh {init|status|check|complete|start|log-agent|update-research|reset} <slug> [args]"
    exit 1
    ;;
esac
