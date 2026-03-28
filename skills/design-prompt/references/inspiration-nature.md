# Nature & Environment Inspiration Themes

Atmospheric ingredient palettes for translating real-world environments into web design CSS. Each theme is a loose collection of composable techniques — not locked templates.

---

### Underwater / Deep Ocean

The page exists below the surface. Pressure builds as you scroll deeper. Light bends, colors shift from warm shallows to absolute black.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Caustic light ceiling | Animated SVG/CSS grid of shifting bright patches at page top — `radial-gradient` clusters that slowly drift and merge, simulating sunlight refracting through moving water | Hero sections, any top-of-page treatment |
| Depth darkness gradient | Full-viewport background that transitions from `hsl(200 60% 15%)` → `hsl(220 80% 4%)` as scroll depth increases — driven by CSS `--scroll-y` custom property | Any multi-section dark page |
| Bioluminescence pulse | Small glowing points (blue-cyan, 2-8px) scattered on dark backgrounds, each pulsing on an independent timing offset — `box-shadow` glow with `animation: pulse 3-8s ease-in-out infinite` | Dark sections, calls to action |
| Bubble physics | SVG circles that rise from bottom with variable speed, slight lateral drift via `translate` keyframes, opacity fades before reaching surface | Backgrounds, loading states |
| Kelp sway | Tall thin SVG paths anchored at base, swaying via `rotate` origin at bottom — vary timing offset per "strand" for organic feel | Page edges, section dividers |
| Pressure vignette | Heavy radial `box-shadow inset` in deep blue-black — corners and edges darkest, center slightly lighter — tightens on scroll depth | Section backgrounds |
| Water column parallax | 3-4 layers of floating particles/debris at different scroll speeds: slow deep silt, medium fish silhouettes, fast surface refraction | Any scroll-heavy page |
| Coral glow accent | Warm orange-pink radial glow sources on container backgrounds — heat-map style soft light from specific anchor points | Cards, feature highlights |

**Color schema:**
```css
/* Shallows (top — warm tropical water) */
--ocean-shallow-bg: 195 55% 18%;      /* turquoise dark */
--ocean-shallow-fg: 190 20% 92%;      /* pale water-white */
--ocean-shallow-accent: 175 60% 55%;  /* bright reef cyan */
--ocean-shallow-caustic: 50 100% 90% / 0.08; /* light patch */

/* Mid-depth */
--ocean-mid-bg: 210 65% 10%;          /* dark blue-green */
--ocean-mid-fg: 200 30% 80%;          /* dim blue-white */
--ocean-mid-accent: 185 70% 45%;      /* deep cyan */
--ocean-mid-bio: 170 80% 60% / 0.4;  /* bioluminescent glow */

/* Abyss (bottom) */
--ocean-abyss-bg: 225 85% 4%;         /* near-black blue */
--ocean-abyss-fg: 210 40% 65%;        /* dim blue-grey */
--ocean-abyss-accent: 200 90% 60%;    /* electric blue pulse */
--ocean-abyss-void: 240 60% 2%;       /* pressure black */
```

**Font pairings:**
- **Scientific wonder:** Crimson Pro (italic headings) + IBM Plex Sans (body) — deep-sea research log
- **Ethereal drift:** Cormorant Garamond (light headings) + Nunito (body) — weightless, ancient
- **Expedition log:** Libre Baskerville (headings) + Source Sans 3 (body) — exploration journal

**NOT a locked theme.** Caustic light works on ANY top-hero section for a dynamic ambient feel. Bioluminescence pulses work on dark tech or analytics dashboards. Depth gradients work on any premium dark brand that wants to feel bottomless.

**Architectural short-schema:**
```
OCEAN PAGE FLOW:
  [Surface] — hero, caustic light ceiling, warm shallow colors
    ↓ bubbles begin rising (going down = going deeper)
  [Reef Zone] — coral glow on cards, bioluminescent accents, kelp edges
    ↓ pressure vignette tightens, colors cool and shift blue
  [Mid-Water Column] — parallax debris, deep blue, content illuminated by glow points
    ↓ light from surface disappears, bioluminescence is the only light
  [Abyss] — near-black background, electric blue pulses, sparse glowing content
    ↓ single point of light emerges from darkness
  [CTA] — isolated glow in void, maximum contrast, high drama
```

**Sensory anchors:** Cold pressure on ears. Muffled silence. Weightless suspension. The sound of your own breath. Colors desaturate as depth increases. Every object moves in slow drift.

**Mixes well with:** Dark Premium (glass cards floating in water column), Crystal Cavern (underwater cave systems), Coral Reef (shallow warm zones).

---

### Arctic / Frozen Tundra

Everything is held still by cold. The page is crystallized. Silence has mass. Then, underneath — the faintest aurora breath in the sky.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Frost spread | SVG filter `feTurbulence` + `feDisplacementMap` on container edges — dendritic frost crystal patterns grow outward from corners via `stroke-dashoffset` animation | Cards, images, borders |
| Ice crack reveal | Hairline SVG paths across surfaces with `stroke-dashoffset` animated reveal — cracks spread, then faint blue-white glow bleeds through via `filter: drop-shadow` | Section backgrounds, dividers |
| Breath vapor | Short-lived white blurred gradient ellipses that appear near interactive elements, expand quickly, fade — `scale(1)→scale(3)`, `opacity: 0.3→0` in 1.5s | Hover states, CTAs |
| Snowdrift particles | Fine white specks moving diagonally at low speed, variable opacity (0.2–0.8), NOT uniformly sized — tiny ice crystals, not cartoon snow | Dark sky backgrounds |
| Aurora shimmer | Slow horizontal gradient bands (green-teal-violet) crossing the upper viewport — `background-position` animated over 12-20s, opacity 0.1–0.3 | Hero backgrounds, top sections |
| Permafrost texture | Cracked polygon background created via Voronoi-ish `clip-path` shapes — each cell slightly different lightness, zero color, dead grey-white | Section backgrounds |
| Glass ice refraction | `backdrop-filter: blur(12px) brightness(1.1)` containers with `border: 1px solid hsl(200 40% 80% / 0.3)` — thick clear ice quality | Cards, modals, overlays |
| Cold snap shake | One-frame micro-shake on trigger (`translate(-2px,0)→translate(2px,0)` in 80ms) — ice cracking, temperature snap event | Scroll-enter animations, warnings |

**Color schema:**
```css
/* Clear ice (pristine) */
--arctic-ice-bg: 205 25% 8%;          /* near-black cold */
--arctic-ice-fg: 200 15% 92%;         /* frost white */
--arctic-ice-accent: 195 60% 70%;     /* pale blue */
--arctic-ice-crack: 210 50% 85% / 0.4; /* glow-through-crack */

/* Storm (overcast) */
--arctic-storm-bg: 215 20% 12%;       /* grey-blue dark */
--arctic-storm-fg: 210 10% 75%;       /* dim white */
--arctic-storm-accent: 200 30% 55%;   /* slate blue */

/* Aurora night */
--arctic-aurora-bg: 230 35% 6%;       /* deep indigo-black */
--arctic-aurora-green: 150 80% 55%;   /* aurora green */
--arctic-aurora-violet: 280 70% 60%;  /* aurora violet */
--arctic-aurora-teal: 175 70% 50%;    /* aurora teal */
```

**Font pairings:**
- **Polar expedition:** Space Grotesk (headings) + Inter (body) — clean cold precision
- **Ice age mystery:** Cormorant Garamond (italic titles) + Karla (body) — ancient and crystalline
- **Research station:** IBM Plex Mono (headings) + IBM Plex Sans (body) — scientific isolation

