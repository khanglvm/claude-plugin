---
name: ideate
description: >
  Transforms a fragment idea into a full, battle-tested product/feature proposal
  with variants, edge cases, and navigable decision trees. Produces a set of
  linked markdown files (PRD, personas, approaches, edge cases, what-if scenarios,
  technical architecture, decision records) that stakeholders can explore without
  re-running agents. Use this skill when the user mentions "ideate", "product idea",
  "feature proposal", "brainstorm a feature", "flesh out this idea", "turn this into
  a proposal", "product spec from scratch", "explore approaches", or any variation
  of converting a rough/fragment idea into a structured product document. Also trigger
  when the user says things like "I have a rough idea for...", "what if we built...",
  "explore this concept", or "think through this feature". This skill handles new
  products, new features for existing products, and feature variant/A-B exploration.
---

# Ideate: Recursive Product Ideation Engine

A Claude Code skill that converts fragment ideas into full, **research-backed**,
battle-tested product proposals through multi-agent recursive expansion. It spawns
layered subagents to research, diverge, critique, fact-check, synthesize, and
branch — producing a navigable network of linked markdown files grounded in
real-world data, competitive intelligence, and industry best practices.

## Research Philosophy

**Opinions are cheap. Data is expensive. This skill pays the cost.**

Every agent in the pipeline follows the Confidence Threshold Rule defined in
`references/research-protocol.md`. The short version:
- Confidence > 0.8 → State the claim directly
- Confidence 0.4–0.8 → **MUST research via WebSearch/WebFetch before including**
- Confidence < 0.4 → **MUST research. If inconclusive, mark ⚠️ UNVERIFIED**

The pipeline includes two dedicated research phases (0.5 and 2.5) plus embedded
research triggers in every agent. The result: proposals cite real benchmarks,
real competitors, real case studies — not LLM confabulations.

## Quick Start

The skill accepts an idea fragment via `$ARGUMENTS`:
```
/ideate "users need better onboarding for our SaaS product"
/ideate "AI-powered code review tool for small teams"
/ideate "add collaborative editing to our note-taking app"
```

---

## Script-Enforced Workflow

The pipeline is enforced by bash scripts in `scripts/`. The main orchestrator
is `scripts/ideate-run.sh` which tracks state, validates gate conditions, and
prevents phases from running out of order.

**Before starting**: Initialize the pipeline:
```bash
bash scripts/ideate-run.sh init "[feature-slug]"
```

**At each phase boundary**: Use `begin` and `end` commands:
```bash
bash scripts/ideate-run.sh begin "[slug]" [phase]   # Checks prereqs, marks started
# ... do the phase work (spawn subagents, write files) ...
bash scripts/ideate-run.sh end "[slug]" [phase]      # Validates outputs, marks complete
```

**After final assembly**: Run the quality checker:
```bash
bash scripts/ideate-run.sh quality "[slug]"
```

The `end` command runs gate validation — if outputs are missing, citations too few,
or research insufficient, the gate FAILS and the phase cannot complete. This makes
the research and quality requirements non-negotiable.

### Pipeline State File

State is tracked in `.claude/ideation/[slug]/pipeline-state.json`. This file
records which phases are complete, research statistics, and agent execution log.
Check status at any time:
```bash
bash scripts/ideate-run.sh status "[slug]"
```

---

## Phase 0: Intake & Clarification (30 seconds)

**Goal**: Turn a fragment into a workable brief with minimal friction.

### Script Enforcement
```bash
# Slugify the feature name from $ARGUMENTS
SLUG=$(echo "$ARGUMENTS" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | head -c 40)
bash scripts/ideate-run.sh init "$SLUG"
bash scripts/ideate-run.sh begin "$SLUG" 0
```

### Routing Logic

Classify the input into one of three tiers:

1. **Vague** (< 10 words, no specifics): Run the full 3-question interview
2. **Partial** (has a problem OR solution, not both): Ask 1-2 targeted questions
3. **Detailed** (has problem + audience + some constraints): Skip to Phase 1

### The Interview: Propose → Refine → Lock

Do NOT ask open-ended questions. Instead, propose concrete options and let the
user confirm or modify. This is the single most effective UX pattern — adopted
from Vibe Architect's workflow.

**Question 1 — Who & What Pain?**
> "Based on your idea, I think the primary user is [proposed persona] dealing with
> [proposed pain point]. Does that sound right, or should I adjust?"

