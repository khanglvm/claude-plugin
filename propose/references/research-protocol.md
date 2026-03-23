# Research Protocol: Confidence-Triggered Deep Research

This protocol governs when and how agents conduct online research. It applies
to EVERY agent in the pipeline, not just the dedicated Research Agent.

---

## The Confidence Threshold Rule

Every claim an agent makes falls into one of three confidence tiers:

| Tier | Confidence | Action Required |
|------|-----------|-----------------|
| **Grounded** | > 0.8 | State the claim. No research needed. |
| **Uncertain** | 0.4 - 0.8 | **MUST research before including.** Use WebSearch/WebFetch. |
| **Speculative** | < 0.4 | **MUST research. If research inconclusive, mark as ⚠️ UNVERIFIED.** |

### What triggers low confidence?

- Market size claims, growth rates, or revenue projections
- "Industry standard" or "best practice" claims without personal knowledge
- Competitor feature comparisons or pricing
- Technology performance benchmarks or limitations
- Regulatory/compliance requirements
- User behavior statistics or conversion rates
- Cost estimates for third-party services or infrastructure
- Any claim containing words like "typically", "usually", "most companies"

**Rule**: If you catch yourself writing "typically" or "usually" — that is your
signal to research. Replace the hedge word with a cited fact or mark it ⚠️ UNVERIFIED.

---

## Research Execution Protocol

### Step 1: Formulate Targeted Queries

Bad: "onboarding best practices"
Good: "SaaS onboarding completion rate benchmarks 2024 2025"
Good: "progressive onboarding vs wizard onboarding conversion data"
Good: "Stripe onboarding flow case study results"

Rules:
- Use specific, data-seeking queries (include years for recency)
- Search for case studies and post-mortems, not blog listicles
- Search for benchmark data and industry reports
- Search for competitor implementations and public teardowns
- Use multiple queries to triangulate — never rely on a single source

### Step 2: Source Quality Hierarchy

Prioritize sources in this order:

1. **Primary data**: Company engineering blogs, published case studies with metrics,
   peer-reviewed research, official documentation
2. **Reputable analysis**: Industry reports (Gartner, Forrester, McKinsey), 
   established tech publications (InfoQ, ThoughtWorks Radar), conference talks
3. **Practitioner experience**: Well-regarded personal blogs with real data,
   HackerNews/Reddit discussions with upvoted technical details
4. **General content**: News articles, marketing content, opinion pieces

**NEVER cite** without checking: SEO-optimized listicles, AI-generated content,
outdated sources (> 3 years for tech, > 5 years for business), sources with no
author or publication date.

### Step 3: Extract and Cite

For each research finding, capture:

```markdown
**Finding**: [The specific claim or data point]
**Source**: [Publication/Author, Date]
**URL**: [Link]
**Relevance**: [How this applies to our proposal]
**Quality**: [Primary | Analysis | Practitioner | General]
**Recency**: [Date of publication]
```

### Step 4: Synthesize, Don't Copy

- Paraphrase findings in your own words
- Combine multiple sources to build a stronger claim
- Note when sources disagree — this is valuable signal
- Always prefer quantitative data over qualitative claims

---

## Research Categories by Agent Role

### PM Agent Research Triggers
- Market size and growth claims → Search industry reports
- User behavior assumptions → Search UX research studies
- Competitor features → Search product pages, changelogs, review sites (G2, Capterra)
- Pricing models → Search competitor pricing pages, SaaS pricing studies
- Best-practice frameworks → Search case studies of companies that applied them

### UX Agent Research Triggers
- Interaction pattern claims → Search Nielsen Norman Group, Baymard Institute
- Accessibility requirements → Search WCAG guidelines, MDN accessibility docs
- Mobile/responsive patterns → Search platform-specific HIG (Apple, Material)
- Conversion rate benchmarks → Search Baymard, CXL, specific industry benchmarks
- User journey patterns → Search published case studies with funnel data

