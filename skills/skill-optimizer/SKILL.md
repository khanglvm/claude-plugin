---
name: skill-optimizer
description: "Autoresearch-pattern skill improvement loop with context-engineered agent orchestration. Analyzes any Claude skill, creates improvement criteria through interactive interview, then runs programmatic evaluate-improve-keep/revert cycles via claude CLI. Use when asked to 'improve a skill', 'optimize a skill', 'run autoresearch on skill', 'make this skill better', 'skill improvement loop', or when the user wants to iteratively improve any Claude Code skill using the Karpathy autoresearch pattern."
metadata:
  author: khang
  version: "1.2.0"
---

# Skill Optimizer — Autoresearch Improvement Loop

Analyze any Claude Code skill, create targeted improvement criteria, then run an autonomous evaluate-improve-keep/revert loop using the Karpathy autoresearch pattern. All agent invocations via `claude` CLI.

## Prerequisites

**skill-creator is required.** Check if available:

```bash
ls ~/.claude/skills/skill-creator/SKILL.md 2>/dev/null && echo "OK" || echo "MISSING"
```

If missing, instruct the user to install it:

```
npx skills add https://github.com/anthropics/skills --skill skill-creator -y
```

The skill-creator provides eval infrastructure, benchmark scoring (accuracy 80% + security 20%), and the 7-dimension quality framework used during criteria creation.

## Workflow

### Phase 1: Setup (Interactive)

Collect from the user via `AskUserQuestion`:

1. **Skill location** — Path to the skill folder (must contain SKILL.md)
   - Can be relative to CWD or absolute
   - Validate: `SKILL.md` exists, read it to understand the skill

2. **Session limit** — How long or how many cycles to run
   - Duration: `30m`, `1h`, `2h`, `overnight` (default: 1 hour)
   - Loop count: `5 loops`, `10 loops`, `20 loops` (exact number of improvement cycles)
   - Can combine both — loop stops at whichever limit is reached first

3. **Parallelism** — Max parallel eval agents (default: 2)
   - 1 = sequential, 2-4 = parallel evals

### Phase 2: Skill Analysis

Read the target skill thoroughly:
1. Read `SKILL.md` — understand purpose, workflow, structure
2. Read all `references/*.md` — understand depth and coverage
3. Use `Bash` to count lines, files, themes/sections (deterministic, not estimated)
4. Identify: what the skill does well, what's missing, what's vague

Present a **skill profile** to the user:
```
Skill: [name]
Purpose: [1-line]
Files: [count] ([total lines] lines)
Strengths: [list]
Gaps: [list]
```

### Phase 2.5: Domain Research (Optional but Recommended)

Before creating criteria, research the skill's domain to ground evaluation in external knowledge. Run:

```bash
python3 scripts/improve.py --skill <name> --skill-path <path> --domain-research
```

This spawns a research agent with `WebSearch` + `WebFetch` access that:
1. Searches for best practices in the skill's domain
2. Finds competing tools, similar frameworks
3. Identifies common pitfalls and user complaints
4. Checks technical correctness standards (valid CSS, real font names, etc.)
5. Proposes 3-5 domain-specific criteria themes

Report saved to `data/domain-research-<skill>.md`. Use findings to inform Phase 3.

### Phase 3: Criteria Creation (Interactive)

Using the skill analysis + domain research + skill-creator's benchmark framework, propose improvement criteria.

**For each criterion, define — prefer `checklist` (binary PASS/FAIL) over `eval_prompt` (scalar) for any verifiable item. Binary scoring is 4-6x more reliable; use scalar only for genuinely subjective quality dimensions.**

Binary checklist format (preferred for verifiable items):
```json
{
  "name": "Criterion Name",
  "weight": 1-10,
  "target_files": ["SKILL.md"],
  "checklist": [
    {"item": "Specific verifiable thing that exists or not", "points": 3},
    {"item": "Another verifiable check", "points": 2}
  ]
}
```

