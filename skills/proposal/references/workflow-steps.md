# Workflow Steps — Procedural Definitions

Each step follows: **GATE IN → EXECUTE → GATE OUT → CHECKPOINT → TRANSITION**

No step may be skipped without mode justification. No transition without checkpoint update.
See `state-machine.md` for state file protocol and audit rules.

**Task Tool Fallback:** `TaskCreate`/`TaskUpdate`/`TaskGet`/`TaskList` are CLI-only. If they error, use `TodoWrite`. All steps remain functional.

---

## Step 0: Intent Detection & Setup

### Gate In
None (first step).

### Execute

1. **Parse input** — determine `mode` from flags/keywords/path:
   - Explicit flags (`--fast`, `--auto`, etc.) override all
   - Path to plan file → `code` mode
   - Keywords: "fast"/"quick" → `fast`, "auto"/"trust me" → `auto`, "no test" → `no-test`
   - 3+ features → `parallel`
   - Default → `interactive`
2. **Create state file** (Write tool):
   ```
   Write(file_path=".proposal-state.md", content="<template from state-machine.md>")
   ```
   If no plan_dir yet, use `./.proposal-state.md` (move later in Step 2).
3. **Create workflow tasks** (TaskCreate) for steps 1-6 with dependencies.
4. **Mark skippable steps** per mode (Edit `[ ]` → `[~] skipped`).

### Gate Out
```
Read(file_path=".proposal-state.md")
```
Verify: file exists, mode recorded, skippable steps marked.

### Checkpoint
```
Edit: "- [ ] step-0: intent-detection" → "- [x] step-0: intent-detection | mode={mode}"
```

### Transition
→ IF mode=fast/code: skip to Step 2 (fast) or Step 3 (code)
→ ELSE: proceed to Step 1
→ **DO NOT STOP. Immediately begin next step.**

**Output:** `Step 0: Mode [{mode}] — {reason}`

---

## Step 1: Research (skip if fast/code)

### Gate In
```
Grep(pattern="\\[x\\] step-0", path=".proposal-state.md", output_mode="count")
```
Must return `1`.

### Execute

1. **Spawn researcher agents** (Agent tool — parallel):
   ```
   Agent(subagent_type="researcher", prompt="Research {topic-1}. Report ≤150 lines. End with Status: DONE|BLOCKED.", description="Research {topic-1}")
   Agent(subagent_type="researcher", prompt="Research {topic-2}. Report ≤150 lines. End with Status: DONE|BLOCKED.", description="Research {topic-2}")
   ```
2. **Spawn scout** (Agent tool):
   ```
   Agent(subagent_type="Explore", prompt="Find files related to {feature} in codebase. List paths and purposes.", description="Scout {feature}")
   ```
3. **Collect results** — read returned reports.

### Gate Out
Verify: at least 1 researcher returned `Status: DONE`.

### Checkpoint
```
Edit: "- [ ] step-1: research" → "- [x] step-1: research | reports={N}"
```

### Transition
→ IF mode=auto: proceed to Step 2 (skip gate)
→ ELSE: proceed to Gate 1

**Output:** `Step 1: Research complete — {N} reports`

---

### Gate 1: Research Review (skip if auto)

**REQUIRED TOOL CALL:**
```
AskUserQuestion(question="Research complete with {N} reports. Key findings:\n{bullet_summary}\n\nProceed to planning?", options=["Proceed to planning", "Request more research", "Abort"])
```

**Handle response:**
- "Proceed" → checkpoint gate-1, proceed to Step 2
- "More research" → return to Step 1 Execute
- "Abort" → checkpoint `gate-1: aborted`, STOP

**Checkpoint:**
```
Edit: "- [ ] gate-1: research-reviewed" → "- [x] gate-1: research-reviewed | approved"
```

---

## Step 2: Planning

### Gate In
```
Grep(pattern="\\[x\\] (gate-1|step-0.*mode=fast)", path=".proposal-state.md", output_mode="count")
```
Must return ≥ `1`.

