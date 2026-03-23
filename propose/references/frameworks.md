# Product Frameworks Reference

Quick reference for PM frameworks used across agents. Agents should internalize
these definitions rather than quoting them verbatim in outputs.

## Jobs-to-be-Done (JTBD)

Users "hire" products to get jobs done. Three job types:

- **Functional**: The practical task ("I need to send a report to my team")
- **Emotional**: The feeling sought ("I want to feel confident the data is right")
- **Social**: The perception desired ("I want my team to see me as organized")

Format: "When [situation], I want to [motivation], so I can [expected outcome]."

## Opportunity Solution Tree (OST)

Teresa Torres' framework. Top-down structure:

```
Desired Outcome (metric)
  └── Opportunity (unmet need)
        ├── Solution A
        │     └── Experiment (cheapest test)
        ├── Solution B
        │     └── Experiment
        └── Solution C
              └── Experiment
```

Key rule: Always compare 3+ solutions per opportunity. Never evaluate in isolation.

## RICE Scoring

Prioritization formula: RICE = (Reach × Impact × Confidence) / Effort

| Factor     | Scale                                      |
|------------|--------------------------------------------|
| Reach      | # of users affected per quarter             |
| Impact     | 0.25 (minimal) / 0.5 (low) / 1 (medium) / 2 (high) / 3 (massive) |
| Confidence | 100% (high) / 80% (medium) / 50% (low)    |
| Effort     | Person-months                               |

## MoSCoW Prioritization

- **Must have**: Without this, the release is not viable
- **Should have**: Important but not critical for launch
- **Could have**: Desirable if time/resources permit
- **Won't have (this time)**: Explicitly excluded from scope

## Business Model Canvas (Lightweight)

For feature-level analysis, focus on:
- **Value Proposition**: What unique value does this deliver?
- **Customer Segments**: Who benefits most?
- **Revenue Streams**: How does this generate/protect revenue?
- **Cost Structure**: What does this cost to build and maintain?
- **Key Resources**: What do we need that we don't have?

## Assumption Testing

From Teresa Torres' framework. For each proposal:

1. List all assumptions (desirability, viability, feasibility, usability)
2. Rate each: Impact (if wrong) × Uncertainty (how sure are we)
3. Test highest-risk assumptions first
4. Cheapest test that produces a clear signal wins

## Pre-Mortem

Gary Klein's technique:
1. "Imagine it's 6 months from now. This feature has completely failed."
2. Each participant writes down WHY it failed (independently)
3. Compile all failure reasons
4. Address the most common/severe ones in the plan

## Architecture Decision Records (ADR)

MADR format for recording key decisions:

```markdown
# ADR-NNN: [Decision Title]

## Status: [Proposed | Accepted | Deprecated | Superseded]

## Context
[What is the issue that we're seeing that is motivating this decision?]

## Decision Drivers
- [driver 1]
- [driver 2]

## Considered Options
1. [option 1]
2. [option 2]
3. [option 3]

## Decision Outcome
Chosen option: "[option N]", because [justification].

## Consequences
- Good: [positive outcome]
- Bad: [negative outcome]
- Neutral: [tradeoff accepted]
```