Scalar eval_prompt format (use only when items are too subjective for binary):
```json
{
  "name": "Criterion Name",
  "weight": 1-10,
  "target_files": ["SKILL.md", "references/file.md"],
  "eval_prompt": "Specific scoring instructions (0-10) with checklist"
}
```

**Standard criteria categories (adapt per skill):**

| Category | What to check |
|----------|--------------|
| Instruction Clarity | Can a fresh Claude follow the SKILL.md without confusion? |
| Output Quality | Does the skill produce high-quality outputs? |
| Completeness | Are all expected sections/features present? |
| Correctness | Are examples, values, code snippets valid? |
| Conversation Efficiency | Minimum turns to complete the skill's task? |
| Anti-Pattern Avoidance | Does it prevent known bad patterns? |
| Reference Depth | Are reference files comprehensive and useful? |
| Security/Scope | Does it declare scope and refuse out-of-scope? |

**Writing effective eval_prompts:**

| Principle | Good | Bad |
|-----------|------|-----|
| Binary checklist items | "Section X exists with 3+ entries" | "Section X is good quality" |
| Concrete point allocation | "2pts per item: (1) exists, (2) has table..." | "Score based on overall quality" |
| No LLM arithmetic | Let pre-computed facts handle counts | "Count the lines in file X" |
| Anti-gaming | "Content must be *substantive*, not keyword-stuffing" | "Check if keywords appear" |
| Scoped to editable files | "Read SKILL.md and check..." | "Verify runtime behavior" |

**Anti-gaming rules for eval_prompts:**
- Never score purely on presence/absence — require *substance* checks
- Include at least one "quality gate" per criterion (e.g., "entries must be genuinely distinct, not slight variations")
- For counting criteria, specify what counts as a valid entry vs padding

Present proposed criteria to user. Let them:
- Accept all
- Remove criteria they don't want
- Add custom criteria
- Adjust weights

Save criteria to `skills/skill-optimizer/criteria/<skill-name>.json`.

### Phase 4: Baseline Evaluation

Run initial evaluation across all criteria. Present the baseline scorecard:

```
BASELINE: [skill-name]
D1 Criterion Name:     [score]/10  (weight: [w])
D2 Criterion Name:     [score]/10  (weight: [w])
...
Weighted total:        [total]/10
```

Ask user to confirm before starting the loop.

### Phase 5: Run Loop

Launch the loop as a **background agent** so results report back automatically — the user does NOT need to ask for updates.

**Spawn the background agent** using the `Agent` tool:
- `name`: `"optimizer-<skill-name>"`
- `run_in_background`: `true`
- `prompt`: Run the optimization loop and return structured results when done

The background agent runs:

```bash
cd <skill-optimizer-dir>
python3 scripts/improve.py \
  --skill <skill-name> \
  --skill-path <path-to-skill> \
  --hours <duration> \
  --max-loops <count> \
  --parallel <parallelism> \
  --cycle-minutes 8 \
  --auto-refine
```

After spawning, tell the user:
> "Optimization loop started for [skill]. Running [X loops / Y hours]. I'll report results automatically when it completes — you can keep working."

**Do NOT poll, sleep, or check status.** The Agent tool notifies you when the background agent finishes. On notification, proceed directly to Phase 6.

The loop (6-step cycle):
1. **Evaluate** all criteria with confidence-weighted dual-sample scoring + pre-computed file facts
2. **Discover** new criteria every N cycles (if `--discover-interval` > 0)
3. **Pick weakest** criterion (lowest score * highest weight * confidence boost, skipping cooldown/parked)
4. **Improve** via research agent (Read+Bash+Grep) → improve agent (Read+Edit)
5. **Re-evaluate** affected criteria → **anti-gaming check** if score jumped 5+ points
6. **Keep/revert** — keep if improved AND total didn't regress, auto-commit on keep

