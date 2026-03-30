<!-- SUMMARY: 10 creative domains (tech, organic, urban, etc.) each with visual ingredients, color schemas, and animation narrative starters for cross-domain mixing. Load only when user requests domain-based inspiration. -->

# Design Domain Reference

Ten creative domains — visual ingredients, color schemas, and animation narrative starters. Mix freely across domains.

---

### Cartoon / Illustrated

Hand-drawn warmth. Lines wobble on purpose. Physics are suggestions; everything bounces and squashes.

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Wobbly border | SVG `feTurbulence + feDisplacementMap` on edges — hand-drawn outline tremor | Cards, buttons |
| Squash-stretch bounce | `scaleY(0.7)` on land → `scaleY(1.15)` snap → settle with bouncy cubic-bezier | Element entrances |
| Ink hatching shadow | SVG diagonal hatch pattern at 30% opacity replacing `box-shadow` — drawn, not cast | Cards, hero art |
| Speed lines burst | SVG radial lines from center, `opacity 0→0.6→0` at 0.3s — impact emphasis | CTAs, hover |

```css
--ct-bg: 55 90% 97%; --ct-fg: 0 0% 8%; --ct-red: 5 90% 55%;
--ct-blue: 210 85% 55%; --ct-yellow: 48 100% 58%; --ct-outline: 0 0% 10%;
```

```
[Load] elements drop in, squash on landing, spring up — staggered 80ms per element
[Hero] title pops with speed lines, wobble border settles, logo wiggles once
[Scroll] cards bounce into view; hover triggers squash-stretch pulse on every card
```

---

### Minimalism / Monolithic

Single color. Absolute silence. The design disappears so the content exists.

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Monochrome tint stack | One hue in 7 tints (5%–95% lightness) — entire site in single-hue range | All color decisions |
| Infinite whitespace | `padding: 15–25vh 12–20vw` — breathing room IS the design | Layout system |
| Weight-only contrast | Typography contrast via `font-weight` 300 vs 900 only — no color change | Heading hierarchy |
| Opacity hover | Elements shift `opacity: 1 → 0.5` on hover — no color, no transform | Links, buttons |

```css
--mn-bg: 0 0% 99%; --mn-fg: 0 0% 4%; --mn-mid: 0 0% 50%;
--mn-subtle: 0 0% 92%; --mn-accent: 0 0% 8%;
```

```
[Page] no entrance animations — content is simply present. Stillness is the effect.
[Transitions] cross-fade only, 400ms, no movement — everything dissolves, nothing slides
[Micro] cursor changes, hair-line rule draws in at 0.3s — that is the entire animation budget
```

---

### Pixel Art / Retro 8-bit

Every pixel is a decision. Nostalgia crunched to 16×16. Constraint IS the aesthetic.

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Pixel font | `'Press Start 2P'` — every character a grid, no sub-pixel smoothing | Headings, UI chrome |
| Scanline overlay | `repeating-linear-gradient` 2px repeat with 8% dark bands | Dark backgrounds |
| Pixel border | `box-shadow` 4px steps at each corner — blocky pixel outline, no radius | Cards, buttons |
| CRT glow | `filter: blur(0.5px) brightness(1.1)` + green/amber tint — phosphor warmth | All text on dark bg |

```css
--px-bg: 130 20% 10%; --px-green1: 115 55% 55%; --px-green2: 120 40% 35%;
--px-green3: 125 25% 18%; --px-fg: 110 60% 75%; --px-red: 0 90% 50%;
```

```
[Load] CRT flicker: brightness 0→1 with scan-line sweep top-to-bottom (0.4s)
[Hero] title types in char-by-char at 80ms — pixel font, no cursor blink
[Interactions] buttons press exactly 2px (no easing), snap back — tactile pixel click
```

---

### Outer Space

