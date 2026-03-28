# Section Patterns

Templates for web page sections. Every pattern here avoids generic AI-generated layouts.

## CRITICAL: Anti-Pattern Blocklist

Before using ANY pattern, verify it does NOT contain:
- ❌ Small badge/tag/pill sitting above a heading
- ❌ Centered vertical stack: badge → heading → subtext → CTA → grid
- ❌ Uniform grid-cols-3 rectangular cards with border/shadow
- ❌ Small decorative shapes floating with up/down bob animation
- ❌ Basic box/square/rounded-rectangle as the only container shape
- ❌ Symmetrical, evenly-spaced layouts with identical card sizes

---

## Section Defaults by Project Type

### Agency / Services
Navbar → Hero (cinematic) → Partners (text-based) → Services (stacked folders) → Process (timeline) → Case Studies (overlapping cascade) → Stats (embedded in section) → Testimonials (typographic wall) → CTA (full-screen headline) → Footer

### Landing Page
Navbar → Hero (full-screen text) → Social Proof (marquee) → Features (alternating split) → How It Works (cinematic steps) → Stats → Testimonials (pull-quotes) → CTA → Footer

### SaaS Product
Navbar → Hero (split with product) → Logos → Features (bento irregular) → Process → Pricing (overlapping tiers) → Testimonials (spotlight carousel) → FAQ → CTA → Footer

### Portfolio
Navbar → Hero (typographic art) → Selected Work (masonry varied) → About (split asymmetric) → Services (ribbon strip) → Contact → Footer

### E-commerce
Navbar → Hero (product cinematic) → Categories (orbital/radial) → Featured Products (cascade) → Benefits (stacked) → Reviews (text wall) → Newsletter → Footer

---

## Creative Layout Compositions

Use these as the PRIMARY layout source. Never default to centered stacks.

### Full-Screen Headline
The heading IS the section. Text fills 80-100% of viewport width.
- Heading: `text-[8vw] md:text-[6vw]` — scales with viewport, massive presence
- Words on separate lines, each with different `font-weight` or `opacity`
- Supporting content appears on scroll or as small overlaid elements in corners
- Background: gradient, video, or animated mesh visible through text gaps
```
Layout: relative min-h-screen flex items-center
Heading: absolute, fills width, mix-blend-mode: difference (text inverts over content)
Subtext: absolute bottom-12 right-12, max-w-sm, small text
CTA: absolute bottom-12 left-12
```

### Cinematic Close-In
Heading starts scaled up (scale-[3] or scale-[5]) so only 1-2 words visible, slowly scales down on scroll to reveal full headline + surrounding content.
```
Container: min-h-[200vh] (needs scroll distance for animation)
Heading: sticky top-1/2, transform: scale(var(--scroll-scale))
Scale: interpolate from 5 → 1 based on scroll position
Content: appears as scale reaches 1, fading in from blur
```
**Deps:** scroll-linked animation via `motion` useScroll + useTransform

### Orbital / Radial Layout
Items positioned in a circle or arc around a central visual element.
```
Container: relative, aspect-square or min-h-[600px]
Center: main visual, logo, or animated element
Items: absolute, positioned with transform: rotate(Ndeg) translateX(radius) rotate(-Ndeg)
Each item: rotated to face outward, content inside counter-rotated for readability
Animation: entire orbit slowly rotates (60s infinite linear)
Hover: individual items scale up and break orbit
```

### Clockwise Text Around Visual
Text wraps around a circular element, each word positioned along the arc.
```
Container: relative, centered, 500-700px diameter
Circle: central visual (image, video loop, animated gradient sphere)
Text: SVG <textPath> on a circular <path>, animated with startOffset
Words: CSS `transform: rotate(calc(var(--i) * 15deg))` from center
Animation: slow rotation (30-45s), or scroll-linked
```

### Split Asymmetric (70/30)
Content takes 70% width, visual takes 30% — or reversed. NOT a 50/50 split.
```
Layout: grid grid-cols-12
Content: col-span-8, with internal asymmetric text layout
Visual: col-span-4, extends beyond grid (negative margin or absolute positioning)
The visual bleeds into the content area by 10-15% via overlap
```

