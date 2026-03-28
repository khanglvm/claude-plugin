# Mood & Atmosphere Themes

Pure emotional states translated into visual + interactive CSS. These are not aesthetics or eras — they are FEELINGS. Use them as the emotional layer underneath any other design direction. Every ingredient is extractable, mixable, and scalable.

---

## Themes

### Dreamlike / Ethereal

Half-asleep perception, floating between worlds. The page doesn't load — it materializes. The user is never quite sure if they're reading or dreaming.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Soft-focus aura | Global `backdrop-filter: blur(1-3px)` on non-hero sections — everything slightly out of focus except the focused element | Any dark or light minimal site |
| Floaty animation | All transitions 3-5s ease-in-out. `@keyframes float` — elements drift 8-15px vertically, never settling | Hero elements, CTAs, headings |
| Transparent layering | 4-6 overlapping divs at 10-30% opacity — depth without weight, like gauze curtains | Full-page backgrounds |
| Pastel dissolves | Section transitions via opacity+blur crossfade, no hard cuts. Colors: lilac, powder blue, pearl, blush | Inter-section transitions |
| Gravity defiance | Elements positioned with transforms that suggest floating — slight rotate(-1deg) to rotate(2deg), offset from grid baseline | Cards, images, callouts |
| Dream-haze vignette | Radial gradient overlay at 20-40% opacity from edges to center, edges dissolve to white or deep indigo | Any section background |
| Iridescent shimmer | `background: linear-gradient(135deg, ...)` animated slowly via `hue-rotate` — rainbow shifts at 0.2deg/frame | Accent elements, borders |

**Color schema:**
```css
/* Waking Dream */
--dream-bg: 270 30% 95%;            /* near-white with violet ghost */
--dream-fg: 260 15% 25%;            /* soft indigo text */
--dream-accent: 285 40% 70%;        /* soft violet */
--dream-secondary: 200 50% 80%;     /* powder blue */
--dream-glow: 270 60% 85% / 0.3;

/* Deep Dream (dark variant) */
--dream-deep-bg: 260 25% 8%;        /* midnight indigo */
--dream-deep-fg: 240 30% 90%;       /* pale lavender */
--dream-deep-accent: 290 50% 70%;   /* violet mist */
--dream-deep-shimmer: 220 40% 60% / 0.2;
```

**Font pairings that fit:**
- **Floated editorial:** Cormorant Garamond (italic, headings) + Nunito (300, body) — soft, weightless
- **Whispered clarity:** Playfair Display (light italic) + DM Sans (300) — legible but delicate
- **Otherworldly script:** Italiana (headings) + Lato (200-300, body) — formal but dissolving

**NOT a locked theme.** Soft-focus blur works as a hover state on any gallery. Floaty animation suits any hero that needs gravitas. Pastel dissolves work between any sections that need emotional breathing room.

**Architectural short-schema:**
```
DREAMLIKE PAGE FLOW:
  [Materialization] — hero fades in from white/void, elements float into position (not slide)
    ↓ soft dissolve, blur lifts slowly
  [First Clarity] — content readable but surrounded by haze, edges soft
    ↓ iridescent shimmer on section borders
  [The Float] — elements gently drift, nothing anchored hard to grid
    ↓ layered transparencies overlap, depth without solidity
  [Deep Dream] — darkest section, violet/indigo, ghostly overlapping type
    ↓ slow fade back to light
  [Waking] — CTA section, clearest focus, dream-haze recedes to edges only

Transitions: NEVER slide or hard cut. Always dissolve, blur-in, opacity-cascade.
Motion speed: 3-5x slower than typical UI. Patience is part of the experience.
```

**Sensory anchors:** silk, fog, half-open eyes, 4am, lucid dreaming, underwater-surface light, candlelight through gauze

---

### Noir / Mystery

Shadows hiding truth. Knowledge is a narrow beam — you see only what the light reveals. The rest is inference and dread.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Spotlight reveal | Content visible only in a cone of light — `radial-gradient(circle at cursor, transparent 0%, black 40%)` as cursor-following overlay | Feature sections, hero |
| Fog of war | Sections outside scroll viewport stay heavily darkened — `opacity: 0.05` until in-view, then reveal to 100% | Any multi-section layout |
| Typewriter text | Character-by-character reveal on headings via JS, `monospace` cursor blink retained after | Hero titles, section headings |
| Hard-shadow geometry | `box-shadow: 40px 40px 0px rgba(0,0,0,0.8)` — heavy, directional, 1940s photographic | Cards, containers |
| Rain-slick texture | Dark glossy background via `background: repeating-linear-gradient(...)` — wet asphalt, light-refracting surface | Section backgrounds |
| Evidence pin-board | Content connected by thin lines (SVG `<line>`) — detective wall aesthetic | Feature comparison, timelines |
| Low-key portrait | Single strong side-light source via `box-shadow: inset -40px 0 80px rgba(0,0,0,0.9)` on images | Hero images, profiles |

