# Example: What a Generated Proposal Looks Like

This file shows an abbreviated example of what `/ideate "AI-powered code review
for small teams"` would produce. The actual output has 15-25 files; this shows
the key patterns.

---

## Example SUMMARY.md

```markdown
# AI-Powered Code Review — Executive Summary

← [Back to INDEX](./INDEX.md)

## One-Liner
An AI assistant that reviews pull requests for small teams (5-15 devs), catching
bugs, style issues, and architectural concerns before human review — reducing
review time by 40% while improving consistency.

## Recommendation
Build a **GitHub-integrated bot** that runs on every PR, posting inline comments.
Start with a speed-optimized approach: use Claude API for analysis, focus on 3
languages (JS/TS, Python, Go), ship in 3 weeks.

## Key Numbers
| Metric                 | Target (6 months) |
|------------------------|-------------------|
| Review time saved      | 40%               |
| Bugs caught pre-review | 25%               |
| Team adoption          | > 80%             |

## Critical Risks
1. **False positive rate** — If > 15%, devs will ignore all suggestions
2. **Cost at scale** — API costs grow linearly with PR volume
3. **Security** — Code leaves the repo boundary (see Security analysis)

## Open Questions (need human decision)
1. Should we support private/self-hosted repos? (cost implications)
2. What's the acceptable false positive rate? (5% vs 15% threshold)
3. Do we need SOC2 compliance before enterprise customers?

→ [Full PRD](./core/PRD.md) | [Compare approaches](./COMPARISON.md) |
  [What could go wrong](./edge-cases/INDEX.md)
```

---

## Navigation Patterns to Follow

Every file must include:

1. **Breadcrumb**: `← [Back to INDEX](../INDEX.md) | [Section](./INDEX.md)`
2. **Cross-links**: Inline references to related analysis
3. **Footer nav**: `→ [Next logical file] | [Alternative path]`

These patterns ensure the proposal is explorable as a graph, not just a list.