**Question 2 — What Does Success Look Like?**
Propose 3 concrete success metrics:
> "In 6 months, success probably looks like one of these:
> A) [Metric tied to adoption]
> B) [Metric tied to retention/engagement]  
> C) [Metric tied to revenue/efficiency]
> Which resonates most, or describe your own?"

**Question 3 — Constraints?**
Propose likely constraints based on the idea domain:
> "I'm assuming these constraints apply:
> - Timeline: [proposed]
> - Team size: [proposed]  
> - Tech stack: [proposed based on codebase scan if available]
> - Budget: [proposed range]
> Confirm or adjust?"

### Output: idea-brief.md (internal working doc)

Write the consolidated brief to `.claude/ideation/[feature-slug]/idea-brief.md`:

```markdown
# Idea Brief: [Feature Name]

## Problem Statement
[1-2 sentences]

## Target User
[Persona description with JTBD statement]

## Success Metrics
[3 measurable outcomes]

## Constraints
[Timeline, team, tech, budget]

## Scope
- [ ] New product from scratch
- [ ] New feature for existing product  
- [ ] Feature variant / A-B exploration

## Raw Input
> [Original user fragment, verbatim]
```

### Complete Phase 0
```bash
bash scripts/ideate-run.sh end "$SLUG" 0
```

---

## Phase 0.5: Research Grounding (2 parallel subagents, ~90s)

**Goal**: Establish the factual foundation before any creative work begins.

### Script Enforcement
```bash
bash scripts/ideate-run.sh begin "$SLUG" 0.5
```
No agent should be "thinking in a vacuum" — every expansion in Phase 1 should
build on real market data, competitor intelligence, and proven patterns.

### Why This Phase Exists

Without upfront research, agents produce plausible-sounding but ungrounded
proposals. The PM Agent guesses market size. The Engineering Agent recommends
technology stacks based on training data, not current maturity. The Business
Agent invents competitor pricing. This phase eliminates that failure mode.

### Spawn 2 Parallel Research Subagents

Read `agents/ideate-research-agent.md` AND `references/research-protocol.md` before spawning.

```
# Research Agent A: Market & Competitive Intelligence
Task(prompt="[Research Agent instructions]
             [Idea brief]
             Focus on: Phase A (Market Context), Phase B (Competitive Landscape), 
             Phase E (Regulatory if applicable).
             You MUST use WebSearch and WebFetch tools.
             Minimum 10 searches. Fetch at least 3 full articles.
             Output: research-market.md")

# Research Agent B: Best Practices & Technology Landscape
Task(prompt="[Research Agent instructions]
             [Idea brief]
             Focus on: Phase C (Best Practices & Case Studies), 
             Phase D (Technology Landscape).
             You MUST use WebSearch and WebFetch tools.
             Minimum 10 searches. Fetch at least 3 full articles.
             Output: research-technical.md")
```

### Merge into Research Dossier

After both agents return, the main agent merges their outputs into a single
`research-dossier.md` following the dossier template in `references/research-protocol.md`.

**This dossier is passed to ALL subsequent agents.** It becomes shared context
that grounds every analysis, critique, and variant in real data.

### Research Quality Gate

Before proceeding to Phase 1, verify:
- [ ] At least 20 total searches were conducted
- [ ] At least 3 competitors were identified with real data
- [ ] At least 2 case studies with quantitative results were found
- [ ] At least 1 technology benchmark with real numbers was found
- [ ] The Source Registry has at least 10 unique, real URLs
- [ ] Any "Research Gaps" are documented (not silently skipped)

If the quality gate fails, run additional targeted searches to fill gaps.

### Complete Phase 0.5
```bash
bash scripts/ideate-run.sh research-stats "$SLUG" [searches] [sources] 0
bash scripts/ideate-run.sh end "$SLUG" 0.5
```

---

## Phase 1: Divergent Expansion (5 parallel subagents, ~60s)

**Goal**: Generate 8-12 distinct solution branches from multiple perspectives.

### Script Enforcement
```bash
bash scripts/ideate-run.sh begin "$SLUG" 1
```

### Codebase Context (if available)

Before spawning agents, scan the codebase for relevant context:

```
Task(prompt="Search the codebase for files related to [feature domain]. 
List: existing data models, API endpoints, UI components, and test files 
that would be affected. Output as a structured markdown summary.")
```

Pass this context to all Layer 1 agents.

### Spawn 5 Parallel Subagents

Read agent definitions from `agents/` directory before spawning.

