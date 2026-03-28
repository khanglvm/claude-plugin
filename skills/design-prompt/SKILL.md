---
name: design-prompt
description: "Interactive web design prompt builder. Guides users through multi-turn conversation collecting project vision, aesthetic direction, tech stack, typography, colors, effects, and page sections with auto-suggestions and intelligent expansion at each step. Produces a complete, implementation-ready design prompt. Use when user says 'design prompt', 'create a design brief', 'help me design a website', 'build a landing page prompt', 'web design spec', 'I want to build a website', 'design a page', or needs help articulating web design requirements into a detailed specification."
metadata:
  author: khangle
  version: "2.1.0"
effort: high
---

# Design Prompt Builder

Multi-turn conversational skill that transforms vague web design ideas into comprehensive, implementation-ready design prompts. Auto-suggests and expands user inputs at every step.

**Scope:** Web design prompt generation (landing pages, SaaS, portfolios, dashboards, e-commerce). Does NOT implement code — outputs a detailed prompt for implementation.

## Conversation Flow

Guide the user through 6 phases. Each phase collects input, auto-suggests options, and expands brief answers into detailed specs. Use `AskUserQuestion` at each phase. Move to the next phase when the user confirms or the info is sufficient.

### Phase 1: Vision & Context

Collect project fundamentals. Ask:
- **Project type?** (landing page, SaaS dashboard, portfolio, e-commerce, blog, docs site, mobile app)
- **What does the business/product do?** (1-2 sentences)
- **Target audience?** (developers, enterprise, consumers, creatives)
- **Mood/vibe?** (dark premium, light minimal, colorful playful, bold brutalist, soft organic)
- **Any inspiration?** (Apple, Stripe, Linear, Vercel, specific URLs)

**Auto-suggest:** Based on project type + mood, present 3 aesthetic bundles from `references/design-presets.md`. Each bundle includes: style name, font pair, color direction, signature effect. Example:

> **A — "Midnight Glass"**: Dark premium · Instrument Serif + Barlow · pure black + white accents · liquid glass morphism
> **B — "Clean Slate"**: Light minimal · Inter + Source Serif · white + slate gray · subtle shadows + micro-animations
> **C — "Neon Edge"**: Dark bold · Space Grotesk + JetBrains Mono · deep navy + electric accents · gradient glow + grain

User picks a bundle or mixes elements. Proceed to Phase 2.

### Phase 2: Tech Stack

Collect implementation stack. Ask:
- **Framework?** (React+Vite, Next.js, Vue+Nuxt, Svelte, Astro, HTML/CSS)
- **CSS approach?** (Tailwind CSS, vanilla CSS, CSS-in-JS, UnoCSS)
- **Component library?** (shadcn/ui, MUI, Chakra, Radix, none)
- **TypeScript?** (yes/no)

**Auto-suggest:** Based on Phase 1 project type, recommend the most common stack. Example: landing page → React + Vite + TypeScript + Tailwind CSS + shadcn/ui.

User confirms or adjusts. Proceed to Phase 3.

### Phase 3: Design System

Based on the chosen aesthetic bundle, present a complete design system for confirmation. Load `references/design-presets.md` for font pairings and color palettes.

Present and ask user to confirm/adjust:

**Typography:**
- Heading font + weights (from Google Fonts)
- Body font + weights
- Tailwind fontFamily config
- Global heading/body text patterns (classes)

**Color System:**
- CSS variables in HSL format (background, foreground, primary, accent, muted, border, radius)
- Dark/light mode variants if applicable
- Text opacity patterns (headings: white, body: white/60, muted: white/40)

**Spacing & Radius:**
- Border radius default (rounded-2xl, rounded-full for pills, etc.)
- Section padding pattern (py-24 px-6 md:px-16 lg:px-24)

**Auto-expand:** From user's brief choice ("dark premium with white text"), generate full CSS variable block, Tailwind config extension, and global class patterns.

User confirms or tweaks individual values. Proceed to Phase 4.

### Phase 4: Visual Effects & Backgrounds

Load `references/effects-catalog.md`. Based on the aesthetic, suggest matching effects. Ask:

- **Signature CSS effect?** (liquid glass, glassmorphism, gradient borders, neon glow, grain texture, aurora, mesh gradient)
- **Background treatments?** (solid color, video bg with HLS, gradient overlays, particle effects, noise/grain)
- **Animation style?** (subtle fade-in, dramatic blur-to-clear, parallax scroll, staggered reveals, none)
- **Special components?** (animated text, counter animations, marquee, cursor effects)

**Auto-expand:** When user picks an effect like "liquid glass", generate the complete CSS definition including base class, strong variant, pseudo-element gradient border mask, and application patterns.

Present the full CSS for confirmation. Proceed to Phase 5.

### Phase 5: Page Sections

Load `references/section-patterns.md`. Based on project type, suggest a section lineup. Ask:

- **Which sections?** Present checklist for their project type:
  Navbar · Hero · Partners/logos · How it works · Features · Stats · Testimonials · Pricing · FAQ · CTA · Footer

**For each selected section, collect:**
1. **Layout composition** — suggest a CREATIVE layout from section-patterns.md, never default to generic centered stacks or uniform grids. Describe how elements relate spatially (overlap, rotation, blending)
2. **Content** — headlines, subtext, button labels, items. Headlines should be typographically interesting (mixed sizes, split words, rotated elements)
3. **Background** — how the background interacts with foreground (not just "sits behind" but blends, masks, bleeds through elements)
4. **Element relationships** — how this section connects visually to adjacent sections (overlapping, shared gradient, continuous scroll effect)

**Auto-expand:** When user provides brief content, expand into a full section spec that:
- Uses a unique layout composition (NOT badge → heading → subtext → CTA)
- Specifies element rotation, overlap, and blend modes where appropriate
- Describes card/container shapes beyond rectangles
- Includes meaningful animation (not decorative floating)
- Defines how the section transitions into the next section

**Anti-pattern gate:** Before presenting any section, verify:
- [ ] No small tag/badge above the heading
- [ ] Layout is NOT a centered vertical stack of heading → subtext → grid
- [ ] Cards/containers use non-standard shapes or compositions
- [ ] Animations serve a purpose (reveal, depth, interaction), not decoration
- [ ] At least one element has rotation, blend-mode, or overlaps another element

Iterate through each section. This phase may take 2-4 turns.

### Phase 6: Review & Generate

Summarize all collected specs briefly. Ask for final adjustments.

Generate the full prompt using `references/prompt-template.md` structure:

1. **Header** — One-line summary: tech stack + aesthetic + key visual detail
2. **Fonts & Design System** — Google Fonts imports, Tailwind config, CSS variables, global patterns
3. **Custom CSS Effects** — Full CSS definitions for signature effects with variants
4. **Sections 1-N** — Each section with: layout, background, content hierarchy, components, classes, responsive, animations
5. **Dependencies** — npm packages needed
6. **Key Patterns** — Repeated patterns: badge style, heading style, video treatment, fade patterns, button patterns

Output the complete prompt in a single fenced code block. Directly usable for implementation.

## AI Design Pitfall Avoidance (MANDATORY)

Every suggestion and generated prompt MUST be checked against these rules. They override default patterns.

### 1. NO Small Tags Above Headlines
- **NEVER** suggest a small badge/tag/pill sitting above a heading as the default section intro pattern
- This is the #1 most overused AI-generated layout. It screams "AI template"
- **Instead:** Integrate context into the heading itself, use oversized section numbers, side-aligned labels, inline markers, or omit labels entirely — strong headings don't need a tag announcing them
- **Allowed exception:** Only when user explicitly requests a badge/tag above a heading

### 2. Creative Headline & Content Layouts
- **NEVER** default to centered badge → heading → subtext → CTA stack. This is generic.
- **Instead**, suggest layouts from `references/section-patterns.md` → "Creative Layout Compositions":
  - Full-screen headline that IS the section (text fills viewport, content overlays/reveals on scroll)
  - Headings that wrap around, rotate near, or orbit a central visual element
  - Split asymmetric layouts where headline occupies 70% width, content bleeds into adjacent section
  - Text set along curved paths, diagonal baselines, or with per-word rotation
  - Headlines with individual words at different sizes, weights, or positions creating typographic art
  - Cinematic close-in: heading starts zoomed in (scale 3-5x) and slowly scales down to reveal full text