**NOT a locked theme.** Frost spread on card borders works on any winter, premium, or cold-tech brand. Aurora shimmer backgrounds work on any dark hero that needs gentle movement. Ice crack reveals work as dramatic page dividers anywhere.

**Architectural short-schema:**
```
ARCTIC PAGE FLOW:
  [Open Tundra] — hero, vast emptiness, cold palette, aurora hint at top
    ↓ wind particles begin diagonal drift
  [Ice Field] — frost borders on content, permafrost texture, crack patterns
    ↓ cold snap on section enter, crack lines spread
  [Deep Winter] — near-monochrome, glass-ice containers, maximum stillness
    ↓ aurora band brightens overhead
  [Aurora Peak] — color enters only in aurora bands above, dark ground below
    ↓ temperature visually drops to absolute
  [The Void] — single element illuminated against perfect cold black, CTA
```

**Sensory anchors:** Burning cold in the lungs. Sound travels impossibly far. Footsteps crunch. Sky is violet-black at noon. Ice groans under pressure. Nothing moves except the aurora.

**Mixes well with:** Dark Premium (crystalline glass cards), Northern Lights (direct pairing), Deep Ocean (cold monochrome shared palette).

---

### Desert / Sand Dunes

Time moves differently here. The light is permanent gold. Distances lie. The horizon is always at the same height but the dune shapes never repeat.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Heat shimmer | Animated `backdrop-filter: blur(0px→2px→0px)` cycling on background elements, slight vertical `translate` oscillation — distortion visible above hot surfaces | Footer zones, hero lower thirds |
| Sand grain texture | SVG `feTurbulence` noise filter at very high frequency/low octave applied to backgrounds — roughens solid colors into grainy surfaces | Section backgrounds, containers |
| Wind ripple patterns | CSS `repeating-linear-gradient` at shallow angle (5-10deg) with alternating light/dark sand tones, animated `background-position` — dune surface texture scrolling slowly | Section backgrounds |
| Mirage distortion | At specific scroll depths: brief `filter: blur(3px) brightness(1.2)` on lower viewport areas — mirage effect of false water on ground | Hero base, hot-ground sections |
| Oasis reveal | Full-section transition: arid palette → sudden lush teal/green, `clip-path: circle(0→100%)` expanding from a point | Section transitions, CTA areas |
| Dune silhouette horizon | SVG wave paths as section dividers — gentle slope curves, not sharp lines. Layer 2-3 in near/mid/far tones | Any section boundary |
| Golden hour lock | Background `hsl(--sun-angle, 70%, var(--hour-lightness))` — single warm golden tone that never changes, no "night" — this desert is always at 4pm | Page-wide color anchor |
| Sandstorm overlay | Semi-opaque diagonal particle storm (tiny 1px dots at 20% opacity) that sweeps across viewport from right — activates on specific scroll or interaction | Transitions, dramatic moments |

**Color schema:**
```css
/* Dune gold (base) */
--desert-sand-bg: 35 40% 10%;         /* dark warm brown */
--desert-sand-fg: 38 30% 88%;         /* bleached bone white */
--desert-sand-accent: 38 70% 55%;     /* warm amber */
--desert-sand-mid: 32 50% 35%;        /* medium dune tone */

/* Blaze noon */
--desert-noon-bg: 40 50% 8%;          /* scorched earth */
--desert-noon-fg: 45 60% 92%;         /* sun-bleached white */
--desert-noon-accent: 30 90% 60%;     /* heat orange */
--desert-noon-sky: 210 40% 70%;       /* bleached blue sky */

/* Oasis */
--desert-oasis-bg: 150 30% 12%;       /* deep shade green */
--desert-oasis-fg: 80 20% 88%;        /* pale green-white */
--desert-oasis-water: 185 60% 45%;    /* still pool teal */
--desert-oasis-palm: 100 40% 25%;     /* deep frond green */
```

**Font pairings:**
- **Ancient caravan:** Playfair Display (headings) + Lato (body) — timeless, sun-weathered
- **Dune epic:** Cinzel (headings) + Crimson Pro (body) — monumental, carved-stone
- **Field research:** Libre Baskerville (headings) + Source Sans 3 (body) — explorer-surveyor

**NOT a locked theme.** Heat shimmer works on any dark site footer or hero base. Sand grain texture replaces flat backgrounds on any warm, earthy brand. Oasis reveal is a powerful CTA transition technique usable in any context.

**Architectural short-schema:**
```
DESERT PAGE FLOW:
  [Dune Crest] — hero, vast sky, golden horizon, heat shimmer below
    ↓ wind ripples animate across surface
  [Mid-Desert] — sand grain textures, dune silhouette dividers, full golden palette
    ↓ sandstorm sweeps through (section transition)
  [Stone Canyon] — harder surfaces, shadow relief, rock texture overlays
    ↓ mirage flickers on ground-level elements
  [Oasis Approach] — color begins shifting, first hint of green and water-teal
    ↓ oasis circle-reveal expansion
  [Oasis] — full lush contrast against desert memory, CTA as water source
```

**Sensory anchors:** Skin tightening from dry heat. Ground radiates back what the sun put in. Wind lifts fine grit. Distances impossible to judge. Gold light makes everything look eternal.

**Mixes well with:** Volcanic/Magma (geological partner), Autumn Foliage (both golden warm tones), Deep Forest (extreme contrast — arid-to-lush journey).

---

### Storm / Lightning

The page is charged. Something is about to happen. Then it does. Then the tension rebuilds.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Flash reveal | Content hidden behind dark overlay (`opacity: 0.95`) — on scroll trigger: `opacity: 0→0.95→0` (1 frame white flash), content fully revealed | Section entry animations |
| Rain streak overlay | Pseudo-element with `repeating-linear-gradient(170deg, transparent, transparent 2px, rgba(180,200,255,0.07) 2px, transparent 3px)` animating `background-position` downward at 0.3s | Any dark background overlay |
| Lightning branch | SVG polyline paths with `stroke-dashoffset` instant reveal (0ms), glow via `filter: drop-shadow(0 0 8px hsl(220 100% 80%))`, then fade in 400ms — never slow, never gradual | Hero, section backgrounds |
| Thunder shake | `transform: translate(var(--shake-x), var(--shake-y))` on page wrapper, randomized values, 3-5 frames, `animation-timing-function: steps(1)` — brutal not smooth | Post-lightning moments |
| Cloud scroll | Massive blurred dark gradient shapes (`filter: blur(60px)`) as background layers moving at different horizontal speeds — low opacity (0.3-0.5) | Hero backgrounds, any section |
| Pre-storm tension | Desaturated yellow-green tint (`hsl(70 30% 50% / 0.05)` overlay) on sections before a lightning event — the sick light before a storm | Pre-climax sections |
| Static electricity | Small random dot sparks near interactive elements on hover — 4-6 tiny `box-shadow` points that scatter outward in 200ms then disappear | Buttons, links |
| Dark wet ground | Reflective `linear-gradient` at bottom of dark sections — inverted silhouettes at low opacity, simulating wet pavement reflection | Dark section footers |

