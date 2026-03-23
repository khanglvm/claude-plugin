---
name: propose
description: >
  Converts a rough idea into a full product proposal or feature spec through
  multi-agent research, critique, and synthesis. Auto-detects whether the user
  needs a lightweight feature proposal (codebase-aware, 4 agents, ~5-8 min) or
  a full product proposal (8+ agents, deep research, ~15-25 min). Single entry
  point: /propose "your idea". Triggers on: "propose", "product idea",
  "feature proposal", "flesh out this idea", "turn this into a proposal",
  "spec from scratch", "explore this concept", "I have a rough idea for",
  "what if we built", "think through this feature".
---

# Propose: Dual-Mode Product Ideation Engine

Converts fragment ideas into research-backed proposals through multi-agent
expansion, critique, and synthesis. Two modes share one entry point:
- **Feature mode** — lighter, codebase-aware, 4 agents, ~5-8 min
- **Product mode** — full ideation, 8+ agents, deep research, ~15-25 min

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

### Scope Challenge (Feature: 3 questions | Product: 5 questions)

Ask before expanding — surfaces fatal assumptions early:

1. **Expansion**: "Is there a bigger version worth exploring, or is scope deliberate?"
2. **Hold**: "Which constraint is non-negotiable — timeline, team, or tech stack?"
3. **Reduction**: "What's the one thing this MUST do? What can we cut if forced?"
4. _(Product only)_ **Adoption**: "Who is the first user who would pay, and what's their current workaround?"
5. _(Product only)_ **Moat**: "What stops a well-funded competitor from copying this in 6 months?"

Lock answers into `idea-brief.md`. Use Propose→Refine→Lock: propose concrete options,
follow threads not checklists, switch to freeform if user says "let me explain."

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

### Feature Phase 1: Focused Expansion (4 parallel agents, ~60s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 1
```

Spawn 4 agents in parallel. Each receives: idea brief + codebase context + feature research.
Agents must NOT see each other's outputs.

```
Task → PM Agent       (agents/ideate-pm-agent.md)       → pm-analysis.md
Task → UX Agent       (agents/ideate-ux-agent.md)       → ux-analysis.md
Task → Eng Agent      (agents/ideate-eng-agent.md)      → eng-analysis.md
Task → RedTeam Agent  (agents/ideate-redteam-agent.md)  → redteam-analysis.md
```

RedTeam in Feature mode: focus on integration risks, security edge cases, most likely
failure scenario for this specific feature in this codebase.
All agents: WebSearch when confidence < 0.8. Cite sources.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 1
```

### Feature Phase 2: Cross-Critique (2 parallel agents, ~30s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 2
```

Spawn 2 critics in parallel. Each receives all 4 Phase 1 outputs.

```
Technical Critic: challenges PM/UX assumptions — integration debt, arch conflicts, security gaps
  Severity: Blocking | Concerning | Minor — Output: critique-technical.md

Product/UX Critic: challenges Eng/RedTeam assumptions — scope creep, friction, UX conflicts
  Severity: Blocking | Concerning | Minor — Output: critique-product-ux.md
```

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 2
```

### Feature Phase 2.5: Quick Fact-Check (1 agent, ~20s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 2.5
```

Read `agents/ideate-fact-checker.md`. Receives all Phase 1 + 2 outputs.

```
Task → Identify top 5 most impactful claims. Verify with WebSearch (min 5 searches).
       Focus: quantitative estimates, tech recommendations, stated constraints.
       Output: fact-check-report.md — VERIFIED | DISPUTED | UNVERIFIABLE per claim.
```

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 2.5
```

### Feature Phase 3: Synthesis + Variant Generation (1 agent, ~45s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 3
```

Read `agents/ideate-synthesizer.md`. Synthesizer receives all Phase 1 + 2 + 2.5 outputs
plus codebase context.

Produces 2 variants (lean):
- **Recommended**: Best balance of quality and integration fit
- **Speed**: Fastest path with acceptable debt, max reuse of existing code

Applies all critique corrections. Applies all fact-check corrections.
Cites research. Marks uncertain items NEEDS_CLARIFICATION.

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
    ├── SOURCES.md
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

### Product Phase 0.5: Deep Research Grounding (3 parallel agents, ~120s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 0.5
```

No agent should think in a vacuum. Research grounds all Phase 1 expansion in real data.

Read `agents/ideate-research-agent.md` AND `references/research-protocol.md` before spawning.