### Execute

1. **Spawn planner** (Agent tool):
   ```
   Agent(
     subagent_type="planner",
     prompt="Create implementation plan for: {task}.\nResearch context: {report_paths}\nScout context: {scout_results}\nSave to: {plan_dir}/\nCreate: plan.md + phase-XX-*.md files.\nEnd with Status: DONE.",
     description="Plan {task}"
   )
   ```
   **Fast mode:** minimal plan, single phase file.
2. **Move state file** if plan_dir changed:
   ```bash
   mv .proposal-state.md {plan_dir}/.proposal-state.md
   ```
3. **Update state file** plan_dir field.

### Gate Out
```
Glob(pattern="{plan_dir}/plan.md")
Glob(pattern="{plan_dir}/phase-*.md")
```
Both must return results.

### Checkpoint
```
Edit: "- [ ] step-2: planning" → "- [x] step-2: planning | phases={N} plan_dir={path}"
```

### Transition
→ IF mode=auto: proceed to Step 3 (skip gate)
→ ELSE: proceed to Gate 2

**Output:** `Step 2: Plan created — {N} phases in {plan_dir}`

---

### Gate 2: Plan Review (skip if auto)

**Present plan overview first** (Read plan.md, summarize phases).

**REQUIRED TOOL CALL:**
```
AskUserQuestion(
  question="Plan created with {N} phases:\n{phase_list}\n\nChoose action:",
  options=["Approve — start implementation", "Request revisions", "Abort"]
)
```

**Handle response:**
- "Approve" → checkpoint gate-2, proceed to Step 3
- "Revisions" → revise plan, re-ask
- "Abort" → checkpoint `gate-2: aborted`, STOP

**Checkpoint:**
```
Edit: "- [ ] gate-2: plan-approved" → "- [x] gate-2: plan-approved"
```

---

## Step 3: Implementation

### Gate In
```
Grep(pattern="\\[x\\] (gate-2|step-2.*mode=code)", path="{plan_dir}/.proposal-state.md", output_mode="count")
```
Must return ≥ `1`.

### Execute

1. **Check for existing tasks:**
   ```
   TaskList
   ```
   If tasks exist from planning → use them. If not → create from plan.

2. **Create tasks from plan** (if needed):
   Read each phase-XX-*.md → extract unchecked `[ ]` items → TaskCreate for each with priority, phase metadata. Set dependencies via addBlockedBy where sequential.

3. **Implement each task:**
   - TaskUpdate → `in_progress` immediately when picking up
   - Execute implementation (use `ui-ux-designer` agent for frontend work)
   - **Run type check after each file** (Bash: build/compile command)
   - TaskUpdate → `completed` immediately after finishing
   - Update phase file checkbox: `[ ]` → `[x]`

4. **Parallel mode variant:**
   ```
   Agent(subagent_type="fullstack-developer", prompt="Implement {phase-file} with file ownership: {files}. End with Status: DONE.", description="Implement phase {N}")
   ```
   Launch multiple in parallel. Respect file ownership. Wait for group before next.

### Gate Out
```
TaskList → verify all tasks for current phase are `completed`
```

### Checkpoint
```
Edit: "- [ ] step-3: implementation" → "- [x] step-3: implementation | tasks={completed}/{total}"
```

### Transition
→ IF mode=auto: proceed to Step 4 (skip gate)
→ ELSE: proceed to Gate 3
→ **DO NOT STOP HERE. Testing and review are mandatory next steps.**

**Output:** `Step 3: Implemented — {files_changed} files, {completed}/{total} tasks`

---

### Gate 3: Implementation Review (skip if auto)

**REQUIRED TOOL CALL:**
```
AskUserQuestion(
  question="Implementation complete. {files_changed} files modified.\n\nKey changes:\n{change_summary}\n\nProceed to testing?",
  options=["Proceed to testing", "Request changes", "Abort"]
)
```