**Color schema:**
```css
/* Classic Noir */
--noir-bg: 220 10% 5%;              /* near-black with cool tint */
--noir-fg: 40 15% 85%;              /* cream-yellow newsprint */
--noir-accent: 40 60% 55%;          /* spotlight gold */
--noir-shadow: 0 0% 0% / 0.85;
--noir-mist: 220 15% 30% / 0.4;     /* fog */

/* Neo Noir */
--noir-neo-bg: 240 20% 5%;          /* cold blue-black */
--noir-neo-fg: 200 20% 85%;         /* cold white */
--noir-neo-accent: 350 80% 55%;     /* neon red slit */
--noir-neo-secondary: 200 100% 50%; /* cold blue sliver */
```

**Font pairings that fit:**
- **Pulp fiction:** Special Elite (headings) + Courier Prime (body) — newsprint, typewriter
- **Neo noir:** Space Grotesk (700, headings) + IBM Plex Mono (body) — cold, digital
- **Classic mystery:** Playfair Display (italic) + Source Serif 4 (body) — literary, weighted

**NOT a locked theme.** Spotlight cursor overlay works on ANY portfolio or interactive demo. Typewriter reveal works on any hero with a punchy single line. Fog-of-war scroll works on any narrative page that benefits from sequential disclosure.

**Architectural short-schema:**
```
NOIR PAGE FLOW:
  [The Dark] — hero: near-black, single text line typewriter-reveals in spotlight
    ↓ cursor moves, spotlight follows — user discovers content by exploring
  [The Scene] — content layout, but heavy shadows suppress non-focus elements
    ↓ scroll trigger lifts fog on each section
  [Evidence Board] — feature/comparison section, pin-board aesthetic
    ↓ rain-slick texture, reflective surface
  [The Reveal] — the answer/offer. Spotlight widens, fog lifts.
  [Closing] — CTA in full light, all shadow retreats. The mystery is solved.

Light source: always from a single implied direction (top-left or center-above)
Darkness: default state. Light is earned by scroll/interaction.
```

**Sensory anchors:** cigarette smoke, single desk lamp, rain on window, overcoat collar up, footsteps receding

---

### Carnival / Festival

Explosive joy that doesn't apologize. Every element competes for attention and somehow the chaos is the point.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Confetti burst | On CTA click or section enter: colored paper pieces scatter from element with physics (gravity, rotation, drift) | CTAs, hero reveals, wins |
| Marquee-light borders | Border flickers via `animation: marquee-lights` — dots travel around container perimeter like bulb-lit signs | Cards, headers, feature boxes |
| Tilt-fun | `transform: rotate(-2deg)` on cards and elements — nothing sits straight on the carnival ground | All cards, all sections |
| Clashing palette | Simultaneous red + yellow + blue + green — Matisse boldness, not pastel softness | Section backgrounds, text |
| Barker typography | Mix of font sizes in single heading: ONE WORD at 120px, rest at 40px — the bellowing carnival barker | Hero, section titles |
| Spinning accent | Decorative elements (stars, suns, ribbons) continuously rotate — `animation: spin 8s linear infinite` | Dividers, background deco |
| Crowd energy | High particle count (50-100 slow-drifting specks) always present — the air is alive | Full-page background |

**Color schema:**
```css
/* Carnival Day */
--carnival-bg: 45 100% 97%;         /* bright fairground sunlight */
--carnival-red: 0 90% 55%;          /* candy apple red */
--carnival-yellow: 48 100% 50%;     /* electric mustard */
--carnival-blue: 210 100% 45%;      /* royal blue tent */
--carnival-green: 140 70% 40%;      /* deep awning green */
--carnival-fg: 0 0% 10%;            /* bold dark type */

/* Night Carnival */
--carnival-night-bg: 260 30% 8%;    /* dark fairground sky */
--carnival-night-light: 45 100% 65%; /* light-bulb yellow */
--carnival-night-accent: 350 100% 60%; /* neon pink-red */
```

**Font pairings that fit:**
- **Big top:** Lilita One (headings) + Nunito (700, body) — round, bold, fun
- **Vintage fair:** Alfa Slab One (headings) + Libre Baskerville (body) — poster, editorial
- **Wild posting:** Oswald (900, headings) + Barlow Condensed (body) — compressed energy

**NOT a locked theme.** Confetti burst works on any conversion moment. Marquee-light borders work on pricing tables or pricing highlights. Tilt-fun works on any testimonial or feature card that needs personality.

