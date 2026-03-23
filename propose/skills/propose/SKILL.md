---
name: propose
description: >
  Converts a rough idea into a full product proposal or feature spec through
  multi-agent research, critique, and synthesis. Auto-detects whether the user
  needs a lightweight feature proposal (codebase-aware, 3 agents, ~5 min) or
  a full product proposal (5+ agents, deep research, ~15 min). Single entry
  point: /propose "your idea". Triggers on: "propose", "product idea",
  "feature proposal", "flesh out this idea", "turn this into a proposal",
  "spec from scratch", "explore this concept", "I have a rough idea for",
  "what if we built", "think through this feature".
---

# Propose: Dual-Mode Product Ideation Engine

Converts fragment ideas into research-backed proposals through multi-agent
expansion, critique, and synthesis. Two modes share one entry point:
- **Feature mode** — lighter, codebase-aware, 3 agents, ~3-5 min
- **Product mode** — full ideation, 5+ agents, deep research, ~8-15 min

## Path Resolution (read first)

```bash
PROPOSE_HOME="$(for d in "$HOME/.claude/plugins/propose" "$HOME/.claude/plugins/cache/propose" "$HOME/.claude/skills/propose"; do [ -f "$d/scripts/ideate-run.sh" ] && echo "$d" && break; done)"
```

Call scripts: `bash "$PROPOSE_HOME/scripts/ideate-run.sh" ...`
Read agents: `$PROPOSE_HOME/agents/ideate-*.md`
Read refs: `$PROPOSE_HOME/references/research-protocol.md`

Pipeline state: `.claude/ideation/[slug]/` in CWD
Proposal output: `proposal-[slug]/` in CWD

## Quick Start

```
/propose "add collaborative editing to our note-taking app"   → Feature mode
/propose "AI-powered code review tool for small teams"        → Product mode
/propose "better onboarding for our SaaS"                     → auto-detects
```

---

## Phase 0: Intake & Classification

```bash
SLUG=$(echo "$ARGUMENTS" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | head -c 40)
bash "$PROPOSE_HOME/scripts/ideate-run.sh" init "$SLUG"
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 0
```

### Mode Detection

Scan CWD for codebase signals, then apply language signals:

| Signal | Score |
|--------|-------|
| CWD has `package.json`, `src/`, `*.py`, `go.mod`, etc. | +2 Feature |
| Input contains "add", "extend", "integrate", "new feature for" | +2 Feature |
| Input contains "build from scratch", "new product", "startup", "create a" | +2 Product |
| Input contains "app", "tool", "platform" with no existing codebase | +1 Product |
| Input < 10 words with no codebase context | neutral |

- Score >= +2 Feature → **Feature mode**
- Score >= +2 Product → **Product mode**
- Ambiguous → Use `AskUserQuestion`:
  > "I'm thinking this looks like a **[Feature/Product]** proposal based on [signal].
  > Which fits better? A) Feature for an existing product  B) New product from scratch"

### Scope Challenge (3 questions before Phase 1)

Ask before expanding — surfaces fatal assumptions early:

1. **Expansion check**: "Is there a bigger version of this worth exploring? Or is the scope deliberate?"
2. **Hold check**: "Which constraint is non-negotiable — timeline, team size, or tech stack?"
3. **Reduction check**: "What's the one thing this MUST do? What can we cut if forced?"

Lock answers into `idea-brief.md` then run clarification using Propose→Refine→Lock pattern:
- Propose concrete options, don't ask open-ended questions
- Follow threads, not checklists. Challenge vague answers.
- If user says "let me explain" → switch to freeform

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 0
```

---

## Feature Mode (Phases 0.5 → 4)

For extending existing products. Lighter, faster, codebase-aware.

### Feature Phase 0.5: Codebase Scan + Targeted Research (~45s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 0.5
```

Spawn 2 tasks in parallel:

