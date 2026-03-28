# Urban & Architecture Inspiration Themes

Twelve ingredient palettes translated from real built environments into composable CSS. Each theme is a sensory experience first, a design system second.

---

### Neon Tokyo / Night City

Rain-slicked streets at 2am. Every surface reflects a different color. The page IS sensory overload — neon bleeding through wet asphalt, kanji stacks pulsing, electric hum you can almost hear.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Neon sign glow | `box-shadow` with 3 layers: tight inner glow (2px), mid spread (8px), wide atmospheric bloom (20-40px) — all in saturated hue. Animate `opacity` 0.8→1→0.9 on 2s loop with slight hue-rotate drift | Any card, heading, border |
| Rain streak overlay | Pseudo-element with repeating-linear-gradient of near-transparent vertical lines (1px wide, random spacing via background-size variation), animated `background-position-y` downward at 2-4s | Dark hero sections, full-page backgrounds |
| Wet surface reflection | Vertically flipped, blurred (blur 8-15px), opacity 15-30% duplicate of content positioned below it — simulates puddle mirror | Hero images, section footers |
| Neon flicker | `@keyframes` with opacity jumps: 100%→85%→100%→70%→100% at irregular intervals (use `animation-delay` per element) — NOT smooth fade, actual flicker with micro-off moments | Sign text, accent borders |
| Kanji/signage layering | Large semi-transparent unicode or SVG text characters (opacity 5-15%) positioned `absolute` behind content, different scales and rotations — environmental noise | Dark backgrounds, hero sections |
| Fog/steam vent | Blurred radial-gradient blob (white/gray, filter:blur 60-100px, opacity 8-20%) that drifts slowly upward via `translateY` animation — street-level steam | Floor-level elements, section dividers |
| Bokeh city lights | Multiple radial-gradient circles (12-30px) at low opacity (10-20%), scattered positions, animate subtle scale and opacity pulse — out-of-focus city background | Dark backgrounds |
| Chromatic aberration text | `text-shadow` with red offset left 1-2px, cyan offset right 1-2px — neon sign distortion effect | Large display headings |
| Electric wire dividers | SVG `<path>` with catenary curve (power lines between buildings), optional animated current-pulse dot traveling the path | Section breaks |
| Holographic sheen | `background: linear-gradient(135deg, hsl(290,100%,70%), hsl(200,100%,70%), hsl(340,100%,65%))` + `background-clip: text`, animate `hue-rotate` continuously | Premium feature labels, accent text |

**Color schema (time-of-night dial):**
```css
/* Midnight base */
--neon-bg: 240 15% 4%;              /* near-black with cold blue tint */
--neon-surface: 240 12% 8%;         /* dark surface, slightly lifted */
--neon-fg: 200 10% 88%;             /* cool white text */

/* Neon accent palette */
--neon-pink: 320 100% 60%;          /* hot pink sign */
--neon-cyan: 185 100% 55%;          /* cyan tube light */
--neon-yellow: 55 100% 60%;         /* warm neon yellow */
--neon-violet: 275 100% 65%;        /* purple glow */
--neon-orange: 20 100% 58%;         /* ramen shop orange */

/* Atmospheric glow layers */
--neon-glow-pink: 320 100% 60% / 0.3;
--neon-glow-cyan: 185 100% 55% / 0.25;
--neon-wet-asphalt: 230 20% 12%;    /* rain-darkened ground */
--neon-mist: 200 15% 60% / 0.08;    /* ambient fog layer */
```

**Font pairings that fit:**
- **Cyberpunk editorial:** Rajdhani (700, headings) + IBM Plex Mono (body) — technical, dense, urban
- **Night market:** Noto Sans JP (headings, weight 900) + Inter (body) — authentic Tokyo mixed-script feel
- **Electric signage:** Space Grotesk (headings) + DM Sans (body) — clean modern with edge

**NOT a locked theme.** Neon glow works on any dark premium site. Rain streaks work on any atmospheric hero. Flicker animation works on any accent label. Wet reflection works on any footer above a dark floor element.

**Architectural short-schema:**
```
NEON CITY PAGE FLOW:
  [Street Level Entry] — hero, rain streaks active, neon signs flicker into view
    ↓ fog/steam vents from below fold, kanji layers drift in background
  [The Strip] — content cards glow individually, each its own neon color
    ↓ bokeh lights intensify, chromatic aberration on section headings
  [Deep Alley] — darker, more intimate — single accent color dominates
    ↓ wet reflection below featured content, electric wire dividers
  [Night Market] — densest content section, maximum layering, holographic sheen on CTAs
    ↓ neon dims slowly, fog thickens
  [Late Night Exit] — sparse, one glowing CTA in the dark, rain still falling

Foreground: neon signs, steam, rain — all z-index above content
Background: wet asphalt, kanji layers, bokeh — deeply recessed
Content: exists in the middle zone, illuminated by surrounding neon
```

**Sensory anchors:**
- Temperature: Cold and wet. Damp jacket. Breath visible.
- Sound: Sizzling rain on pavement, distant bass from a club, electric hum of signs, moped engine.
- Texture: Slick wet concrete, greasy puddle surface, neon tube glass.
- Light: Oversaturated, colored, directionless — comes from everywhere and nowhere.
- Smell: Rain on asphalt, frying oil, cigarette smoke, ozone from signs.

---

### Industrial Warehouse

Raw creative space. Exposed everything. Beauty isn't applied — it IS the structure. The page is a converted loft: concrete floor, steel beams, Edison bulbs, walls that remember previous tenants.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Concrete texture | `background-image` with noise SVG filter (`feTurbulence baseFrequency="0.65"` + `feColorMatrix`) at 4-8% opacity over flat gray — subtle grain, not wallpaper | Section backgrounds, cards |
| Exposed pipe dividers | SVG horizontal rule: two parallel lines (pipe silhouette) with circular joint connectors at endpoints, optional `linear-gradient` rust stain | Section breaks |
| Caged bulb spotlight | Radial-gradient: warm amber center (hsl 40,80%,70%) bleeding to near-black, positioned off-center. Add SVG cage wireframe overlay (z-index above gradient) | Hero sections, featured content |
| Rivet grid | Repeating pattern of 4-6px circles at regular grid intervals via `radial-gradient` in `background-image` — metal panel texture | Card backgrounds, full-width panels |
| Loading dock reveal | Content enters from side (translateX) with heavy `cubic-bezier(0.25, 0.46, 0.45, 0.94)` easing — like a freight door sliding open | Section transitions |
| Spray paint stencil | `mix-blend-mode: multiply` text or graphic element over concrete — rough, uneven opacity via SVG filter | Accent headings, background art |
| Chain-link overlay | SVG diagonal grid pattern (45deg lines, crossing, 20px grid) at 3-6% opacity — industrial fence texture | Hero overlays, section dividers |
| Floor stripe | Bold yellow/white diagonal stripe (like safety floor marking) using `repeating-linear-gradient` at 45deg — 60px repeat | Attention bars, warning sections |
| Rusted I-beam shadow | Deep lateral drop shadow (`box-shadow: 8px 0 20px rgba(0,0,0,0.6)`) on vertical elements — structural weight | Sidebar containers, vertical cards |
| Graffiti accent | Bold, irregular SVG tag-style letterforms as decoration — NOT readable text, pure visual energy | Background layers, section art |