**Architectural short-schema:**
```
CARNIVAL PAGE FLOW:
  [The Gates Open] — hero: full-width chaos, clashing colors, confetti rains in
    ↓ barker heading, spinning stars, crowd specks in background
  [The Midway] — features as carnival game booths (tilted cards, marquee borders)
    ↓ every card is a different bold color
  [The Main Stage] — CTA/testimonial area, spotlight effect on stage
    ↓ confetti burst on entering section
  [The Finale] — conversion. Full burst. Everything spins, flashes, celebrates.

Rule: if it's not too much, add more. The restraint IS the design choice — there is none.
```

**Sensory anchors:** popcorn smell, spinning lights, crowd roar, gameshow buzzer, candy floss in hand

---

### Sacred / Spiritual

Transcendence through emptiness. Light that arrives from nowhere. Silence that has weight.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Golden emanation | `radial-gradient` from center/top — gold bleeding into deep space, subtle enough to feel found not placed | Hero, feature sections |
| Incense wisps | Thin SVG paths that slowly drift and dissolve upward, `stroke: gold/30%`, `stroke-width: 1px` | Dividers, section accents |
| Reverent spacing | `padding: 15vh 20vw` minimum — content surrounded by silence on all sides | All sections |
| Choir stacking | Heading broken into single words, each on its own line, centered — cathedral resonance | Hero titles |
| Mandala geometry | Rotational SVG geometry as background — symmetrical, slowly rotating at 0.5rpm | Section backgrounds, hero |
| Icon as relic | Single symbolic image, small, centered, given enormous surrounding whitespace | Logo zones, separators |
| Candlelight flicker | Subtle brightness animation on accent elements — `opacity: 0.8 → 1.0 → 0.85`, 2-3s cycle | Borders, glows |

**Color schema:**
```css
/* Temple Gold */
--sacred-bg: 40 20% 6%;             /* dark incense chamber */
--sacred-fg: 40 30% 88%;            /* candlelight white */
--sacred-gold: 42 80% 60%;          /* aged temple gold */
--sacred-emanation: 40 100% 70% / 0.08; /* barely-there glow */
--sacred-shadow: 0 0% 0% / 0.7;

/* Cathedral Light */
--sacred-light-bg: 40 25% 96%;      /* parchment-warm white */
--sacred-light-fg: 30 15% 20%;      /* ink on vellum */
--sacred-light-gold: 42 70% 45%;    /* manuscript illumination */
--sacred-light-glow: 42 100% 75% / 0.15;
```

**Font pairings that fit:**
- **Ancient manuscript:** Cormorant Garamond (300, italic, headings) + EB Garamond (body) — illuminated, sacred
- **Modern temple:** Cinzel (headings) + Philosopher (body) — classical authority
- **Zen stone:** Noto Serif (light, headings) + Noto Sans (300, body) — neutral, reverent

**NOT a locked theme.** Reverent spacing works on ANY luxury or mindfulness brand. Golden emanation works as a hero background for wellness, premium, or spiritual products. Choir stacking works on any brand with a powerful single statement.

**Architectural short-schema:**
```
SACRED PAGE FLOW:
  [The Threshold] — hero: darkness, single word appears, golden light blooms from it
    ↓ silence (slow scroll, no animation speed)
  [The Nave] — content in vast whitespace, incense wisps border sections
    ↓ each section feels like a different chamber of the same temple
  [The Altar] — core offer/product. Centered, glowing, elevated. Surrounded by void.
    ↓ mandala geometry rotates slowly behind
  [The Blessing] — CTA. Golden light maxes. Space collapses warmly around the action.

Rule: ONE focal element per section. Everything else is void.
Sound analogy: Gregorian chant — one voice at a time, never crowded.
```

**Sensory anchors:** frankincense, stone floor, choir echo, single candle, cathedral height, hushed breath

---

### Chaotic / Explosive

Energy that has exceeded its container. The design broke itself to show you how much it contains.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Container escape | Elements with `overflow: visible`, content spilling outside parent bounds — intentional, not broken | Cards, feature boxes |
| Crack animation | SVG crack paths with `stroke-dashoffset` reveal — surfaces fracture on scroll trigger | Section backgrounds, headers |
| Scatter layout | Absolute-positioned elements at wild offsets — deliberate compositional chaos | Hero, feature highlights |
| Screen shake | `@keyframes shake` on high-impact moments — 3-6px translate in random directions, 0.3s, triggered by CTA hover | CTAs, high-impact buttons |
| Explosion particles | Radial particle burst from center — NOT gentle confetti, sharp fast outward scatter | Section enters, click events |
| Glitch interrupt | Brief `clip-path` slice animation — content momentarily splits into offset layers, rejoins | Headings, section titles |
| Over-print collision | Typography overlapping itself and other elements, z-index deliberate collision | Hero typography |