```
Agent A: Market & Competitive Intelligence
  Focus: market sizing, competitive landscape, pricing signals, regulatory risks
  Minimum 15 searches, fetch 3+ full articles — Output: research-market.md

Agent B: Technology & Architecture Landscape
  Focus: tech maturity, build-vs-buy analysis, case studies, benchmarks
  Minimum 15 searches, fetch 3+ full articles — Output: research-technical.md

Agent C: UX Patterns & Case Studies
  Focus: UX conventions, onboarding patterns, analogous product post-mortems
  Minimum 15 searches, fetch 3+ full articles — Output: research-ux.md
```

Merge outputs into `research-dossier.md` (template in `references/research-protocol.md`).
This dossier is passed to ALL subsequent agents.

Research quality gate (30+ sources required):
- [ ] >= 45 total searches (15 per agent)
- [ ] >= 3 competitors with real pricing/feature data
- [ ] >= 2 case studies with quantitative results
- [ ] >= 30 unique real URLs in source registry
- [ ] Research gaps documented

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" research-stats "$SLUG" [searches] [sources] 0
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 0.5
```

### Product Phase 1: Divergent Expansion (5 parallel agents, ~60s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 1
```

Each agent receives: idea brief + research dossier + role instructions.
If CWD has a codebase, include codebase context for Eng Agent.
Agents must NOT see each other's outputs (prevents anchoring bias).
All agents follow Confidence Threshold Rule. WebSearch when confidence < 0.8.

```
Task → PM Agent       (agents/ideate-pm-agent.md)       → pm-analysis.md
Task → UX Agent       (agents/ideate-ux-agent.md)       → ux-analysis.md
Task → Eng Agent      (agents/ideate-eng-agent.md)      → eng-analysis.md  [flag Novel complexity items]
Task → Biz Agent      (agents/ideate-biz-agent.md)      → biz-analysis.md
Task → RedTeam Agent  (agents/ideate-redteam-agent.md)  → redteam-analysis.md
```

Score each proposed branch on 4 dimensions (1-5): Feasibility (0.30), Impact (0.30),
Novelty (0.20), Alignment (0.20). Keep top 5 branches (beam width = 5).
Store all in `.claude/ideation/[slug]/branches/`.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 1
```

### Product Phase 1.5: Validation Interviews (2 parallel agents, ~45s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 1.5
```

Simulate user interviews to surface friction before critique. Each agent receives the
top-scoring branch + personas from idea-brief.md.

```
# Agent A: Primary Persona Interview
Task → Simulate the primary target user walking through the proposed product.
       Identify: onboarding friction, missing features, confusing flows, value gaps.
       Output: validation-primary.md

# Agent B: Edge-Case Persona Interview
Task → Simulate one of: low-tech user, power user, or adversarial user.
       Choose whichever reveals the most risk for this specific idea.
       Identify: accessibility gaps, abuse vectors, unmet power-user needs.
       Output: validation-edge.md
```

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 1.5
```

### Product Phase 2: Structured Critique (3 parallel agents, ~45s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 2
```

Each critique agent receives all Phase 1 + 1.5 outputs.

```
# Critique Agent A: PM+UX lens → challenges Eng+Biz assumptions
# Critique Agent B: Eng+Biz lens → challenges PM+UX assumptions
# Devil's Advocate  (agents/ideate-devils-advocate.md) → finds strongest counter to any consensus
```

Each critique entry: `## Challenge`, Evidence Against, Severity (Blocking|Concerning|Minor),
Confidence (0.0-1.0), Alternative.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 2
```

### Product Phase 2.5: Fact-Check & Research Deepening (1-2 agents, ~60s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 2.5
```

Phase 0.5 research is broad. This phase verifies specific claims from Phases 1 and 2:
quantitative projections, technology recommendations, competitor pricing, ROI estimates.

```
# Fact-Checker (agents/ideate-fact-checker.md)
Task → Receives: all Phase 1 + Phase 2 files + research dossier
       Minimum 15 verification searches. Focus: quantitative, disputed, tech claims.
       Output: fact-check-report.md
```

If domain touches healthcare, finance, or legal — also spawn:
```
Task → Research [domain] compliance/certifications. Min 5 searches. Output: domain-research.md
```

Fact-check quality gate:
- [ ] >= 10 claims verified
- [ ] All quantitative claims in top recommendation are sourced
- [ ] Disputed claims resolved with external evidence
- [ ] Unverifiable claims explicitly listed

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" research-stats "$SLUG" [searches] [sources] [claims_verified]
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 2.5
```

### Product Phase 3: Synthesis (1 agent, best model, ~45s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 3
```