**Color schema:**
```css
/* Overcast (building) */
--storm-build-bg: 220 20% 7%;         /* storm grey-black */
--storm-build-fg: 215 15% 80%;        /* dim grey-white */
--storm-build-accent: 210 25% 50%;    /* steel blue */
--storm-build-sick: 70 25% 55% / 0.08; /* pre-storm yellow-green */

/* Strike */
--storm-strike-flash: 210 100% 95%;   /* lightning white-blue */
--storm-strike-core: 220 100% 80%;    /* electric blue center */
--storm-strike-glow: 200 80% 60% / 0.5; /* discharge glow */

/* Aftermath */
--storm-after-bg: 215 25% 9%;         /* wet dark */
--storm-after-fg: 210 20% 75%;        /* rain-washed grey */
--storm-after-accent: 185 40% 55%;    /* clearing sky */
--storm-after-puddle: 210 50% 40% / 0.3; /* wet reflection */
```

**Font pairings:**
- **Emergency broadcast:** Space Mono (headings) + Barlow Condensed (body) — urgent, dense
- **Weather system:** DM Sans (700 headings) + DM Sans (400 body) — clean meteorological
- **Storm chaser:** Oswald (headings) + Source Sans 3 (body) — documentary intensity

**NOT a locked theme.** Flash reveals are powerful entry animations for ANY content — not just storm sites. Rain streak overlays add cinematic texture to any dark hero. Thunder shake is a micro-interaction for critical alerts or errors on any product.

**Architectural short-schema:**
```
STORM PAGE FLOW:
  [Clear Before] — slightly oppressive calm, dark sky, pre-storm tint
    ↓ wind picks up (cloud layers begin moving), rain streaks appear faintly
  [Storm Approach] — cloud scroll accelerates, static sparks on interactive elements
    ↓ tension builds — darker, more desaturated, rain thickens
  [Strike] — lightning flash reveal on key content section, thunder shake
    ↓ immediate dark aftermath, rain at peak intensity
  [Heavy Rain] — maximum rain streaks, all elements revealed, wet-ground reflections
    ↓ rain slows, streaks thin
  [Clearing] — sky lightens, fresh blue-grey, wet earth tones, CTA in clean air
```

**Sensory anchors:** Hair standing up. The smell of ozone. Sky turns sickly yellow-green. Sound disappears before the crack. Rain on concrete. Everything is louder and cleaner after.

**Mixes well with:** Deep Ocean (shared dark electric palette), Volcanic/Magma (catastrophic weather pairing), Arctic (ice storm variant).

---

### Volcanic / Magma

The earth is not solid here. Surfaces crack, glow from beneath. Gravity feels heavier. The color range is obsidian to white-hot — nothing in between is interesting.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Lava crack surfaces | SVG network of irregular paths over dark backgrounds — animated `stroke-dashoffset` slow reveal, paths glow orange-red via `filter: drop-shadow`, cracks widen over time | Section backgrounds, card borders |
| Molten flow | Slow-moving `linear-gradient(180deg, transparent, hsl(20 100% 45%), hsl(35 100% 55%))` gradient strips that animate downward — lava rivers between content sections | Section dividers |
| Heat glow from below | `box-shadow: 0 20px 60px hsl(20 100% 45% / 0.4)` on containers — light source is below, not above — reverses normal card lighting | All cards, all containers |
| Basalt column layout | CSS Grid columns with vertical SVG hexagonal texture overlays — rigid geometric dark columns with lava-light edges | Multi-column sections |
| Obsidian glass | `background: hsl(0 0% 6%)` + `border: 1px solid hsl(15 20% 20%)` + sharp `clip-path` — volcanic glass quality, edges cut perfect and cold | Cards, modals, premium containers |
| Eruption burst | Radial explosion of particles from a point — fast outward `translate` from origin, scale from 0.5→1→0, ember colors, staggered timing | Interaction feedback, section entry |
| Magma skin | CSS `background: conic-gradient(from var(--rotation), hsl(0 70% 15%), hsl(20 90% 35%), hsl(35 100% 50%), hsl(20 90% 35%), hsl(0 70% 15%))` animated `--rotation` — rotating magma surface | Hero backgrounds, section fills |
| Sulfur sky | Background gradient `hsl(45 30% 8%)→hsl(15 20% 5%)` with slight yellow tint at horizon — volcanic atmosphere | Upper page backgrounds |

**Color schema:**
```css
/* Obsidian (cold volcanic) */
--magma-obsidian-bg: 0 5% 5%;         /* volcanic glass black */
--magma-obsidian-fg: 20 15% 80%;      /* ash grey-white */
--magma-obsidian-accent: 10 80% 40%;  /* deep magma red */
--magma-obsidian-edge: 15 30% 20%;    /* cooled lava edge */

/* Active (flowing) */
--magma-active-bg: 10 15% 7%;         /* hot dark */
--magma-active-fg: 40 50% 88%;        /* ember-lit white */
--magma-active-flow: 25 100% 50%;     /* lava orange */
--magma-active-core: 45 100% 65%;     /* white-hot center */
--magma-active-glow: 20 90% 45% / 0.35;

/* Eruption */
--magma-erupt-bg: 5 20% 4%;           /* near-black red */
--magma-erupt-accent: 0 100% 50%;     /* pure volcanic red */
--magma-erupt-burst: 50 100% 70%;     /* explosion flash */
--magma-erupt-ash: 25 10% 40%;        /* ash cloud */
```

**Font pairings:**
- **Tectonic force:** Space Grotesk (800) + Barlow (300) — geological mass
- **Ancient power:** Cinzel (headings) + Cormorant Garamond (body) — primordial civilization
- **Industrial heat:** Bebas Neue (headings) + IBM Plex Sans (body) — forge and factory

**NOT a locked theme.** Heat glow from below flips all card lighting — powerful on ANY dark premium site. Lava crack animations are dramatic dividers for any intense brand. Obsidian glass is a container style applicable across dark UI patterns.

**Architectural short-schema:**
```
VOLCANIC PAGE FLOW:
  [Sulfur Sky] — dark amber atmosphere, distant glow on horizon
    ↓ crack lines begin spreading from page edges
  [Lava Field] — crack network visible, molten flow between sections, heat glow on cards
    ↓ eruption burst on key content entry
  [Caldera] — maximum heat, white-hot elements, rotating magma skin background
    ↓ basalt columns rise as layout, obsidian glass containers
  [Cooling] — colors shift from orange-red to obsidian black-grey
    ↓ ash fall begins, cracks cool and go dark
  [Obsidian Plain] — cold geological black, CTA as single surviving light source
```

**Sensory anchors:** Heat through boot soles. Sulfur in the throat. The ground moves without warning. Sound is dull and heavy — absorbs into rock. Sky is orange at noon.

**Mixes well with:** Storm/Lightning (geological apocalypse), On Fire (direct combination — same heat family), Desert (shared arid palette, different intensity).

---

### Coral Reef

Everything alive competes for space. Color is not decoration here — it is survival signal. The water is warm, the light playful, and nothing holds still.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Anemone sway | Tall thin elements (cards, CTAs) with `transform-origin: bottom center` and gentle `rotate(-3deg→3deg)` on a 4-6s sine wave — anchored base, drifting top | Card components, CTA buttons |
| School of fish | 20-40 small SVG fish shapes moving in formation — `translate` along curved SVG path, formation bends around obstacles, scatter on click | Background animation layer |
| Sun-dappled surfaces | `background-image` of repeating animated ellipse gradients (bright spots on container backgrounds) at slow drift — same caustic technique as Ocean but warm and colorful | Shallow section backgrounds |
| Reef texture overlay | SVG or raster coral texture at `mix-blend-mode: overlay`, 15-25% opacity — roughens smooth backgrounds into organic surfaces | Section backgrounds, cards |
| Vibrant accent flood | Multiple competing accent colors simultaneously — 3-4 hues at once (coral pink, electric yellow, reef blue, sea-green) rather than monochromatic | Cards, buttons, tags |
| Bubble trail | Clusters of circles rising from interactive elements on hover — reef fish and coral constantly release microbubbles | Button interactions |
| Stripe fish dividers | Horizontal striped gradient rules (`repeating-linear-gradient` with thin color stripes) as section boundaries — tropical fish pattern reference | Section dividers |
| Coral polyp reveal | Tiny radial elements that expand from points on hover/scroll — polyp "blooming" interaction, scale(0→1) with ease-out | Micro-interactions, list items |

