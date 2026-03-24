# Subagent Patterns

Exact tool call patterns. Copy these — do not paraphrase.

## Spawn Pattern

```
Agent(subagent_type="{type}", prompt="{task}", description="{3-5 word summary}")
```

Every subagent prompt MUST end with:
```
End with: Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Summary: [1-2 sentences]
Concerns/Blockers: [if applicable]
```

## Post-Spawn Validation

After EVERY agent spawn, verify the result:
1. Check status line in response (`Status: DONE` etc.)
2. If `BLOCKED` or `NEEDS_CONTEXT` → provide missing info and re-spawn
3. If `DONE_WITH_CONCERNS` → read concerns, address if correctness-related
4. Update state file checkpoint with result metadata

---

## Research

```
Agent(
  subagent_type="researcher",
  prompt="Research {topic} for implementing {feature}.\nFocus: {specific_questions}\nReport ≤150 lines with citations.\nEnd with: Status: DONE | BLOCKED\nSummary: [findings]",
  description="Research {topic}"
)
```
Spawn 2-3 in parallel for different topics.

## Scout

```
Agent(
  subagent_type="Explore",
  prompt="Find files related to {feature} in codebase.\nList: file paths, their purpose, key exports/functions.\nEnd with: Status: DONE\nSummary: [N files found]",
  description="Scout {feature}"
)
```

## Planning

```
Agent(
  subagent_type="planner",
  prompt="Create implementation plan for: {task}\nResearch reports: {report_paths}\nScout results: {scout_summary}\nSave to: {plan_dir}/\nCreate: plan.md + phase-XX-*.md files\nEnd with: Status: DONE\nSummary: [N phases created]",
  description="Plan {task}"
)
```

## Testing (MANDATORY — never skip spawn)

```
Agent(
  subagent_type="tester",
  prompt="Test implementation for plan: {plan_dir}\nChanged files: {file_list}\nRun existing tests. Write new tests for: happy path, edge cases, errors.\nDO NOT mock, fake, or skip. DO NOT modify assertions to pass.\nEnd with: Status: DONE | BLOCKED\nInclude: pass_count={N} fail_count={N} coverage={N}%",
  description="Test {task}"
)
```

**State file update after spawn:**
```
Edit: "tester_spawned=false" → "tester_spawned=true pass={N} fail={N}"
```

## Debugging (spawn when tests fail)

```
Agent(
  subagent_type="debugger",
  prompt="Analyze test failures:\n{failure_details}\nRoot cause analysis. Provide fix.\nEnd with: Status: DONE | BLOCKED\nSummary: [root cause + fix]",
  description="Debug test failures"
)
```

## Code Review (MANDATORY — never skip spawn)

```
Agent(
  subagent_type="code-reviewer",
  prompt="Review all changes for plan: {plan_dir}\nChanged files: {file_list}\nCheck: security (OWASP), performance, YAGNI/KISS/DRY, architecture.\nReturn: score={X}/10 critical_count={N} warnings=[...] suggestions=[...]\nEnd with: Status: DONE",
  description="Code review"
)
```

**State file update after spawn:**
```
Edit: "reviewer_spawned=false" → "reviewer_spawned=true score={X}"
```

## Project Management (MANDATORY in finalize)

```
Agent(
  subagent_type="project-manager",
  prompt="Run full sync-back for plan: {plan_dir}\n1. Read ALL phase-XX-*.md files\n2. Mark completed items [ ] → [x]\n3. Update plan.md status/progress for ALL phases\nEnd with: Status: DONE\nSummary: [sync results]",
  description="Sync plan status"
)
```

**State file update:** `Edit: "pm=false" → "pm=true"`

## Documentation (MANDATORY in finalize)

```
Agent(
  subagent_type="docs-manager",
  prompt="Review changes from plan: {plan_dir}\nChanged files: {file_list}\nUpdate ./docs/ if warranted.\nEnd with: Status: DONE",
  description="Update docs"
)
```

**State file update:** `Edit: "docs=false" → "docs=true"`

## Git (MANDATORY in finalize)

```
Agent(
  subagent_type="git-manager",
  prompt="Stage and commit all changes with conventional commit message.\nDo NOT push unless explicitly requested.\nEnd with: Status: DONE",
  description="Commit changes"
)
```

**State file update:** `Edit: "git=false" → "git=true"`

## Parallel Execution (parallel mode)

```
Agent(
  subagent_type="fullstack-developer",
  prompt="Implement {phase_file}\nFile ownership: {owned_files}\nDO NOT modify files outside ownership.\nEnd with: Status: DONE",
  description="Implement phase {N}"
)
```
Launch multiple. Respect file ownership. Wait for group before next.
