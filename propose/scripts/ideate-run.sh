#!/usr/bin/env bash
# ideate-run.sh — Orchestration wrapper for the ideate pipeline
#
# This script is called by the SKILL.md between phases to enforce
# the workflow. It wraps state tracking, gate validation, and
# quality checks into single commands.
#
# Usage:
#   ideate-run.sh init <slug>                Initialize a new pipeline
#   ideate-run.sh begin <slug> <phase>       Validate prereqs + mark phase started
#   ideate-run.sh end <slug> <phase>         Validate outputs + mark phase complete
#   ideate-run.sh scaffold <slug>            Create output directory structure
#   ideate-run.sh quality <slug>             Run full quality checks on output
#   ideate-run.sh status <slug>              Show pipeline status
#   ideate-run.sh research-stats <slug> <searches> <sources> <claims>
#                                            Update research statistics

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cmd_init() {
  local slug="$1"
  bash "${SCRIPT_DIR}/ideate-state.sh" init "$slug"
  echo ""
  echo "📋 Next: Run Phase 0 (Intake & Clarification)"
  echo "   When done, call: ideate-run.sh end ${slug} 0"
}

cmd_begin() {
  local slug="$1"
  local phase="$2"

  # Check prerequisites
  bash "${SCRIPT_DIR}/ideate-state.sh" check "$slug" "$phase"
  if [[ $? -ne 0 ]]; then
    exit 1
  fi

  # Mark phase as running
  bash "${SCRIPT_DIR}/ideate-state.sh" start "$slug" "$phase"

  # Phase-specific setup
  case "$phase" in
    0)
      echo "📝 Phase 0: Ask ≤3 clarifying questions using Propose→Refine→Lock"
      echo "   Output: .claude/ideation/${slug}/working/idea-brief.md"
      ;;
    0.5)
      echo "🔬 Phase 0.5: Spawn 2 research subagents (market + technical)"
      echo "   Both MUST use WebSearch/WebFetch — minimum 10 searches each"
      echo "   Output: research-market.md, research-technical.md → merge to research-dossier.md"
      ;;
    1)
      echo "🌿 Phase 1: Spawn 5 parallel agents (PM, UX, Eng, Biz, RedTeam)"
      echo "   All receive: idea-brief + research-dossier + research-protocol"
      echo "   All have WebSearch access for confidence < 0.8 claims"
      echo "   Output: {pm,ux,eng,biz,redteam}-analysis.md"
      ;;
    2)
      echo "⚔️  Phase 2: Spawn 3 critique agents (CrossA, CrossB, Devil's Advocate)"
      echo "   Devil's Advocate MUST disagree with consensus"
      echo "   Output: critique-{a,b,devils}.md"
      ;;
    2.5)
      echo "🔍 Phase 2.5: Spawn fact-checker to verify top claims"
      echo "   MUST use WebSearch/WebFetch — minimum 10 verification searches"
      echo "   Output: fact-check-report.md"
      ;;
    3)
      echo "🧬 Phase 3: Spawn synthesizer (use best model available)"
      echo "   Input: ALL Phase 1 + 2 + 2.5 outputs + research dossier"
      echo "   MUST apply fact-check corrections, cite sources, preserve dissent"
      echo "   Output: synthesis.md"
      ;;
    4)
      echo "🔀 Phase 4: Spawn 3 variant agents (Speed, Excellence, Lean)"
      echo "   Each gets: synthesis.md + their disposition instructions"
      echo "   All have WebSearch for cost/pricing verification"
      echo "   Output: variant-{speed,excellence,lean}.md"
      ;;
    5)
      echo "📦 Phase 5: Assemble final proposal documents"
      echo "   Use: ideate-run.sh scaffold ${slug}"
      echo "   Then write all files. Run quality check when done."
      ;;
  esac
}

