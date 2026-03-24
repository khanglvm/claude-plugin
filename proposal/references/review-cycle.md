# Code Review Cycle

Deterministic review-fix cycle. All review gates use exact tool calls.

## Interactive Cycle (max 3 cycles)

```
cycle = 0
LOOP:
  1. SPAWN code-reviewer (MANDATORY — exact call):
     Agent(
       subagent_type="code-reviewer",
       prompt="Review changes. Return: score (X/10), critical[], warnings[], suggestions[]. End with Status: DONE.",
       description="Code review cycle {cycle}"
     )
     PARSE: score, critical_count, warnings, suggestions

  2. DISPLAY (output to user):
     ┌──────────────────────────────────────┐
     │ Code Review: {score}/10              │
     ├──────────────────────────────────────┤
     │ Critical ({N}): MUST FIX             │
     │  - {issue} at {file:line}            │
     │ Warnings ({N}): SHOULD FIX           │
     │  - {issue} at {file:line}            │
     │ Suggestions ({N}): NICE TO HAVE      │
     │  - {suggestion}                      │
     └──────────────────────────────────────┘

  3. GATE — AskUserQuestion (MANDATORY tool call):
     IF critical_count > 0:
       AskUserQuestion(
         question="Review: {score}/10 with {critical_count} critical issues.\nChoose action:",
         options=["Fix critical issues", "Fix all issues", "Approve anyway", "Abort"]
       )
       → "Fix critical" → fix criticals, re-spawn tester, cycle++, LOOP
       → "Fix all" → fix all, re-spawn tester, cycle++, LOOP
       → "Approve anyway" → PROCEED
       → "Abort" → STOP

     ELSE:
       AskUserQuestion(
         question="Review: {score}/10, no critical issues.\nChoose action:",
         options=["Approve", "Fix warnings/suggestions", "Abort"]
       )
       → "Approve" → PROCEED
       → "Fix warnings" → fix, cycle++, LOOP
       → "Abort" → STOP

  4. IF cycle >= 3 AND user selects fix:
     AskUserQuestion(
       question="3 review cycles completed. Final decision required.",
       options=["Approve with noted issues", "Abort workflow"]
     )
```

## Auto-Handling Cycle

```
cycle = 0
LOOP:
  1. SPAWN code-reviewer (same as above)
     PARSE: score, critical_count

  2. IF score >= 9.5 AND critical_count == 0:
     → Auto-approve. PROCEED.

  3. ELSE IF critical_count > 0 AND cycle < 3:
     → Auto-fix critical issues
     → Re-spawn tester to verify fixes
     → cycle++, LOOP

  4. ELSE IF critical_count > 0 AND cycle >= 3:
     → ESCALATE to user via AskUserQuestion

  5. ELSE (no critical, score < 9.5):
     → Approve with warnings logged. PROCEED.
```

## State File Update (after review completes)

```
Edit(
  file_path="{plan_dir}/.proposal-state.md",
  old_string="- [ ] step-5: code-review | reviewer_spawned=false",
  new_string="- [x] step-5: code-review | reviewer_spawned=true score={score}"
)
```

## Critical Issues Definition
- Security: XSS, SQL injection, OWASP vulnerabilities
- Performance: bottlenecks, inefficient algorithms
- Architecture: pattern violations, tight coupling
- Principles: YAGNI, KISS, DRY violations