**Color schema:**
```css
/* Raw material base */
--warehouse-concrete: 210 5% 72%;   /* raw concrete */
--warehouse-bg: 220 8% 12%;         /* dark industrial space */
--warehouse-surface: 220 6% 18%;    /* slightly lifted surface */
--warehouse-fg: 30 10% 88%;         /* warm white, Edison-lit */

/* Accent materials */
--warehouse-steel: 210 15% 45%;     /* cold steel gray */
--warehouse-rust: 18 65% 42%;       /* oxidized iron */
--warehouse-safety: 48 100% 52%;    /* safety yellow */
--warehouse-amber: 38 85% 55%;      /* Edison bulb warm */
--warehouse-brick: 10 55% 38%;      /* exposed brick red */

/* Texture layers */
--warehouse-shadow: 220 15% 5% / 0.7;
--warehouse-grime: 40 20% 30% / 0.06;
```

**Font pairings that fit:**
- **Foundry bold:** Bebas Neue (headings) + Source Sans 3 (body) — industrial print, signage weight
- **Blueprint technical:** DM Mono (headings) + Inter (body) — technical drawings, engineer's notebook
- **Raw editorial:** Anton (display) + Lato (body) — warehouse printing press energy

**NOT a locked theme.** Concrete texture works on any grunge or editorial site. Caged bulb spotlight works for any dark feature section. Loading dock reveal is a generic scroll animation. Rivet grid works on any tech/mechanical product.

**Architectural short-schema:**
```
WAREHOUSE PAGE FLOW:
  [Loading Dock Entry] — freight door slide reveal, raw concrete hero
    ↓ Edison bulbs flicker on (staggered), structural grid appears
  [Open Floor] — primary content area, high ceiling, floor stripe accents
    ↓ pipe dividers cross the page, rivet panels mark content zones
  [Workshop Zone] — denser content, tool walls, spray stencil headings
    ↓ shadows deepen, chain-link overlay on background
  [Storage / Archive] — secondary content, stacked, ordered, caged bulb spots
    ↓ brick wall becomes visible through damaged concrete
  [Exit / Loading Bay] — CTA, safety floor stripe, open door/light beyond

Vertical rhythm: heavy, grounded. No floaty elements.
Dividers are structural, not decorative.
```

**Sensory anchors:**
- Temperature: Cool, drafty. Metal surfaces cold to touch.
- Sound: Echo of footsteps on concrete, distant machinery, pigeons in rafters.
- Texture: Rough poured concrete, cold steel, gritty floor, flaking paint.
- Light: Warm amber spots in vast cool darkness. Strong contrast.
- Smell: Machine oil, concrete dust, old wood, faint paint solvent.

---

### Art Deco Lobby

1925. You've just pushed through the brass-handled revolving door. Everything is geometry, gold, symmetry, and the quiet confidence of wealth. The page drips with vertical ambition.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Gold-line geometric borders | `border-image: linear-gradient(gold, goldenrod) 1` combined with SVG corner ornaments (45-degree angle cuts) — NOT simple border-radius | Any container, card, section |
| Sunburst radial | `conic-gradient` with alternating narrow/wide segments radiating from center, gold on dark or dark on cream — fan pattern | Hero backgrounds, CTA sections |
| Stepped pyramid container | `clip-path: polygon()` creating stepped/notched corners at all four edges — ziggurat silhouette | Feature cards, image frames |
| Chevron repeat | `repeating-linear-gradient` at 45deg with gold and black alternation, tight (8-10px) — floor or border marquetry | Horizontal bands, footer |
| Mirror symmetry | CSS `transform: scaleX(-1)` on pseudo-element duplicates — use for flanking decorative elements left and right | Hero flanking elements |
| Marble-effect background | SVG `feTurbulence` noise at low frequency (0.02) + high contrast → cream/gold veining on dark surface | Panel backgrounds |
| Brass-relief text | `text-shadow` with 3-step depth: 1px gold, 2px darker gold, 3px near-black — embossed metal letterpress feel | Large display headings |
| Fan vault overlay | Repeating SVG arch/fan geometry as semi-transparent overlay — ceiling-plaster pattern | Hero and section overlays |
| Illuminated reveal | Content enters via `clip-path` expand from center outward on scroll, as if curtains parting or a safe opening | Section entries |
| Elevator door transition | Two panels sliding out (translateX ±50%) to reveal content — actual elevator door reveal | Page or section transitions |

**Color schema:**
```css
/* Ivory and gold base */
--deco-bg: 40 20% 8%;               /* dark marble-black */
--deco-surface: 40 15% 14%;         /* deep charcoal with warm tint */
--deco-fg: 45 40% 92%;              /* cream ivory text */

/* Gold system */
--deco-gold: 42 85% 52%;            /* primary gold */
--deco-gold-pale: 45 60% 72%;       /* pale champagne gold */
--deco-gold-deep: 35 70% 35%;       /* burnished dark gold */
--deco-gold-bright: 50 100% 65%;    /* highlight gleam */

/* Accent neutrals */
--deco-marble: 40 8% 88%;           /* cream marble */
--deco-onyx: 220 10% 6%;            /* pure black accent */
--deco-copper: 22 75% 48%;          /* warm copper secondary */
```

**Font pairings that fit:**
- **Deco authority:** Playfair Display (italic headings) + Cormorant Garamond (body) — gilded-age editorial
- **Hotel marquee:** Libre Baskerville (headings) + Lato (300, body) — lobby placard precision
- **Geometric sans:** Josefin Sans (headings) + Raleway (body) — geometric clean deco

**NOT a locked theme.** Gold-line borders work on any luxury product. Sunburst radial works on any hero needing geometric drama. Stepped pyramid clip-path works on any contemporary card layout. Brass-relief text works on any dark premium header.

**Architectural short-schema:**
```
ART DECO PAGE FLOW:
  [Grand Entrance] — elevator door reveal OR symmetrical curtain part, full gold border frame
    ↓ sunburst radial expands from center, geometric grid resolves
  [Lobby Floor] — geometric tilework visible, mirrored flanking columns
    ↓ vertical stacked content rises like a tower facade
  [Mezzanine Level] — secondary content, stepped pyramid cards, chevron bands
    ↓ gold lines intensify, depth increases
  [The Safe Room] — most precious content (pricing, feature), illuminated reveal, maximum ornament
    ↓ symmetry resolves, CTA emerges centered
  [Exit Revolving Door] — final CTA perfectly centered, flanked by mirrored elements

Symmetry is structural — not decorative. Every element has a mirrored counterpart.
Vertical emphasis: tall containers, stacked type, upward-pointing geometry.
```

