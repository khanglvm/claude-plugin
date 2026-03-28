# Prompt Output Template

Structure for the final generated design prompt. Fill each section with the collected specs from the conversation.

## Template

```
Build a {page_type} for {business_description} using {tech_stack}. The aesthetic is {aesthetic_summary}. {key_visual_detail}.

FONTS & DESIGN SYSTEM
Google Fonts import:

{heading_font} ({heading_weights}) — headings
{body_font} ({body_weights}) — body text

Tailwind config — extend fontFamily:

heading: ["'{heading_font}'", "{heading_fallback}"]
body: ["'{body_font}'", "{body_fallback}"]

CSS Variables (:root in index.css):

{css_variables_block}

All headings use: {heading_classes}
All body text uses: {body_classes}
All buttons use: {button_classes}

{effect_name} CSS (in @layer components)
{effect_css_definition}

SECTION 1 — {section_name}
{section_spec}

SECTION 2 — {section_name}
{section_spec}

... (repeat for all sections)

DEPENDENCIES
{dependency_list}

KEY PATTERNS
{repeated_patterns}
```

## Section Spec Template

Each section should contain ALL of these when applicable:

```
SECTION N — {NAME} ({type: fixed/sticky/full-width/contained})
{Layout composition: how elements relate spatially — overlap, rotation, blending}

Background:
{Background treatment: color/video/gradient/mesh}
{How background interacts with foreground — blend modes, masks, shared gradients}
{Transition into next section — fade, overlap, shared gradient}

Content ({z-index}, {alignment}):
{Element 1: component type — specific text — classes — rotation/blend if any}
{Element 2: ...}
{...}

Element Relationships:
{How elements overlap, intersect, or blend with each other}
{Rotation values for non-axis-aligned elements}
{Mix-blend-mode specifications}
{Gradient masks between elements}

{Layout details: NOT uniform grids — specify asymmetric splits, cascades, orbits, or stacks}
{Container shapes: clip-path, irregular boundaries, gradient perimeters}

{Animation details: purpose-driven animations with durations ≥0.6s}
{Responsive behavior: how composition adapts (not just column count changes)}
```

## Completeness Checklist

Before outputting, verify the prompt includes:

- [ ] **Header**: tech stack + aesthetic + one distinguishing visual detail
- [ ] **Fonts**: Google Fonts names, weights, Tailwind config, fallback stacks
- [ ] **CSS Variables**: All design tokens in HSL (background, foreground, primary, secondary, muted, accent, border, radius)
- [ ] **Global patterns**: Heading classes, body classes, button classes
- [ ] **Custom effects**: Full CSS with variants, pseudo-elements, application guidance
- [ ] **Every section**: Layout composition + background + content hierarchy + element relationships
- [ ] **Section content**: Actual headline text, subtext, button labels, card items
- [ ] **Media specs**: Video sources (MP4/HLS), image paths, poster fallbacks
- [ ] **Animation details**: Library (motion), trigger (scroll/load), duration (≥0.6s), delay
- [ ] **Dependencies**: All npm packages needed
- [ ] **Key patterns**: Heading style, section transitions, video treatment, animation system
- [ ] **Responsive**: Breakpoint-specific classes (md:, lg:) for key elements
- [ ] **Consistent terminology**: Same class names and patterns repeated across sections

## AI Pitfall Avoidance Checklist (MANDATORY)

Run this check on EVERY generated prompt. Any failure = revise before output.

- [ ] **No small tags above headings**: Search for "badge", "tag", "pill" + "above" + "heading" patterns. Remove any found. Context belongs IN the heading or as offset small text.
- [ ] **No centered vertical stacks**: No section follows badge → heading → subtext → CTA → grid. Each section has a unique layout composition.
- [ ] **No uniform grid cards**: Features/services/testimonials do NOT use grid-cols-3 with identical rectangular cards. Verify each uses a creative container shape (stacked, cascading, orbital, irregular clip-path, gradient perimeter).
- [ ] **No meaningless floating decorations**: Search for "float", "bob", "drift" + small shapes. Remove any that aren't atmospheric (full-section gradients, grain overlays are fine).
- [ ] **Creative headline treatments**: At least the hero and CTA sections have non-standard headline layouts (typographic art, cinematic close-in, full-screen text, rotated/split words).
- [ ] **Element composition**: At least 3 sections specify element rotation, overlap, blend-mode, or gradient-mask interactions between elements.
- [ ] **Meaningful animations only**: Every animation has a purpose tag: (reveal), (depth), (atmosphere), (interaction). No animation is purely decorative without atmospheric scale.
- [ ] **Section transitions**: Sections blend into each other (shared gradients, overlapping content, gradient masks) rather than sitting in isolated blocks.

## Quality Rules

1. **Specificity over abstraction** — "text-[8vw] font-heading italic text-white mix-blend-mode: difference" not "large heading"
2. **Real content** — actual headline text, not "[headline here]"
3. **Complete CSS** — full property blocks, not "similar to above"
4. **Explicit responsive** — breakpoint classes for every dimension that changes
5. **Measurable values** — "min-h-screen", "py-32", "rotate-3", "margin-top: -80px", not "generous spacing"
6. **Named dependencies** — "hls.js", "motion", "lucide-react", not "animation library"
7. **Icon specificity** — "Zap from lucide-react" not "lightning icon"
8. **Color precision** — HSL values for CSS vars, Tailwind opacity classes for text (text-white/60)
9. **Composition over decoration** — describe how elements relate (overlap, blend, rotate) not just individual element styles
10. **Unique per section** — no two sections should share the same layout pattern; each has its own spatial composition