**Color schema:**
```css
/* High Energy */
--chaos-bg: 0 0% 4%;                /* near-black */
--chaos-fg: 0 0% 96%;               /* white */
--chaos-accent1: 15 100% 55%;       /* aggressive orange-red */
--chaos-accent2: 55 100% 55%;       /* electric yellow */
--chaos-accent3: 270 100% 65%;      /* ultraviolet */
--chaos-crack: 45 100% 75%;         /* glowing fracture */
```

**Font pairings that fit:**
- **Impact zone:** Black Han Sans (headings) + Barlow (900, body) — weight that breaks containers
- **Deconstructed:** Bebas Neue (headings) + Space Mono (body) — industrial, cracking
- **Screaming:** Oswald (900, caps) + Inter (300, body) — maximum contrast

**NOT a locked theme.** Screen shake works as hover feedback on ANY bold CTA. Container escape works on any hero that wants to feel too big for the page. Crack animations work on any "before/after" reveal.

**Architectural short-schema:**
```
CHAOS PAGE FLOW:
  [Impact] — hero: text crashes into view (not fades), particles scatter from center
    ↓ glitch interrupt on hero title, then stabilizes
  [Fracture] — feature section, crack animations on section entry, containers slightly escaped
  [Overload] — densest section, elements collide, over-print typography
    ↓ screen shake on hover
  [Release] — CTA, explosion burst on click, energy discharges into conversion

Danger: visual chaos must have rhythm underneath. The grid is still there — just bent.
Rule: Chaotic LAYOUT, not chaotic COLOR. Pick 2 accent colors max. Chaos in space, not hue.
```

**Sensory anchors:** bass drop, shockwave, broken glass, lightning strike, pressure release

---

### Zen / Serene

Intentional emptiness is not absence — it is the thing itself. One breath. One element. Complete.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Maximal whitespace | `padding: 20vh 25vw` — content as a meditation object in surrounding space | Every section |
| Single-element focus | One element per viewport. No sidebar, no related content bleeding in. | Hero, key features |
| Ripple interaction | Click/hover creates concentric circle ripple from interaction point — water surface | CTAs, links, backgrounds |
| Breathing animation | `@keyframes breathe` — scale(1) → scale(1.015) → scale(1), 4s ease-in-out — matches human breath | Hero images, logos |
| Rock garden grid | Irregular but precise element placement — looks asymmetric, is mathematically balanced | Feature grid, gallery |
| Sound space | Long scroll between elements — the space IS content, not wasted area | Section spacing |
| Ink wash | `filter: grayscale(30%) contrast(1.1)` on images — brush-stroke, watercolor-adjacent | All images |

**Color schema:**
```css
/* Stone Garden */
--zen-bg: 40 8% 96%;                /* warm paper-white */
--zen-fg: 30 10% 18%;               /* sumi ink */
--zen-accent: 160 25% 45%;          /* sage — single breath of color */
--zen-secondary: 30 15% 70%;        /* warm gray stone */
--zen-void: 40 5% 98%;              /* the emptiness between elements */

/* Dark Stone */
--zen-dark-bg: 220 8% 8%;           /* night stone */
--zen-dark-fg: 30 10% 85%;          /* moonlit parchment */
--zen-dark-accent: 160 30% 50%;     /* still water */
```

**Font pairings that fit:**
- **Brushwork:** Noto Serif (300, headings) + Noto Sans (200, body) — brush meets print
- **Pure signal:** Inter (300, headings) + Inter (200, body) — no decoration, pure clarity
- **Stone inscription:** Cormorant (300) + Source Sans 3 (200-300) — carved, not printed

**NOT a locked theme.** Ripple interactions work on ANY page that wants organic, calming feedback. Breathing animation works on any logo or hero image. Rock garden grid works as an elegant gallery or feature layout.

**Architectural short-schema:**
```
ZEN PAGE FLOW:
  [Arrival] — hero: single sentence, centered, surrounded entirely by space. Nothing else.
    ↓ long scroll pause — intentional
  [First Stone] — one feature. One. Surrounded by void. Breathes on its own.
    ↓ ripple as you move past it
  [The Path] — sequential single elements, large gaps between
    ↓ each element has its own breath-cycle animation
  [Still Water] — CTA, perfectly centered, ripple-on-hover, no decoration

Rule: if you can remove it, remove it. Then ask again if you can remove it.
Constraint: max 3 elements visible at once, ALWAYS.
```

**Sensory anchors:** raked gravel, single bell, morning mist, held breath, the pause between notes

---

### Melancholic Rain