**Sensory anchors:**
- Temperature: Controlled, cool marble and brass. Climate is also a luxury.
- Sound: Echoing marble footsteps, elevator bell, hushed voices, distant orchestra.
- Texture: Cold smooth marble, warm polished brass, thick carpet underfoot.
- Light: Indirect, warm, upward-casting sconces. Gold reflects gold.
- Smell: Fresh flowers in tall vases, brass polish, subtle perfume.

---

### Gothic Cathedral

Stone vaults impossibly high. Vertical lines that end in darkness. Colored light that moves as the sun moves. The page earns the user's awe before it earns their click.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Pointed arch frame | SVG or `clip-path` with ogival arch shape — pointed at apex, curved flanks — used as image mask, container shape, or decorative frame | Images, cards, modal frames |
| Rose window projection | Circular SVG with radial geometric petal pattern, colored segments via `fill` with opacity 0.3-0.6, rotated slowly — cast as overlay on content | Hero sections, behind CTAs |
| Ribbed vault pattern | Diagonal crossing line grid (SVG or `background-image` with `linear-gradient` at 45deg and 135deg) radiating from vaulting points — ceiling texture | Section backgrounds |
| Stained glass color cast | Irregular `clip-path` polygon patches of color (blue, red, amber, green) at 8-20% opacity overlaid on white/light backgrounds — window light landing on stone floor | Light background sections |
| Candlelight flicker | Radial-gradient spot (amber, 80% transparent at edges) with `opacity` and `scale` keyframe animation at irregular intervals — flame physics approximation | Dark sections, CTA zones |
| Stone weight typography | Extra-heavy (900 weight) text with slight `letter-spacing: -0.02em`, vertical `writing-mode` option for pillar-like labels — carved weight | Display headings, section labels |
| Flying buttress sidebar | Visual structural element: angled support shape on edge of main content column — `clip-path` diagonal container | Sidebar, annotation elements |
| Tracery overlay | Fine geometric line network (SVG with small circles at intersections) — window stone leading pattern | Card borders, background overlays |
| Height reveal | Content sections that animate with `scaleY` from 0 up, as if vaults are rising — vertical growth, not horizontal fade | Section entry animations |
| Dark alcove container | Deep inset container: heavy `inset box-shadow` (20-40px spread, dark), slightly different background hue — recessed stone niche | Feature highlight boxes |

**Color schema:**
```css
/* Stone and shadow base */
--gothic-stone: 220 8% 22%;         /* cool limestone gray */
--gothic-bg: 230 12% 7%;            /* nave darkness */
--gothic-fg: 35 15% 88%;            /* candlelit parchment */
--gothic-shadow: 230 20% 3%;        /* deepest vault shadow */

/* Stained glass spectrum */
--gothic-ruby: 350 75% 42%;         /* deep red glass */
--gothic-sapphire: 220 70% 38%;     /* deep blue glass */
--gothic-amber-glass: 38 90% 50%;   /* amber/gold glass */
--gothic-emerald: 145 55% 30%;      /* deep green glass */
--gothic-violet: 270 55% 38%;       /* violet glass */

/* Atmospheric */
--gothic-candlelight: 38 80% 60%;   /* warm candle glow */
--gothic-incense: 280 10% 35% / 0.2; /* smoky purple haze */
```

**Font pairings that fit:**
- **Medieval authority:** IM Fell English (headings) + Crimson Text (body) — manuscript hand
- **Cathedral inscription:** Cinzel (headings) + Lora (body) — carved Roman letterforms
- **Modern sacred:** Spectral (headings) + Source Serif 4 (body) — contemporary liturgical

**NOT a locked theme.** Pointed arch frames work on any editorial image treatment. Rose window patterns work on any circular hero element. Stained glass color cast works on any light-background feature section. Candlelight flicker works on any dark atmospheric CTA.

**Architectural short-schema:**
```
GOTHIC PAGE FLOW:
  [Portal Entry] — pointed arch frame gates the hero, stone tracery fades in
    ↓ vault height reveal — sections grow upward from floor
  [Nave] — primary content, ribbed vault background, vertical rhythm dominates
    ↓ rose window projection appears as scroll midpoint marker
  [Transept] — cross-axis content (features, testimonials), stained glass color cast
    ↓ candlelight spot activates on featured content
  [Choir] — premium/precious content, dark alcoves, maximum stone weight typography
    ↓ atmosphere shifts, incense haze layer
  [Altar / Sanctuary] — final CTA, rose window fully revealed, maximum luminosity

Light source: always from above and through colored glass.
Shadow: pervasive, deep, purposeful — not decorative.
```

**Sensory anchors:**
- Temperature: Cool and constant. Stone holds cold year-round.
- Sound: Footstep echo, distant choir, stone silence, occasional organ drone.
- Texture: Rough-hewn limestone, smooth carved marble, iron door fixtures.
- Light: Jewel-colored, shifting, otherworldly — lands on stone like a painting.
- Smell: Incense, cold stone, aged wood, beeswax candles.

---

### Mediterranean / Santorini

3pm in August. Every surface is white or blue. The light is so strong it dissolves edges. Steps cascade toward an impossibly blue sea. The page breathes with heat and ease.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Whitewash texture | High-key flat white with subtle `feTurbulence` noise at 3-5% opacity — lime plaster, not perfect paint | Section backgrounds, card surfaces |
| Blue dome accent | SVG semicircle (dome silhouette) as decorative section divider or background element — iconic Cycladic architecture | Section transitions, hero elements |
| Stepped terrace layout | Content sections offset horizontally by 40-80px alternating left/right — like descending terrace levels on a hillside | Multi-section content flow |
| Bougainvillea splash | Irregular cluster of deep magenta/pink shapes (circles, organic blobs via `border-radius: 60%`) scattered at element edges — flowering vine intrusion | Card corners, section edges |
| Mediterranean shadow | Crisp, hard `box-shadow` with minimal blur (2-4px) and high offset — strong midday sun, minimal diffusion | Cards, containers |
| Cicada shimmer | Subtle `hue-rotate` animation on accent elements cycling through warm spectrum — heat haze color shift | Gold/amber accent elements |
| Infinity edge illusion | Background gradient that merges seamlessly from below-fold color to sky blue at the horizon line — pool-to-sea visual | Footer, bottom sections |
| Terracotta grid | `border` or `background-image` grid in terracotta/burnt orange — floor tile reference | Background accents, card borders |
| Sea-glass border | Border with varying opacity and slight color variation — hand-made ceramic glazed tile edge | Images, containers |
| Winding path line | Organic SVG `<path>` (slight S-curve) as visual connector between sections — whitewashed alley | Section connectors |

