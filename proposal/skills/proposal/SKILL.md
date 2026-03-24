---
name: proposal
description: >
  Deterministic feature implementation workflow with state-tracked checkpoints.
  Enforces every step (research, plan, implement, test, review, finalize) runs
  to completion via checkpoint files, mandatory agent delegation, and a completion
  audit. Use when implementing features, plans, or fixes. Triggers on: "proposal",
  "implement this", "build this feature", "execute this plan", or any task that
  needs structured implementation with quality gates.
---

# Proposal: Deterministic Feature Implementation

State-tracked workflow that enforces every step runs to completion.
No skipped steps, no silent failures.

## Path Resolution (read first)

```bash
PROPOSAL_HOME="$(for d in "$HOME/.claude/plugins/proposal" "$HOME/.claude/plugins/cache/proposal" "$HOME/.claude/skills/proposal"; do [ -f "$d/SKILL.md" ] && [ -d "$d/references" ] && echo "$d" && break; done)"
```

Read references: `$PROPOSAL_HOME/references/*.md`
State file: `{plan_dir}/.proposal-state.md`

## Quick Start

```
/proposal "Add user authentication to the app"
/proposal plans/auth/phase-02-api.md --auto
/proposal "implement dashboard" --fast
```

## Modes

| Flag | Behavior |
|------|----------|
| (default) | Full workflow with review gates |
| `--auto` | Auto-approve, no stops |
| `--fast` | Skip research |
| `--parallel` | Multi-agent execution |
| `--no-test` | Skip testing step |

## Workflow

```
Intent → Research → Plan → Implement → Test → Review → Finalize → Audit
```

Review gates pause for user approval in all modes except `--auto`.

## How It Works

1. **State file** (`.proposal-state.md`) tracks every step as a checkbox
2. Each step verifies the previous checkpoint before starting
3. Mandatory agent spawns for testing, review, and finalization
4. Completion audit validates all checkpoints before marking done

## Full Specification

Read `$PROPOSAL_HOME/SKILL.md` for complete step definitions, then load
references as needed:

- `$PROPOSAL_HOME/references/state-machine.md` — Checkpoint protocol and audit
- `$PROPOSAL_HOME/references/workflow-steps.md` — GATE IN/EXECUTE/GATE OUT per step
- `$PROPOSAL_HOME/references/intent-detection.md` — Mode detection algorithm
- `$PROPOSAL_HOME/references/review-cycle.md` — Review-fix cycle
- `$PROPOSAL_HOME/references/subagent-patterns.md` — Agent spawn patterns

**IMPORTANT:** Read the full SKILL.md before executing. The state machine
enforcement, step continuation rules, and completion audit are mandatory.