**Color schema:**
```css
/* Shallow tropical */
--reef-shallow-bg: 185 45% 14%;       /* warm deep teal */
--reef-shallow-fg: 190 15% 92%;       /* water-white */
--reef-coral: 5 80% 65%;              /* living coral pink */
--reef-yellow: 50 100% 60%;           /* butterflyfish yellow */
--reef-blue: 200 80% 60%;             /* electric reef blue */
--reef-green: 150 60% 45%;            /* sea grass green */

/* Vibrant noon */
--reef-noon-bg: 190 55% 10%;          /* noon blue-teal */
--reef-noon-accent: 15 90% 60%;       /* hot coral */
--reef-noon-flash: 55 100% 65%;       /* neon yellow flash */
--reef-noon-deep: 220 70% 30%;        /* shadow blue */

/* Dusk reef */
--reef-dusk-bg: 200 40% 8%;           /* twilight water */
--reef-dusk-biolum: 170 90% 60%;      /* polyp glow */
--reef-dusk-coral: 350 60% 55%;       /* dim coral */
```

**Font pairings:**
- **Tropical editorial:** Nunito (rounded headings) + Nunito Sans (body) — playful organic
- **Marine biology:** Libre Baskerville (headings) + Source Sans 3 (body) — scientific warmth
- **Dive magazine:** Raleway (headings) + Lato (body) — clean adventurous

**NOT a locked theme.** Anemone sway is a subtle animation for ANY card layout. Vibrant accent flood works as a multicolor tag/badge system on any product. Sun-dappled surfaces add life to any light-background section.

**Architectural short-schema:**
```
REEF PAGE FLOW:
  [Surface Entry] — warm light, high caustics, first reef shapes visible below
    ↓ school-of-fish animation crosses viewport
  [Reef Crest] — maximum color, anemone cards, sun-dappled backgrounds
    ↓ coral polyp reveals on scroll, vibrant accents
  [Reef Wall] — color gradient deepens, columns of life, fish trails
    ↓ light dims but bioluminescence picks up
  [Sandy Bottom] — quieter, open space, occasional discovery
    ↓ single coral outcrop glows in dim water
  [Hidden Grotto CTA] — warm glow from within, invitation to explore
```

**Sensory anchors:** Water temperature exactly body heat. Sound is muffled but rich — clicking, humming, movement. Colors are almost too saturated to believe. Something always moving in peripheral vision.

**Mixes well with:** Underwater/Deep Ocean (depth extension), Jungle/Tropical (shared saturation palette), Tide Pool (same coastal system, different zone).

---

### Cave / Crystal Cavern

The outside world does not exist here. The scale is impossible to judge. Then a beam of light strikes a crystal and the darkness explodes into spectrum.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Crystal refraction | `filter: hue-rotate(var(--refract-angle))` animation on specific elements — as "light" moves, elements cycle through rainbow spectrum in sequence | Glass containers, feature highlights |
| Stalactite drip | Single pixel-wide vertical trails that descend from container tops, pause, then a droplet (`border-radius: 50%`) falls and ripples on "floor" | Section tops, card edges |
| Torch-lit reveal | `radial-gradient(circle at var(--torch-x) var(--torch-y), transparent 150px, black 400px)` that follows cursor — content only visible within torch radius | Dark discovery sections |
| Geode burst | Circular section reveals: dark outer ring → thin crystal band (rainbow gradient) → bright mineral core. Expands from point on scroll enter | Section transitions, hero reveals |
| Cave depth haze | Background layers at increasing blur: far wall (blur 20px), mid formations (blur 8px), near surfaces (sharp) — depth via progressive blur | Multi-layer backgrounds |
| Mineral texture | `background-image: repeating-conic-gradient(...)` with sharp angular facets in near-monochrome dark — simulates mineral surface crystallization | Card backgrounds |
| Echo space | Wide letter-spacing on headings (`0.15-0.3em`) + long `text-shadow` trails — type feels like it echoes in cathedral space | Headings, labels |
| Hidden inscription | Text revealed by `clip-path: inset(0 100% 0 0 → inset(0 0% 0 0))` — ancient carved text appearing as "torch" finds it | Section text reveals |

**Color schema:**
```css
/* Stone dark */
--cave-stone-bg: 210 10% 6%;          /* wet limestone black */
--cave-stone-fg: 200 8% 75%;          /* dim grey-white */
--cave-stone-accent: 200 30% 40%;     /* cold mineral grey-blue */

/* Crystal */
--cave-crystal-1: 280 70% 65%;        /* amethyst violet */
--cave-crystal-2: 185 80% 60%;        /* aquamarine */
--cave-crystal-3: 45 90% 65%;         /* citrine gold */
--cave-crystal-4: 0 70% 60%;          /* garnet red */
--cave-crystal-glow: 200 80% 70% / 0.3; /* refracted light */

/* Deep chamber */
--cave-deep-bg: 220 15% 4%;           /* absolute cave dark */
--cave-deep-torch: 35 90% 55% / 0.6; /* torch warm glow */
--cave-deep-discovery: 195 100% 70%;  /* found-it moment */
```

**Font pairings:**
- **Ancient chamber:** Cormorant Garamond (italic) + Libre Baskerville (body) — inscribed, discovered
- **Crystal science:** Crimson Pro (headings) + IBM Plex Sans (body) — natural history museum
- **Spelunker journal:** Playfair Display (headings) + Source Sans 3 (body) — explorer narrative

**NOT a locked theme.** Torch-lit reveals are powerful interactive dark-section techniques for ANY site. Geode burst transitions are dramatic reveal animations usable independently. Echo spacing works on any wide, dramatic heading style.

**Architectural short-schema:**
```
CAVE PAGE FLOW:
  [Cave Entrance] — natural light fading, torch appears, content at perimeter of glow
    ↓ cave depth haze establishes layers
  [Inner Passages] — torch-lit navigation, stalactite drips, mineral textures
    ↓ deeper — torch radius narrows, more discovery required
  [Crystal Chamber] — geode burst reveal, refraction spectrum floods viewport
    ↓ each crystal formation = a content section
  [Hidden Altar / Deep Discovery] — most important content at greatest depth
    ↓ full crystal light, all darkness resolved
  [Emergence CTA] — crystal glow becomes exit light, content surface reveal
```

**Sensory anchors:** Perfect 55°F regardless of season. Drip-echo with long reverb. Absolute darkness at arm's length. The smell of ancient water and mineral dust. Finding something no sunlight has ever touched.

**Mixes well with:** Arctic (frozen cave — ice crystal variant), Volcanic/Magma (lava tube cave system), Underground as counterpart to any surface environment.

---

### Jungle / Tropical