Read `agents/ideate-synthesizer.md`. Synthesizer receives ALL Phase 1 + 1.5 + 2 + 2.5 outputs.

Synthesizer must:
1. Identify areas of agreement across all agents
2. Resolve tensions using confidence-weighted synthesis (GoT-style merging)
3. Apply ALL corrections from fact-check report
4. Incorporate friction points from validation interviews into persona section
5. Cite research using [N] notation for all key claims
6. Mark uncertain items NEEDS_CLARIFICATION
7. Preserve minority opinions in a "Dissenting Views" section
8. Run targeted WebSearch/WebFetch for remaining gaps before finalizing

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 3
```

### Product Phase 3.5: Feasibility Spike (1 agent, conditional, ~45s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 3.5
```

**Condition**: Only run if Eng Agent in Phase 1 flagged any items as "Novel" complexity.
If no Novel items → skip, log "Phase 3.5 skipped: no Novel complexity items."

```
# Feasibility Spike Agent
Task → Receives: eng-analysis.md (Novel items list) + synthesis.md
       For EACH Novel complexity item: minimum 3 searches.
       Find real-world implementations, benchmarks, or post-mortems.
       Output: feasibility-spike.md
       Format per item:
         ## [Technology/Pattern Name]
         - Status: GO | NO-GO | CONDITIONAL
         - Evidence: [links + summary]
         - Risk if wrong: [impact on overall proposal]
         - Mitigation: [fallback approach]
```

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 3.5
```

### Product Phase 4: Variant Generation (3 parallel agents, ~45s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 4
```

Each variant agent receives the synthesized core PRD with a distinct optimization target.
Include feasibility-spike.md if Phase 3.5 ran.

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
│   ├── validation-primary.md
│   ├── validation-edge.md
│   └── PERSONA-MATRIX.md
├── approaches/
│   ├── INDEX.md
│   ├── approach-speed.md
│   ├── approach-excellence.md
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
│   ├── migration.md
│   └── feasibility-spike.md      ← included if Phase 3.5 ran
├── decisions/
│   ├── INDEX.md
│   └── ADR-001-[topic].md
└── meta/
    ├── OPEN-QUESTIONS.md
    ├── GLOSSARY.md
    └── GENERATION-LOG.md