**Checkpoint:**
```
Edit: "- [ ] gate-3: implementation-reviewed" → "- [x] gate-3: implementation-reviewed | approved"
```

---

## Step 4: Testing (skip if no-test)

### Gate In
```
Grep(pattern="\\[x\\] (gate-3|step-3)", path="{plan_dir}/.proposal-state.md", output_mode="count")
```
Must return ≥ `1`.

### Execute

**MANDATORY AGENT SPAWN — non-negotiable:**
```
Agent(
  subagent_type="tester",
  prompt="Test implementation for plan: {plan_dir}.\nChanged files: {file_list}\nRun existing tests. Write new tests for: happy path, edge cases, errors.\nDO NOT mock, fake, or skip. DO NOT modify assertions to pass.\nEnd with: Status: DONE | BLOCKED\nInclude: pass_count, fail_count, coverage.",
  description="Test {task}"
)
```

**IF tester returns failures — MANDATORY debugger spawn:**
```
Agent(
  subagent_type="debugger",
  prompt="Analyze test failures:\n{failure_details}\nProvide root cause and fix.\nEnd with Status: DONE | BLOCKED.",
  description="Debug test failures"
)
```
Then fix and re-spawn tester. Max 3 cycles.

**FORBIDDEN:** Fake mocks, commented tests, weakened assertions, skipping tester spawn.

### Gate Out
Tester must report: `Status: DONE` with `fail_count=0`.

### Checkpoint
```
Edit: "- [ ] step-4: testing | tester_spawned=false" → "- [x] step-4: testing | tester_spawned=true pass={N} fail=0"
```

### Transition
→ IF mode=auto: proceed to Step 5 (skip gate)
→ ELSE: proceed to Gate 4
→ **DO NOT STOP. Code review is mandatory.**

**Output:** `Step 4: Tests {pass}/{total} passed — tester agent spawned`

---

### Gate 4: Testing Review (skip if auto)

**REQUIRED TOOL CALL:**
```
AskUserQuestion(
  question="Tests complete: {pass}/{total} passed.\n\nProceed to code review?",
  options=["Proceed to code review", "Request test fixes", "Abort"]
)
```

**Checkpoint:**
```
Edit: "- [ ] gate-4: testing-reviewed" → "- [x] gate-4: testing-reviewed | approved"
```

---

## Step 5: Code Review

### Gate In
```
Grep(pattern="\\[x\\] (gate-4|step-4)", path="{plan_dir}/.proposal-state.md", output_mode="count")
```
Must return ≥ `1`.

### Execute

**MANDATORY AGENT SPAWN — non-negotiable:**
```
Agent(
  subagent_type="code-reviewer",
  prompt="Review all changes for plan: {plan_dir}.\nChanged files: {file_list}\nCheck: security (OWASP), performance, YAGNI/KISS/DRY, architecture.\nReturn: score (X/10), critical_count, warnings[], suggestions[].\nEnd with Status: DONE.",
  description="Code review"
)
```

**DO NOT review code yourself. DELEGATE to agent.**

**Handle result per `review-cycle.md`:**
- Interactive: show findings, AskUserQuestion for approval (max 3 fix cycles)
- Auto: auto-approve if score >= 9.5 AND critical_count=0, else auto-fix (max 3 cycles)

### Gate Out
Review must be approved (user or auto).

### Checkpoint
```
Edit: "- [ ] step-5: code-review | reviewer_spawned=false" → "- [x] step-5: code-review | reviewer_spawned=true score={score}"
```

### Transition
→ Proceed to Step 6 (no gate between review and finalize)
→ **DO NOT STOP. Finalize is mandatory and must run NOW.**

**Output:** `Step 5: Review {score}/10 — {approved_by} — code-reviewer agent spawned`

---

## Step 6: Finalize

### Gate In
```
Grep(pattern="\\[x\\] step-5", path="{plan_dir}/.proposal-state.md", output_mode="count")
```
Must return `1`.