Plus: hot-reload criteria each cycle, cooldown/park stuck criteria, auto-refine if enabled.
**Log** result to `data/results-<skill>.jsonl`. **Repeat** until time/loops/stop.

### Stuck Criteria Handling

The loop tracks consecutive and total failures per criterion:

| Threshold | Action |
|-----------|--------|
| 3 consecutive reverts | **Cooldown** — skip for 3 cycles, then retry |
| 6 total failures | **Park** — stop targeting until criteria refined or manually unparked |
| All criteria blocked | **Halt** — stop loop after 3 consecutive all-blocked cycles |

**`--auto-refine` mode:** When a criterion is about to hit cooldown, the loop spawns an agent to rewrite the `eval_prompt` in the criteria JSON. The refined prompt is saved to disk, failure counters reset, and the criterion gets a fresh start. If a parked criterion exists and all others are blocked, auto-refine attempts to unpark it.

**Manual intervention:** Edit `criteria/<skill>.json` at any time — the loop hot-reloads criteria each cycle. Or use `--unpark` to reset failure state:

```bash
# Unpark specific criteria
python3 scripts/improve.py --skill <name> --unpark C1 C3

# Unpark all
python3 scripts/improve.py --skill <name> --unpark
```

### Criteria Lifecycle (Context Engineering)

Criteria follow a lifecycle that bounds eval cost as the criteria set grows:

| Tier | Score Range | Eval Frequency | Targeted? |
|------|-------------|----------------|-----------|
| **Hot** | 0-6 | Every cycle | Yes |
| **Warm** | 7-8 | Every 2nd cycle | Yes |
| **Cold/Graduated** | 9-10 (3+ consecutive) | Every 5th cycle | No |
| **Parked** | Stuck | Never | No |

**Graduation:** Criteria scoring 9-10 for 3 consecutive cycles are auto-graduated — removed from the improvement loop and only spot-checked. If a spot-check reveals regression below 7, the criterion is un-graduated back to active.

**Active cap:** Max 15 active (non-graduated, non-parked) criteria. If discovery pushes over the cap, the highest-scoring active criteria are force-graduated. Prevents unbounded eval cost growth.

**Overlap detection:** Discovery checks candidate criteria against existing ones for target-file overlap (>50%) AND name similarity. Overlapping candidates are rejected.

```bash
# List graduated criteria
python3 scripts/improve.py --skill <name> --graduate

# Manually graduate criteria
python3 scripts/improve.py --skill <name> --graduate D1 D3

# Set custom active cap
python3 scripts/improve.py --skill <name> --max-active 20 --hours 1
```

### Cancellation

The user can request to stop the loop at any time. When requested, run the stop command from a **separate bash call** while the loop is still running:

```bash
python3 scripts/improve.py --skill <skill-name> --stop
```

This creates a stop signal file that the running loop checks every ~10 seconds. The loop will:
1. Finish the current cycle (evaluate + improve + keep/revert)
2. Print the final summary with all state saved
3. Exit gracefully

**As the invoking agent:** If the user asks to stop, cancel, or terminate the optimization loop, run the `--stop` command above via a `Bash` tool call. The loop process will detect it and halt cleanly. The background agent will then return with partial results — proceed to Phase 6 with whatever data is available.

### Phase 6: Report

When the background agent completes (you are notified automatically), parse its output and present a concise summary to the user:
- Runs completed
- Improvements kept vs reverted
- Score progression (baseline → final)
- Per-criterion before/after
- Parked and struggling criteria (with tip to review eval_prompts)
- Recommendations for next loop

## Context Engineering

The optimizer applies research-backed context engineering to minimize token waste and maximize agent quality:

### Eval Prompt Structure (Lost-in-the-Middle Defense)
LLMs reliably attend to instructions at the START and END of prompts but ignore content in the middle ("lost-in-the-middle" problem). Eval prompts are structured to exploit this:

1. **First 30% — Criterion name + scoring rubric**: What to evaluate goes at the top so it's never missed.
2. **Middle — Pre-computed file facts**: Supporting data (line counts, heading counts) goes in the middle where it serves as context without competing with instructions.
3. **Last 20% — Final scoring methodology + output format**: How to score and what to return goes at the very end, ensuring the LLM's final attention is on the output format.

**When writing `eval_prompt` text**: Put the criterion-specific checklist first, then any context, never bury rubric items between large data blocks.

### Deterministic Pre-Computation
Before each eval, `precompute_file_facts()` runs bash commands (`wc -l`, `grep -c`) to gather line counts, heading counts, and code block counts. These facts are injected into the eval prompt as "Pre-Computed File Facts" so the LLM doesn't need to do arithmetic — a known source of scoring noise.

### Confidence-Weighted Scoring

**LLM confidence self-reporting is unreliable.** Research shows LLMs overestimate their own certainty by 20–40% — models frequently self-report `high` confidence even when scores are inconsistent across samples or criteria are vague. For this reason, **the optimizer does not rely on self-reported confidence as the primary calibration signal**. Instead, it uses cross-model disagreement as an objective proxy: when two model families evaluate the same criterion and disagree by 3+ points, confidence is forced to `low` *regardless of what each model individually self-reported*.

Scores are weighted by confidence:
- **high** (1.0): Clear binary checklist, or models agree within 2 points
- **medium** (0.7): Some interpretation required
- **low** (0.4): Major uncertainty, vague criteria, or forced by cross-model disagreement

The weights are conservative by design: `low` (0.4) is 0.4× `high` (1.0) — at most 0.5× — so unreliable evals have a proportionally smaller influence on the optimization direction.

### Anti-Gaming Verification
When a criterion jumps 5+ points in a single cycle, a **verification pass** runs with a rephrased eval prompt that specifically checks for superficial content. If the verification score disagrees by 3+ points, the average is used instead. Prevents reward hacking where the improve agent adds keyword-matching content without substance.

### Score Stability Detection
Each cycle compares untouched criteria scores to their previous values. If an untouched criterion shifts 3+ points, it's flagged as `[NOISE]` — indicating the eval_prompt is unreliable and should be rewritten for determinism.

### Selective Re-evaluation
After each improvement, only criteria whose `target_files` overlap with modified files are re-evaluated. Unchanged criteria keep their previous scores. Full re-evaluation runs every 5th cycle to catch cumulative drift.

### Separated Research → Improve Pipeline
Following the CRISPY methodology, improvement uses two agents:
1. **Research agent** (read + bash + grep): Describes what exists in target files without knowing the improvement goal. Runs grep/bash for validation.
2. **Improve agent** (read + edit): Receives the research summary + edit directives (not scoring language).

### Domain Research (External Grounding)
The `--domain-research` flag spawns a research agent with `WebSearch` + `WebFetch` access to gather external best practices, competitive analysis, and technical validation standards. This breaks the closed-loop echo chamber of purely introspective evaluation.

### Criteria Discovery
Every N cycles (default: 5, configurable via `--discover-interval`), the loop spawns an agent that reads the current skill state, identifies quality dimensions not covered by existing criteria, and proposes new ones. Prevents the criteria set from becoming stale.

### Cross-Model Ensemble Scoring
Each criterion is evaluated by two DIFFERENT models (default: sonnet + haiku). Self-enhancement bias — where an LLM rates its own style 15-30% higher — cancels out across model families. When models disagree by 3+ points, a capability-weighted average is used and confidence drops to `low`. Configurable via `--eval-model` and `--eval-model-2`.

### Binary Checklist Mode (Preferred)
**Use binary checklist as the default criterion format.** Binary scoring is 4-6x more reliable than scalar 0-10 scoring: LLMs show ~30% inter-rater variance on subjective scales, but near-zero variance on binary PASS/FAIL questions where the answer is verifiable by reading a file. Reserve `eval_prompt` (scalar) only for genuinely subjective quality dimensions (e.g., "prose clarity") that cannot be broken into discrete checks.