Beautiful sadness — the kind you choose to sit with. Looking through glass at a world that continues without you.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Rain streak overlay | Canvas or CSS `repeating-linear-gradient` diagonal streaks at 1px width, moving downward — speed varies with scroll velocity | Any dark section |
| Condensation blur | `backdrop-filter: blur(8px)` with subtle moisture texture — glass between viewer and content | Hero image, backgrounds |
| Muted desaturation | `filter: saturate(40-60%)` on images and backgrounds — color exists but grief has drained it | All imagery |
| Slow drip | Single elements (drops, lines) that fall slowly from top of section, pause, continue | Decorative accents |
| Fog distance | Far elements lighter opacity than near — atmospheric perspective like looking through misty window | Multi-layer backgrounds |
| Window frame | Content inside implied window frame (inset border, slight vignette, world outside) | Hero, feature sections |
| Piano sustain timing | Transitions at 800-1200ms — not lazy, but weighted with feeling | All micro-animations |

**Color schema:**
```css
/* Gray Rain */
--rain-bg: 210 15% 10%;             /* stormy blue-gray */
--rain-fg: 210 10% 80%;             /* cold light through glass */
--rain-accent: 200 30% 50%;         /* steel water reflection */
--rain-streak: 210 20% 70% / 0.15;  /* rain on glass */
--rain-fog: 210 10% 50% / 0.3;

/* Amber Rain (nostalgic variant) */
--rain-amber-bg: 30 15% 10%;        /* warm dark evening */
--rain-amber-fg: 35 15% 80%;        /* lamp-lit interior */
--rain-amber-accent: 35 60% 55%;    /* window lamp glow */
--rain-amber-streak: 35 20% 60% / 0.12;
```

**Font pairings that fit:**
- **Interior monologue:** Lora (italic, headings) + Lora (300, body) — continuous, intimate voice
- **Journal entry:** Fraunces (italic, headings) + Source Serif 4 (light) — literary, handwritten-adjacent
- **Cold clarity:** DM Serif Display (headings) + DM Sans (300) — clear but weighted

**NOT a locked theme.** Rain streak overlay works as a subtle texture on ANY dark background. Desaturation filter is a powerful "past" signal for before/after sections. Condensation blur works as a glassmorphism variant with emotional weight.

**Architectural short-schema:**
```
MELANCHOLIC PAGE FLOW:
  [The Window] — hero: world outside, rain-streak overlay, viewer is inside looking out
    ↓ slow scroll, condensation blur on background imagery
  [Memory] — content reads like looking at old photographs — muted, soft edges
    ↓ rain continues, ambient presence not spectacle
  [Recognition] — the core value/offer. A lamp-lit moment of warmth in gray.
    ↓ amber accent warms the palette briefly
  [Acceptance] — CTA. Quiet. Rain eases. The decision is intimate, not sold.

Pace: the slowest theme. No urgency. Scroll should feel like turning pages of a journal.
```

**Sensory anchors:** rain on glass, wet wool, fog horn, old tea, looking out the window, one lamp on

---

### Euphoric / Celebration

You just won. The best moment. The crowd roars. Nothing will ever be this good and that's okay because right now it's perfect.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Firework burst | On section enter: radial particle explosion with trails — multiple simultaneous bursts at different positions | Hero enter, CTA trigger |
| Starburst flash | `@keyframes flash` — brief white overlay that fades in 150ms, fades out 600ms — photo flash of the peak moment | High-impact moments |
| Gold shower | Dense downward particles in gold/yellow — slower and heavier than confetti | CTA sections, wins |
| Rising balloons | SVG circles that drift upward from bottom, slight sway, pop and disappear at top | Background element |
| Champagne fizz | Tiny bubble particles rise from bottom of containers — `border-bottom` as rim | Cards, feature boxes |
| Stadium brightness | Full-screen white-out that recedes to reveal the content — crowd-flash reveal | Section transitions |
| Trophy glow | Single element with golden pulsing `box-shadow` — the moment of recognition | CTA, key stat, award |

**Color schema:**
```css
/* Gold Victory */
--euphoric-bg: 45 30% 97%;          /* daylight celebration */
--euphoric-gold: 42 100% 55%;       /* stadium gold */
--euphoric-fg: 40 10% 10%;          /* grounding dark type */
--euphoric-burst1: 348 100% 60%;    /* celebration pink */
--euphoric-burst2: 190 100% 45%;    /* pop cyan */
--euphoric-glow: 45 100% 60% / 0.4;

/* Night Victory */
--euphoric-night-bg: 250 25% 6%;    /* stadium night */
--euphoric-night-gold: 45 100% 60%; /* spotlight gold */
--euphoric-night-fg: 0 0% 97%;
--euphoric-night-burst: 290 100% 65%; /* purple flash */
```