**Color schema:**
```css
/* Cycladic base */
--med-white: 40 15% 97%;            /* warm plaster white */
--med-bg-bright: 210 10% 95%;       /* bleached surface, high sun */
--med-bg-shade: 220 20% 82%;        /* shadow on white wall */
--med-fg: 220 30% 15%;              /* deep navy text */

/* Blue spectrum */
--med-dome: 215 85% 38%;            /* iconic dome blue */
--med-sea: 200 70% 52%;             /* Aegean sea */
--med-sky: 205 55% 72%;             /* summer sky */
--med-pool: 190 60% 60%;            /* pool turquoise */

/* Accent warmth */
--med-bougainvillea: 340 85% 52%;   /* deep magenta flower */
--med-terracotta: 18 65% 50%;       /* fired clay orange */
--med-gold: 45 80% 58%;             /* bleached gold light */
--med-shadow: 220 40% 20% / 0.25;   /* strong noon shadow */
```

**Font pairings that fit:**
- **Island editorial:** Merriweather (headings) + Open Sans (body) — warm, readable, unhurried
- **Coastal luxury:** Cormorant Garamond (headings) + Raleway (300, body) — elegant and airy
- **Whitewashed modern:** DM Sans (headings) + Karla (body) — contemporary Mediterranean

**NOT a locked theme.** Whitewash texture works on any clean editorial brand. Hard shadow works on any bright-background product. Stepped terrace layout works on any alternating content section. Bougainvillea splash works as a generic accent element on warm brands.

**Architectural short-schema:**
```
MEDITERRANEAN PAGE FLOW:
  [Hilltop Arrival] — high-key white hero, strong shadows, bougainvillea splashes at edges
    ↓ stepped terrace layout begins, each section slightly offset
  [Village Alley] — winding path connector, whitewash texture, blue dome accents visible
    ↓ sea appears in background gradient, light shifts golden
  [Terrace Overlook] — featured content, Mediterranean shadow on cards, pool turquoise accents
    ↓ sun lower, warmth increases, cicada shimmer on accents
  [The Pool] — premium section, infinity edge illusion, maximum blue
    ↓ sun hits horizon, terracotta grid warms the palette
  [Sunset Bar] — CTA, golden light, bougainvillea at maximum, sea below

Light is the dominant design element — everything is about what the sun does to white surfaces.
```

**Sensory anchors:**
- Temperature: Scorching surfaces, cool breeze from the sea. Contrast is constant.
- Sound: Cicadas, distant waves on rock, wind through bougainvillea, church bell.
- Texture: Rough lime plaster, smooth rounded whitewash edges, warm terracotta tile.
- Light: Brutal, bleaching, directional — white walls act as reflectors.
- Smell: Sea salt, jasmine, sun-warmed stone, oregano.

---

### Moroccan Riad

Through a plain wooden door off the medina street: sudden courtyard paradise. Geometric complexity at every surface. Every tile is hand-placed. The page rewards patience and looking closely.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Zellige tile grid | CSS `background-image` combining multiple `linear-gradient` at 0deg, 90deg, 45deg creating 8-point star repeat pattern — approximates hand-cut tile | Section backgrounds, card fills |
| Keyhole arch frame | `clip-path: path()` with horseshoe arch plus keyhole indent at base — distinctive Moorish silhouette | Image masks, modal frames, hero shapes |
| Fountain center layout | Content radiates from centered circular element — `display: grid` with `place-items: center`, decorative ring borders | Hero sections, feature spotlights |
| Lantern glow | Geometric faceted light shape (SVG hexagon or octagon with metalwork cutout pattern) as overlay casting light-dot pattern on surface below | Dark section overlays |
| Mashrabiya screen | SVG lattice pattern (interlocking squares and circles) as `background-image` or overlay — wooden carved screen texture | Hero overlays, card backgrounds |
| Geometric interlace border | SVG border with continuous knotwork (lines crossing over/under at regular intervals) — `stroke-dasharray` animated on scroll for reveal | Section borders, card frames |
| Terracotta plaster texture | Warm orange-tan `feTurbulence` noise layer — hand-troweled wall finish | Section backgrounds |
| Inner courtyard depth | `perspective` transform on inner container to suggest looking down into a recessed space — architectural depth illusion | Featured content sections |
| Arabesque backdrop | Large-scale flowing vegetal scroll pattern (SVG) at very low opacity (3-6%) — continuous background ornament | Any background surface |
| Souk color burst | Scattered product/content cards each in different saturated color — pile of spice market goods | Grid of items, card collections |

**Color schema:**
```css
/* Riad base */
--riad-plaster: 28 40% 78%;         /* warm cream plaster */
--riad-bg: 25 25% 12%;              /* shaded interior cool dark */
--riad-fg: 30 20% 90%;              /* warm candlelit white */
--riad-courtyard: 40 30% 88%;       /* sun-filled courtyard cream */

/* Tile spectrum */
--riad-cobalt: 215 80% 40%;         /* deep cobalt blue tile */
--riad-turquoise: 175 65% 42%;      /* aqua-green glaze */
--riad-saffron: 38 90% 52%;         /* saffron yellow |
--riad-terracotta: 18 70% 45%;      /* fired earth orange */
--riad-emerald: 150 50% 32%;        /* deep garden green */
--riad-bordeaux: 350 55% 30%;       /* deep wine */

/* Metalwork */
--riad-brass: 42 75% 50%;           /* hammered brass lantern */
--riad-shadow: 25 30% 5% / 0.5;     /* deep courtyard shadow */
```

**Font pairings that fit:**
- **Medina manuscript:** Lora (headings) + Noto Naskh Arabic / Amiri (if Arabic content) — authentic mixed script
- **Heritage modern:** Fraunces (headings) + Nunito (body) — warm and intricate
- **Geometric ornament:** Josefin Sans (headings) + Source Sans 3 (body) — geometric echo of zellige

**NOT a locked theme.** Zellige patterns work as any geometric background texture. Keyhole arches work on any image framing. Lantern glow works on any dark atmospheric section. Mashrabiya screens work as any decorative overlay.

**Architectural short-schema:**
```
RIAD PAGE FLOW:
  [Medina Door] — narrow, plain exterior — understated entry (hero is simple)
    ↓ threshold crossed — geometric complexity explosion
  [Courtyard Reveal] — fountain center layout, zellige tile floor visible, lantern glows
    ↓ arabesque backdrop intensifies, mashrabiya screen overlays
  [Upper Gallery] — secondary content on railed walkway above courtyard
    ↓ perspective shift, looking down into tiled floor
  [The Hammam] — deepest, most private content — maximum sensory richness, steam layers
    ↓ geometric borders on all containers, interlace reveals on scroll
  [Garden / Exit] — CTA, garden greenery, filtered light through screen

Every surface is ornament. Negative space is the exception, not the rule.
```

