# Comparison Matrix: {{FEATURE_NAME}}

← [Back to INDEX](./INDEX.md)

## Weighted Scoring

| Criterion        | Weight | Speed ⚡ | Recommended ✓ | Lean 💰 |
|------------------|--------|----------|---------------|---------|
| Feasibility      | 30%    | ★★★★☆ (4) | ★★★★☆ (4) | ★★★★★ (5) |
| Impact           | 30%    | ★★★☆☆ (3) | ★★★★☆ (4) | ★★★☆☆ (3) |
| Novelty          | 20%    | ★★☆☆☆ (2) | ★★★★☆ (4) | ★★☆☆☆ (2) |
| Alignment        | 20%    | ★★★★☆ (4) | ★★★★☆ (4) | ★★★☆☆ (3) |
| **Weighted Total** | 100% | **3.2**  | **4.0**       | **3.4** |

## Quick Comparison

| Dimension         | Speed ⚡          | Recommended ✓      | Lean 💰           |
|-------------------|-------------------|---------------------|-------------------|
| Timeline          | {{speed_time}}    | {{rec_time}}        | {{lean_time}}     |
| Team Size         | {{speed_team}}    | {{rec_team}}        | {{lean_team}}     |
| Effort (T-shirt)  | {{speed_effort}}  | {{rec_effort}}      | {{lean_effort}}   |
| Tech Debt Risk    | {{speed_debt}}    | {{rec_debt}}        | {{lean_debt}}     |
| Scale Ceiling     | {{speed_scale}}   | {{rec_scale}}       | {{lean_scale}}    |
| Rollback Difficulty | {{speed_rollback}} | {{rec_rollback}} | {{lean_rollback}} |

## Sensitivity Analysis

> These pre-computed scenarios show how the recommendation changes under
> different stakeholder priorities — no need to re-run agents.

| If...                                        | Winner Changes To |
|----------------------------------------------|-------------------|
| Cost weight increases from 20% to 40%        | {{sensitivity_1}} |
| Timeline is cut by 50%                       | Speed ⚡           |
| Team grows by 2 engineers                    | {{sensitivity_3}} |
| Feasibility of Approach X improves (post-spike) | {{sensitivity_4}} |

## Where to go next

- Deep dive into the winner: [Recommended Approach](./approaches/approach-recommended.md)
- Understand the risks: [Edge Cases](./edge-cases/INDEX.md)
- Check what's unresolved: [Open Questions](./meta/OPEN-QUESTIONS.md)