**Font pairings that fit:**
- **Trophy cabinet:** Fraunces (700, headings) + Inter (500, body) — warm, winning
- **Podium moment:** Clash Display (700) + DM Sans (500) — designed to celebrate
- **Championship:** Bebas Neue (headings, wide-tracked) + Source Sans 3 (body) — announcer voice

**NOT a locked theme.** Firework burst works on any conversion confirmation. Gold shower works on pricing page success states. Trophy glow works on any key metric or stat that deserves celebration.

**Architectural short-schema:**
```
EUPHORIC PAGE FLOW:
  [The Win] — hero: stadium brightness flash reveals, fireworks burst immediately
    ↓ gold shower ongoing in background
  [The Highlights] — features as trophy moments, each with own glow
    ↓ champagne fizz borders on feature cards
  [The Crowd] — social proof/testimonials, rising balloons ambient
    ↓ energy builds
  [The Podium] — CTA. Maximum gold glow. Firework burst on hover. Click = full celebration.

Energy: does NOT sustain maximum. Builds → peaks → peaks again at CTA.
Rule: every interaction should feel like scoring a goal.
```

**Sensory anchors:** crowd roar, firework pop, champagne cork, confetti in hair, jumping up and down

---

### Haunted / Eerie

Something is wrong but you can't name it. Things move when you're not watching. The uncanny valley is the destination.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Peripheral drift | Elements move 2-3px while scroll is idle — stop when user looks directly (mouse-over resets) — seen from corner of eye | Background elements, decorative |
| Flicker instability | `@keyframes flicker` — opacity 1 → 0.97 → 1 → 0.94 → 1, irregular intervals, 0.05s per frame | Headings, borders, any element |
| Static interrupt | Brief noise texture flash (SVG feTurbulence) over content, 80ms, triggered randomly every 15-40s | Full page overlay |
| Desaturated accent | Page fully desaturated except one color (red, sickly green, bruise purple) — the one thing that notices you | Key accent color only |
| Wrong distance | Elements sized incongruently — something small is too close, something large is too far. Perspective broken. | Card layouts, imagery |
| Echo typography | Heading's text repeated behind it at `opacity: 0.04`, offset 2px — the whisper layer | All headings |
| Temperature drop | Color temperature shifts toward cold blue-gray as user scrolls deeper — something gets colder | Background color transition |

**Color schema:**
```css
/* Haunted Gray */
--haunted-bg: 220 8% 7%;            /* cold empty room */
--haunted-fg: 220 5% 75%;           /* pale, drained */
--haunted-accent: 0 60% 45%;        /* the one red thing */
--haunted-static: 220 5% 50% / 0.03; /* barely-there noise */
--haunted-cold: 230 15% 50%;        /* the chill sets in */

/* Pale Green Variant */
--haunted-green-accent: 140 40% 35%; /* wrong green — organic in inorganic space */
```

**Font pairings that fit:**
- **Wrong normal:** Inter (400, headings — too normal for the context) + Inter (300, body) — uncanny normalcy
- **Decaying formal:** Cormorant Garamond (headings, italic) + Courier Prime (body) — formal disintegrating
- **Cold system:** IBM Plex Mono (headings) + IBM Plex Sans (200, body) — clinical, wrong

**NOT a locked theme.** Peripheral drift works as a subtle engagement mechanic on ANY dark background. Flicker instability is a powerful "unstable/glitch" signal for any project in disruption. Echo typography adds cinematic depth to any heading.

**Architectural short-schema:**
```
HAUNTED PAGE FLOW:
  [Normal Entry] — hero appears normal. Slightly too quiet. Echo on heading only hint.
    ↓ peripheral drift begins in background, very subtle
  [Something's Off] — layout is standard but proportions feel wrong. Static interrupt triggers once.
  [The Cold] — color temperature drops. Desaturation increases. Accent color is present.
    ↓ flicker on headings intensifies
  [The Room] — deepest section. Peripheral drift increases. Temperature is coldest.
  [The Turn] — CTA. Accent color is the only warm thing in the room. It's the exit.

Rule: build dread through accumulation, not jump scares.
Sound analogy: a room that's too quiet, then a door closes somewhere far away.
```

**Sensory anchors:** cold draft, wrong silence, door you didn't open, footsteps in ceiling, mirror at night

---

### Rebellious / Punk