cmd_end() {
  local slug="$1"
  local phase="$2"

  echo "🔍 Validating Phase ${phase} outputs..."
  echo ""

  # Run gate validation
  if bash "${SCRIPT_DIR}/ideate-gate.sh" "$slug" "$phase"; then
    # Mark complete
    bash "${SCRIPT_DIR}/ideate-state.sh" complete "$slug" "$phase"

    # Show next phase
    local next_phase=""
    case "$phase" in
      0)   next_phase="0.5" ;;
      0.5) next_phase="1" ;;
      1)   next_phase="2" ;;
      2)   next_phase="2.5" ;;
      2.5) next_phase="3" ;;
      3)   next_phase="4" ;;
      4)   next_phase="5" ;;
      5)   echo "🎉 Pipeline complete! Run quality check: ideate-run.sh quality ${slug}" ;;
    esac

    if [[ -n "$next_phase" ]]; then
      echo ""
      echo "📋 Next: ideate-run.sh begin ${slug} ${next_phase}"
    fi
  else
    echo ""
    echo "⛔ Phase ${phase} gate FAILED — fix issues above before proceeding."
    bash "${SCRIPT_DIR}/ideate-state.sh" start "$slug" "$phase"  # keep as running
    exit 1
  fi
}

cmd_scaffold() {
  local slug="$1"
  bash "${SCRIPT_DIR}/ideate-scaffold.sh" "$slug"
}

cmd_quality() {
  local slug="$1"
  bash "${SCRIPT_DIR}/ideate-check-quality.sh" "$slug"
}

cmd_status() {
  local slug="$1"
  bash "${SCRIPT_DIR}/ideate-state.sh" status "$slug"
}

cmd_research_stats() {
  local slug="$1"
  local searches="${2:-0}"
  local sources="${3:-0}"
  local claims="${4:-0}"
  bash "${SCRIPT_DIR}/ideate-state.sh" update-research "$slug" "$searches" "$sources" "$claims"
  echo "📊 Research stats updated: +${searches} searches, +${sources} sources, +${claims} claims"
}

cmd_log_agent() {
  local slug="$1"
  local agent="$2"
  local phase="$3"
  bash "${SCRIPT_DIR}/ideate-state.sh" log-agent "$slug" "$agent" "$phase"
}

# ─── Main ──────────────────────────────────────────────────────────
case "${1:-help}" in
  init)           cmd_init "${2:?slug required}" ;;
  begin)          cmd_begin "${2:?slug required}" "${3:?phase required}" ;;
  end)            cmd_end "${2:?slug required}" "${3:?phase required}" ;;
  scaffold)       cmd_scaffold "${2:?slug required}" ;;
  quality)        cmd_quality "${2:?slug required}" ;;
  status)         cmd_status "${2:?slug required}" ;;
  research-stats) cmd_research_stats "${2:?slug}" "${3:-0}" "${4:-0}" "${5:-0}" ;;
  log-agent)      cmd_log_agent "${2:?slug}" "${3:?agent}" "${4:?phase}" ;;
  help|*)
    cat <<'EOF'
ideate-run.sh — Pipeline orchestration for /ideate skill

Commands:
  init <slug>                    Initialize new pipeline
  begin <slug> <phase>           Check prereqs + start phase
  end <slug> <phase>             Validate outputs + complete phase
  scaffold <slug>                Create proposal output dirs
  quality <slug>                 Run full quality checks
  status <slug>                  Show pipeline status
  research-stats <slug> S C V    Update research counters
  log-agent <slug> <agent> <ph>  Log an agent execution

Phases: 0 → 0.5 → 1 → 2 → 2.5 → 3 → 4 → 5

Example workflow:
  ideate-run.sh init onboarding
  ideate-run.sh begin onboarding 0
  # ... do Phase 0 work ...
  ideate-run.sh end onboarding 0
  ideate-run.sh begin onboarding 0.5
  # ... spawn research agents ...
  ideate-run.sh end onboarding 0.5
  # ... continue through all phases ...
  ideate-run.sh quality onboarding
EOF
    ;;
esac