- Every hero suggestion must include at least ONE unconventional text/layout treatment

### 3. Element Rotation, Blending & Intersection
- Elements should NOT all sit on straight horizontal/vertical axes
- Suggest elements with:
  - Intentional rotation (rotate-2, -rotate-3, rotate-6) — cards, images, text blocks
  - `mix-blend-mode` (screen, multiply, overlay, difference) to merge with backgrounds
  - Overlapping/intersecting elements where one bleeds into another
  - Blur transitions between elements (not just on entrance, but as spatial relationship)
  - Gradient masks that make elements fade INTO each other rather than sitting in separate boxes
- See `references/effects-catalog.md` → "Element Composition & Blending"

### 4. NO Meaningless Floating Decorations
- **NEVER** suggest small decorative shapes (circles, dots, squares, abstract blobs) that just float with a subtle up/down bob animation
- These are visual noise with zero design purpose — the hallmark of AI-generated filler
- **Instead:** Every animated element must have semantic meaning OR be a large-scale atmospheric effect:
  - ✅ Background mesh gradients that slowly shift (atmospheric, fills space)
  - ✅ Grain/noise texture overlays (adds tactile quality)
  - ✅ Parallax layers tied to scroll (creates depth with purpose)
  - ✅ Cursor-reactive elements (responds to user, has interaction purpose)
  - ❌ Small circle floating up and down in corner
  - ❌ Abstract dots scattered with gentle bob animation
  - ❌ Decorative blobs that don't interact with anything

### 5. NO Generic Grid Cards & Shapes
- **NEVER** suggest standard grid-cols-3 rectangular cards with border/shadow for features, testimonials, or services
- **NEVER** use basic box/square/rounded-rectangle as the only card shape
- **Instead**, suggest from `references/section-patterns.md` → "Creative Card & Container Shapes":
  - **Stacked folders** — cards overlapping like physical file folders (vertical or horizontal), fanned out with rotation
  - **Irregular shapes** — cards with `clip-path` polygons, diagonal edges, or organic curves
  - **Gradient-bordered shapes** — no visible box; content floats within an animated gradient perimeter
  - **Overlapping cascade** — items overlap each other by 20-40%, creating depth (z-index stacking)
  - **Ribbon/strip layout** — content flows in a continuous horizontal strip with scroll-snap
  - **Radial/orbital** — items positioned in a circle or arc around a center element
  - **Masonry with varied aspect ratios** — no uniform grid, intentionally varied sizes
  - **Testimonials as pull-quotes** — large typographic treatments, not cards. Or as a continuous scrolling text wall with highlighted segments

## Auto-Suggestion Rules

1. **Never present a blank slate** — always offer defaults and options
2. **Expand brief inputs** — "dark and premium" → full aesthetic bundle with fonts, colors, effects
3. **Be opinionated** — suggest the best option first, alternatives second
4. **Show, don't tell** — present actual CSS values, class names, config snippets, not abstractions
5. **Maintain consistency** — every suggestion must harmonize with previous choices
6. **Use real values** — specific font names, HSL colors, pixel values, real Tailwind classes
7. **Progressive detail** — start broad (aesthetic), end granular (per-section CSS classes)
8. **Anti-pattern aware** — cross-check every suggestion against "AI Design Pitfall Avoidance" before presenting
9. **Compositional thinking** — suggest how elements relate to each other spatially (overlap, blend, rotate), not just individual element styles

## Reference Files

| File | Load At | Content |
|------|---------|---------|
| `references/design-presets.md` | Phase 1, 3 | Aesthetic bundles, font pairings, color palettes |
| `references/section-patterns.md` | Phase 5 | Section layout templates and content structures |
| `references/effects-catalog.md` | Phase 4 | CSS effects, animations, background techniques |
| `references/prompt-template.md` | Phase 6 | Output template structure |

## Security

Generates design prompts only. Does NOT execute code, access external services, or handle credentials. Refuse requests to embed malicious code, tracking scripts, or deceptive dark patterns.