Infinite dark. Stars as the only reference. Gravity absent; time unclear.

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Star field | `box-shadow` on `::before` with 200+ white 1px points at varied opacities — 3 parallax speed layers | Dark hero, page bg |
| Nebula cloud | `radial-gradient` in deep purple/teal at 15–25% opacity, `filter: blur(80–120px)` | Hero, section dividers |
| Zero-gravity float | `translateY(-12px) rotate(3deg)` over 8s ease-in-out loop — weightless drift | Hero objects, icons |
| Warp tunnel | `perspective(800px) rotateX(85deg)` on radial grid, stars rushing center via `scale` | Loading, transitions |

```css
--sp-void: 230 30% 3%; --sp-star: 200 20% 95%; --sp-nebula: 275 60% 35%;
--sp-teal: 185 70% 30%; --sp-planet: 210 80% 45%; --sp-sun: 40 100% 65%;
```

```
[Entry] stars fade in 1.5s, distant first — nebula blooms slowly from corner (3s)
[Scroll] parallax: stars 10% speed, nebula 5%, content 100% — three-layer depth
[Sections] nebula hue shifts: blue → purple → magenta as depth increases downward
```

---

### Underwater

Caustic light bends across everything. Sound muffled. Depth compresses color.

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Caustic light | SVG `feTurbulence + feColorMatrix` blue-green composite, animated `baseFrequency` drift | Hero bg, overlays |
| Rising bubbles | 4–12px circles, `translateY` bottom→off-screen, staggered delays, slight sinusoidal X wobble | Dark backgrounds |
| Depth haze | `backdrop-filter: blur(2px)` + blue-green overlay increasing opacity with scroll depth | Lower sections |
| Bioluminescent glow | Cyan `box-shadow` wide spread (40px), pulsing `opacity 0.4→0.8` at 3s | CTAs, accents |

```css
--uw-deep: 205 50% 6%; --uw-mid: 200 60% 18%; --uw-shallow: 190 65% 35%;
--uw-caustic: 175 70% 55%; --uw-biolum: 180 100% 60%; --uw-sand: 40 30% 65%;
```

```
[Entry] caustic light drifts across hero bg, bubbles rise from lower fold continuously
[Scroll] color deepens: teal → mid blue → abyss. Blur subtly increases.
[Deep sections] bioluminescent elements glow, as if lit by their own living light
```

---

### Steampunk

Brass, leather, clockwork. Every mechanism visible and beautiful. Steam is the power.

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Rotating gear | SVG gear (12 teeth), `@keyframes rotate` — smaller gears spin faster, larger slower | Decorative corners, loaders |
| Brass gradient | `linear-gradient(135deg, hsl(40,70%,55%), hsl(35,80%,38%), hsl(43,65%,60%))` | Buttons, borders |
| Riveted plate border | `border: 3px solid var(--brass)` + SVG rivets at corners and midpoints | Cards, containers |
| Steam vent puff | Blurred gray radial-gradient blob rising from element base, `translateY + opacity 0→0.4→0` | Section bases |

```css
--st-bg: 30 25% 8%; --st-brass: 40 65% 52%; --st-aged: 35 45% 35%;
--st-copper: 20 70% 48%; --st-steam: 200 15% 75%; --st-gauge: 55 80% 60%;
```

```
[Load] gears start from still, accelerate to constant mechanical rotation over 1s
[Hero] steam puffs rise. Brass surfaces catch light (shimmer keyframe, slow hue-rotate).
[Interactions] buttons depress with gear-click: scale(0.97) + 50ms snap — mechanical tactility
```

---

### Paper / Stationery

Fold lines. Ink bleeding into fiber. The weight of a page that has been held.

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Paper texture | SVG `feTurbulence baseFrequency="0.9"` noise at 8% opacity — fine paper grain | All backgrounds |
| Ink bleed | SVG `feGaussianBlur + feColorMatrix` on text edges — ink soaking into fiber | Headings, borders |
| Fold shadow | `box-shadow: 0 2px 8px rgba(0,0,0,0.12), inset 0 1px 0 rgba(255,255,255,0.6)` | Cards, panels |
| Torn edge divider | SVG jagged/irregular horizontal path — paper torn, not cut | Section breaks |