**Task A — Codebase scan**
```
Search CWD for files related to [feature domain].
List: existing data models, API endpoints, UI components, auth patterns,
test files that would be affected.
Output as structured markdown: feature-codebase-context.md
```

**Task B — Domain research (1 agent)**
Read `agents/ideate-research-agent.md`. Focus on feature domain only:
- Existing patterns/libraries solving this problem
- UX conventions for this feature type
- Known failure modes
Minimum 5 searches. Output: `research-feature.md`

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 0.5
```

### Feature Phase 1: Focused Expansion (3 parallel agents, ~60s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 1
```

Spawn 3 agents in parallel. Each receives: idea brief + codebase context + feature research.
Agents must NOT see each other's outputs.

```
Task → PM Agent  (agents/ideate-pm-agent.md)   → pm-analysis.md
Task → UX Agent  (agents/ideate-ux-agent.md)   → ux-analysis.md
Task → Eng Agent (agents/ideate-eng-agent.md)  → eng-analysis.md
```

All agents follow Confidence Threshold Rule from `references/research-protocol.md`.
WebSearch when confidence < 0.8. Cite sources.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 1
```

### Feature Phase 2: Quick Critique (1 combined agent, ~30s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 2
```

Single critic agent receives all 3 Phase 1 outputs:
- Challenges assumptions across all three perspectives
- Identifies blockers vs. concerns (severity: Blocking | Concerning | Minor)
- Surfaces integration risks with existing codebase

Output: `critique-combined.md`

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 2
```

### Feature Phase 3: Synthesis + Variant Generation (1 agent, ~45s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 3
```

Read `agents/ideate-synthesizer.md`. Synthesizer receives all Phase 1 + 2 outputs plus codebase context.

Produces 2 variants (not 3 — leaner):
- **Recommended**: Best balance of quality and integration fit
- **Speed**: Fastest path with acceptable debt, max reuse of existing code

Applies all critique corrections. Cites research. Marks uncertain items NEEDS_CLARIFICATION.

Output: `synthesis.md` with embedded variant sections.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 3
```

### Feature Phase 4: Document Assembly (main agent, ~20s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 4
bash "$PROPOSE_HOME/scripts/ideate-run.sh" scaffold "$SLUG"
```

Feature output structure (lighter — no personas, no what-if, no full research dir):

```
proposal-[slug]/
├── INDEX.md
├── SUMMARY.md
├── core/
│   ├── PRD.md
│   └── ASSUMPTIONS.md
├── approaches/
│   ├── approach-recommended.md
│   ├── approach-speed.md
│   └── TRADEOFF-MATRIX.md
├── edge-cases/
│   └── failure-modes.md
├── technical/
│   ├── architecture.md
│   └── integration-points.md
├── decisions/
│   └── ADR-001-*.md
└── meta/
    ├── OPEN-QUESTIONS.md
    └── GENERATION-LOG.md
```

Every file: breadcrumb header + inline cross-refs + "where next" footer.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 4
bash "$PROPOSE_HOME/scripts/ideate-run.sh" quality "$SLUG"
bash "$PROPOSE_HOME/scripts/ideate-run.sh" status "$SLUG"
```

---

## Product Mode (Phases 0.5 → 5)

For new products and full ideation from scratch. Heavier, deeper research.

### Product Phase 0.5: Deep Research Grounding (2 parallel agents, ~90s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 0.5
```

No agent should think in a vacuum. Research grounds all Phase 1 expansion in real data.

Read `agents/ideate-research-agent.md` AND `references/research-protocol.md` before spawning.

```
# Agent A: Market & Competitive Intelligence
Task → Focus: market context, competitive landscape, regulatory signals
       Minimum 10 searches, fetch 3+ full articles
       Output: research-market.md

# Agent B: Best Practices & Technology Landscape
Task → Focus: case studies, technology maturity, build-vs-buy landscape
       Minimum 10 searches, fetch 3+ full articles
       Output: research-technical.md
```