**Sensory anchors:**
- Temperature: Cool inside versus fierce heat outside. The riad IS the escape.
- Sound: Splashing fountain, muezzin distant, bird in orange tree, leather slippers on tile.
- Texture: Hand-cut ceramic tile, carved plaster, woven wool kilim, hammered brass.
- Light: Intense courtyard sun versus dim interior shade. Lantern patterns on surfaces.
- Smell: Orange blossom, cedar wood, cumin from the kitchen, rose water.

---

### Japanese Zen Garden

Intentional emptiness IS the design. Every element exists because removing it would create worse balance. The page earns attention through restraint, and rewards it with profound calm.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Sand rake lines | SVG parallel curved lines (varying radius, closely spaced) — raked gravel pattern as background texture or section divider | Background sections, dividers |
| Asymmetric rock placement | CSS grid with intentional empty cells — content "rocks" placed according to rule of thirds, not centered | Feature layouts, image grids |
| Bamboo fence divider | SVG vertical line pattern with circular joint accents (bamboo culm sections) — `background-image` horizontal rule | Section breaks |
| Water ripple focus | Concentric circle SVG centered on CTA or key element, animates outward `scale` slowly from 1 to 1.05 to 1 — water-drop stillness | CTAs, focal points |
| Moss accent | Irregular blob shape (organic `border-radius` 40%/60%) in deep green at very low opacity — stone moss presence | Image corners, container edges |
| Stepping stone path | Series of rounded rectangles in slight arc, each revealed with staggered scroll delay — path through garden | Navigation, progress indicators |
| Paper screen (shoji) | White/cream `background` + fine horizontal grid lines (0.5px, 5% opacity) — translucent paper and wood lattice | Section backgrounds, modal overlays |
| Bonsai silhouette | SVG tree silhouette (asymmetric, pruned) as decorative element — carefully shaped, never symmetrical | Hero elements, section markers |
| Gravel void | Deliberate large empty zone with sand-rake texture — active negative space, not missed content | Hero empty areas, section breathing room |
| Ma (interval) spacing | Extra-generous `margin` / `padding` (3-5x normal) between elements — the Japanese concept of negative space as presence | All spacing decisions |

**Color schema:**
```css
/* Zen restraint base */
--zen-bg: 40 8% 94%;                /* raked sand, light */
--zen-bg-dark: 200 10% 8%;          /* night garden, dark variant */
--zen-surface: 35 5% 88%;           /* aged paper white */
--zen-fg: 200 15% 18%;              /* sumi ink black */

/* Natural accents */
--zen-stone: 210 8% 55%;            /* weathered granite */
--zen-moss: 130 30% 28%;            /* deep moss green */
--zen-bamboo: 80 35% 52%;           /* young bamboo */
--zen-pine: 130 25% 22%;            /* aged pine */
--zen-water: 205 40% 60%;           /* clear shallow water */
--zen-copper-maple: 20 75% 38%;     /* autumn maple accent */

/* Minimalist */
--zen-ink: 200 20% 10%;             /* sumi ink stroke */
--zen-void: 200 5% 92% / 0.0;       /* transparent — the void IS the color */
```

**Font pairings that fit:**
- **Brush and ink:** Noto Serif JP (headings) + Noto Sans JP (body) — authentic Japanese typographic rhythm
- **Minimal Western:** Cormorant (light weight, headings) + Work Sans (300, body) — sparse and contemplative
- **Printed poetry:** IM Fell English (italic headings) + Crimson Text (body) — haiku visual weight

**NOT a locked theme.** Sand rake patterns work on any minimal background. Asymmetric rock placement works on any editorial grid. Water ripple focus works on any CTA that benefits from calm rather than urgency. Ma spacing works on any premium product that wants breathing room.

**Architectural short-schema:**
```
ZEN GARDEN PAGE FLOW:
  [Garden Gate] — sparse entry, single element, sand-rake background
    ↓ content appears as stepping stones — one at a time, with deliberate delay
  [First Rock Grouping] — primary content, asymmetric placement, moss accents
    ↓ water ripple animates slowly around featured element
  [Raked Gravel Field] — intentional void section, breathing room — nothing is a mistake
    ↓ bamboo fence divider, pace slows further
  [Bonsai Corner] — secondary content, reduced, curated
    ↓ shoji paper texture shifts in, light gentles
  [The Viewing Stone] — CTA, alone in the frame, perfectly placed — nothing competes

Speed: everything is 0.3x slower than a typical site.
Each element entered with individual, gentle fade-and-rise.
Hover states: almost invisible — a whisper, not a shout.
```

**Sensory anchors:**
- Temperature: Cool, clean. Morning air before the city wakes.
- Sound: Raking gravel, water from a bamboo pipe, distant pine wind, absolute silence.
- Texture: Cool dry raked sand, rough lichened granite, smooth bamboo surface.
- Light: Soft, gray-white, diffused — no harsh shadows. Dawn or overcast.
- Smell: Pine resin, cool mineral water, green moss, cedar wood.

---

### Brutalist Concrete

No disguise. No decoration. This IS the structure. The page makes no apology for its weight. Beauty emerges from honesty and scale — not from ornament.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Raw concrete texture | `background-image` SVG filter: `feTurbulence type="fractalNoise" baseFrequency="0.85"` + high contrast `feColorMatrix` at 8-12% — formwork grain, visible pour seams | Section backgrounds |
| Board form imprint | Repeating horizontal lines pattern (3px line, 40px gap) at 6% opacity — wooden formwork impression in concrete | Background overlays, panel dividers |
| Weight-implying shadow | Enormous `box-shadow` values (40-80px spread, near-black, low blur) — mass that threatens to fall off the viewport | Containers, header elements |
| Cantilevered overhang | Element positioned with large negative `margin-top` creating visible overlap — structural cantilever over lower section | Section overlaps, hero to content transitions |
| Exposed seam | 2-4px hairline `border` or `box-shadow inset` in slightly lighter gray — where concrete panels meet | Container edges, grid lines |
| Type as structure | Enormous typographic elements (vw units, 15-25vw) treated as load-bearing elements — text IS architecture | Display headings |
| Negative space aggression | Large empty zones that feel pressurized, not incomplete — void as structural element | Section pacing |
| Poured fill reveal | `clip-path` animation that fills container from bottom to top on scroll — liquid concrete poured into form | Section entry animation |
| Crack detail | Thin irregular SVG path with very slight glow on hover — the structure has history | Background textures, aging details |
| Industrial grid | Strict `12-column` or `8-column` CSS grid with `gap: 0` and explicit structural lines shown — exposed infrastructure | Layout system |

**Color schema:**
```css
/* Concrete spectrum */
--brutalist-raw: 210 5% 68%;        /* unfinished concrete */
--brutalist-weathered: 210 4% 55%;  /* outdoor weathered gray */
--brutalist-dark: 210 8% 18%;       /* deep shadow concrete */
--brutalist-bg: 210 6% 12%;         /* brutalist dark base */
--brutalist-fg: 35 8% 90%;          /* off-white, concrete-dust white */

/* Structural accents */
--brutalist-rebar: 210 10% 35%;     /* rebar gray */
--brutalist-oxide: 18 50% 35%;      /* rust oxide stain */
--brutalist-grime: 200 8% 30%;      /* weathering grime */

/* Rare accent (use sparingly) */
--brutalist-signal: 195 90% 48%;    /* single high-contrast signal color */
--brutalist-void: 0 0% 0%;          /* absolute black */
```