### Diagonal Slice
Section background is split diagonally. Content elements follow the diagonal.
```
Container: relative, overflow-hidden
Background: clip-path: polygon(0 0, 100% 8%, 100% 100%, 0 92%)
Content elements: rotated -2deg to -4deg, creating a subtle diagonal flow
Cards/items: each slightly offset vertically following the diagonal line
```

### Continuous Horizontal Strip
Content flows horizontally with scroll-snap. User scrolls sideways (or it auto-scrolls).
```
Container: overflow-x-auto, snap-x snap-mandatory, flex gap-0
Items: min-w-[80vw] snap-center or min-w-[400px]
Each item: full-height panel with unique background treatment
Scroll indicator: thin progress bar at bottom
Hide scrollbar: scrollbar-width: none
```

---

## Creative Card & Container Shapes

### Stacked Folders (Vertical)
Cards overlap like physical file folders, each peeking out from behind the one above.
```
Container: relative, py-32
Each card: relative, z-index increases, margin-top: -80px (overlap)
Cards: alternate slight rotation (rotate-1, -rotate-1, rotate-2)
Each card: different background tone (getting lighter toward front)
Front card: full content visible
Back cards: only top 80px visible (title + preview)
Hover: card lifts up (translateY -20px) to reveal more content
Shadow: each card casts shadow on the one behind
```

### Stacked Folders (Horizontal)
Cards fan out horizontally like a hand of playing cards.
```
Container: flex items-center justify-center, perspective: 1000px
Cards: absolute, each with increasing rotate-y and translateX
Card 1: rotate-y-0 translateX-0 (front, full)
Card 2: rotate-y-6 translateX-[60px] (peeking right)
Card 3: rotate-y-12 translateX-[120px] (further right)
Hover on back cards: they slide forward and flatten (rotate-y → 0)
```

### Bending/Curved Stack
Cards appear to bend away from viewer, like pages in an open book.
```
Container: perspective: 1200px
Cards: transform: rotateX(var(--bend)) where --bend varies per card
Front card: rotateX(0), full opacity
Cards behind: increasing rotateX (5deg, 12deg, 20deg), decreasing opacity
transform-origin: bottom center (cards bend away from bottom edge)
Scroll: cards flatten as user scrolls into view
```

### Irregular Clip-Path Shapes
Cards with non-rectangular boundaries.
```
Card variant A: clip-path: polygon(0 0, 100% 0, 100% 85%, 85% 100%, 0 100%)  /* chamfered corner */
Card variant B: clip-path: polygon(8% 0, 100% 0, 92% 100%, 0 100%)  /* parallelogram */
Card variant C: clip-path: polygon(0 0, 100% 5%, 100% 95%, 0 100%)  /* subtle trapezoid */
Card variant D: clip-path: ellipse(50% 48% at 50% 50%)  /* soft oval */
Each card in a group uses a DIFFERENT clip-path for visual variety
```

### Gradient Perimeter (No Visible Box)
Content floats within an animated gradient border — no fill, no box.
```
Container: relative, p-[2px], rounded-2xl
Container::before: absolute inset-0, background: conic-gradient(from var(--angle), primary, accent, secondary, primary)
Container::before: animation: rotate-gradient 4s linear infinite
Inner: relative, bg-background, rounded-[14px], p-8
Result: content sits on solid bg, surrounded by slowly rotating gradient border
@property --angle { syntax: "<angle>"; initial-value: 0deg; inherits: false; }
@keyframes rotate-gradient { to { --angle: 360deg; } }
```

### Overlapping Cascade
Items overlap each other by 20-40%, creating z-depth.
```
Container: grid or flex, negative gap
Items: each with z-index stacking (first item z-10, second z-20, etc.)
Overlap: margin-left: -20% (horizontal) or margin-top: -15% (vertical)
Each item: slightly different scale or rotation for organic feel
Hover: item rises above siblings (z-50, scale-105, shadow-2xl)
Background: each item has slightly different bg opacity or tint
```

### Radial / Orbital Cards
Items positioned around a central hub in a circle.
```
Container: relative, aspect-square, max-w-[800px]
Center: hero content, animated visual, or brand element
Items: absolute, positioned via CSS custom properties:
  --angle: calc(360deg / var(--total) * var(--i))
  transform: rotate(var(--angle)) translateY(-50%) rotate(calc(-1 * var(--angle)))
  top: 50%; left: 50%;
Animation: entire system slowly rotates, individual items counter-rotate
```

