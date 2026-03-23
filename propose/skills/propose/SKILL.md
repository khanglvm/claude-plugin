---
name: propose
description: >
  Converts a rough idea into a full product proposal or feature spec through
  multi-agent research, critique, and synthesis. Auto-detects whether the user
  needs a lightweight feature proposal (codebase-aware, 4 agents, ~5-8 min) or
  a full product proposal (pillar-based, 10+ agents, deep research, ~20-35 min).
  Single entry point: /propose "your idea". Triggers on: "propose", "product idea",
  "feature proposal", "flesh out this idea", "turn this into a proposal",
  "spec from scratch", "explore this concept", "I have a rough idea for",
  "what if we built", "think through this feature".
---

# Propose: Dual-Mode Product Ideation Engine

Converts fragment ideas into research-backed proposals through multi-agent
expansion, critique, and synthesis. Two modes share one entry point:
- **Feature mode** — lighter, codebase-aware, 4 agents, ~5-8 min
- **Product mode** — pillar-based with feedback loops, 10+ agents, ~20-35 min

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

**CRITICAL: Phase 0 is the ONLY interactive phase.** After `end "$SLUG" 0`, the
entire pipeline runs autonomously with zero user prompts. Conflicts, uncertainties,
and unresolvable items are documented in the output files (OPEN-QUESTIONS.md,
conflict-report.md, NEEDS_CLARIFICATION sections) — never surfaced as blocking
gates or AskUserQuestion calls. The user reviews everything post-assembly.

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
All agents: WebSearch when confidence < 0.8. Must cite what they searched for.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 1
```

### Feature Phase 2: Cross-Critique + Cross-Validation (2 parallel agents, ~30s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 2
```

Spawn 2 critics in parallel. Each receives all 4 Phase 1 outputs TOGETHER.
Key question for each: "Do these 4 perspectives produce a coherent feature, or do they contradict?"

```
Technical Critic: challenges PM/UX assumptions — integration debt, arch conflicts, security gaps.
  Also check: do Eng and PM agree on scope? Do UX and Eng agree on data needs?
  Severity: Blocking | Concerning | Minor — Output: critique-technical.md

Product/UX Critic: challenges Eng/RedTeam assumptions — scope creep, friction, UX conflicts.
  Also check: does RedTeam's risk model align with PM's success criteria?
  Severity: Blocking | Concerning | Minor — Output: critique-product-ux.md
```

If either critic finds unresolved factual conflicts between agents, they may trigger
1-2 targeted WebSearches to break the tie before finalizing their output.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 2
```

### Feature Phase 3: Synthesis + Variant Generation (1 agent, ~45s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 3
```

Read `agents/ideate-synthesizer.md`. Receives all Phase 1 + 2 outputs + codebase context.

Produces 2 variants:
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

Feature output structure:

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

## Product Mode (Phases 0.5 → 8)

For new products from scratch. Architecture is **pillar-based with feedback loops** —
not a linear assembly line. Research is continuous: Phase 1 establishes broad landscape,
Phase 3 pillar agents research their own domain deeply, Phase 5 adversaries verify claims,
Phase 6 synthesizer fills remaining gaps. Every agent has WebSearch.

Proposals validate against each other: Phase 4 cross-validates all pillars to catch
contradictions ("Auth assumes JWT, Dashboard assumes sessions"). Feedback flows backward:
cross-validation conflicts must be resolved by the synthesizer; adversarial BLOCKING items
must be addressed or escalated.

### Product Phase 0.5: Landscape Research (3 parallel agents, ~90s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 0.5
```

Broad research grounds all downstream work. Read `agents/ideate-research-agent.md`
AND `references/research-protocol.md` before spawning.

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

Merge outputs into `landscape/DOSSIER.md`. This dossier is passed as context to ALL
subsequent phases. Research quality gate:
- [ ] >= 45 total searches (15 per agent)
- [ ] >= 3 competitors with real pricing/feature data
- [ ] >= 2 case studies with quantitative results
- [ ] >= 30 unique real URLs in source registry

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" research-stats "$SLUG" [searches] [sources] 0
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 0.5
```

### Product Phase 1: Pillar Decomposition (main agent, ~15s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 1
```

Main agent reads idea brief + landscape dossier and decomposes the product into 3-6
feature pillars. Each pillar is a major capability area (e.g., Auth, Dashboard, Payments,
Notifications, Admin, API).

Output: `pillars/INDEX.md` containing:
- Pillar names and one-line descriptions
- Known dependencies between pillars (e.g., "Payments depends on Auth")
- Suggested shipping sequence (earliest pillar that others depend on)

This becomes the work contract for Phase 3.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 1
```

