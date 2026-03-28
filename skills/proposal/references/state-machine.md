# Workflow State Machine

Deterministic state tracking. Every step writes a checkpoint. Every transition verifies the previous checkpoint. Missing checkpoints = incomplete workflow.

## State File

**Location:** `{plan_dir}/.proposal-state.md`
**Created at:** Step 0 (before any other work)
**Updated at:** Every step completion and gate passage

### Initialize (Step 0 — Write tool)

```markdown
# Proposal State
task: {description}
mode: {detected_mode}
plan_dir: {path_or_TBD}
started: {ISO_timestamp}

## Checkpoints
- [ ] step-0: intent-detection
- [ ] step-1: research
- [ ] gate-1: research-reviewed
- [ ] step-2: planning
- [ ] gate-2: plan-approved
- [ ] step-3: implementation
- [ ] gate-3: implementation-reviewed
- [ ] step-4: testing | tester_spawned=false
- [ ] gate-4: testing-reviewed
- [ ] step-5: code-review | reviewer_spawned=false
- [ ] step-6: finalize | pm=false docs=false git=false
- [ ] audit: completion-verified
```

### Update a Checkpoint (Edit tool)

```
Edit(
  file_path="{plan_dir}/.proposal-state.md",
  old_string="- [ ] step-N: {label}",
  new_string="- [x] step-N: {label} | {key=value metadata}"
)
```

**Rule:** Update checkpoint IMMEDIATELY after step completes, BEFORE any output or transition.

### Error Marker (Bash or Edit tool)

Use `[!]` for steps where an agent failed or state was unrecoverable:

```
- [!] step-N: {label} | agent={name} error={summary}
```

The audit treats `[!]` as a failure — the step must be retried or user-escalated before audit can pass.

### Verify Previous Step (Grep tool — Gate In)

```
Grep(
  pattern="\\[x\\] step-{N-1}",
  path="{plan_dir}/.proposal-state.md",
  output_mode="count"
)
```

Result MUST be `1`. If `0` → previous step incomplete → DO NOT PROCEED → execute missing step first.

## Mode-Specific Checkpoint Skips

Steps that may be skipped per mode (mark as `- [~] step-N: skipped ({reason})`):

| Mode | Skip | Keep |
|------|------|------|
| interactive | none | all |
| auto | gates 1-4 | all steps |
| fast | step-1, gate-1 | all others |
| no-test | step-4, gate-4 | all others |
| code | step-1, gate-1, step-2, gate-2 | all others |

## Completion Audit Protocol

Run at END of Step 6. Workflow is INCOMPLETE until audit passes.

### Audit Checks (Bash tool)

```bash
STATE="{plan_dir}/.proposal-state.md"
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

### Pass Criteria

| Check | Rule |
|-------|------|
| Pending count | Must be `0` (only `[x]` or `[~]` allowed) |
| `step-4` | `tester_spawned=true` OR `skipped (no-test)` |
| `step-5` | `reviewer_spawned=true` (never skippable) |
| `step-6` | `pm=true docs=true git=true` (never skippable) |
| `audit` | `completion-verified` (final checkpoint) |

### Audit Failure Recovery

If any check fails:
1. Identify which step has `[ ]` (pending)
2. Execute that step NOW
3. Re-run audit
4. NEVER mark audit complete until all checks pass


## Partial Completion / Resume Protocol

When a workflow is suspended (context limit, process crash, user exit):

1. User resumes with `/proposal --resume {plan_dir}`
2. Read `.proposal-state.md` — find last `[x]`, start from next `[ ]` or `[!]`
3. **Do NOT re-execute `[x]` steps** — verify output artifacts exist (plan files, code changes, test reports)
4. If an artifact is missing for a `[x]` step, downgrade it to `[ ]` and re-run

### State File Corruption Recovery

| Situation | Action |
|-----------|--------|
| File missing | Reconstruct: scan `{plan_dir}/` for plan files, reports, git diff |
| File exists but unreadable | Delete and recreate from evidence; add `recovered: true` header |
| Partial write (truncated) | Append missing checkpoints as `[ ]`; do not assume they completed |

Add to state header when recovered:
```
recovered: true
recovered_at: {ISO_timestamp}
recovery_reason: {crash|context-limit|manual}
```

## Step Continuation Rules

**These rules prevent the agent from stopping mid-workflow.**

1. After completing a step, IMMEDIATELY proceed to next step or review gate. No pausing.
2. The ONLY valid pause points are **review gates** (where `AskUserQuestion` is called).
3. In **auto mode**, there are ZERO valid pause points except fatal errors.
4. You may NOT output a summary and stop. Workflow ends at audit checkpoint, not before.
5. If you are about to stop and `audit: completion-verified` is not `[x]`, you are violating this protocol.
6. If context window is running low, output: `"WORKFLOW SUSPENDED at step-N. Resume with: /proposal --resume {plan_dir}"` — but this is a last resort, not a convenience.