**Font pairings that fit:**
- **Concrete slab:** Bebas Neue (headings) + Space Mono (body) — industrial, printed, utilitarian
- **Soviet constructivist:** Anton (headings) + IBM Plex Mono (body) — propaganda poster energy
- **Honest sans:** DIN Condensed / Barlow Condensed (headings) + Source Code Pro (body)

**NOT a locked theme.** Board form texture works on any industrial site. Weight-implying shadow works on any dark editorial. Cantilevered overlaps work on any multi-section page. Type-as-structure works on any site that wants bold architectural hierarchy.

**Architectural short-schema:**
```
BRUTALIST PAGE FLOW:
  [Monolith Entry] — no intro, no fade — full-weight concrete hero lands immediately
    ↓ exposed seams reveal grid structure, nothing is hidden
  [Podium Level] — wide, low, primary content — horizontal mass dominates
    ↓ cantilevered overhang — upper section extends over lower
  [Tower Section] — vertical content, type-as-structure headings 20vw+
    ↓ board form imprints deepen, weathering visible
  [The Void] — intentional blank concrete expanse — breathing space as statement
    ↓ poured fill reveal activates next section
  [Rooftop Slab] — CTA, nothing extra — text + button on raw concrete

No gradients (unless structural). No rounded corners. No decorative elements.
Every design decision is justified by structural logic, not aesthetic preference.
```

**Sensory anchors:**
- Temperature: Cold. Concrete stores cold and releases it slowly.
- Sound: Echo, footstep reverb, distant HVAC drone, silence of great mass.
- Texture: Rough cast surface, smooth polished face, cold to the touch always.
- Light: Top-lit, harsh, directional. Deep shadows in recesses.
- Smell: Concrete dust, mineral damp, industrial oil, stairwell cold.

---

### Abandoned / Urban Decay

Nature won. The building lost. In the gap between them: unexpected beauty. Peeling paint is autobiography. Rust tells time. The page is what happens when design surrenders to entropy.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Peel-away reveal | Content beneath revealed as top layer peels back — CSS `transform-origin: top-left` + `rotate(-5deg)` + `translateY(-100%)` on scroll — paint layer lifting | Section transitions |
| Rust bleed gradient | `radial-gradient` of rust colors (orange-red → burnt umber → dark brown) centered on top corners or edges — rust spreading from fastener | Container edges, image borders |
| Cracked surface texture | SVG `<path>` network of irregular cracks with 1px stroke, semi-transparent — aggregate fracture pattern | Backgrounds, overlays |
| Vine intrusion | SVG organic stems/tendrils growing from edges inward, animated `stroke-dashoffset` to grow on scroll — nature reclaiming | Edge decorations, section breaks |
| Faded paint layer | `mix-blend-mode: multiply` color wash at 20-40% opacity — sun-bleached, chalky, overexposed | Background overlays |
| Broken grid | Intentionally misaligned layout elements — some shifted by 2-8px from perfect alignment — settled foundation | Content grids |
| Graffiti layer | Bold SVG tag shapes behind content at 10-20% opacity — previous inhabitants left marks | Background depth |
| Water stain mapping | Irregular organic shapes in darker tone — `clip-path` with complex polygon — moisture history on walls | Background accents |
| Broken glass mask | Jagged `clip-path` polygon on images — shattered pane of glass | Image treatments |
| Seedling growth | Small botanical elements (SVG grass, weeds) appearing in cracks between sections — entropy indicator | Section dividers |

**Color schema:**
```css
/* Decay palette */
--decay-bg: 35 10% 12%;             /* dark weathered interior */
--decay-surface: 40 12% 22%;        /* aged plaster surface |
--decay-fg: 40 15% 82%;             /* dusty light text */

/* Rust and oxidation */
--decay-rust: 18 70% 38%;           /* primary rust orange */
--decay-rust-dark: 12 60% 25%;      /* deep rust brown */
--decay-oxide: 30 55% 45%;          /* surface oxidation */

/* Faded layers */
--decay-paint-green: 150 20% 42%;   /* faded industrial green */
--decay-paint-blue: 210 25% 38%;    /* old institutional blue */
--decay-paint-yellow: 48 40% 55%;   /* peeling caution yellow */

/* Nature intrusion */
--decay-vine: 120 35% 28%;          /* dark vine green */
--decay-moss-decay: 90 25% 35%;     /* moss on concrete */
--decay-sky-hole: 200 40% 55%;      /* sky visible through roof hole */
```

**Font pairings that fit:**
- **Stencil remnant:** Bebas Neue (headings) + Space Mono (body) — industrial markings
- **Found object:** Playfair Display (worn weight) + Courier Prime (body) — typewritten history
- **Raw energy:** Antonio (headings) + Barlow (body) — street-level, physical

**NOT a locked theme.** Peel-away reveals work on any layered storytelling site. Rust bleed gradients work on any industrial/aged aesthetic. Vine intrusion works on any organic brand. Broken grid works on any creative/editorial site that wants controlled chaos.

**Architectural short-schema:**
```
DECAY PAGE FLOW:
  [Threshold] — dark entry, peel-away reveal from previous life (glimpse of original design)
    ↓ rust bleeds in from corners, cracked texture resolves on scroll
  [Main Hall] — primary content visible through decay — beauty despite entropy
    ↓ broken grid: elements slightly misaligned, vine intrusion from left edge
  [Deeper Ruin] — more nature, less structure — seedlings in section dividers
    ↓ graffiti layers increase opacity, water stains map the ceiling
  [The Discovery Zone] — found beauty — the hidden treasure content
    ↓ broken glass mask on images, maximum atmospheric texture
  [New Growth] — CTA, vine/seedling accent — hope in the ruin, something beginning

Entropy increases as you scroll. The page is deteriorating in real time.
But the deterioration IS beautiful — that's the entire point.
```

**Sensory anchors:**
- Temperature: Cold drafts through broken windows. Damp. Inconsistent.
- Sound: Wind through broken glass, distant bird, floor creak, dripping water.
- Texture: Peeling paint layers (thick), crumbling plaster, gritty concrete dust.
- Light: Through roof holes, through broken windows — beautiful because accidental.
- Smell: Wet concrete, mold, rust, old wood, outside air intruding.

---

### Rooftop / Skyline