### Product Phase 2: Per-Pillar Deep Dive (loop per pillar, ~90s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 2
```

For EACH pillar identified in Phase 1, spawn a pillar team of 3 parallel tasks.
All pillars run in parallel (or as Agent Team teammates — see Experimental section).
The main agent calls begin/end around the WHOLE phase, not per pillar.

**Per-pillar team** (receives: idea brief + landscape dossier + pillar name + other pillar names):

```
Task → Pillar Researcher  (agents/ideate-research-agent.md, scoped to pillar domain)
  Builds on landscape dossier. Goes deeper into this specific capability area.
  Minimum 5 searches specific to this pillar. Output: pillar-[name]-research.md

Task → Pillar PM+UX       (agents/ideate-pm-agent.md + ideate-ux-agent.md combined prompt)
  User stories, acceptance criteria, UX flows, and success metrics for this pillar.
  Must note: "does this conflict with other pillars I know about?"
  Output: pillar-[name]-pm-ux.md

Task → Pillar Eng         (agents/ideate-eng-agent.md, scoped to pillar)
  Architecture, data model, APIs, dependencies, and complexity for this pillar.
  Must flag any Novel complexity items. Must note cross-pillar technical dependencies.
  Output: pillar-[name]-eng.md
```

Merge three per-pillar files into a single `pillars/pillar-[name].md` per pillar.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 2
```

### Product Phase 3: Cross-Validation (2 parallel agents, ~45s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 3
```

Both agents receive ALL pillar outputs together. They validate the pillars as a
system, not in isolation.

```
Agent A: Coherence Validator
  - Do pillars fit together as one product with consistent UX flow?
  - Data model consistency: do pillars share or conflict on entity definitions?
  - Shared dependencies / conflicting assumptions (e.g., auth strategy, state management)
  - Output: validation/cross-validation.md

Agent B: Integration Architect
  - Technical integration points between pillars (shared services, event flows, API contracts)
  - Sequencing: which pillar must ship before others can function?
  - Build a dependency graph with rationale
  - Output: validation/cross-validation.md (append integration section)
```

After both agents complete, main agent merges outputs and produces:
`validation/conflict-report.md` — lists every contradiction found, severity
(Blocking | Concerning | Minor), and which pillars are involved. The synthesizer
in Phase 5 MUST resolve each item or document it as NEEDS_CLARIFICATION in
OPEN-QUESTIONS.md. Never pause the pipeline — the user reviews after assembly.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 3
```

### Product Phase 4: Adversarial Review (2 parallel agents, ~45s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 4
```

Both agents see ALL pillar outputs + cross-validation results. They evaluate the
whole product, not individual pillars. Both have WebSearch — they verify claims,
find real failure cases, and search for post-mortems.

```
Agent A: Red Team  (agents/ideate-redteam-agent.md)
  Attacks the product: abuse vectors, competitive responses, regulatory traps,
  economic failure modes, security gaps across pillar boundaries.
  Severity per finding: Blocking | Concerning | Minor
  Output: (adversarial-review.md)

Agent B: Devil's Advocate  (agents/ideate-devils-advocate.md)
  Challenges the consensus assumptions: "what if the core premise is wrong?"
  Focus on the strongest possible counter-argument to the whole product.
  Severity per finding: Blocking | Concerning | Minor
  Output: (appended to adversarial-review.md)
```

Merge into `validation/adversarial-review.md`. Any BLOCKING items must be
addressed by the synthesizer. If unresolvable, document in OPEN-QUESTIONS.md
with both positions preserved — never pause the pipeline.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 4
```

### Product Phase 5: Synthesis (1 agent, best model, ~60s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 5
```

Read `agents/ideate-synthesizer.md`. Synthesizer receives EVERYTHING:
- Landscape dossier
- All pillar analyses
- Cross-validation conflict report
- Adversarial review

Synthesizer MUST:
1. Resolve every item in conflict-report.md — document resolution rationale
2. Address every BLOCKING item from adversarial-review.md
3. Produce coherent product recommendation organized by pillar
4. Run additional WebSearch to fill gaps before finalizing
5. Mark unresolvable items `NEEDS_CLARIFICATION` — write them to OPEN-QUESTIONS.md, never pause
6. Preserve dissenting views in a "Dissenting Views" section
7. Cite research using [N] notation for all quantitative claims

Output: `synthesis.md` (input to Phase 6 variant agents and final PRD)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 5
```