### Engineering Agent Research Triggers
- Technology choices → Search official docs, GitHub stars/issues, ThoughtWorks Radar
- Performance benchmarks → Search published benchmarks, load test reports
- Architecture patterns → Search engineering blogs (Netflix, Stripe, Uber, Airbnb)
- Library/framework maturity → Search GitHub activity, npm/pip download trends
- Infrastructure costs → Search cloud provider pricing calculators, cost studies
- Scaling characteristics → Search post-mortems and scaling stories

### Business Agent Research Triggers
- Market size → Search industry reports, analyst estimates
- Revenue models → Search comparable SaaS metrics, OpenView/Bessemer benchmarks
- Cost benchmarks → Search SaaS cost structure analyses
- Competitive positioning → Search G2 grids, Gartner quadrants, product comparisons
- ROI claims → Search published ROI case studies in the same domain

### Red Team Agent Research Triggers
- Security vulnerabilities → Search OWASP, CVE databases, security advisories
- Regulatory requirements → Search official regulatory text, compliance guides
- Failure post-mortems → Search "postmortem" + technology/pattern in question
- Misuse precedents → Search news articles about product abuse, fraud patterns
- Scale failure modes → Search outage reports, incident write-ups

---

## The Research Dossier

All research findings are compiled into a structured dossier that flows through
the pipeline. The dossier uses this format:

```markdown
# Research Dossier: [Feature Name]

## Market & Industry
### Finding: [Title]
- **Data**: [Specific numbers/facts]
- **Source**: [Author/Pub, Date, URL]
- **Confidence**: [High/Medium/Low based on source quality]
- **Applied to**: [Which proposal section uses this]

## Competitive Landscape
### [Competitor Name]
- **Relevant Feature**: [What they do]
- **How They Do It**: [Implementation approach if known]
- **Results**: [Published metrics if available]
- **Source**: [URL]
- **Implication for Us**: [What we should learn]

## Technical Benchmarks
### [Technology/Pattern]
- **Benchmark Data**: [Performance numbers]
- **Conditions**: [Under what conditions were these measured]
- **Source**: [URL]
- **Applied to**: [Which architecture decision this informs]

## Best Practices & Case Studies
### [Case Study Title]
- **Company**: [Who]
- **What They Did**: [Summary]
- **Results**: [Outcomes with numbers]
- **Lesson for Us**: [Specific takeaway]
- **Source**: [URL]

## Regulatory & Compliance
### [Regulation/Standard]
- **Requirement**: [What it mandates]
- **Applicability**: [Does it apply to us? Why?]
- **Source**: [Official reference]

## Unresolved / Conflicting Data
### [Topic where sources disagree]
- **Position A**: [Claim + source]
- **Position B**: [Claim + source]
- **Our Take**: [Which is more applicable and why]
```

---

## Integration with Pipeline Phases

### Phase 0.5 (Dedicated Research Sprint)
The Research Agent runs broad searches to establish the landscape:
- Market context and sizing
- Competitive landscape scan
- Relevant best-practice patterns
- Technology landscape for the domain
Output → `research-dossier.md` shared with ALL Phase 1 agents

### Phase 1 (Embedded in Each Agent)
Each agent conducts targeted research specific to their domain when confidence
drops below threshold. Results appended to their analysis with inline citations.

### Phase 2 (Critique Verification)
Critique agents MUST research claims they're challenging:
- "The PM Agent claims 40% time savings — is this realistic?"
- Search for actual benchmarks to support or refute

### Phase 3 (Synthesis Gap-Filling)
Synthesizer identifies claims that NO agent researched but should have been.
Runs targeted searches to fill gaps before finalizing.

### Phase 4 (Variant Grounding)
Variant agents research cost estimates, timeline benchmarks, and technology
choices specific to their disposition.

---

## Citation Format in Output Files

All research-backed claims in the final proposal use inline citations:

```markdown
Progressive onboarding improves completion rates by 20-30% compared to
traditional wizard flows [1]. However, this benefit diminishes for expert
users who prefer immediate access to advanced features [2].

---
**Sources**:
[1] Baymard Institute, "Onboarding UX Benchmarks", 2024
[2] Nielsen Norman Group, "Progressive Disclosure", 2023
```

Every output file that contains research-backed claims MUST include a
**Sources** section at the bottom with numbered references.