The page is photosynthesizing. Color is violence here — every hue fighting for light. Nothing is straight. Everything drips.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Vine growth | SVG path with `stroke-dashoffset` animated reveal — vine "grows" along container edges or between sections, leaves branch off via staggered sub-paths | Section frames, navigation borders |
| Tropical downpour | Dense rain: `repeating-linear-gradient` at 165deg, thin streaks at 1px wide, 8% opacity, fast animation (0.15s loop) — heavier than storm rain, vertical | Dark section backgrounds |
| Canopy density | Hero starts in dense foliage (dark green, 80% of viewport blocked by leaf shapes), scroll reveals content through gaps — similar to Forest but tighter, more aggressive | Hero sections |
| Parrot flash | 1-3 bright neon accent colors (`hsl(340 90% 60%)`, `hsl(55 100% 55%)`, `hsl(280 80% 65%)`) that appear briefly on content entry — color flashes against green | Key statistics, highlights |
| Humidity fog | Very slight warm white haze (`rgba(255,255,255,0.03)`) that pulsates slowly — air has visible weight | Background overlay on all sections |
| Frog-call timing | Micro-interactions triggered at 3-7s intervals (not on user action) — small pulse/glow on an element "calls" and another "responds" across the page | Ambient animations |
| Oversaturation | `filter: saturate(1.3)` on image/background sections — colors pushed past realistic to tropical-membrane-vibrant | Images, background textures |
| Muddy ground | Footer/bottom sections with dark brown-red tones, root textures, wet earth — contrast to bright canopy above | Page footers |

**Color schema:**
```css
/* Deep canopy */
--jungle-canopy-bg: 130 35% 6%;       /* near-black green */
--jungle-canopy-fg: 80 15% 85%;       /* pale leaf-filtered light */
--jungle-canopy-leaf: 120 50% 25%;    /* deep saturated green */
--jungle-canopy-shaft: 80 60% 70% / 0.08; /* light through leaves */

/* Bright clearing */
--jungle-clear-bg: 110 30% 10%;       /* rich dark green */
--jungle-clear-fg: 75 25% 90%;        /* dappled white */
--jungle-clear-accent: 140 65% 45%;   /* vivid green */
--jungle-clear-flower: 340 85% 60%;   /* jungle flower flash */

/* Floor */
--jungle-floor-bg: 30 40% 8%;         /* dark wet earth */
--jungle-floor-fg: 45 20% 70%;        /* filtered warm light */
--jungle-floor-root: 25 50% 20%;      /* exposed root brown */
--jungle-floor-fungi: 280 40% 40%;    /* fungi purple accent */
```

**Font pairings:**
- **Colonial expedition:** Playfair Display (headings) + Crimson Pro (body) — journal, discovered
- **Botanical illustration:** Cormorant Garamond (italic) + Lato (body) — scientific exuberance
- **Adventure brand:** Raleway (700) + Open Sans (body) — modern exploration

**NOT a locked theme.** Vine growth borders work on any organic brand. Tropical downpour adds cinematic texture to dark sections. Parrot flash accent technique — brief explosive color on entry — works on any brand with a bold accent color.

**Architectural short-schema:**
```
JUNGLE PAGE FLOW:
  [Canopy Entry] — dense foliage, dark green, content barely visible through leaf gaps
    ↓ vine growth along section edges, downpour begins
  [Interior Forest] — humidity visible, parrot flashes on key content, oversaturated colors
    ↓ canopy thins slightly, more light, more color
  [River Clearing] — open water, full sky visible, relief from density
    ↓ brief calm before density returns
  [Ancient Site] — foliage reclaiming stone, vine growth on content containers
    ↓ floor level — roots, mud, fungi, ground life
  [Floor Discovery CTA] — quiet after the noise, single illuminated find
```

**Sensory anchors:** Sweat-damp immediately. Sound is overwhelming — layers of calls, drips, rustles. Green so saturated it hurts. Can't see 10 meters. Ground moves. Something watches.

**Mixes well with:** Coral Reef (shared saturation ethic), Rainforest Mist (same biome, misty variant), Deep Forest (temperate cousin — shared techniques, different palette).

---

### Mountain Peak / Alpine

The page earns its height. Every section is an elevation gain. At the top: impossible clarity and nothing between you and the edge of the atmosphere.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Cloud-passing transition | White-grey gradient overlay that sweeps diagonally across viewport between sections — 2-3 second cloud-pass, content briefly obscured then revealed sharper | Section transitions |
| Elevation color shift | CSS `--elevation` custom property driving `hsl()` transitions: lush green (0%) → rocky grey-brown (40%) → white snow (70%) → pure sky blue (100%) as scroll progresses | Background, border, text color systems |
| Vertigo scroll | On specific sections: content container has slight `perspective(800px) rotateX(2deg)` — looking down from height | Height-reveal sections |
| Thin air clarity | `filter: contrast(1.1) brightness(1.05)` on entire high-elevation sections — air is cleaner, everything slightly more defined | Top-of-page hero, peak sections |
| Wind push | Horizontal particle streams at very low opacity — not vertical rain, horizontal ice crystals pushing from one side — speed accelerates with elevation | High sections, exposed ridges |
| Stone texture gradient | `background` alternating between organic (green-grey) and geometric (angular hexagon clip-paths) — biological life giving way to pure geology | Mid-elevation sections |
| Summit horizon reveal | At highest section: `clip-path: polygon(0 50%, 100% 50%, 100% 100%, 0 100%)` expands to full viewport, revealing panoramic sky | Peak section |
| Alpine flora accent | Tiny vivid wildflower colors (`hsl(340 80% 65%)` edelweiss white-pink, `hsl(260 70% 60%)` gentian violet) against grey stone — color is precious at altitude | Accent elements, icons |

**Color schema:**
```css
/* Treeline base */
--alpine-base-bg: 160 20% 8%;         /* dark evergreen */
--alpine-base-fg: 80 15% 85%;         /* grey-green light */
--alpine-base-accent: 140 35% 40%;    /* conifer green */

/* Rocky zone */
--alpine-rock-bg: 25 10% 10%;         /* dark stone */
--alpine-rock-fg: 30 8% 80%;          /* grey sky light */
--alpine-rock-accent: 200 20% 55%;    /* cold sky blue */
--alpine-rock-lichen: 80 40% 35%;     /* lichen olive */

/* Summit */
--alpine-summit-bg: 210 30% 12%;      /* high sky blue-black */
--alpine-summit-fg: 200 20% 95%;      /* brilliant thin air white */
--alpine-summit-sky: 205 50% 65%;     /* true altitude blue */
--alpine-summit-snow: 210 30% 95%;    /* pure snow */
--alpine-summit-horizon: 190 40% 80%; /* infinite horizon */
```

**Font pairings:**
- **Alpine expedition:** Space Grotesk (headings) + Inter (body) — clean altitude precision
- **Summit journal:** Libre Baskerville (headings) + Source Sans 3 (body) — earned narrative
- **Geographic survey:** IBM Plex Serif (headings) + IBM Plex Sans (body) — measured, precise

**NOT a locked theme.** Elevation color shift is a powerful scroll-progress color system for ANY multi-section page. Cloud-passing transitions work between ANY major sections. Thin air clarity (`filter: contrast + brightness`) enhances any hero section.

**Architectural short-schema:**
```
ALPINE PAGE FLOW:
  [Valley] — lush, warm, dense starting point — green palette
    ↓ treeline transition, vegetation thins
  [Treeline] — last dense section, views begin opening, alpine flora accents
    ↓ stone begins replacing soil, wind push particles
  [Rocky Approach] — exposed stone, cold blue palette, vertical scale visible
    ↓ cloud-pass transition obscures then reveals higher section
  [Ridge Walk] — panoramic, both valleys visible, thin air clarity
    ↓ vertigo scroll as users realize the drop on both sides
  [Summit] — full sky, horizon reveal, nothing above — CTA at world's edge
```