### Product Phase 6: Variant Generation (3 parallel agents, ~45s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 6
```

Each variant agent receives synthesis + ALL pillar analyses. Each proposes how
to sequence, cut, or expand pillars for their optimization target. Variants must
differ on fundamental tradeoffs, not surface details.

```
Task → Speed Variant      (agents/ideate-variant-speed.md)     → approach-speed.md
Task → Excellence Variant (agents/ideate-variant-excellence.md) → approach-excellence.md
Task → Lean Variant       (agents/ideate-variant-lean.md)       → approach-lean.md
```

Each variant must include: pillar sequencing for that strategy, what gets cut/deferred,
and the core tradeoff rationale.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 6
```

### Product Phase 7: Document Assembly (main agent, ~30s)

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" begin "$SLUG" 7
bash "$PROPOSE_HOME/scripts/ideate-run.sh" scaffold "$SLUG"
```

Full output structure:

```
proposal-[slug]/
├── INDEX.md                      ← navigation hub, links all pillars + validation files
├── SUMMARY.md                    ← 1-page executive summary
├── COMPARISON.md                 ← weighted scoring matrix across variants
├── core/
│   ├── PRD.md                    ← organized by pillar sections
│   ├── OUTCOME.md
│   └── ASSUMPTIONS.md
├── landscape/                    ← Phase 0.5 research
│   ├── INDEX.md
│   ├── DOSSIER.md
│   ├── COMPETITIVE-LANDSCAPE.md
│   ├── BENCHMARKS.md
│   └── SOURCES.md                ← master source registry (all phases)
├── pillars/                      ← Phase 2 per-pillar analyses
│   ├── INDEX.md                  ← pillar overview + dependency map
│   ├── pillar-[name-1].md
│   ├── pillar-[name-2].md
│   └── pillar-[name-N].md
├── validation/                   ← Phase 3 + 4 outputs
│   ├── cross-validation.md
│   ├── conflict-report.md        ← items resolved in synthesis
│   └── adversarial-review.md
├── approaches/
│   ├── INDEX.md
│   ├── approach-speed.md
│   ├── approach-excellence.md
│   ├── approach-lean.md
│   └── TRADEOFF-MATRIX.md
├── technical/
│   ├── architecture.md
│   ├── data-model.md
│   ├── integration-points.md     ← from cross-validation
│   └── pillar-sequencing.md      ← which pillars ship first
├── edge-cases/
│   ├── failure-modes.md
│   ├── scale-scenarios.md
│   └── security.md
├── what-if/
│   ├── budget-constrained.md
│   ├── timeline-compressed.md
│   └── scope-expanded.md
├── decisions/
│   ├── INDEX.md
│   └── ADR-001-*.md              ← includes conflict resolutions from Phase 5
└── meta/
    ├── OPEN-QUESTIONS.md
    ├── GLOSSARY.md
    └── GENERATION-LOG.md
```

INDEX.md role-based entry points: Executive → SUMMARY.md (2 min), PM → COMPARISON.md
(5 min), Engineer → technical/pillar-sequencing.md (10 min), Skeptic →
validation/adversarial-review.md (5 min), Designer → pillars/INDEX.md (5 min).

Every file: breadcrumb header + inline cross-refs + "where next" footer.

```bash
bash "$PROPOSE_HOME/scripts/ideate-run.sh" end "$SLUG" 7
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
- [ ] No UNVERIFIED claims in SUMMARY.md or PRD.md

### Product Mode Checks

Structural:
- [ ] Every pillar has a dedicated `pillars/pillar-[name].md`
- [ ] `validation/cross-validation.md` exists and covers all pillar pairs
- [ ] Every item in `validation/conflict-report.md` is RESOLVED or NEEDS_CLARIFICATION
- [ ] `validation/adversarial-review.md` has no unaddressed BLOCKING items
- [ ] `technical/pillar-sequencing.md` exists with dependency rationale
- [ ] `pillars/INDEX.md` links to all pillar files
- [ ] INDEX.md links to all pillars and validation files
- [ ] COMPARISON.md has scores for all variants
- [ ] OPEN-QUESTIONS.md has >= 3 items
- [ ] >= 2 ADR records (at least one must be a conflict resolution)