Anti-everything. Built from found materials. Loud on purpose. Agreeing would be betrayal.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Spray paint splatter | SVG blob shapes at section edges, `mix-blend-mode: multiply` or `screen` — tagging the frame | Section borders, backgrounds |
| Torn edges | `clip-path: polygon(...)` with jagged irregular points — ripped paper/sticker aesthetic | Cards, images, sections |
| Anarchy markers | Hand-drawn X, circle-A, cross-out marks in SVG — decorative but loaded | Feature callouts, testimonials |
| Xerox noise | High grain `filter: contrast(1.3) brightness(0.85)` + SVG feTurbulence — photocopied 50 times | Image overlays, backgrounds |
| Aggressive hand | Indie Flower or similar — aggressive scrawl annotation over formal elements | Pull quotes, margin notes |
| Ransom collage | Mixed fonts within single heading — different weights, sizes, transforms — ransom note | Hero titles, section headers |
| Overexposed flash | `filter: brightness(1.5) contrast(1.4)` on key images — DIY flash photography | Photos, image sections |

**Color schema:**
```css
/* Xerox Punk */
--punk-bg: 0 0% 96%;                /* cheap white paper */
--punk-fg: 0 0% 5%;                 /* photocopier black */
--punk-spray1: 0 90% 50%;           /* red tag */
--punk-spray2: 55 100% 45%;         /* yellow tag */
--punk-noise: 0 0% 50% / 0.08;      /* grain */

/* Night Punk */
--punk-night-bg: 0 0% 5%;           /* black wall */
--punk-night-fg: 0 0% 92%;          /* chalk, spraypaint white */
--punk-night-spray: 290 80% 60%;    /* neon purple tag */
```

**Font pairings that fit:**
- **DIY manifesto:** Bangers (headings) + Courier Prime (body) — comic book meets typewriter
- **Street press:** Oswald (900, caps) + Special Elite (body) — silk-screen meets newsprint
- **Zine aesthetic:** Bebas Neue (headings) + Anonymous Pro (body) — cut-and-paste

**NOT a locked theme.** Torn edges work on any brand that wants rough authenticity. Xerox noise is a universal "underground/indie" texture. Spray paint splatter works on any section divider that should feel raw.

**Architectural short-schema:**
```
PUNK PAGE FLOW:
  [The Wall] — hero: spray paint reveal, content tagged onto background
    ↓ no hero transition — it slams in
  [The Manifesto] — core value statement in ransom collage typography
    ↓ torn-edge section divider
  [The Evidence] — features/proof as xerox-quality flyers and handouts
    ↓ anarchy markers and aggressive hand-annotations
  [The Call] — CTA as sticker, torn, crooked, intentionally undesigned. That's the design.

Rule: every polished instinct is wrong here. When in doubt, make it rougher.
Anti-rule: this is still legible. Chaos has intention. DIY does not mean unreadable.
```

**Sensory anchors:** Sharpie smell, sticker residue, staple gun, xerox warmth, band poster on telephone pole

---

### Opulent / Luxury