Merge outputs into `research-dossier.md` (template in `references/research-protocol.md`).
This dossier is passed to ALL subsequent agents.

Research quality gate before proceeding:
- [ ] >= 20 total searches conducted
- [ ] >= 3 competitors with real data
- [ ] >= 2 case studies with quantitative results
- [ ] >= 1 technology benchmark with real numbers
- [ ] >= 10 unique real URLs in source registry
- [ ] Research gaps documented (not silently skipped)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" research-stats "$SLUG" [searches] [sources] 0
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 0.5
```

### Product Phase 1: Divergent Expansion (5 parallel agents, ~60s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 1
```

Each agent receives: idea brief + research dossier + their role instructions.
Agents must NOT see each other's outputs (prevents anchoring bias).
All agents follow Confidence Threshold Rule. WebSearch when confidence < 0.8.

```
Task → PM Agent       (agents/ideate-pm-agent.md)       → pm-analysis.md
Task → UX Agent       (agents/ideate-ux-agent.md)       → ux-analysis.md
Task → Eng Agent      (agents/ideate-eng-agent.md)      → eng-analysis.md
Task → Biz Agent      (agents/ideate-biz-agent.md)      → biz-analysis.md
Task → RedTeam Agent  (agents/ideate-redteam-agent.md)  → redteam-analysis.md
```

After all 5 return, score each proposed branch on 4 dimensions (1-5):

| Dimension   | Weight | Description |
|-------------|--------|-------------|
| Feasibility | 0.30   | Build with current resources? |
| Impact      | 0.30   | Moves success metrics? |
| Novelty     | 0.20   | Differentiates from competitors? |
| Alignment   | 0.20   | Fits constraints and culture? |

Keep top 5 branches (beam width = 5). Store all in `.claude/ideation/[slug]/branches/`.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 1
```

### Product Phase 2: Structured Critique (3 parallel agents, ~45s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 2
```

```
# Critique Agent A: PM+UX lens → challenges Eng+Biz assumptions
# Critique Agent B: Eng+Biz lens → challenges PM+UX assumptions
# Devil's Advocate  (agents/ideate-devils-advocate.md) → finds strongest counter to any consensus
```

Each critique entry format:
```markdown
## Challenge: [Specific claim]
- Evidence Against: [Why this may be wrong]
- Severity: [Blocking | Concerning | Minor]
- Confidence: [0.0-1.0]
- Alternative: [What to do instead]
```

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 2
```

### Product Phase 2.5: Fact-Check & Research Deepening (1-2 agents, ~60s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 2.5
```

Phase 0.5 research is broad. This phase verifies specific claims that emerged in Phases 1 and 2:
quantitative projections, technology recommendations, competitor pricing, ROI estimates.

```
# Fact-Checker (agents/ideate-fact-checker.md)
Task → Receives: all Phase 1 files + all Phase 2 files + research dossier
       Must use WebSearch/WebFetch. Minimum 10 verification searches.
       Focus: quantitative claims, disputed claims, tech recommendations
       Output: fact-check-report.md
```

If domain touches healthcare, finance, or legal — spawn additional domain researcher:
```
Task → Research [domain] compliance requirements, certifications, regulations
       Minimum 5 searches. Output: domain-research.md
```

Fact-check quality gate:
- [ ] >= 10 claims verified
- [ ] All quantitative claims in top recommendation are sourced
- [ ] Disputed claims resolved with external evidence
- [ ] "Corrections Required" section complete
- [ ] Unverifiable claims explicitly listed

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" research-stats "$SLUG" [searches] [sources] [claims_verified]
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 2.5
```

### Product Phase 3: Synthesis (1 agent, best model, ~45s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 3
```

Read `agents/ideate-synthesizer.md`. Synthesizer receives ALL Phase 1 + 2 + 2.5 outputs.