**Sensory anchors:** Each breath slightly insufficient. Sun burns through thin air. Wind from nowhere with no warning. The silence is aggressive. Scale is only visible from height, not within it.

**Mixes well with:** Arctic/Frozen Tundra (winter alpine), Storm/Lightning (alpine storm), Desert (high altitude desert plateau).

---

### Autumn / Fall Foliage

Decay made beautiful. The page is in a state of transformation — nothing is at peak, everything is at its most vivid right before it falls. There is nostalgia in every pixel.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Leaf color scroll | Background hue transitions via `--scroll-progress`: `hsl(120 40% 20%)` (green) → `hsl(35 70% 30%)` (amber) → `hsl(15 80% 25%)` (rust) → `hsl(8 60% 20%)` (deep burgundy) | Full-page background system |
| Falling leaves | SVG leaf shapes (4-6 varieties — oak, maple, birch) tumbling with `rotate` + `translate` keyframes — NOT circles, NOT symmetric — must tumble with asymmetric timing | Atmospheric background layer |
| Golden shaft light | Diagonal `linear-gradient` at 30-40deg, warm gold (`hsl(40 80% 60% / 0.08-0.12)`), shifts position slowly — afternoon sun through bare branches | Dark section backgrounds |
| Carpet of leaves | Footer zone: packed leaf shapes as footer background via SVG pattern, warm rust/amber/brown tones — content sits ON the leaf pile | Footer sections |
| Bark texture | `background` with SVG noise filter producing vertical grain at low contrast — tree bark quality for container backgrounds | Cards, sidebar containers |
| Cold morning mist | Thin horizontal white bands at 3% opacity moving slowly from one side — morning mist visible between trees | Background ambient layer |
| Branch silhouette | Bare black SVG branch network along page edges — calligraphic line quality, a few hanging leaves remaining | Page frame, section edges |
| Harvest warmth | Global `filter: sepia(0.15) warmth-simulate` — not quite sepia, just aging the palette toward amber | Image treatment, full-page filter |

**Color schema:**
```css
/* Early autumn (still green) */
--autumn-early-bg: 115 20% 8%;        /* dark green-brown */
--autumn-early-fg: 50 20% 85%;        /* warm light */
--autumn-early-accent: 35 60% 50%;    /* first gold */

/* Peak color */
--autumn-peak-bg: 20 25% 8%;          /* warm dark earth */
--autumn-peak-fg: 40 30% 88%;         /* amber-lit white */
--autumn-peak-amber: 38 80% 55%;      /* full amber */
--autumn-peak-rust: 15 75% 45%;       /* rust red */
--autumn-peak-burgundy: 350 50% 30%;  /* deep burgundy */

/* Late autumn */
--autumn-late-bg: 25 15% 7%;          /* near-bare dark */
--autumn-late-fg: 30 10% 75%;         /* grey morning light */
--autumn-late-accent: 20 40% 40%;     /* subdued rust */
--autumn-late-bark: 25 20% 15%;       /* bark grey-brown */
```

**Font pairings:**
- **Harvest editorial:** Playfair Display (headings) + Lato (body) — nostalgic warmth
- **October journal:** Cormorant Garamond (headings) + Crimson Pro (body) — literary autumn
- **Seasonal brand:** Merriweather (headings) + Source Sans 3 (body) — approachable tradition

**NOT a locked theme.** Leaf color scroll is a powerful scroll-progress color transition for ANY warm brand. Falling leaf particles — done with actual asymmetric shapes — work on seasonal campaigns. Bark texture containers work on any organic, natural, or artisan brand.

**Architectural short-schema:**
```
AUTUMN PAGE FLOW:
  [Late Summer] — still mostly green, first hints of amber at edges, morning mist
    ↓ palette shifts, branch silhouettes appear at margins
  [Peak Color] — full amber-rust-burgundy, golden shaft light, leaf particles dense
    ↓ leaves thicken in fall, ground coverage begins
  [Wind Day] — leaf particles accelerate, branch silhouettes sway, mist dissipates
    ↓ palette cools toward late autumn grey-brown
  [Bare Trees] — bark textures, sparse leaves, cold morning light
    ↓ leaf carpet fills footer zone
  [Harvest End] — warm single light source, content as preserved thing, CTA
```

**Sensory anchors:** Wood smoke in cold air. Crunch underfoot. Slant of afternoon light that makes everything gold. The melancholy of abundance ending. Sweater and cider temperature. Silence has a different quality than summer.

**Mixes well with:** Deep Forest (seasonal variant of the same forest), Cherry Blossom (seasonal partners — spring counterpart), Rainforest Mist (if cold morning mist is emphasized).

---

### Cherry Blossom / Spring

Everything is temporary. The page knows it. Petals fall because they bloom — the falling is the point, not the failure. Pale pink on pale white on pale grey sky.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Petal drift | SVG petal shapes (irregular 5-point, not circles or ellipses) drifting diagonally — slow, variable speed, gentle wobble rotation. Each petal unique size (8-20px). Wind shifts direction slowly | Background atmosphere |
| Branch silhouette frame | Dark/grey SVG branch structure along top and one side of hero — petals attached at tips, a few hanging mid-frame | Hero section frame |
| Soft focus bloom | `filter: blur(0.5px) brightness(1.03)` on backgrounds behind text — very slight glow, like shooting through net fabric. NOT aggressive blur | Background images, section fills |
| Pastel gradient wash | Background gradients only in `hsl(320-350 20-40% 90-96%)` range — barely-there pinks, never saturated. Gradients transition in 20% increments | Section backgrounds |
| Wind gust event | On trigger: petal density doubles for 3s, lateral drift speed increases 3x, then subsides. Feels like a gust sweeping petals | Scroll triggers, interaction moments |
| Dew drop | Tiny perfect circles (3-5px) on container edges with inner glow — morning dew on surface. Appear in clusters, random spacing | Card edges, container outlines |
| Pale sky gradation | Upper hero background: `hsl(200 15% 88%)` → `hsl(200 20% 82%)` — overcast spring sky, no drama | Hero background |
| Bloom timing | Staggered `scale(0)→scale(1)` on content elements with `cubic-bezier(0.34, 1.56, 0.64, 1)` spring easing — elements "bloom" into existence | All content entry animations |

**Color schema:**
```css
/* Pale blossom */
--sakura-pale-bg: 340 15% 97%;        /* near-white with pink */
--sakura-pale-fg: 220 15% 25%;        /* soft dark text */
--sakura-pale-petal: 340 35% 85%;     /* petal pink */
--sakura-pale-branch: 25 20% 30%;     /* grey-brown branch */

/* Full bloom */
--sakura-bloom-bg: 345 20% 95%;       /* pink-white */
--sakura-bloom-fg: 240 15% 20%;       /* deep text */
--sakura-bloom-accent: 340 50% 70%;   /* blush pink */
--sakura-bloom-sky: 200 20% 88%;      /* overcast spring sky */

/* Twilight blossom */
--sakura-twilight-bg: 280 15% 12%;    /* dark violet dusk */
--sakura-twilight-petal: 340 40% 80%; /* glowing petal */
--sakura-twilight-accent: 320 50% 70%;/* pink-violet */
--sakura-twilight-star: 220 30% 70%;  /* first stars */
```

**Font pairings:**
- **Japanese spring:** Noto Serif JP (headings) + Noto Sans JP (body) — authentic, restrained
- **Soft editorial:** Cormorant Garamond (light italic) + Raleway (300 body) — delicate precision
- **Modern minimal:** DM Serif Display (headings) + DM Sans (body) — clean spring freshness