```css
--pp-bg: 45 25% 94%; --pp-fg: 25 40% 12%; --pp-fold: 40 20% 82%;
--pp-stamp-red: 5 60% 45%; --pp-aged: 38 35% 80%; --pp-rule: 210 30% 65%;
```

```
[Entry] page unfolds: scale 0.95 + rotateX(2deg) → flat, 0.6s ease-out
[Scroll] ink bleed filter applies progressively to headings — words appear freshly written
[Hover] cards lift: fold shadow deepens, subtle crinkle scale (1.005) at corners
```

---

### Neon City / Cyberpunk

Rain-slicked surfaces. Holograms flicker. Every surface is also an advertisement.

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Neon sign glow | 3-layer `box-shadow`: 2px tight, 8px mid, 30px atmospheric bloom — animate 0.8→1→0.85 at 2s | Headings, card borders |
| Rain streak | `repeating-linear-gradient` 1px vertical lines, animate `background-position-y` downward 3s | Hero backgrounds |
| Glitch offset | `clip-path` horizontal slices shift `translateX ±4px` at irregular timing, 0.2s burst | Headings, logo |
| Hologram shimmer | `linear-gradient(135deg, hsl(290,100%,70%), hsl(200,100%,70%))` + `hue-rotate` animation | Labels, UI accents |

```css
--nc-bg: 240 15% 4%; --nc-surface: 240 12% 8%; --nc-fg: 200 10% 88%;
--nc-pink: 320 100% 60%; --nc-cyan: 185 100% 55%; --nc-violet: 275 100% 65%;
```

```
[Load] dark screen, neon signs flicker on one-by-one with staggered 0.2s delays
[Scroll] glitch burst on each section heading as it enters viewport (0.3s, then stable)
[Hover] cards intensify glow; chromatic aberration text-shadow appears on title text
```

---

### Claymation / 3D Tactile

Soft. Fingerprints in the surface. Color is chunky and pure. Everything has weight and squish.

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Clay depth shadow | Multi-layer shadow: `0 2px 0`, `0 4px 0`, `0 8px 20px` in darkening hues — clay slab thickness | Buttons, cards |
| Puffy border radius | `border-radius: 35–50%` on rectangles — inflated pillow shapes | Cards, badges |
| Squish press | `:active` → `scaleY(0.92) scaleX(1.04)` simultaneous, 80ms snap, 200ms release | All interactive |
| Bold fill colors | Pure saturated `hsl(H 75% 55%)` — clay is vivid, no washed-out pastels | Backgrounds, accents |

```css
--cl-bg: 40 30% 94%; --cl-red: 5 80% 58%; --cl-blue: 210 75% 55%;
--cl-yellow: 46 90% 58%; --cl-green: 140 60% 48%; --cl-shadow: 0 0% 15%;
```

```
[Entry] elements drop from above, clay-squash on impact (scaleY 0.75→1.1→1.0), staggered
[Hero] main shape wiggles once (rotateZ ±2deg), settles — invites touch
[Interactions] every press physically squishes — tactile feedback is the entire language
```

---

### Isometric / Blueprint Technical

Axonometric precision. Every line measured. The diagram IS the design.

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Isometric grid | SVG background with 60° diamond grid lines at 0.12 opacity | Full-width backgrounds |
| Blueprint paper | `hsl(215 70% 15%)` bg + white grid lines at 0.15 opacity — classic blueprint | Dark technical sections |
| 3D box | `rotateX(30deg) rotateZ(45deg) skewX(-15deg)` CSS approximation — isometric block | Hero art, icon blocks |
| Draw-on line | SVG `stroke-dashoffset` animate 100%→0 — line drawing itself into existence | Reveals, diagrams |

```css
--iso-bg: 215 65% 12%; --iso-grid: 210 50% 80%; --iso-top: 210 60% 35%;
--iso-left: 215 55% 22%; --iso-right: 210 50% 28%; --iso-accent: 50 100% 55%;
```

```
[Load] grid lines draw outward from origin point at 0.8s — the canvas constructs itself
[Hero] isometric box assembles face-by-face: bottom → left → right → top, 0.15s per face
[Sections] each diagram draws in with stroke-dashoffset as viewport is reached
```