Excess as language. Weight communicates worth. Gold does not suggest value — it announces it.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Heavy gold gradient | `linear-gradient(135deg, #B8860B, #FFD700, #DAA520, #B8860B)` — not flat gold, layered metallic | Headers, borders, accents |
| Velvet texture | Deep `background` with subtle depth via `box-shadow: inset`, `linear-gradient` — surface has weight | Section backgrounds |
| Gemstone accents | Rich jewel tones alongside gold: sapphire (#0F52BA), emerald (#50C878), ruby (#9B111E) | Accent elements, bullets |
| Chandelier particle | Sparkle particles that fall slowly and glint — `opacity: 0 → 1 → 0` with scale pulse | Hero, CTA backgrounds |
| Wax seal geometry | Circular stamp motifs as dividers and decorators — SVG with radial inner design | Section markers, logo area |
| Weight typography | Heavy serif headings with extreme letter-spacing (`tracking: 0.15em`) — each letter has mass | All headings |
| Exclusive whitespace | Not zen emptiness — space as VIP exclusion. Only the chosen elements exist. | All sections |

**Color schema:**
```css
/* Dark Opulence */
--opulent-bg: 30 15% 5%;            /* velvet black */
--opulent-fg: 42 30% 85%;           /* aged ivory */
--opulent-gold: 42 80% 55%;         /* estate gold */
--opulent-gold-bright: 45 100% 65%; /* chandelier highlight */
--opulent-sapphire: 225 70% 35%;    /* deep jewel */
--opulent-velvet: 270 40% 15%;      /* deep purple-black */

/* Cream Opulence */
--opulent-light-bg: 40 30% 95%;     /* heavy cream */
--opulent-light-fg: 30 20% 12%;     /* ink on vellum */
--opulent-light-gold: 38 70% 40%;   /* burnished, not bright */
```

**Font pairings that fit:**
- **Estate auction:** Cormorant Garamond (300, wide-tracked) + Libre Baskerville (body) — aged wealth
- **Haute couture:** Bodoni Moda (headings) + Lato (300, body) — fashion house seriousness
- **Black card:** Playfair Display (700) + EB Garamond (body) — private banker weight

**NOT a locked theme.** Heavy gold gradient works as border-only on any premium pricing section. Chandelier particles work on any dark hero needing "event" quality. Weight typography works on any brand positioning for premium tier.

**Architectural short-schema:**
```
OPULENT PAGE FLOW:
  [The Entrance] — hero: pure dark, single gold line reveals, chandelier sparkles descend
    ↓ weight typography resolves slowly — each word matters
  [The Gallery] — content displayed like museum objects — spaced, lit from above
    ↓ velvet backgrounds on feature sections
  [The Collection] — features as curated objects with gold borders, gemstone accents
    ↓ no crowding. One thing at a time.
  [The Private Room] — CTA. Gold gradient on button. Wax seal decoration. Exclusive weight.

Rule: scarcity is designed in. Never suggest abundance — suggest curation.
Sound analogy: a clock ticking in a quiet room. Everything takes its time.
```

**Sensory anchors:** heavy door, leather smell, crystal weight in hand, low lighting, name on guest list

---

### Nostalgic / Vintage

The warmth that lives inside old photographs. Not the past itself — the feeling of finding the past unexpectedly.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Sepia shift | `filter: sepia(30-60%) saturate(80%)` — color photographs become memory | All images, hero backgrounds |
| Rounded photograph | `border-radius: 4px` + heavy vignette `box-shadow: inset 0 0 60px rgba(0,0,0,0.4)` — photo print edge | Image containers |
| Film scratch | SVG `feTurbulence` + vertical line overlay at 1-2px, random placement — old projector | Full-screen overlays |
| Vintage paper | Warm `background: hsl(40, 25%, 88%)` with very subtle grain — aged document | Section backgrounds |
| Typewriter reveal | `font-family: Courier Prime`, character-by-character with `caret` cursor — letter being typed | Key callouts, hero sub |
| Vignette frame | `box-shadow: inset 0 0 120px rgba(brown, 0.4)` on page — photo album edge | Page/section wrapper |
| Worn-off detail | `opacity: 0.7-0.85` on non-primary elements — things fade with time | Secondary content |

**Color schema:**
```css
/* Kodachrome Memory */
--vintage-bg: 38 25% 90%;           /* warm cream stock */
--vintage-fg: 25 20% 20%;           /* sepia ink */
--vintage-accent: 15 60% 50%;       /* warm rust orange */
--vintage-secondary: 40 30% 65%;    /* faded tan */
--vintage-grain: 35 15% 50% / 0.05; /* dust on lens */

/* Night Polaroid */
--vintage-night-bg: 25 15% 10%;     /* old dark room */
--vintage-night-fg: 38 20% 80%;     /* lamplight text */
--vintage-night-accent: 30 70% 55%; /* warm amber lamp */
```

**Font pairings that fit:**
- **Analog warmth:** Fraunces (italic, headings) + Lora (body) — letter from the past
- **Typewriter archive:** Courier Prime (headings) + Libre Baskerville (body) — filed away
- **Photo album:** Playfair Display (italic) + Source Serif 4 (light) — captioned memories

**NOT a locked theme.** Sepia filter works as hover state on any gallery. Vignette frame works on any full-bleed hero that needs contained, intimate feeling. Rounded photograph style works on any testimonial with author photo.

**Architectural short-schema:**
```
NOSTALGIC PAGE FLOW:
  [The Album] — hero opens like a photo album page, vignette frame, sepia shift
    ↓ typewriter reveals the tagline
  [Old Letters] — content reads like correspondence — warm paper, ink typography
    ↓ worn-off detail on secondary elements (faded)
  [The Archive] — feature section as photograph collection, film scratch overlay
    ↓ each card is a found photograph with rounded edges
  [The Last Page] — CTA. Single image. Single line. Warm, not urgent.

Rule: urgency is the enemy of nostalgia. Slow everything down. Let them linger.
```

**Sensory anchors:** photo album smell, yellowed paper, handwriting you recognize, old song on radio

---

## Combinability Notes

These mood themes layer over any other design category:
- **Dreamlike + any nature theme** = magical realism
- **Noir + any urban theme** = neo noir cityscape
- **Sacred + any luxury theme** = high ceremony brand
- **Melancholic Rain + any vintage theme** = faded photograph sadness
- **Euphoric + any carnival theme** = peak festival energy
- **Haunted + any industrial theme** = abandoned factory dread
- **Zen + any material theme** = mindful tactile space
- **Rebellious + any era theme** = punk history
- **Opulent + any cinema theme** = film noir luxury or golden age Hollywood
- **Nostalgic + any nature theme** = pastoral memory