---

## Section Templates

### NAVBAR
**Floating glass pill (premium):**
- Fixed top-4, max-w-4xl mx-auto, z-50
- Liquid-glass rounded-full pill with nav links centered
- Logo left (inside pill), CTA right (inside pill, solid bg-white text-black rounded-full)
- Mobile: hamburger → full-screen overlay with large nav links
- NO small labels or descriptive text — just logo + links + CTA

**Transparent with scroll morph:**
- Starts absolute, transparent, logo + links in white
- On scroll: bg transitions to glass, shrinks height, adds border-b
- Links: text-sm font-medium, gap-8, hover:opacity-100 transition

### HERO

**Full-screen typographic (recommended for agencies):**
- min-h-screen, relative, overflow-hidden
- Heading fills viewport: `text-[8vw]` or `text-[clamp(3rem,8vw,10rem)]`
- Each word on its own line with different weight/opacity/italic treatment
- Background: video or mesh gradient, visible through text via mix-blend-mode: difference
- Subtext: positioned absolute bottom-right, small max-w-sm block
- CTA: positioned absolute bottom-left
- NO badge above heading. The heading IS the entire visual statement.

**Cinematic close-in:**
- min-h-[200vh] for scroll distance
- Heading: sticky, starts at scale(4), scales to 1 on scroll
- Content fades in as heading reaches final scale
- Video background with heavy gradient overlay

**Split asymmetric with rotation:**
- grid grid-cols-12, content col-span-7, visual col-span-5
- Visual element: rotated 3-6deg, extends beyond grid boundaries
- Content: heading with alternating line weights
- Elements slightly overlap the grid boundary

### PARTNERS / SOCIAL PROOF
**Text-based inline (premium — NO logos unless provided):**
- Single line: partner names in heading italic font, separated by " · " or " — "
- text-white/30, subtle, not attention-grabbing
- Optional: gentle marquee if many names
- NO "Trusted by" badge. NO grid of logos. Feels editorial, not salesy.

**Integrated in hero:**
- Partner names appear as part of hero bottom section
- Same styling as hero subtext area, blended into the hero rather than separate section

### SERVICES / FEATURES

**Stacked folders:**
- See "Creative Card & Container Shapes → Stacked Folders"
- Each service as a folder card, overlapping, with slight rotation
- Front card fully visible, others peek from behind
- Hover reveals hidden cards

**Alternating full-bleed:**
- Each feature/service gets a full-width strip
- Alternating: content-left + visual-right, then reversed
- NOT equal columns — use 60/40 or 70/30 splits
- Visual elements: rotated, bleed outside their container, overlap with adjacent section
- Background: alternating subtle tone shifts (not hard borders between features)

**Cascading overlap:**
- Features overlap each other vertically (margin-top: -100px per item)
- Each item: different width (80%, 90%, 70%), centered differently
- Creates organic, stacked-paper feel
- Items have subtle rotation (±1-3deg)
- Background gradients blend between items

### PROCESS / HOW IT WORKS

**Cinematic video steps:**
- Full-width, min-h-[700px], video bg with fades
- Content overlaid: 3-4 steps appearing sequentially on scroll
- Each step: large number (text-[120px] font-heading opacity-10) behind step text
- Steps are NOT evenly spaced — vary positioning for organic rhythm

**Connected path:**
- Steps connected by an SVG path (curved, not straight line)
- Path animates on scroll (stroke-dashoffset)
- Steps positioned along the path at irregular intervals
- Content appears as the path reaches each step

### STATS / METRICS

**Embedded in content (NOT a separate section):**
- Stats woven into other sections (hero, services, CTA)
- Individual stat numbers: massive typography (text-[80px]) blended with content
- mix-blend-mode: overlay or soft-light so numbers merge with background
- Counter animation on scroll intersection
- NO glass card around stats. NO border. NO grid-cols-4 layout.

**Typographic watermark style:**
- Stats as giant background text (text-[200px] opacity-[0.04])
- Actual stat values overlaid on top at normal size
- Creates depth — huge faded numbers behind, readable numbers in front

### TESTIMONIALS