Each agent receives:
- The idea brief
- **The research dossier from Phase 0.5** (market data, competitors, benchmarks)
- Codebase context (if any)
- Their specific role instructions (from agents/*.md)
- **The research protocol** (from references/research-protocol.md)
- Output format requirements

**CRITICAL**: Agents must NOT see each other's outputs. This prevents anchoring
bias and ensures genuine perspective diversity.

**CRITICAL**: Every agent MUST follow the Confidence Threshold Rule from the
research protocol. When uncertain about a claim, the agent uses WebSearch/WebFetch
to verify BEFORE including it. Every agent has access to these tools.

```
# Spawn all 5 in parallel — each receives the research dossier
Task(prompt="[PM Agent instructions + idea brief + research-dossier.md + research-protocol.md]
             You have access to WebSearch and WebFetch. USE THEM when your confidence
             on any claim drops below 0.8. Cite sources for all market, competitor,
             and benchmark claims.")         → pm-analysis.md

Task(prompt="[UX Agent instructions + idea brief + research-dossier.md + research-protocol.md]
             You have access to WebSearch and WebFetch. USE THEM to find real UX
             benchmarks, interaction pattern studies, and accessibility requirements.
             Cite sources.")                  → ux-analysis.md

Task(prompt="[Engineering Agent instructions + idea brief + research-dossier.md + research-protocol.md]
             You have access to WebSearch and WebFetch. USE THEM to verify technology
             maturity, find real performance benchmarks, and check current pricing
             for infrastructure/services. Cite sources.")  → eng-analysis.md

Task(prompt="[Business Agent instructions + idea brief + research-dossier.md + research-protocol.md]
             You have access to WebSearch and WebFetch. USE THEM to verify market
             data, find real pricing comparisons, and source ROI benchmarks.
             Cite sources.")                  → biz-analysis.md

Task(prompt="[Red Team Agent instructions + idea brief + research-dossier.md + research-protocol.md]
             You have access to WebSearch and WebFetch. USE THEM to find real
             post-mortems, security advisories, regulatory requirements, and
             documented failure modes. Cite sources.")  → redteam-analysis.md
```

### Beam Search Scoring

After all 5 agents return, the main agent scores each proposed solution branch
on 4 dimensions (1-5 scale):

| Dimension   | Weight | Description                              |
|-------------|--------|------------------------------------------|
| Feasibility | 0.30   | Can we build this with current resources? |
| Impact      | 0.30   | How much does this move success metrics?  |
| Novelty     | 0.20   | Does this offer something competitors don't? |
| Alignment   | 0.20   | Does this fit our constraints and culture? |

**Beam width = 5**: Keep top 5 branches, soft-prune (don't delete) the rest.
Store all branches in `.claude/ideation/[slug]/branches/`.

### Complete Phase 1
```bash
bash scripts/ideate-run.sh end "$SLUG" 1
```

---

## Phase 2: Structured Critique (3 subagents, ~45s)

**Goal**: Stress-test the top branches through adversarial cross-review.

### Script Enforcement
```bash
bash scripts/ideate-run.sh begin "$SLUG" 2
```

### Cross-Review Protocol

Spawn 3 parallel critique subagents:

1. **Critique Agent A**: Reviews branches from PM + UX perspective, challenges
   engineering and business assumptions
2. **Critique Agent B**: Reviews branches from Engineering + Business perspective,
   challenges user and market assumptions  
3. **Devil's Advocate Agent**: MUST disagree with any emerging consensus. Finds the
   strongest counter-argument for every recommendation. Read `agents/ideate-devils-advocate.md`.

Each critique must follow this format:
```markdown
## Challenge: [Specific claim being challenged]
- **Evidence Against**: [Why this claim may be wrong]
- **Severity**: [Blocking | Concerning | Minor]
- **Confidence**: [0.0-1.0]
- **Alternative**: [What to do instead]
```

### Complete Phase 2
```bash
bash scripts/ideate-run.sh end "$SLUG" 2
```

---

## Phase 2.5: Fact-Check & Research Deepening (1-2 subagents, ~60s)

**Goal**: Verify the most impactful claims from Phase 1 and 2 through targeted
research.

### Script Enforcement
```bash
bash scripts/ideate-run.sh begin "$SLUG" 2.5
``` Upgrade opinions to facts. Catch any research the Phase 0.5 dossier
missed now that we know what the proposal actually recommends.

### Why This Phase Exists

Phase 0.5 research is broad — it establishes the landscape. But after Phase 1
and 2, specific claims emerge that need targeted verification. The PM Agent
claims "40% time savings" — is that realistic? The Engineering Agent recommends
a specific framework — is it actually production-ready? The Business Agent
estimates pricing — does it match reality? This phase answers those questions.

### Spawn Fact-Check Agent(s)

Read `agents/ideate-fact-checker.md` before spawning.

```
# Fact-Checker: Verify top claims from Phase 1 + 2
Task(prompt="[Fact-Checker Agent instructions]
             [All 5 Phase 1 analysis files]
             [All 3 Phase 2 critique files]
             [Research dossier from Phase 0.5]
             You MUST use WebSearch and WebFetch tools.
             Minimum 10 verification searches.
             Focus on: quantitative claims, disputed claims,
             competitor comparisons, technology recommendations.
             Output: fact-check-report.md")
```

If the idea touches a specialized domain (healthcare, finance, legal), spawn
an additional domain-specific research subagent:

```
# Domain-Specific Researcher (conditional)
Task(prompt="Research [domain]-specific regulations, compliance requirements,
             industry standards, and specialized best practices for [feature].
             Search for: [domain] compliance checklist, [domain] technology
             requirements, [domain] vendor certifications needed.
             Use WebSearch and WebFetch. Minimum 5 searches.
             Output: domain-research.md")
```

### Fact-Check Quality Gate

Before proceeding to Phase 3, verify:
- [ ] At least 10 claims were verified
- [ ] All quantitative claims in the top recommendation are sourced
- [ ] Disputed claims between agents are resolved with external evidence
- [ ] The "Corrections Required" section is complete
- [ ] Unverifiable claims are explicitly listed

### Feed Results into Synthesis

The fact-check report is passed to the Phase 3 Synthesizer alongside all other
materials. The Synthesizer MUST apply corrections from the fact-check before
finalizing the recommendation.

### Complete Phase 2.5
```bash
bash scripts/ideate-run.sh research-stats "$SLUG" [searches] [sources] [claims_verified]
bash scripts/ideate-run.sh end "$SLUG" 2.5
```

---

## Phase 3: Synthesis (1 subagent on best available model, ~45s)

**Goal**: Merge insights into a unified recommendation with preserved dissent.

### Script Enforcement
```bash
bash scripts/ideate-run.sh begin "$SLUG" 3
```

Spawn a single Synthesizer subagent with ALL Phase 1 + Phase 2 + Phase 2.5 outputs:

```
Task(prompt="[Synthesizer instructions from agents/ideate-synthesizer.md]
             [All 5 analysis files]
             [All 3 critique files]
             [Fact-check report from Phase 2.5]
             [Research dossier from Phase 0.5]
             [Idea brief]
             
Produce a unified recommendation that:
1. Identifies areas of agreement across all agents
2. Resolves tensions using confidence-weighted synthesis
3. **APPLIES all corrections from the fact-check report**
4. **CITES research sources for all key claims** using [N] notation
5. Marks genuinely uncertain items as NEEDS_CLARIFICATION
6. Preserves minority opinions in a 'Dissenting Views' section
7. Produces the core PRD structure with a Sources section
8. Identifies any remaining research gaps and runs targeted
   WebSearch/WebFetch to fill them before finalizing")
```

### GoT-Style Merging

The synthesizer should look for **complementary elements across branches** that
can be combined. Example: if Branch A proposes "API-first architecture" and
Branch B proposes "event-driven notifications," the merge might be "event-driven
API gateway with webhook subscriptions."

### Complete Phase 3
```bash
bash scripts/ideate-run.sh end "$SLUG" 3
```

---

## Phase 4: Variant Generation (3 parallel subagents, ~45s)

**Goal**: Produce 3 meaningfully different strategic variants.

### Script Enforcement
```bash
bash scripts/ideate-run.sh begin "$SLUG" 4
```

Each variant agent receives the synthesized core PRD and a distinct disposition:

1. **Speed Variant** (`agents/ideate-variant-speed.md`): Optimize for time-to-market.
   Managed tech debt, aggressive scope cuts, maximum reuse.
   
2. **Excellence Variant** (`agents/ideate-variant-excellence.md`): Optimize for technical
   quality. Robust architecture, comprehensive testing, future-proof design.
   
3. **Lean Variant** (`agents/ideate-variant-lean.md`): Optimize for cost efficiency.
   Minimum viable scope, build-vs-buy analysis favoring buy, smallest team.

Variants must differ on **fundamental tradeoffs**, not surface details.

### Complete Phase 4
```bash
bash scripts/ideate-run.sh end "$SLUG" 4
```

---

## Phase 5: Document Assembly (main agent, ~30s)

**Goal**: Write the final explorable proposal as linked markdown files.

### Script Enforcement
```bash
bash scripts/ideate-run.sh begin "$SLUG" 5
bash scripts/ideate-run.sh scaffold "$SLUG"
```

### Output Directory Structure

Create all files under `proposal-[feature-slug]/`:

```
proposal-[feature-slug]/
├── INDEX.md                      ← Navigation hub (use template)
├── SUMMARY.md                    ← 1-page executive summary  
├── COMPARISON.md                 ← Weighted scoring matrix
│
├── core/
│   ├── PRD.md                    ← Core product requirements
│   ├── OUTCOME.md                ← Desired outcome + metrics
│   └── ASSUMPTIONS.md            ← Explicit assumptions list
│
├── research/
│   ├── INDEX.md                  ← Research overview + source quality
│   ├── DOSSIER.md                ← Full research dossier (from Phase 0.5)
│   ├── FACT-CHECK.md             ← Claim verification report (from Phase 2.5)
│   ├── COMPETITIVE-LANDSCAPE.md  ← Competitor deep dive with citations
│   ├── BENCHMARKS.md             ← Industry/tech benchmarks collected
│   └── SOURCES.md                ← Master source registry (all URLs)
│
├── personas/
│   ├── INDEX.md                  ← Persona overview
│   ├── persona-[name].md         ← Per-persona deep dive
│   └── PERSONA-MATRIX.md         ← Cross-persona feature priorities
│
├── approaches/
│   ├── INDEX.md                  ← Approach comparison
│   ├── approach-speed.md         ← Speed-optimized variant
│   ├── approach-recommended.md   ← Synthesized recommendation
│   ├── approach-lean.md          ← Cost-optimized variant
│   └── TRADEOFF-MATRIX.md        ← Weighted scores + sensitivity
│
├── edge-cases/
│   ├── INDEX.md                  ← Edge case inventory
│   ├── failure-modes.md          ← Red Team output
│   ├── scale-scenarios.md        ← Behavior under load
│   └── security.md               ← Security + misuse scenarios
│
├── what-if/
│   ├── INDEX.md                  ← What-if navigator
│   ├── budget-constrained.md     ← If budget drops 40%
│   ├── timeline-compressed.md    ← If deadline moves up
│   └── scope-expanded.md         ← If stakeholders want more
│
├── technical/
│   ├── architecture.md           ← High-level architecture
│   ├── data-model.md             ← Data model + storage
│   ├── integration-points.md     ← External dependencies
│   └── migration.md              ← Migration/rollout strategy
│
├── decisions/
│   ├── INDEX.md                  ← Decision log
│   └── ADR-001-[topic].md        ← Architecture Decision Records
│
└── meta/
    ├── OPEN-QUESTIONS.md         ← Unresolved items
    ├── GLOSSARY.md               ← Terms used
    └── GENERATION-LOG.md         ← Agent trace + scores
```

### File Templates

Read templates from `templates/` directory for consistent formatting.
Every output file MUST include:

1. **Breadcrumb header**: `← [INDEX](../INDEX.md) | [Parent](./INDEX.md)`
2. **Inline cross-references**: Link to related files wherever claims depend on
   analysis elsewhere
3. **"Where to go next" footer**: 2-3 contextual navigation links

### The INDEX.md Role-Based Entry Points

```markdown
| Your Role       | Start Here                                    | Time  |
|-----------------|-----------------------------------------------|-------|
| Executive       | [Summary](./SUMMARY.md)                       | 2 min |
| Product Manager | [Comparison](./COMPARISON.md)                 | 5 min |
| Engineer        | [Recommended](./approaches/approach-recommended.md) | 10 min |
| Skeptic         | [Edge Cases](./edge-cases/INDEX.md)           | 5 min |
| Designer        | [Personas](./personas/INDEX.md)               | 5 min |
```

### TRADEOFF-MATRIX.md Sensitivity Analysis

Include pre-computed sensitivity notes:
> "If cost weight increases from 20% to 35%, Approach A overtakes Approach B"
> "If feasibility for Approach C improves (pending tech spike), it becomes the winner"

This lets stakeholders explore how the recommendation changes under different
priorities WITHOUT re-running agents.

### Complete Phase 5
```bash
bash scripts/ideate-run.sh end "$SLUG" 5
bash scripts/ideate-run.sh quality "$SLUG"
bash scripts/ideate-run.sh status "$SLUG"
```

---

## Quality Checks (before presenting output)

**These checks are enforced by `scripts/ideate-check-quality.sh`** — running
`ideate-run.sh quality [slug]` executes them automatically. The script returns
exit 1 if any critical check fails, preventing premature delivery.

Before presenting the final proposal, verify:

### Structural Checks
- [ ] Every file has breadcrumb navigation
- [ ] INDEX.md links to all files  
- [ ] COMPARISON.md has scores for all approaches
- [ ] OPEN-QUESTIONS.md has at least 3 items (if not, the Red Team didn't push hard enough)
- [ ] failure-modes.md exists and is non-trivial
- [ ] At least 2 ADR decision records exist
- [ ] No file references a path that doesn't exist

### Research Quality Checks
- [ ] SOURCES.md exists with at least 15 unique, real URLs
- [ ] DOSSIER.md covers market, competitors, case studies, and technology
- [ ] FACT-CHECK.md has verified at least 10 claims
- [ ] Every approach file cites at least 3 external sources
- [ ] The core PRD.md has inline citations [N] for all quantitative claims
- [ ] COMPETITIVE-LANDSCAPE.md has real competitor data (not hallucinated)
- [ ] BENCHMARKS.md has at least 3 industry/technology benchmarks with sources
- [ ] No claim marked ⚠️ UNVERIFIED appears in the executive summary
- [ ] All "Corrections Required" from the fact-check are applied

### Citation Format Check
- [ ] Every file with research-backed claims has a **Sources** footer section
- [ ] Citations use [N] inline notation linked to the Sources section
- [ ] Source entries include: Author/Publication, Title, Date, URL
- [ ] No source URL is fabricated (if uncertain, search to verify the URL exists)

If any check fails, fix it before presenting.

---

## Context Engineering Notes

- Each subagent receives ONLY the context it needs (observation masking)
- Subagents start with fresh context — embed all necessary info in the Task prompt
- The main agent maintains a running status summary between phases
- Auto-compact instruction: "When compacting, preserve: idea brief, all scoring
  results, list of generated files, and current phase status"
- Budget: Use Sonnet-class for Layer 1/2/4 agents, best available for Layer 3 synthesis

---

## Agent Definitions

Read the following files from `agents/` before spawning each subagent:

| Agent              | File                               | Phase | Has WebSearch? |
|--------------------|------------------------------------|-------|----------------|
| Research Agent     | `agents/ideate-research-agent.md`  | 0.5   | **YES — primary tool** |
| PM Agent           | `agents/ideate-pm-agent.md`        | 1     | YES — on low confidence |
| UX Agent           | `agents/ideate-ux-agent.md`        | 1     | YES — on low confidence |
| Engineering Agent  | `agents/ideate-eng-agent.md`       | 1     | YES — on low confidence |
| Business Agent     | `agents/ideate-biz-agent.md`       | 1     | YES — on low confidence |
| Red Team Agent     | `agents/ideate-redteam-agent.md`   | 1     | YES — on low confidence |
| Devil's Advocate   | `agents/ideate-devils-advocate.md` | 2     | YES — to back challenges |
| Fact-Checker       | `agents/ideate-fact-checker.md`    | 2.5   | **YES — primary tool** |
| Synthesizer        | `agents/ideate-synthesizer.md`     | 3     | YES — gap-filling |
| Speed Variant      | `agents/ideate-variant-speed.md`   | 4     | YES — cost/pricing checks |
| Excellence Variant | `agents/ideate-variant-excellence.md`| 4   | YES — tech maturity checks |
| Lean Variant       | `agents/ideate-variant-lean.md`    | 4     | YES — vendor pricing checks |

**All agents** receive `references/research-protocol.md` as context and must follow
the Confidence Threshold Rule. Research-primary agents (Research Agent, Fact-Checker)
are expected to make 10-20+ searches each. Other agents make 2-5 searches as needed.

## Creative Directives

Read `directives/creative-directives.md` during Phase 1 for the catalog of
expansion techniques (SCAMPER, Reverse Brainstorming, First Principles, etc.)

## Reference Frameworks

Read `references/frameworks.md` for PM framework definitions (JTBD, OST, RICE,
MoSCoW, Business Model Canvas) used across agents.

## Research Protocol

Read `references/research-protocol.md` for the Confidence Threshold Rule,
search strategy guidelines, source quality hierarchy, citation format, and
the research dossier template. **This file is mandatory context for ALL agents.**