You've climbed to the top and the city is below you now. Wind. Open sky. Golden hour. The vertigo of standing on the edge and choosing to stay.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Skyline silhouette | SVG building silhouette strip (varied heights, identifiable skyline shape) as `footer` decoration or `background-image` at bottom of sections | Section footers, hero base |
| City light bokeh | Scattered radial-gradient circles (orange, yellow, white) at 8-15% opacity, varied sizes (4-20px) — city lights far below | Dark background sections |
| Golden hour gradient | `linear-gradient` from bottom: deep amber → orange → coral → pale lavender → deep blue — sunset color stack | Hero backgrounds, full sections |
| Wind-blown typography | `transform: rotate(-1deg to -3deg)` on text with slight random variation per element — wind effect on signage | Display headings, decorative text |
| Rooftop railing grid | SVG horizontal bars pattern (equal spacing, perspective transform applied) — parapet railing | Bottom-of-section horizontal rule |
| Cloud drift | Elongated blurred white shapes at very low opacity (5-10%), animated `translateX` extremely slowly | Sky section backgrounds |
| Height vertigo | First scroll section has `perspective: 800px` and slight `rotateX` that normalizes on scroll — looking-down sensation | Hero section |
| Water tower silhouette | Distinctive cylindrical SVG water tower element — iconic rooftop furniture | Decorative background elements |
| Tar paper texture | Dark rough texture (similar to concrete noise but darker, irregular) — actual rooftop surface material | Background base |
| Open sky void | Large, single-color `background-color: hsl(210,60%,15%)` expanse — just sky, nothing else — confident emptiness | Section breathing space |

**Color schema (golden hour dial):**
```css
/* Dawn / Dusk transition */
--sky-night: 230 30% 8%;            /* pre-dawn or post-sunset */
--sky-dusk: 220 40% 15%;            /* deep blue hour */
--sky-horizon: 210 50% 25%;         /* horizon deep blue */

/* Golden hour spectrum */
--sky-golden: 38 90% 58%;           /* golden hour amber */
--sky-coral: 12 80% 60%;            /* late sunset coral */
--sky-rose: 350 55% 65%;            /* pink evening sky */
--sky-lavender: 265 30% 62%;        /* twilight lavender */

/* City at night */
--city-light: 45 90% 65%;           /* warm window glow */
--city-neon-far: 185 70% 50%;       /* distant neon haze */
--rooftop-dark: 220 15% 10%;        /* tar paper dark */
```

**Font pairings that fit:**
- **City magazine:** Canela / GT Super style → Playfair Display (headings) + Libre Franklin (body)
- **Skyline editorial:** Montserrat (700, headings) + Nunito Sans (body) — modern urban
- **Wind and light:** Raleway (300, headings) + Lato (body) — airy, open

**NOT a locked theme.** Golden hour gradient works on any warm-ambiance brand. City light bokeh works on any dark urban section. Skyline silhouettes work as decorative footers on any urban product. Wind-blown type works on any outdoor/adventure brand.

**Architectural short-schema:**
```
ROOFTOP PAGE FLOW:
  [Stairwell Exit] — tight, dark entry — the door opens onto sky
    ↓ height vertigo hero: perspective tilt, city below, open sky above
  [The Edge] — primary content, tar paper surface, golden hour backdrop
    ↓ skyline silhouette anchors the bottom, city light bokeh below
  [Open Roof Field] — wide open content, cloud drift background, wind typography
    ↓ water tower silhouette marks section, rooftop railing divides
  [Golden Hour Peak] — maximum color intensity, warmest light, featured content
    ↓ city lights come on below, sky darkens above
  [City Night CTA] — dark sky, city bokeh at maximum, single lit CTA

Wind is always present — slight tilt, drift, gentle movement.
Horizon line is the dominant compositional element.
```

**Sensory anchors:**
- Temperature: Wind chill despite warmth. Sun on face, wind on back.
- Sound: City hum far below, wind, distant traffic, a helicopter, AC units.
- Texture: Rough tar paper, painted metal railing, warm ventilation exhaust.
- Light: Unobstructed golden hour — nowhere to hide from it.
- Smell: Warm asphalt, exhaust from below, food from restaurants at street level.

---

### Library / Archive

Every surface is knowledge. The light is the color of late afternoon and old paper. Hushed purpose. The smell of time. The page is where ideas are stored and retrieved.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Book spine dividers | Vertical element with narrow `width` (8-12px), rich color, slight `border-radius` at top — row of book spines | Section separators, sidebar elements |
| Card catalog grid | Dense `grid` with small, uniform cards — library filing system reference | Feature grids, archive listings |
| Reading lamp spotlight | Off-center radial-gradient: warm amber glow, limited radius, dark periphery — desk lamp cone of light | Feature section backgrounds, cards |
| Paper yellowed texture | `sepia()` filter at 30-50% plus `feTurbulence` noise — aged document surface | Section backgrounds, card fills |
| Dewey decimal typography | Monospace small text labels arranged in hierarchical indentation — classification system visual | Navigation, category labels |
| Leather binding texture | Fine horizontal grain lines (repeating-linear-gradient, 1px, 2% opacity) in deep brown — bookbinding material | Card backgrounds, containers |
| Dust mote particle | Tiny light particles (1-2px) slowly drifting upward, semi-transparent white — undisturbed archive air | Reading lamp sections |
| Margin annotation | Hand-like italic text in pale ink, positioned in `::before` pseudo-element in the margin — scholar's notes | Pull quotes, sidebar content |
| Stack height shadow | Multiple identical `box-shadow` offsets creating paper-stack illusion — books or files stacked | Cards, content blocks |
| Gilt edge | `border-right` or `border-bottom` with gold/amber linear-gradient (3-4px) — gilded page edges | Text blocks, cards |

**Color schema:**
```css
/* Archive atmosphere */
--library-bg: 35 25% 8%;            /* dark wood and shadow */
--library-surface: 38 20% 14%;      /* wood-paneled wall */
--library-fg: 40 25% 85%;           /* lamp-lit reading light |

/* Paper spectrum */
--library-vellum: 45 35% 88%;       /* old vellum page */
--library-parchment: 40 30% 80%;    /* aged parchment */
--library-foxed: 35 25% 70%;        /* foxed/spotted old paper */

/* Book palette */
--library-leather: 20 55% 25%;      /* deep burgundy leather */
--library-spine-red: 5 65% 35%;     /* classic red binding */
--library-spine-green: 155 35% 28%; /* forest green cloth binding */
--library-spine-navy: 220 50% 22%;  /* navy blue binding */
--library-gilt: 42 80% 52%;         /* gilt edge gold */

/* Lamp light */
--library-lamp: 38 85% 55%;         /* warm reading lamp */
--library-shadow: 30 20% 4% / 0.7;  /* deep shelf shadow */
```

**Font pairings that fit:**
- **Scholar's edition:** EB Garamond (headings) + Crimson Text (body) — academic press typography
- **Archive catalogue:** Libre Baskerville (headings) + Lora (body) — catalog card weight
- **Reading room:** Spectral (headings) + Merriweather (body) — long-form contemplative