**Typographic wall (NO cards):**
- Continuous flowing text, different testimonials at different sizes
- Key phrases highlighted (font-bold, or primary color)
- Large pull-quote: one testimonial at text-3xl or text-4xl, italic
- Smaller quotes surround it at text-sm, opacity-50
- Author names inline, subtle — "(Name, Role)" in muted text
- NO borders, NO card shapes, NO profile photos in circles

**Cascading pull-quotes:**
- 3-5 quotes positioned with intentional overlap and varied rotation
- Each quote: different size, different rotation (rotate-[-3deg] to rotate-[2deg])
- Some quotes larger (emphasis), some smaller (ambient)
- Author attribution: small, positioned at quote corner
- Background: gradient or blur that ties the overlapping quotes together

**Horizontal scroll ribbon:**
- Single horizontal strip that scrolls left, showing testimonials as full-width panels
- Each panel: large quote text centered, author below
- scroll-snap-type: x mandatory
- Panels have different background tones (gradient progression)
- NO card borders — just text on shifting backgrounds

**Stacked letter style:**
- Testimonials styled like physical letters/notes stacked on desk
- Each: slightly rotated, different sizes, shadow creating depth
- Handwriting-style font optional for quotes
- Click/hover: letter rises and centers for reading

### PRICING

**Overlapping tiers:**
- 2-3 pricing cards that overlap horizontally
- Featured tier: scale-105, z-10, full opacity, slightly forward
- Other tiers: scale-95, z-0, rotated ±2deg, reduced opacity
- NOT equal grid-cols-3 with borders
- Background: featured tier has gradient perimeter animation

**Comparison slider:**
- Two plans side by side with a draggable divider
- Left: Plan A (dark), Right: Plan B (light) — or reverse
- Features list spans both sides with checkmarks indicating inclusion
- Divider: glass strip with drag handle

### FAQ

**Expanding text blocks (NOT accordion with chevrons):**
- Questions displayed as large text blocks, stacked with tight line-height
- Click: answer text fades in below question, pushing others down
- Active question: highlighted (white), inactive: muted (white/30)
- NO chevron icons. NO border separators. Typography does the work.

### CTA / FINAL CALL

**Full-screen headline:**
- min-h-[80vh], heading fills the space: `text-[6vw]`
- mix-blend-mode: difference so text inverts over bg
- Single CTA button: absolute, bottom-center
- Background: video or animated gradient

**Overlapping text layers:**
- Main CTA text repeated 3-5 times at increasing opacity
- Each layer offset slightly (translateX/translateY)
- Creates ghosting/echo effect emphasizing the message
- Front layer: full white, back layers: white/10, white/5

### FOOTER

**Minimal editorial:**
- mt-32 pt-8 border-t border-white/5
- Single row: copyright left, horizontal links right
- text-xs text-white/30
- NO multi-column grid. Clean single line.

**Split minimal:**
- Left: logo + 1-line description
- Right: single row of links (no column grouping)
- Bottom: thin border + copyright
- Total footer height: under 120px

---

## Common Pattern: Section Heading (REPLACES badges)
```
Heading as statement: text-[clamp(2.5rem,5vw,5rem)] font-heading italic text-white tracking-tight leading-[0.9]
Context built into heading itself, e.g.: "We build digital experiences" not "[Services badge] What We Do → heading"
Sub-context: positioned offset (absolute, or flex with gap-16), small text-sm text-white/40, max-w-xs
```

## Common Pattern: Section Transition
```
Sections blend into each other rather than having hard edges:
- Shared gradient: bottom of section A and top of section B share a gradient
- Overlapping content: last element of section A peeks into section B's space
- No visible gap between sections (no py-24 gap; use padding within sections)
```

## Common Pattern: Section Padding
```
py-24 px-6 md:px-16 lg:px-24
For full-bleed sections: px-0, content inside max-w-7xl mx-auto px-6
```

## Common Pattern: Video Background with Fades
```
- Video: absolute inset-0, w-full h-full object-cover z-0
- Top fade: absolute top-0, h-[200px], bg-gradient-to-b from-black to-transparent
- Bottom fade: absolute bottom-0, h-[200px], bg-gradient-to-t from-black to-transparent
- Content: relative z-10
```