**NOT a locked theme.** Petal drift (with actual petal shapes) works on any organic, beauty, or seasonal brand. Bloom entry animation (spring easing on content entry) works universally — it is the most natural-feeling appear animation in CSS. Pastel gradient washes work on any soft, premium, or wellness brand.

**Architectural short-schema:**
```
BLOSSOM PAGE FLOW:
  [Before Bloom] — pale grey sky, bare branch frame, first buds visible
    ↓ petals begin — sparse, hesitant
  [First Bloom] — branch fills with blossoms, petal drift increases, soft focus
    ↓ wind gust sweeps through, petal density peaks
  [Full Bloom Peak] — maximum petal density, full pastel palette, bloom entry animations
    ↓ petals begin thinning — each section slightly barer
  [Petal Carpet] — petals settle on ground-elements, pale pink coverage
    ↓ last petals in still air
  [After] — bare branch, single petal, profound quiet, CTA as what remains
```

**Sensory anchors:** Petals land cold on warm skin. Fragrance so thick it has texture. Silence in the middle of a city. The color is wrong — too pink, too brief. You know it's ending while it's still at peak.

**Mixes well with:** Autumn Foliage (seasonal partner — same branch structure, different stage), Rainforest Mist (shared gentle moisture), Northern Lights (dark twilight blossom variant).

---

### Northern Lights / Aurora

The sky is alive with slow curtains of colored light. The page is black earth looking up. Color arrives unexpectedly, hangs, fades. Stars visible between events.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Curtain wave gradient | Wide vertical gradient bands (`hsl(150 80% 40%)`, `hsl(280 70% 50%)`, `hsl(190 70% 55%)`) with `background-position` animated horizontally at `20-40s` — slow curtain drift | Hero backgrounds, key sections |
| Color band undulation | `@keyframes` on `filter: hue-rotate(0→30→-20→0deg)` on curtain bands — bands shift through green-teal-violet-blue spectrum over 15-30s | Aurora gradient layers |
| Star field backdrop | 200-400 tiny white/pale-blue dots at variable opacity (0.3-1.0), some with subtle twinkle via `opacity` keyframe — fixed position behind scrolling content | Page background base |
| Ground reflection | Bottom 15% of viewport sections: same aurora colors at 20% opacity, inverted — reflecting off snow/ice ground | Section footers, page bottom |
| Aurora pulse event | On scroll trigger: curtain brightness increases (`filter: brightness(1.3)`) over 3s, then settles — aurora intensifying | Major section transitions |
| Dark ground silhouettes | Black SVG tree/mountain/horizon shapes at 100% opacity against aurora background — classic aurora composition | Hero, section backgrounds |
| Magnetic particle drift | Slow particles (not fast) drifting horizontally in curved paths following `path()` animation — charged particles in magnetic field | Background ambient layer |
| Cold white text | Typography in `hsl(210 40% 92%)` with subtle `text-shadow: 0 0 30px hsl(150 60% 60% / 0.3)` — aurora-reflected on snow | Headings, key text |

**Color schema:**
```css
/* Ground dark */
--aurora-ground-bg: 220 30% 4%;       /* arctic night black */
--aurora-ground-fg: 210 20% 85%;      /* cold white */
--aurora-ground-star: 220 40% 80% / 0.6; /* star white */

/* Aurora green */
--aurora-green: 150 85% 50%;          /* classic aurora green */
--aurora-green-dim: 155 60% 35%;      /* distant green */
--aurora-teal: 175 80% 50%;           /* teal transition */

/* Aurora violet */
--aurora-violet: 280 65% 60%;         /* violet band */
--aurora-pink: 310 55% 65%;           /* pink edge */

/* Aurora blue */
--aurora-blue: 200 80% 55%;           /* electric blue band */
--aurora-white: 180 40% 85%;          /* white corona at top */
```

**Font pairings:**
- **Arctic poetry:** Cormorant Garamond (italic light) + Raleway (300) — otherworldly delicacy
- **Nordic minimal:** Space Grotesk (300-400) + Inter (300) — clean Scandinavian restraint
- **Observatory:** IBM Plex Mono (headings) + IBM Plex Sans (body) — scientific wonder

**NOT a locked theme.** Curtain wave gradients work as animated background on ANY dark, dramatic site. Star field backdrop adds depth to any dark minimal layout. Color band undulation (slow `hue-rotate`) is a universal technique for living backgrounds that don't feel animated.

**Architectural short-schema:**
```
AURORA PAGE FLOW:
  [Dark Ground] — star field only, ground silhouettes, cold stillness
    ↓ first aurora hint appears on horizon (low, pale green band)
  [Aurora Rising] — curtains grow upward, green fills mid-sky, particles drift
    ↓ color expands — violet joins green at higher altitude
  [Peak Display] — full viewport aurora, all color bands active, pulse event
    ↓ reflection on ground below, dark silhouettes backlit
  [Fade and Rest] — curtains slow, star field returns, quiet
    ↓ single band remains, faint but present
  [Cold Clarity CTA] — ground level, aurora faint above, stars sharp, content clear
```

**Sensory anchors:** Sounds carry in cold air, then silence. Aurora makes no sound despite looking like it should. Stars are too sharp. Your own heartbeat is audible. Standing still generates no warmth.

**Mixes well with:** Arctic/Frozen Tundra (direct pairing — same environment), Cherry Blossom (twilight variant with blossoms), Deep Ocean (shared electric color palette).

---

### Rainforest Mist

Time here is geological. The mist has been here longer than the trees. Everything is coated in moisture. Sound is muffled and ancient. Green is not a color here — it is the atmosphere itself.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Condensation viewport | Pseudo-element over full viewport: `backdrop-filter: blur(0.5px)` with scattered tiny `radial-gradient` bright spots — moisture on the lens | Hero overlay |
| Drip streams | 1px wide semi-transparent vertical lines descending from container tops at different speeds — `height: 0→100%` animating, then opacity fade | Card tops, section edges |
| Moss surface | `background`: dark green base + SVG `feTurbulence` filter at medium scale producing soft organic blotching in darker green — moss-covered quality | Container backgrounds, section fills |
| Layered canopy depth | 4-5 background layers at increasing opacity as scroll depth increases: palest (far background) → solid (foreground vegetation) — primordial depth | Hero, deep section backgrounds |
| Mist breathing | `opacity: 0.3→0.6→0.3` on mist overlay layers with `animation: 8-15s ease-in-out infinite` — mist contracts and expands | Background mist layers |
| Ancient root texture | Low-contrast SVG pattern of tangled curves at `mix-blend-mode: multiply` 15% — root network visible through surfaces | Floor sections, container backgrounds |
| Frog-call rhythm | DOM element pulses in 2-second intervals (independent of user) — ambient "life" signal in the background | Side elements, corner accents |
| Primordial green shift | `hsl(120→140→155, 30-50%, 8-15%)` — green tones slightly yellow-green at top, deep blue-green at depth | Per-section background color system |

**Color schema:**
```css
/* Surface mist */
--mist-surface-bg: 130 25% 8%;        /* dark misted green */
--mist-surface-fg: 120 10% 85%;       /* pale filtered light */
--mist-surface-mist: 180 15% 85% / 0.12; /* mist white */
--mist-surface-accent: 130 40% 40%;   /* vivid through mist */

/* Deep canopy */
--mist-deep-bg: 145 35% 6%;           /* cathedral green-dark */
--mist-deep-fg: 130 12% 78%;          /* dim canopy light */
--mist-deep-drip: 170 30% 40% / 0.5; /* water droplet */
--mist-deep-moss: 130 45% 18%;        /* saturated moss */

/* Floor */
--mist-floor-bg: 150 20% 5%;          /* jungle floor dark */
--mist-floor-root: 100 20% 12%;       /* dark root brown-green */
--mist-floor-fungi: 30 40% 20%;       /* fungi amber-brown */
```