**NOT a locked theme.** Reading lamp spotlight works on any focused content section. Card catalog grid works on any dense archive or product listing. Paper yellowed texture works on any heritage brand. Book spine dividers work on any vertical navigation system.

**Architectural short-schema:**
```
LIBRARY PAGE FLOW:
  [Entry Hall] — dark wood paneling, reading lamp hero glow, card catalog visible
    ↓ book spine dividers flank content columns, gilt edges appear
  [The Stacks] — primary content, dense grid, dust mote particles in lamplight
    ↓ paper yellowed texture deepens, stack height shadows on cards
  [Reading Room] — long-form or featured content, single reading lamp focus
    ↓ margin annotations appear as scroll depth indicators
  [Special Collections] — most precious content, leather textures, maximum lamplight
    ↓ dewey labels become section navigation
  [The Carrel] — CTA, single lamp, alone with the knowledge, intimate

Sound and pace are both deliberately slow. No urgency. Knowledge waits.
```

**Sensory anchors:**
- Temperature: Warm pockets under lamps, cool shadows in stacks.
- Sound: Page turn, pen scratch, distant cart wheel, hushed voices, clock tick.
- Texture: Leather binding, smooth vellum, gilt edge under thumb, wood reading table.
- Light: Warm incandescent amber in pools, deep shadow between.
- Smell: Lignin decay (old book smell), leather, wood polish, paper, ink.

---

### Museum / Gallery White

The object earns all the attention. Everything else dissolves. Track lighting. Silence. The reverence of the perfectly placed. The page creates the condition for attention.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Spotlight focus | `radial-gradient(circle at 50% 30%, rgba(255,255,255,0) 0%, rgba(0,0,0,0.25) 100%)` inverted — spotlight cone from above onto object | Feature images, hero objects |
| Gallery spacing | `padding: 15vw` or `margin-block: 20vh` — museum-level breathing room between elements | Section spacing |
| Caption plate label | Small monospace text in sans-serif, left-aligned beneath element — exhibition label format | Image captions, feature descriptions |
| Track light shadow | Hard, directional `drop-shadow` (45-degree, 0 blur, dark gray) — track-mounted spot lamp physics | Images, 3D objects, cards |
| White void section | Pure `background: white` with zero decorative elements — the gallery wall IS the design | Background between content |
| Plinth container | Element with subtle bottom `box-shadow` and slight inset `padding` — museum display plinth | Feature content, product showcase |
| Red dot indicator | Small circle (8-12px) in sold/active accent color — gallery sold-dot convention as UI element | Status indicators, active states |
| Conservation glass effect | `backdrop-filter: brightness(1.02)` + very subtle blue tint — glass case over precious object | Feature overlays, hover states |
| Velvet rope path | Dashed or dotted line in warm color connecting flow of content — visitor path through gallery | Scroll progress indicator |
| Reveal with reverence | Single element that fades in slowly (1.5-2s, ease-in) while everything else dims — the unveiling | Hero reveals, feature spotlights |

**Color schema:**
```css
/* Gallery white system */
--gallery-bg: 0 0% 98%;             /* gallery white (slightly warm) */
--gallery-surface: 0 0% 100%;       /* pure display white |
--gallery-wall: 30 5% 94%;          /* warm exhibition wall |
--gallery-fg: 0 0% 12%;             /* deep neutral text */

/* Precise neutrals */
--gallery-caption: 0 0% 35%;        /* caption gray |
--gallery-border: 0 0% 88%;         /* minimal separator */
--gallery-shadow: 0 0% 0% / 0.12;   /* soft track shadow */

/* Accent (used extremely sparingly) */
--gallery-red-dot: 5 80% 48%;       /* sold dot red */
--gallery-signal: 220 70% 45%;      /* institutional blue — labels |
--gallery-gold: 42 70% 48%;         /* award/highlight gold */

/* Track lighting warmth */
--gallery-spot: 38 60% 75% / 0.15;  /* warm spot glow overlay */
--gallery-dark: 220 10% 8%;         /* dark gallery variant bg */
```

**Font pairings that fit:**
- **Museum identity:** Neue Haas Grotesk style → Inter (headings + body, different weights) — Swiss neutrality
- **Institutional authority:** Garamond Premier → EB Garamond (headings) + Source Sans 3 (body)
- **Contemporary gallery:** DM Sans (headings, light) + DM Serif Display (body) — modern institutional

**NOT a locked theme.** Spotlight focus works on any product hero. Gallery spacing works on any luxury or premium site. Caption plate labels work on any factual content presentation. Track light shadow works on any object-on-white photography.

**Architectural short-schema:**
```
GALLERY PAGE FLOW:
  [Entrance Hall] — pure white, single object in spotlight, absolute silence
    ↓ reveal with reverence — slow fade, no hurry
  [First Gallery] — curated grid, track light shadows on each item, caption plates
    ↓ gallery spacing between rooms — the walk matters
  [The Feature Room] — single hero object, plinth container, velvet rope path
    ↓ conservation glass effect on hover, red dot if exclusive/sold
  [Collection Overview] — broader grid, white void sections between groups
    ↓ lighting changes rooms — different accent warmth per gallery
  [Exit Gift / Archive] — CTA, minimal, institutional — never pushy in a museum

Silence is a design element. Competing for attention is forbidden.
Every element is chosen; nothing decorative exists without purpose.
```

**Sensory anchors:**
- Temperature: Climate-controlled cool. Precise. For the object's benefit, not yours.
- Sound: Shoe squeak on polished concrete, low ventilation hum, whispered conversation.
- Texture: Smooth painted wall, polished concrete or parquet, glass case edge.
- Light: Track-mounted halogen/LED — warm, directional, focused exclusively on objects.
- Smell: Neutral air, slight polish, climate control — the absence of smell is institutional.

---

## Mixes Well With

| Urban Theme | Pairs With | Result |
|-------------|-----------|--------|
| Neon Tokyo | Dark Premium glass | Frosted glass cards in neon-lit rain |
| Industrial Warehouse | Brutalist Concrete | Maximum raw material honesty |
| Art Deco Lobby | Library Archive | Gilded knowledge palace |
| Gothic Cathedral | Forest (forest file) | Sacred grove, ancient and vertical |
| Mediterranean Santorini | Silk Fabric (material file) | Luxury coastal resort |
| Moroccan Riad | Ceramic Pottery (material file) | Full sensory tile and glaze richness |
| Japanese Zen Garden | Paper Origami (material file) | Folded stillness |
| Abandoned Decay | Rust Patina (material file) | Maximum oxidation and entropy |
| Rooftop Skyline | Chrome Metal (material file) | High-altitude mirror steel |
| Library Archive | Leather Hide (material file) | Bound knowledge, aged luxury |
| Museum Gallery | Marble Stone (material file) | Precious objects on veined white |
| Brutalist Concrete | Industrial Warehouse | Honest structure at every scale |
