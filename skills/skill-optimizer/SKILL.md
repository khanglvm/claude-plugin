---
name: skill-optimizer
description: "Autoresearch-pattern skill improvement loop. Analyzes any Claude skill, creates improvement criteria through interactive interview, then runs programmatic evaluate-improve-keep/revert cycles via claude CLI. Use when asked to 'improve a skill', 'optimize a skill', 'run autoresearch on skill', 'make this skill better', 'skill improvement loop', or when the user wants to iteratively improve any Claude Code skill using the Karpathy autoresearch pattern."
metadata:
  author: khang
  version: "1.0.0"
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

2. **Session duration** — How long to run (default: 1 hour)
   - Accept: `30m`, `1h`, `2h`, `overnight`

3. **Parallelism** — Max parallel eval agents (default: 2)
   - 1 = sequential, 2-4 = parallel evals

### Phase 2: Skill Analysis

Read the target skill thoroughly:
1. Read `SKILL.md` — understand purpose, workflow, structure
2. Read all `references/*.md` — understand depth and coverage
3. Count lines, files, themes/sections
4. Identify: what the skill does well, what's missing, what's vague

Present a **skill profile** to the user:
```
Skill: [name]
Purpose: [1-line]
Files: [count] ([total lines] lines)
Strengths: [list]
Gaps: [list]
```

### Phase 3: Criteria Creation (Interactive)

Using the skill analysis + skill-creator's benchmark framework, propose improvement criteria.

**For each criterion, define:**
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
Weighted total:        [total]/100
```

Ask user to confirm before starting the loop.

### Phase 5: Run Loop

Execute the autoresearch loop via the `scripts/improve.py` script:

```bash
python3 scripts/improve.py \
  --skill <skill-name> \
  --skill-path <path-to-skill> \
  --hours <duration> \
  --parallel <parallelism> \
  --cycle-minutes 8
```

The loop:
1. **Evaluate** all criteria (parallel `claude -p` calls)
2. **Pick weakest** criterion (lowest score * highest weight)
3. **Improve** via `claude -p` with Write/Edit tools
4. **Re-evaluate** the targeted criterion
5. **Keep** if score improved, **revert** via `git checkout` if not
6. **Log** result to `data/results-<skill>.jsonl`
7. **Repeat** until time expires

### Phase 6: Report

After loop completes, generate summary:
- Runs completed
- Improvements kept vs reverted
- Score progression (baseline → final)
- Per-criterion before/after
- Recommendations for next loop

## Script Reference

| File | Purpose |
|------|---------|
| `scripts/improve.py` | Main autoresearch loop (Python) |
| `criteria/<skill>.json` | Criteria definitions per skill |
| `data/state-<skill>.json` | Current best scores |
| `data/results-<skill>.jsonl` | Run history (gitignored) |

## improve.py Usage

```bash
# From skill-optimizer directory
python3 scripts/improve.py --skill <name> --skill-path <path> --hours 1 --parallel 2

# Options
--skill         Skill name (used for state/results files)
--skill-path    Path to skill folder (absolute or relative)
--hours         Duration in hours (default: 1.0)
--parallel      Max parallel eval agents (default: 2)
--cycle-minutes Minutes per improvement cycle (default: 8)
```

## Criteria JSON Format

```json
{
  "skill_name": "my-skill",
  "skill_path": "/path/to/skill",
  "criteria": {
    "C1": {
      "name": "Human-Readable Name",
      "weight": 8,
      "target_files": ["SKILL.md", "references/foo.md"],
      "eval_prompt": "Read {skill_path}/SKILL.md. Score 0-10: [specific scoring instructions with checklist]"
    }
  }
}
```

`{skill_path}` in eval_prompt is replaced at runtime with the actual path.

## Git Integration

The loop leverages git for safe keep/revert:
- **Keep:** Changes stay in working tree (commit manually or let loop commit)
- **Revert:** `git checkout -- <skill-path>/` restores previous state
- **History:** `git log` shows what was kept across loops

## Security

This skill reads and modifies skill files only within the specified skill path. It spawns `claude` CLI agents with `--dangerously-skip-permissions` for autonomous operation. Does NOT access external services, credentials, or files outside the skill directory.