**Font pairings:**
- **Primordial discovery:** Crimson Pro (italic) + Source Serif 4 (body) — ancient manuscript
- **Botanical survey:** Libre Baskerville (headings) + Source Sans 3 (body) — scientific reverence
- **Expedition notes:** Cormorant Garamond (headings) + Lato (body) — 19th century naturalist

**NOT a locked theme.** Condensation viewport overlay adds cinematic realism to ANY dark hero. Drip streams work as ambient animation on any organic, nature, or wellness brand. Mist breathing (gentle opacity pulse on overlays) is a universal technique for living backgrounds.

**Architectural short-schema:**
```
MIST PAGE FLOW:
  [Canopy Entry] — condensation on viewport, dense mist, content barely visible
    ↓ mist breathes — contracts to reveal, then returns
  [Mid-Canopy] — layered depth visible, drips from above, moss surfaces
    ↓ primordial green deepens, mist thins to waist level
  [Ancient Interior] — cathedral quality, multiple canopy layers, root textures
    ↓ frog-call rhythm active, ambient life signals
  [Floor Approach] — mist at knee height, ancient roots, fungi accents
    ↓ condensation clears as eyes adjust
  [Floor Discovery CTA] — clear air at ground level, all mist above, grounded and found
```

**Sensory anchors:** Air is a liquid. Every surface is cool and slightly slick. Sounds layer — each call has three echoes. Visibility is 15 meters. Nothing here is in a hurry. You have been here millions of years already.

**Mixes well with:** Jungle/Tropical (same biome, quieter mood), Deep Forest (temperate cousin), Cherry Blossom (mist morning in a blossom grove — spring mist variant).

---

### Tide Pool / Coastal

Every 6 hours the world inverts. What was submerged is exposed. What was air is water. The page has cycles — content reveals follow the tide. Salt is visible.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Wave retreat reveal | Section entry animation: `clip-path: inset(0 0 100% 0)→inset(0 0 0% 0)` from bottom, timed to feel like water pulling back to expose surface | Section reveals, content entry |
| Foam line | 1-3px white `border-top` with blur and animated `opacity: 0.8→0→0.8` at 2-3s — retreating wave foam edge | Section tops, container borders |
| Salt crystal texture | `background`: white `box-shadow` cluster at low blur on dark surfaces — crystallized salt deposit quality. `text-shadow` same effect on headings | Container backgrounds, headings |
| Barnacle containers | `border-radius` irregular via `clip-path: polygon(...)` with slightly jagged small-tooth edge — barnacle-covered rock surface quality | Cards, image containers |
| Tidal pool color | Standing water in a depression: warm teal `hsl(185 50% 35%)` with dark edges (depth) and bright center (sky reflection) | Small container backgrounds |
| Rock exposure | `background: repeating-linear-gradient(...)` with horizontal bands of exposed rock strata — geological layers from tide action | Section backgrounds |
| Spray particle | Fine droplets on scroll trigger — tiny white specks radiating outward from wave-collision point, dissipate in 0.8s | Wave-interaction moments |
| Sea glass accent | Muted, frosted color spots (`hsl(180 30% 60%)` teal, `hsl(210 25% 55%)` blue, `hsl(145 25% 55%)` green) with `filter: blur(0.5px)` — sea glass worn smooth | Accent colors, highlights |

**Color schema:**
```css
/* Low tide (exposed) */
--tide-low-bg: 200 20% 10%;           /* dark wet rock */
--tide-low-fg: 195 15% 82%;           /* grey-blue light */
--tide-low-rock: 210 15% 18%;         /* exposed rock */
--tide-low-pool: 185 50% 25%;         /* tide pool water */

/* High tide */
--tide-high-bg: 195 40% 12%;          /* submerged dark */
--tide-high-fg: 190 20% 88%;          /* underwater light */
--tide-high-water: 190 55% 40%;       /* active water */
--tide-high-foam: 200 15% 92% / 0.8; /* foam white */

/* Sunset coast */
--tide-sunset-bg: 20 30% 8%;          /* warm dark coast */
--tide-sunset-sky: 25 70% 55%;        /* orange sunset */
--tide-sunset-water: 195 50% 35%;     /* gold-teal water */
--tide-sunset-glass: 180 25% 60%;     /* sea glass at sunset */
```

**Font pairings:**
- **Coastal research:** IBM Plex Serif (headings) + IBM Plex Sans (body) — marine station precision
- **Shore editorial:** Libre Baskerville (headings) + Lato (body) — seaside journal
- **Nautical atlas:** Playfair Display (headings) + Source Sans 3 (body) — chart-room document

**NOT a locked theme.** Wave retreat reveals are powerful section entry animations for ANY site — the unmasking direction feels natural and unexpected. Foam line borders replace any `border-top` on sections for a subtle texture upgrade. Salt crystal text shadows work on any coastal, mineral, or craft brand.

**Architectural short-schema:**
```
TIDE PAGE FLOW:
  [High Water] — submerged feel, tidal color, content beneath surface quality
    ↓ water begins receding (wave retreat reveals downward)
  [Shoreline] — foam lines at section boundaries, spray particles, salt textures
    ↓ more surface exposed per section — rock layers appear
  [Tide Pool Zone] — barnacle containers, pool-water section fills, sea glass accents
    ↓ tidal pool close-up — small world revealed
  [Rock Exposure] — geological strata backgrounds, maximum texture, minimal water
    ↓ single remaining pool in the dark
  [Sunset CTA] — warm orange light, tide glass reflections, next tide inevitable
```

**Sensory anchors:** Wind is constant and carries salt. Rock surfaces are both rough (barnacle) and smooth (tide-polished). Cold shock of tide pool water versus warm rock surface. Smell of iodine and brine. The rhythm of each wave audible before it arrives.

**Mixes well with:** Underwater/Deep Ocean (submerged zone partner), Coral Reef (same coastal system, shallow water), Arctic (winter coastline — ice and tide combined).

---

## Cross-Environment Combinations

| Mix | Result |
|-----|--------|
| Underwater abyss + Northern Lights | Bioluminescent deep sea — aurora colors below the surface |
| Arctic frost spread + Crystal Cavern | Ice cave — frost on crystal, cold refraction, no warmth |
| Desert heat shimmer + Volcanic magma | Badlands in eruption — heat and geology united |
| Cherry blossom petals + Rainforest mist | Spring mist grove — petals visible through morning fog |
| Storm flash reveal + Mountain cloud-pass | Alpine storm with lightning — vertical + horizontal drama |
| Coral anemone sway + Tide pool barnacle containers | Intertidal zone — organism texture everywhere |
| Jungle vine growth + Cave torch-lit reveal | Lost ruin — overgrown discovery in torchlight |
| Autumn leaf scroll + Rainforest mist | Late monsoon season — decay and moisture together |
| Aurora curtain bands + Deep ocean depth | Alien bioluminescent ocean — impossible and beautiful |
| Arctic ice crack + Volcanic lava crack | Geological catastrophe — two crack systems in different colors |
| Desert oasis reveal + Coral reef color flood | Mirage that is real — arid to vibrant transition |

**Rule:** Surface ingredients by what the user says FEELS right — pressure, silence, weight, heat, cold, motion, stillness. The sensation is the signal. Match the CSS technique to the sensation, not to the literal environment name.