Synthesizer must:
1. Identify areas of agreement across all agents
2. Resolve tensions using confidence-weighted synthesis (GoT-style merging)
3. Apply ALL corrections from fact-check report
4. Cite research using [N] notation for all key claims
5. Mark uncertain items NEEDS_CLARIFICATION
6. Preserve minority opinions in a "Dissenting Views" section
7. Run targeted WebSearch/WebFetch for remaining gaps before finalizing

GoT merging example: Branch A proposes "API-first architecture" + Branch B proposes
"event-driven notifications" → merge as "event-driven API gateway with webhook subscriptions."

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 3
```

### Product Phase 4: Variant Generation (3 parallel agents, ~45s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 4
```

Each variant agent receives the synthesized core PRD with a distinct optimization target:

```
Task → Speed Variant      (agents/ideate-variant-speed.md)     → approach-speed.md
Task → Excellence Variant (agents/ideate-variant-excellence.md) → approach-excellence.md
Task → Lean Variant       (agents/ideate-variant-lean.md)       → approach-lean.md
```

Variants must differ on fundamental tradeoffs, not surface details.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 4
```

### Product Phase 5: Document Assembly (main agent, ~30s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 5
bash "$PROPOSE_HOME/scripts/ideate-run.sh" scaffold "$SLUG"
```

Full output structure:

```
proposal-[slug]/
├── INDEX.md                      ← Navigation hub with role-based entry points
├── SUMMARY.md                    ← 1-page executive summary
├── COMPARISON.md                 ← Weighted scoring matrix
├── core/
│   ├── PRD.md
│   ├── OUTCOME.md
│   └── ASSUMPTIONS.md
├── research/
│   ├── INDEX.md
│   ├── DOSSIER.md
│   ├── FACT-CHECK.md
│   ├── COMPETITIVE-LANDSCAPE.md
│   ├── BENCHMARKS.md
│   └── SOURCES.md
├── personas/
│   ├── INDEX.md
│   ├── persona-[name].md
│   └── PERSONA-MATRIX.md
├── approaches/
│   ├── INDEX.md
│   ├── approach-speed.md
│   ├── approach-recommended.md
│   ├── approach-lean.md
│   └── TRADEOFF-MATRIX.md
├── edge-cases/
│   ├── INDEX.md
│   ├── failure-modes.md
│   ├── scale-scenarios.md
│   └── security.md
├── what-if/
│   ├── INDEX.md
│   ├── budget-constrained.md
│   ├── timeline-compressed.md
│   └── scope-expanded.md
├── technical/
│   ├── architecture.md
│   ├── data-model.md
│   ├── integration-points.md
│   └── migration.md
├── decisions/
│   ├── INDEX.md
│   └── ADR-001-[topic].md
└── meta/
    ├── OPEN-QUESTIONS.md
    ├── GLOSSARY.md
    └── GENERATION-LOG.md
```

INDEX.md role-based entry points:

| Role | Start Here | Time |
|------|------------|------|
| Executive | SUMMARY.md | 2 min |
| Product Manager | COMPARISON.md | 5 min |
| Engineer | approaches/approach-recommended.md | 10 min |
| Skeptic | edge-cases/INDEX.md | 5 min |
| Designer | personas/INDEX.md | 5 min |

TRADEOFF-MATRIX.md must include sensitivity analysis:
> "If cost weight increases from 20% to 35%, Approach A overtakes Approach B"