Research:
- [ ] SOURCES.md has >= 30 unique real URLs (cumulative across all phases)
- [ ] Every pillar file cites >= 3 sources specific to that pillar domain
- [ ] DOSSIER.md covers market, competitors, UX patterns, and technology
- [ ] Every approach file cites >= 3 external sources
- [ ] PRD.md has inline [N] citations for all quantitative claims
- [ ] COMPETITIVE-LANDSCAPE.md has real competitor data
- [ ] No UNVERIFIED claims in executive summary

Citation format (all modes):
- [ ] Files with research claims have a Sources footer section
- [ ] Citations use [N] inline notation linked to Sources
- [ ] Source entries include: Author/Publication, Title, Date, URL
- [ ] No fabricated source URLs

---

## Agent Table

| Agent | File | Feature | Product |
|-------|------|---------|---------|
| Research Agent | `ideate-research-agent.md` | Phase 0.5 (1x) | Phase 0.5 (3x), Phase 2 (1x per pillar) |
| PM Agent | `ideate-pm-agent.md` | Phase 1 | Phase 2 (1x per pillar, combined) |
| UX Agent | `ideate-ux-agent.md` | Phase 1 | Phase 2 (1x per pillar, combined) |
| Eng Agent | `ideate-eng-agent.md` | Phase 1 | Phase 2 (1x per pillar) |
| RedTeam Agent | `ideate-redteam-agent.md` | Phase 1 | Phase 4 |
| Coherence Validator | _(inline prompt)_ | — | Phase 3 |
| Integration Architect | _(inline prompt)_ | — | Phase 3 |
| Devil's Advocate | `ideate-devils-advocate.md` | — | Phase 4 |
| Synthesizer | `ideate-synthesizer.md` | Phase 3 | Phase 5 |
| Technical Critic | _(inline prompt)_ | Phase 2 | — |
| Product/UX Critic | _(inline prompt)_ | Phase 2 | — |
| Speed Variant | `ideate-variant-speed.md` | Phase 3 (inline) | Phase 6 |
| Excellence Variant | `ideate-variant-excellence.md` | — | Phase 6 |
| Lean Variant | `ideate-variant-lean.md` | — | Phase 6 |

Research-primary agents (Research Agent in Phase 0.5): 15+ searches.
Per-pillar researchers (Phase 2): 5+ searches scoped to pillar domain.
Others: 2-5 per Confidence Threshold Rule (WebSearch when confidence < 0.8).

---

## Context Engineering Notes

- Subagents receive only the context they need — embed all necessary info in Task prompt
- Main agent maintains running status summary between phases
- Auto-compact: preserve idea brief, pillar list, conflict report items, current phase
- Model budget: Sonnet-class for Phase 0.5/2/3/4/6; best available for Phase 5 synthesis
- Mandatory context for ALL agents: `references/research-protocol.md`
- Phase 2 pillar agents also read: `directives/creative-directives.md`, `references/frameworks.md`
- Phase 2 per-pillar agents receive the landscape dossier but are expected to go deeper
  into their specific area — they are NOT limited to the dossier's findings

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
- Phase 0.5 — 3 landscape researcher teammates (true parallel)
- Phase 2 — each pillar is a teammate with isolated file ownership (true parallel)
- Phase 4 — Red Team + Devil's Advocate as teammates (can message each other)

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
File ownership: .claude/ideation/{slug}/pillar-[name].md
```

In Phase 2, each pillar teammate owns its three sub-files and merges them itself:
```
File ownership: .claude/ideation/{slug}/pillar-[name]-research.md,
                .claude/ideation/{slug}/pillar-[name]-pm-ux.md,
                .claude/ideation/{slug}/pillar-[name]-eng.md,
                .claude/ideation/{slug}/pillars/pillar-[name].md
```

No two teammates may own the same file. Main agent assembles final outputs only.

### Phase 4 Adversarial Cross-Messaging

```
Red Team → reads all pillar outputs → drafts adversarial findings
Red Team → SendMessage(to: "devils-advocate", "Flagging [X] as Blocking — concur?")
Devil's Advocate → may adjust severity based on peer confirmation
Both → write output files → TaskUpdate(completed)
```

### Fallback Guarantee

Every teams-mode phase has an exact equivalent in the standard subagent phases above.
If TeamCreate raises any error, log and fall back to standard subagents.
Output files and quality checks are identical in both paths.