Criteria opt into binary evaluation by adding a `checklist` field:
```json
{
  "name": "Example",
  "checklist": [
    {"item": "SKILL.md has a Scope section", "points": 2},
    {"item": "At least 3 reference files exist", "points": 3}
  ]
}
```
The LLM only decides PASS or FAIL per item (binary). Score = sum of passed points / max points * 10. Always `confidence: high` since no subjective judgment is needed. Use for criteria where every item is verifiable by reading files.

### Ground Truth Calibration
Before the loop starts, if a gold standard exists (`calibration/<skill>.json`), it evaluates those criteria and compares to expected scores. Drift of 3+ points triggers a `[DRIFT]` warning.

```bash
# Snapshot current scores as gold standard
python3 scripts/improve.py --skill <name> --calibrate create

# Check eval drift against gold standard
python3 scripts/improve.py --skill <name> --calibrate check
```

Only high-confidence scores are included in the gold standard. This follows the context-engineering principle: "Validate manually before automating."

### Agent Turn Limits
- Eval: 5 turns max
- Research: 5 turns max
- Improve: 10 turns max

### Regression Detection
After improvement, if the weighted total drops below the pre-improvement total, the change is reverted — even if the targeted criterion improved.

### Auto-Commit on Keep
Kept improvements are immediately committed to protect from next cycle's revert.

## Script Reference

| File | Purpose |
|------|---------|
| `scripts/improve.py` | Main autoresearch loop (Python) |
| `criteria/<skill>.json` | Criteria definitions per skill |
| `data/state-<skill>.json` | Current best scores + confidence |
| `data/results-<skill>.jsonl` | Run history (gitignored) |
| `data/domain-research-<skill>.md` | Domain research report (from `--domain-research`) |
| `calibration/<skill>.json` | Gold standard scores for eval drift detection |
| `data/calibration-report-<skill>.json` | Last calibration drift report |

## improve.py Usage

```bash
# From skill-optimizer directory
python3 scripts/improve.py --skill <name> --skill-path <path> --hours 1 --parallel 2

# Run for exactly 10 improvement cycles (no time limit)
python3 scripts/improve.py --skill <name> --skill-path <path> --max-loops 10

# Combine: stop at whichever limit hits first
python3 scripts/improve.py --skill <name> --skill-path <path> --hours 2 --max-loops 20

# With auto-refine for stuck criteria
python3 scripts/improve.py --skill <name> --skill-path <path> --hours 2 --auto-refine

# Domain research before running (grounds criteria in external knowledge)
python3 scripts/improve.py --skill <name> --skill-path <path> --domain-research

# Criteria discovery every 3 cycles
python3 scripts/improve.py --skill <name> --skill-path <path> --hours 2 --discover-interval 3

# Create gold standard for calibration (after a good baseline run)
python3 scripts/improve.py --skill <name> --calibrate create

# Check eval drift against gold standard
python3 scripts/improve.py --skill <name> --calibrate check

# Cancel a running loop (from a separate terminal/bash call)
python3 scripts/improve.py --skill <name> --stop

# Unpark criteria before running
python3 scripts/improve.py --skill <name> --unpark C1 C3 --hours 1

# Options
--skill            Skill name (used for state/results files)
--skill-path       Path to skill folder (absolute or relative)
--hours            Duration in hours (default: 1, or unlimited if --max-loops set)
--max-loops        Max improvement cycles (default: unlimited, time-limited only)
--parallel         Max parallel eval agents (default: 2)
--cycle-minutes    Minutes per improvement cycle (default: 0, no wait)
--auto-refine      Auto-rewrite stuck eval_prompts instead of just parking
--domain-research  Run web-based domain research before starting the loop
--discover-interval N  Run criteria discovery every N cycles (0=disabled, default: 5)
--calibrate <mode> Create gold standard (create) or check eval drift (check)
--profile <name>   Model profile preset (default: balanced). See Model Profiles below.
--eval-model       Primary eval model override (overrides profile)
--eval-model-2     Secondary eval model override (overrides profile)
--improve-model    Improve model override (overrides profile)
--no-multi-sample  Disable dual-sample scoring (faster but less reliable)
--stop             Signal a running loop to stop after current cycle
--unpark [CID]     Reset failure state for specific criteria (or all if no IDs)
--max-active N     Max active criteria cap (default: 15). Overflow force-graduates highest-scoring
--graduate [CID]   List graduated criteria (no args) or manually graduate specific ones
```