Read templates from `templates/` for consistent formatting. Every file must include
breadcrumb header, inline cross-refs, and "where next" footer.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 5
bash "$PROPOSE_HOME/scripts/ideate-run.sh" quality "$SLUG"
bash "$PROPOSE_HOME/scripts/ideate-run.sh" status "$SLUG"
```

---

## Quality Checks (mode-aware)

Enforced by `scripts/ideate-check-quality.sh` via `ideate-run.sh quality [slug]`.
Returns exit 1 on any critical failure.

### Feature Mode Checks

- [ ] Every file has breadcrumb navigation
- [ ] INDEX.md links to all files
- [ ] OPEN-QUESTIONS.md has >= 2 items
- [ ] failure-modes.md exists and is non-trivial
- [ ] >= 1 ADR decision record
- [ ] integration-points.md references actual existing code artifacts
- [ ] SOURCES.md has >= 5 unique real URLs
- [ ] No ⚠️ UNVERIFIED claims in SUMMARY.md or PRD.md

### Product Mode Checks (full)

Structural:
- [ ] Every file has breadcrumb navigation
- [ ] INDEX.md links to all files
- [ ] COMPARISON.md has scores for all approaches
- [ ] OPEN-QUESTIONS.md has >= 3 items
- [ ] failure-modes.md exists and is non-trivial
- [ ] >= 2 ADR decision records
- [ ] No file references a path that doesn't exist

Research:
- [ ] SOURCES.md has >= 15 unique real URLs
- [ ] DOSSIER.md covers market, competitors, case studies, technology
- [ ] FACT-CHECK.md has verified >= 10 claims
- [ ] Every approach file cites >= 3 external sources
- [ ] PRD.md has inline [N] citations for all quantitative claims
- [ ] COMPETITIVE-LANDSCAPE.md has real competitor data
- [ ] BENCHMARKS.md has >= 3 benchmarks with sources
- [ ] No ⚠️ UNVERIFIED in executive summary
- [ ] All "Corrections Required" from fact-check are applied

Citation format (all modes):
- [ ] Files with research claims have a Sources footer section
- [ ] Citations use [N] inline notation linked to Sources
- [ ] Source entries include: Author/Publication, Title, Date, URL
- [ ] No fabricated source URLs

---

## Agent Table

| Agent | File | Feature | Product |
|-------|------|---------|---------|
| Research Agent | `ideate-research-agent.md` | Phase 0.5 (1x) | Phase 0.5 (2x) |
| PM Agent | `ideate-pm-agent.md` | Phase 1 | Phase 1 |
| UX Agent | `ideate-ux-agent.md` | Phase 1 | Phase 1 |
| Eng Agent | `ideate-eng-agent.md` | Phase 1 | Phase 1 |
| Biz Agent | `ideate-biz-agent.md` | — | Phase 1 |
| RedTeam Agent | `ideate-redteam-agent.md` | — | Phase 1 |
| Critic (combined) | _(inline prompt)_ | Phase 2 (1x) | — |
| Critique A/B | _(inline prompts)_ | — | Phase 2 (2x) |
| Devil's Advocate | `ideate-devils-advocate.md` | — | Phase 2 |
| Fact-Checker | `ideate-fact-checker.md` | — | Phase 2.5 |
| Synthesizer | `ideate-synthesizer.md` | Phase 3 | Phase 3 |
| Speed Variant | `ideate-variant-speed.md` | Phase 3 (inline) | Phase 4 |
| Excellence Variant | `ideate-variant-excellence.md` | — | Phase 4 |
| Lean Variant | `ideate-variant-lean.md` | — | Phase 4 |

Research-primary agents (Research Agent, Fact-Checker): 10-20+ searches expected.
Other agents: 2-5 searches as needed per Confidence Threshold Rule.

---

## Context Engineering Notes

- Each subagent receives ONLY the context it needs (no cross-agent leaking in Phase 1)
- Subagents start with fresh context — embed all necessary info in the Task prompt
- Main agent maintains running status summary between phases
- Auto-compact instruction: preserve idea brief, scoring results, generated file list, current phase
- Model budget: Sonnet-class for Phase 1/2/4 agents; best available for Phase 3 synthesis
- Read `references/research-protocol.md` as mandatory context for ALL agents
- Read `directives/creative-directives.md` during Phase 1 for expansion techniques
- Read `references/frameworks.md` for PM framework definitions (JTBD, OST, RICE, MoSCoW)
