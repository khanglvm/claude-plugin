# Creative Directives Catalog

Used during Phase 1 (Divergent Expansion) to generate diverse solution branches.
Each directive is a structured prompt technique applied to the idea fragment.

## SCAMPER Framework

Apply each operation to the core idea to generate variants:

| Operation   | Prompt Pattern | Example |
|-------------|----------------|---------|
| **S**ubstitute | "What if we replaced [component] with [alternative]?" | Replace manual review with AI scoring |
| **C**ombine | "What if we merged this with [adjacent feature]?" | Combine onboarding with tutorial system |
| **A**dapt | "How does [other industry] solve this problem?" | Adapt Duolingo's streak mechanic for SaaS |
| **M**odify | "What if [dimension] was 10x bigger/smaller?" | What if onboarding was 30 seconds, not 5 minutes? |
| **P**ut to other use | "Who else could benefit from this?" | Could the same flow serve API users? |
| **E**liminate | "What if we removed [assumed requirement]?" | What if there was no sign-up step at all? |
| **R**everse | "What if the opposite approach worked?" | What if users taught the system, not vice versa? |

## First Principles Decomposition

1. Strip the idea to its fundamental requirements
2. Rebuild from scratch without assumed constraints
3. Ask: "If we were starting from zero, would we build it this way?"

## Analogy Transfer

Apply solutions from unrelated domains:
- **Gaming**: Progress bars, achievements, leaderboards, difficulty curves
- **Social media**: Feeds, following, sharing, reactions
- **E-commerce**: Recommendations, reviews, wishlists, compare
- **Physical world**: Spatial metaphors, tools, workspaces
- **Education**: Curricula, assessments, certificates, cohorts

## Constraint Injection

Add artificial constraints to force creative solutions:
- "How would we solve this with zero UI?" (API/automation only)
- "How would we solve this for users with no internet?" (offline-first)
- "How would we solve this with a $0 budget?" (open-source/community)
- "How would we solve this in 1 day?" (extreme simplification)

## Inversion

- Instead of "How to onboard users?" → "How to make users NOT need onboarding?"
- Instead of "How to reduce churn?" → "How to make the product so embedded they can't leave?"
- Instead of "How to add a feature?" → "How to solve the problem without any new features?"

## Six Thinking Hats (adapted for idea expansion)

| Hat    | Focus              | Question for each branch                    |
|--------|--------------------|---------------------------------------------|
| White  | Data & Facts       | What data do we have? What's missing?       |
| Red    | Feelings & Intuition | What feels right/wrong about this?        |
| Black  | Caution & Risks    | What could go wrong?                        |
| Yellow | Benefits & Value   | What's the best case scenario?              |
| Green  | Creativity         | What's the wildcard approach nobody expects? |
| Blue   | Process & Control  | How do we decide between these options?     |

## Usage in Phase 1

The main agent selects 3-4 directives most relevant to the idea domain and
distributes them across the 5 Layer 1 agents. Each agent applies 1-2 directives
alongside their primary analysis framework to ensure output diversity.

Default allocation:
- PM Agent: SCAMPER (Combine, Eliminate) + First Principles
- UX Agent: Analogy Transfer + Inversion
- Engineering Agent: Constraint Injection + First Principles
- Business Agent: SCAMPER (Put to other use, Modify) + Six Hats (Yellow, Black)
- Red Team Agent: Inversion + Six Hats (Black, Red) + Constraint Injection