### Execute

**ALL 3 AGENTS MANDATORY — spawn in parallel:**

```
Agent(
  subagent_type="project-manager",
  prompt="Run full sync-back for plan: {plan_dir}.\n1. Read ALL phase-XX-*.md files\n2. Mark completed items [ ] → [x] based on implementation\n3. Update plan.md status/progress for ALL phases\n4. Return: phases_updated, items_checked.\nEnd with Status: DONE.",
  description="Sync plan status"
)
```

```
Agent(
  subagent_type="docs-manager",
  prompt="Review changes from plan: {plan_dir}.\nChanged files: {file_list}\nUpdate ./docs/ if changes warrant.\nIf no changes needed, state why.\nEnd with Status: DONE.",
  description="Update docs"
)
```

**After PM + docs complete:**

```
Agent(
  subagent_type="git-manager",
  prompt="Stage and commit all changes with conventional commit message. Do NOT push unless user requested.\nEnd with Status: DONE.",
  description="Commit changes"
)
```

**Post-agents:**
- TaskUpdate → mark all Claude Tasks `completed` (if Task tools available)

### Gate Out — COMPLETION AUDIT (Bash tool)

**MANDATORY AUDIT — run this exact command:**
```bash
STATE="{plan_dir}/.proposal-state.md" && \
echo "=== PROPOSAL AUDIT ===" && \
echo "Completed: $(grep -c '\[x\]' "$STATE")" && \
echo "Skipped: $(grep -c '\[~\]' "$STATE")" && \
echo "Pending: $(grep -c '\[ \]' "$STATE")" && \
echo "--- Mandatory Agents ---" && \
grep 'step-4:' "$STATE" && \
grep 'step-5:' "$STATE" && \
grep 'step-6:' "$STATE" && \
echo "=== END AUDIT ==="
```

**Audit pass criteria:**
- Pending count = `0` (or `1` for the audit line itself)
- step-4: `tester_spawned=true` OR `skipped`
- step-5: `reviewer_spawned=true` (never skippable)
- step-6: `pm=true docs=true git=true` (never skippable)

**IF AUDIT FAILS:** identify pending step → execute it → re-audit.

### Checkpoint (only after audit passes)
```
Edit: "- [ ] step-6: finalize | pm=false docs=false git=false" → "- [x] step-6: finalize | pm=true docs=true git=true"
Edit: "- [ ] audit: completion-verified" → "- [x] audit: completion-verified"
```

### Transition
→ IF mode=auto AND more phases remain: return to Step 3 for next phase
→ ELSE: workflow COMPLETE

**Output:** `Step 6: Finalized — 3 agents spawned — audit PASSED — committed`

---

## Mode Flow Summary

```
interactive: S0 → S1 → |G1| → S2 → |G2| → S3 → |G3| → S4 → |G4| → S5 → |review| → S6+audit
auto:        S0 → S1 → S2 → S3 → S4 → S5 → S6+audit → [next phase S3...]
fast:        S0 → S2(fast) → |G2| → S3 → |G3| → S4 → |G4| → S5 → |review| → S6+audit
parallel:    S0 → S1? → |G1| → S2(parallel) → |G2| → S3(multi) → |G3| → S4 → |G4| → S5 → |review| → S6+audit
no-test:     S0 → S1 → |G1| → S2 → |G2| → S3 → |G3| → [skip S4] → S5 → |review| → S6+audit
code:        S0 → S3 → |G3| → S4 → |G4| → S5 → |review| → S6+audit
```

## Critical Enforcement

1. **Every step updates the state file.** No exceptions.
2. **Every gate calls AskUserQuestion.** No text-only prompts.
3. **Steps 4, 5, 6 spawn agents.** Direct implementation = violation.
4. **Step 6 runs audit.** Workflow is INCOMPLETE until audit passes.
5. **No stopping between steps** unless at a review gate or fatal error.
6. **State file is the source of truth.** If it shows pending steps, they must execute.