### Model Profiles

Select with `--profile <name>`. Individual `--eval-model` / `--improve-model` flags override profile defaults.

| Profile | Eval (primary) | Eval (secondary) | Improve | Use When |
|---------|---------------|------------------|---------|----------|
| **quality** | opus | sonnet | opus | High-stakes skills, large files (opus has 1M context) |
| **balanced** | sonnet | haiku | sonnet | Default — good accuracy, moderate cost |
| **budget** | haiku | haiku | haiku | Quick iteration, simple criteria, cost-sensitive |
| **auto** | *per-criterion* | *per-criterion* | *per-criterion* | Mixed complexity — routes each criterion to the right model |

**Auto-routing** analyzes each criterion's complexity before selecting a model:
- **opus** — total target file lines > 800, or high weight (9-10) + many checklist items + cross-file eval
- **sonnet** — moderate complexity (200-800 lines)
- **haiku** — simple criteria with small files (< 200 lines)

```bash
# Quality-first: opus eval + sonnet cross-check
python3 scripts/improve.py --skill <name> --skill-path <path> --profile quality --hours 1

# Auto: let the system pick per criterion
python3 scripts/improve.py --skill <name> --skill-path <path> --profile auto --hours 1

# Budget: fast iteration with haiku
python3 scripts/improve.py --skill <name> --skill-path <path> --profile budget --max-loops 10
```

## Criteria JSON Format

```json
{
  "skill_name": "my-skill",
  "skill_path": "/path/to/skill",
  "criteria": {
    "C1": {
      "name": "Binary Checklist Eval — PREFERRED FORMAT (PASS/FAIL per item)",
      "weight": 7,
      "target_files": ["SKILL.md"],
      "checklist": [
        {"item": "SKILL.md has a Scope section declaring what is out-of-scope", "points": 2},
        {"item": "At least 3 reference files exist with 50+ lines each", "points": 3},
        {"item": "Phase descriptions are under 30 lines each", "points": 2},
        {"item": "No inline code blocks in SKILL.md (belong in references)", "points": 3}
      ]
    },
    "C2": {
      "name": "Standard Eval (0-10 scale) — use only for subjective quality",
      "weight": 8,
      "target_files": ["SKILL.md", "references/foo.md"],
      "eval_prompt": "Read {skill_path}/SKILL.md. Score 0-10: [specific scoring instructions]"
    }
  }
}
```

`{skill_path}` in eval_prompt is replaced at runtime. Binary checklist criteria use `checklist` instead of `eval_prompt` — the LLM only decides PASS/FAIL per item (more deterministic).

## Git Integration

The loop uses git for safe keep/revert with proper isolation:
- **Keep:** Changes are committed immediately (`autoresearch: improve <criterion>`)
- **Revert:** `git checkout -- <modified-files>` restores only the files that changed (not the entire skill directory)
- **History:** `git log` shows each kept improvement as a separate commit
- **Regression revert:** If a kept change degrades overall score, it can be reverted via `git revert HEAD`

## Security

This skill reads and modifies skill files only within the specified skill path. It spawns `claude` CLI agents with `--dangerously-skip-permissions` for autonomous operation. Does NOT access external services, credentials, or files outside the skill directory.