```

INDEX.md role-based entry points: Executive → SUMMARY.md (2 min), PM → COMPARISON.md (5 min),
Engineer → approaches/approach-excellence.md (10 min), Skeptic → edge-cases/INDEX.md (5 min),
Designer → personas/INDEX.md (5 min).

TRADEOFF-MATRIX.md must include sensitivity analysis. Read `templates/` for consistent
formatting. Every file: breadcrumb header, inline cross-refs, "where next" footer.

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
- [ ] fact-check-report.md covers >= 5 claims
- [ ] No UNVERIFIED claims in SUMMARY.md or PRD.md

### Product Mode Checks (full)

Structural:
- [ ] Every file has breadcrumb navigation
- [ ] INDEX.md links to all files
- [ ] COMPARISON.md has scores for all approaches
- [ ] OPEN-QUESTIONS.md has >= 3 items
- [ ] failure-modes.md exists and is non-trivial
- [ ] >= 2 ADR decision records
- [ ] No file references a path that doesn't exist
- [ ] validation-primary.md and validation-edge.md exist in personas/

Research:
- [ ] SOURCES.md has >= 30 unique real URLs
- [ ] DOSSIER.md covers market, competitors, UX patterns, and technology
- [ ] FACT-CHECK.md has verified >= 10 claims with minimum 15 searches
- [ ] Every approach file cites >= 3 external sources
- [ ] PRD.md has inline [N] citations for all quantitative claims
- [ ] COMPETITIVE-LANDSCAPE.md has real competitor data
- [ ] BENCHMARKS.md has >= 3 benchmarks with sources
- [ ] No UNVERIFIED in executive summary
- [ ] All "Corrections Required" from fact-check are applied

Feasibility:
- [ ] If Phase 3.5 ran: feasibility-spike.md exists in technical/ and all Novel items have GO/NO-GO verdict
- [ ] If Phase 3.5 skipped: GENERATION-LOG.md documents the skip reason

Citation format (all modes):
- [ ] Files with research claims have a Sources footer section
- [ ] Citations use [N] inline notation linked to Sources
- [ ] Source entries include: Author/Publication, Title, Date, URL
- [ ] No fabricated source URLs

---

## Agent Table

| Agent | File | Feature | Product |
|-------|------|---------|---------|
| Research Agent | `ideate-research-agent.md` | Phase 0.5 (1x) | Phase 0.5 (3x) |
| PM Agent | `ideate-pm-agent.md` | Phase 1 | Phase 1 |
| UX Agent | `ideate-ux-agent.md` | Phase 1 | Phase 1 |
| Eng Agent | `ideate-eng-agent.md` | Phase 1 | Phase 1 |
| RedTeam Agent | `ideate-redteam-agent.md` | Phase 1 | Phase 1 |
| Biz Agent | `ideate-biz-agent.md` | — | Phase 1 |
| Validation Interview A | _(inline prompt)_ | — | Phase 1.5 |
| Validation Interview B | _(inline prompt)_ | — | Phase 1.5 |
| Technical Critic | _(inline prompt)_ | Phase 2 | — |
| Product/UX Critic | _(inline prompt)_ | Phase 2 | — |
| Critique A/B | _(inline prompts)_ | — | Phase 2 (2x) |
| Devil's Advocate | `ideate-devils-advocate.md` | — | Phase 2 |
| Fact-Checker | `ideate-fact-checker.md` | Phase 2.5 | Phase 2.5 |
| Synthesizer | `ideate-synthesizer.md` | Phase 3 | Phase 3 |
| Feasibility Spike | _(inline prompt)_ | — | Phase 3.5 (cond.) |
| Speed Variant | `ideate-variant-speed.md` | Phase 3 (inline) | Phase 4 |
| Excellence Variant | `ideate-variant-excellence.md` | — | Phase 4 |
| Lean Variant | `ideate-variant-lean.md` | — | Phase 4 |

Research-primary agents (Research Agent, Fact-Checker): 15+ searches. Others: 2-5 per Confidence Threshold Rule.

---

## Context Engineering Notes

- Subagents receive only the context they need — embed all necessary info in Task prompt
- Main agent maintains running status summary between phases
- Auto-compact: preserve idea brief, scoring results, file list, current phase
- Model budget: Sonnet-class for Phase 1/1.5/2/4; best available for Phase 3 synthesis
- Mandatory context for ALL agents: `references/research-protocol.md`
- Phase 1 agents also read: `directives/creative-directives.md`, `references/frameworks.md`

---

## Experimental: Agent Teams Mode

**Status**: Experimental. Available when `TeamCreate` tool is detected.

At the start of Product mode Phase 0.5, detect teams availability:

```
If TeamCreate tool is available AND mode == Product:
  → Use Agent Teams workflow (below)
Else:
  → Print: "Agent Teams not available — using standard subagents."
  → Fall back to standard subagent spawning (all phases above)
```

### When Teams Are Used

Product mode only, on the three heaviest parallel phases:
- Phase 0.5 — 3 research teammates (true parallel)
- Phase 1 — 5 expansion teammates (true parallel)
- Phase 2 — 3 critique teammates (can cross-reference via SendMessage)

### Team Workflow

```
1. TeamCreate(team_name: "propose-{slug}")
2. TaskCreate per agent: subject "[Role] Agent — Phase [N]"
   description: "File ownership: .claude/ideation/{slug}/{output-file}.md\n[full prompt]"
3. Spawn teammates via Task tool with team_name: "propose-{slug}"
   Each teammate: TaskList → claim → work → TaskUpdate(completed) → idle
4. Monitor via TaskList until all tasks completed
5. Main agent reads all output files from .claude/ideation/{slug}/
6. SendMessage(type: shutdown_request) to all teammates
7. TeamDelete(team_name: "propose-{slug}")
```

### File Ownership in Team Mode

Each teammate owns exactly one output file. Declare in task description:
```
File ownership: .claude/ideation/{slug}/research-market.md
```
No two teammates may own the same file. Main agent assembles final outputs only.

### Phase 2 Critique with Cross-Messaging

```
Critique A → reads Phase 1 outputs → drafts critique
Critique A → SendMessage(to: "critique-b", "Flagging X as Blocking — concur?")
Critique B → may adjust severity based on peer confirmation
Both → write output files → TaskUpdate(completed)
```

Devil's Advocate waits for Critique A and B to complete, then challenges the
emerging consensus rather than a phantom one.

### Benefits Over Standard Subagents

- True parallelism (not simulated)
- OS-level file isolation per teammate
- Critique agents can cross-confirm severity via SendMessage
- ~10s overhead per team

### Fallback Guarantee

Every teams-mode phase has an exact equivalent in the standard subagent phases above.
If TeamCreate raises any error, log and fall back to standard subagents.
Output files and quality checks are identical in both paths.
