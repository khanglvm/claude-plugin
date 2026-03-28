# Material & Texture Inspiration Themes

Ten ingredient palettes translated from physical materials into composable CSS. Every texture carries memory, weight, and temperature. Touch it through the screen.

---

### Marble / Stone

The vein is not a flaw — it is the signature of pressure, time, and mineral migration. Cut it open and find complexity. Polish it and find depth that shifts with the light.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Marble vein pattern | SVG `<path>` with irregular organic stroke (2-4px, opacity 30-50%) crossing surface diagonally — vein trajectory, not straight line | Container backgrounds, hero sections |
| Polished reflection highlight | `linear-gradient(125deg, transparent 30%, rgba(255,255,255,0.12) 50%, transparent 70%)` — sheen of polished stone | Card surfaces, feature panels |
| Chiseled edge container | `clip-path: polygon(4px 0%, 100% 0%, calc(100% - 4px) 100%, 0% 100%)` — slight angled cut at all corners | Containers, buttons, cards |
| Stone grain background | `feTurbulence baseFrequency="0.015" numOctaves="8"` + high contrast `feColorMatrix` for color, low for neutral stone — crystalline structure | Section backgrounds |
| Veining color shift | `background: linear-gradient(to right, hsl(200,8%,85%), hsl(195,12%,92%), hsl(200,8%,85%))` with vein SVG overlay — surface tonal variation | Wide content panels |
| Cool weight typography | High-contrast serif with `letter-spacing: 0.08em`, uppercase — letterforms carved into stone | Display headings |
| Inlay accent | Geometric `clip-path` shape filled with contrasting marble color — inlaid stone decoration | Dividers, logo areas, CTA backgrounds |
| Subsurface light | `radial-gradient` from center: slightly lighter hue bleeding outward — translucency in alabaster or onyx | Thin stone panel effect |
| Slab joint line | 1px `border-bottom` or `box-shadow: 0 1px 0` in slightly different tone — where slabs meet | Section dividers, horizontal rules |
| Honed vs polished states | Base state: flat/matte surface (no reflection sheen). Hover/focus state: polished sheen gradient appears — material responds to touch | Interactive containers, buttons |

**Color schema (stone variety dial):**
```css
/* Carrara White */
--marble-carrara-bg: 210 5% 94%;    /* cool white marble */
--marble-carrara-vein: 210 8% 72%;  /* gray vein */
--marble-carrara-shadow: 210 10% 55%;

/* Nero Marquina (black) */
--marble-nero-bg: 215 10% 8%;       /* near-black stone */
--marble-nero-vein: 45 60% 75%;     /* gold vein through black */
--marble-nero-sheen: 210 5% 15%;    /* polished surface */

/* Rose / Blush */
--marble-rose-bg: 10 15% 88%;       /* blush pink marble */
--marble-rose-vein: 5 30% 65%;      /* deeper rose vein */
--marble-rose-fg: 0 0% 12%;         /* dark text on light stone */

/* Verde Antico */
--marble-verde-bg: 155 15% 28%;     /* verde antico base */
--marble-verde-vein: 40 40% 70%;    /* cream vein through green */

/* Universal */
--stone-cool: 210 8% 60%;           /* neutral mid-tone stone */
--stone-shadow: 215 12% 25%;        /* deep cut shadow */
```

**Font pairings that fit:**
- **Monument inscription:** Cinzel (headings) + EB Garamond (body) — Roman carved stone
- **Luxury editorial:** Cormorant Garamond (display) + Libre Baskerville (body) — slab-weight serif
- **Contemporary stone:** DM Serif Display (headings) + DM Sans (body) — modern materiality

**NOT a locked theme.** Marble vein SVG patterns work on any luxury background. Chiseled edge clip-paths work on any strong editorial container. Polished sheen gradients work on any premium dark surface. Cool weight typography works on any monument-scale heading.

**Architectural short-schema:**
```
MARBLE PAGE FLOW:
  [Quarry Face] — raw stone texture, unpolished — the material revealed
    ↓ vein SVG paths resolve into surface, detail emerges
  [Cut and Polished] — hero content on honed marble, polished sheen on cards
    ↓ inlay accents mark transitions, cool weight typography dominates
  [The Slab Room] — full-width marble panels, slab joints as section dividers
    ↓ subsurface light effect on featured content — stone glows from within
  [Sculptural Zone] — chiseled edges on all containers, shadow depth increases
    ↓ warm accent marble (rose or verde) enters as counterpoint
  [The Pedestal] — CTA on clean white Carrara, nothing competes with the object

Weight and permanence. Nothing here feels light or temporary.
```

**Sensory anchors:**
- Temperature: Cold surface that warms slowly under your hand.
- Sound: Footstep echo, chisel ring, stone-on-stone, hollow under polish.
- Texture: Smooth-beyond-smooth polished face, rough-cut quarry edge.
- Light: Reflective, directional, cool undertone despite warm hue.
- Smell: Mineral cold, stone dust from cutting, faint dampness in veins.

---

### Wood Grain / Timber

Growth rings are autobiography. Each ring is one year of drought, flood, fire, and calm. Cut it across the trunk and read time. Sand it and smell twenty years of rain.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Wood grain texture | `feTurbulence type="turbulence" baseFrequency="0.01 0.2"` + warm brown `feColorMatrix` — elongated cellular grain | Surface backgrounds, containers |
| End grain circle | Radial concentric rings (SVG `<circle>` elements or `conic-gradient` sector alternation) — cross-section of timber | Circular decorative elements, logos |
| Plank layout container | CSS grid with `gap: 2-4px` and alternating-tone backgrounds — floor or wall planks | Content grids, section backgrounds |
| Knot hole accent | Circular SVG with concentric ovoid rings, darker center — natural knot in timber | Decorative background accents |
| Cross-grain shadow | Strong `box-shadow` perpendicular to grain direction — shadow across wood surface | Raised elements on wood backgrounds |
| Sawdust particle | Tiny warm-toned dots (1-3px) falling slowly with gentle drift — light wood particles | Dark background sections |
| Oiled finish sheen | Thin `linear-gradient` along grain direction (darker at edges, lighter at center) — oil-finished wood lustre | Card surfaces, table surfaces |
| Wood burn text | `text-shadow` with dark amber values, slight soft blur (1-2px) — pyrography mark in wood | Small accent text labels |
| Grain direction change | Adjacent elements with perpendicular grain texture orientation — parquet or board-and-batten | Tiled backgrounds, floor references |
| Age check crack | Thin 1px hairline SVG path along grain direction — checking crack as wood dries | Background aging details |

**Color schema (wood species dial):**
```css
/* Oak (warm, medium) */
--wood-oak-light: 35 40% 70%;       /* golden oak highlight */
--wood-oak-mid: 32 50% 52%;         /* primary oak tone */
--wood-oak-dark: 28 55% 32%;        /* shadow in grain */

/* Walnut (dark, rich) */
--wood-walnut-light: 28 35% 38%;    /* lighter walnut grain */
--wood-walnut-mid: 22 45% 22%;      /* deep walnut base */
--wood-walnut-dark: 18 40% 12%;     /* shadow in walnut */

/* Pine (pale, Nordic) */
--wood-pine-light: 48 55% 82%;      /* pale pine knot */
--wood-pine-mid: 42 45% 68%;        /* mid pine */
--wood-pine-dark: 38 40% 48%;       /* resin-darkened grain */

/* Ebony (very dark) */
--wood-ebony: 220 12% 8%;           /* near-black ebony */
--wood-ebony-grain: 220 10% 14%;    /* barely-visible grain */

/* Universal accents */
--wood-resin: 38 70% 45%;           /* amber resin fill */
--wood-endgrain-ring: 30 30% 35%;   /* growth ring line */
```

**Font pairings that fit:**
- **Craftsman:** Zilla Slab (headings) + Source Serif 4 (body) — woodworker's catalog
- **Nordic timber:** Cabin (headings) + Nunito (body) — Scandinavian warm simplicity
- **Heritage joinery:** Playfair Display (headings) + Lora (body) — furniture maker tradition

**NOT a locked theme.** Wood grain texture works on any warm organic background. Plank layout works on any grid-based content section. Sawdust particles work on any artisan/craft brand. End grain circles work on any heritage brand logo treatment.

**Architectural short-schema:**
```
WOOD PAGE FLOW:
  [The Raw Log] — unfinished surface, visible grain direction, knot accents
    ↓ sawdust particles settle, texture resolves into finished surface
  [The Workshop Table] — primary content on plank layout, oiled finish sheen
    ↓ cross-grain shadow deepens on scroll, wood burn labels appear
  [The Paneled Room] — secondary content, alternating grain direction panels
    ↓ age check cracks visible in deeper sections
  [The Display Case] — precious content on polished walnut, maximum grain depth
    ↓ end grain accents as section markers
  [The Porch] — CTA, outdoor pine light, lighter tone, open feeling

Warmth is the dominant experience. Nothing cold or digital feels right here.
```

**Sensory anchors:**
- Temperature: Warm to the touch. Absorbs and radiates gentle heat.
- Sound: Hollow knock, creak under weight, plane-shaving hiss, grain against sandpaper.
- Texture: Smooth-with-direction — you feel the grain even on polished surfaces.
- Light: Absorbs light warmly, oiled grain catches it sideways.
- Smell: Fresh cut is intoxicating. Aged is dusty, resinous, woody.

---

### Leather / Hide

It was alive. It holds the shape of what it protected. Scratches tell history. Polish returns youth temporarily. The page knows it's durable, and doesn't need to prove it.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Leather grain texture | Fine `feTurbulence` at very high frequency (1.2-1.8) and low contrast — pebbled pore texture | Container backgrounds, card fills |
| Stitch border | `border: 2px dashed` in contrasting thread color (cream on dark leather, dark on tan) + `border-radius: 4px` — saddle-stitch seam | Card borders, container edges |
| Embossed text | `text-shadow: 1px 1px 0 rgba(0,0,0,0.5), -1px -1px 0 rgba(255,255,255,0.1)` — pressed-into-leather lettering | Headings on leather surfaces |
| Debossed container | `box-shadow: inset 0 2px 6px rgba(0,0,0,0.4), inset 0 -1px 2px rgba(255,255,255,0.05)` — tooled depression in leather | Featured content boxes |
| Patina gradient | Darker at edges, lighter at center — `radial-gradient` — worn patina from handling | Card surfaces, panel backgrounds |
| Buckle clasp interaction | SVG buckle/clasp that animates (rotates 90deg, "releases") on section entry — fastening hardware | Section transitions, reveal animations |
| Crease line | Diagonal or curved 1-2px line with slight shadow — leather fold crease | Background detail elements |
| Color rub-off | Lighter area near corner/edge — `radial-gradient` spot of lighter hue at corners — natural wear | Container corners |
| Burnished edge | Inner `box-shadow` with warm amber on all 4 sides, 3-4px spread — edge finishing technique | Cards, buttons, containers |
| Wax polish sheen | High-specular `radial-gradient` highlight spot in warm off-white at 15-25% opacity — freshly polished surface | Hover states, featured elements |

**Color schema (leather type dial):**
```css
/* Tan / Saddle */
--leather-tan: 32 55% 52%;          /* classic saddle tan */
--leather-tan-shadow: 25 55% 32%;   /* oiled shadow */
--leather-tan-highlight: 40 50% 70%; /* worn highlight */

/* Burgundy / Oxblood */
--leather-oxblood: 5 60% 25%;       /* deep oxblood */
--leather-oxblood-worn: 8 50% 35%;  /* lighter worn area */
--leather-oxblood-shadow: 0 50% 12%; /* deep shadow crease */

/* Black (patent or matte) */
--leather-black: 220 10% 8%;        /* matte black leather */
--leather-black-sheen: 220 8% 18%;  /* slight surface lift */

/* Caramel / Honey */
--leather-caramel: 35 65% 48%;      /* warm caramel */
--leather-caramel-dark: 30 60% 30%; /* aged caramel shadow */

/* Stitching */
--leather-stitch-cream: 45 40% 82%; /* cream saddle stitch */
--leather-stitch-wax: 35 50% 55%;   /* waxed thread amber */
```

**Font pairings that fit:**
- **Saddlery:** Abril Fatface (display) + Libre Baskerville (body) — heritage brand
- **Atelier:** Fraunces (headings) + Lato (body) — luxury goods craftsmanship
- **Equestrian:** Playfair Display (headings) + Source Sans 3 (body) — traditional but refined

**NOT a locked theme.** Stitch borders work on any artisan/craft brand. Patina gradients work on any aged-luxury surface. Embossed text works on any dark surface where depth matters. Debossed containers work on any premium featured content box.

**Architectural short-schema:**
```
LEATHER PAGE FLOW:
  [The Hide] — raw grain texture, natural color variation, no polish
    ↓ stitch borders appear on containers, seam detail resolves
  [The Workshop] — primary content, embossed headings, debossed feature boxes
    ↓ patina gradients deepen, crease lines appear in background
  [The Finished Piece] — curated secondary content, burnished edges, stitch detail
    ↓ buckle clasp animations mark section transitions
  [The Vault] — precious content, maximum polish sheen on hover, oxblood depth
    ↓ wax polish sheen animates across featured surface
  [The Showroom] — CTA, single perfect piece on clean surface, nothing competes

Age and wear are features, not flaws. The patina is the selling point.
```

**Sensory anchors:**
- Temperature: Neutral to slightly warm. Adjusts to body temperature quickly.
- Sound: Creak under stress, soft thud of thick hide, buckle click, zipper slide.
- Texture: Smooth with pore memory — pebbled, directional, slightly yielding.
- Light: Absorbs in matte areas, sharp specular in polished areas.
- Smell: Tannery memory. Complex, animal, earthy, wax and oil.

---

### Silk / Fabric

It moves. Drape is function made beautiful. The same surface can be pooled soft or stretched taut. Light hitting silk at one angle versus another transforms the color entirely — and so does this page.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Fabric wave animation | `@keyframes` alternating `skewX(0.5deg) scaleY(1.002)` to `skewX(-0.5deg) scaleY(0.998)` at 4-6s — subtle fabric breathing | Background elements, full sections |
| Silk sheen gradient | `linear-gradient(135deg, transparent 0%, rgba(255,255,255,0.18) 50%, transparent 100%)` with `background-size: 200% 200%` animated `background-position` — sheen slides across surface | Card hover states, hero backgrounds |
| Drape shadow | Concave gradient: `radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.12) 100%)` — fabric hanging between points | Section backgrounds, wide panels |
| Gather point | Radiating `conic-gradient` or SVG lines converging at a point — fabric gathered and tied | Decorative focal points, hero accents |
| Thread line border | 0.5px `border` with slightly warm or cool tint versus background — single thread definition | Container edges, dividers |
| Color-shift sheen | `hue-rotate` animation (+-5deg) on silk elements — color depends on light angle | Accent containers, hover states |
| Taffeta crinkle | `feTurbulence` at medium-high frequency over silk surface — slightly crinkled raw silk | Background texture variation |
| Hem fold | Thin dark line (1-2px) at bottom of element with slight shadow below — finished hem detail | Card bases, section bottoms |
| Woven pattern | `background-image: repeating-linear-gradient(0deg, ...)` + `repeating-linear-gradient(90deg, ...)` at very low opacity — warp and weft | Section backgrounds |
| Cascade drape reveal | Content animates down from top-fold with slight easing — fabric unrolling to reveal content | Section entry animations |

**Color schema (silk variety dial):**
```css
/* Ivory silk */
--silk-ivory: 45 35% 94%;           /* raw silk cream */
--silk-ivory-sheen: 50 25% 98%;     /* sheen highlight */
--silk-ivory-shadow: 35 20% 75%;    /* drape shadow in ivory */

/* Deep jewel tones */
--silk-sapphire: 225 65% 38%;       /* deep sapphire silk */
--silk-ruby: 355 60% 35%;           /* deep ruby silk */
--silk-emerald: 150 50% 30%;        /* deep emerald silk */
--silk-amethyst: 280 50% 38%;       /* deep amethyst silk */

/* Pale pastels */
--silk-blush: 350 40% 88%;          /* blush pink */
--silk-celadon: 165 25% 78%;        /* soft celadon green */
--silk-periwinkle: 225 40% 78%;     /* soft periwinkle */

/* Metallic silk */
--silk-gold-lame: 42 80% 62%;       /* gold lame */
--silk-silver: 220 15% 78%;         /* silver silk */

/* Universal shadow */
--silk-shadow: 240 20% 20% / 0.15;  /* cool drape shadow */
```

**Font pairings that fit:**
- **Couture:** Cormorant Garamond (display italic) + Raleway (300, body) — fashion house delicacy
- **Bridal:** Gilda Display (headings) + Lato (200/300, body) — light as silk
- **Editorial fashion:** Libre Caslon Display (headings) + Source Sans 3 (body) — Vogue weight

**NOT a locked theme.** Fabric wave animations work on any soft, organic brand. Silk sheen gradients work on any luxury hover state. Drape shadows work on any wide background panel. Thread line borders work on any refined container definition.

**Architectural short-schema:**
```
SILK PAGE FLOW:
  [The Bolt] — fabric unrolling — cascade drape reveal of hero
    ↓ fabric wave begins, sheen slides across background
  [The Drape] — primary content, gather points mark key sections
    ↓ jewel tone shifts — color-shift sheen on featured elements
  [The Fitting Room] — secondary content, intimate, soft — blush or ivory palette
    ↓ woven pattern visible in background, thread line borders
  [The Gown] — hero product/content, maximum sheen animation, metallic silk accent
    ↓ hem fold at section bases, taffeta crinkle texture
  [The Atelier] — CTA, single gathering point, gathered silk around the offer

Movement is the defining quality. Stillness is the exception.
```

**Sensory anchors:**
- Temperature: Body-warm almost instantly. Light weight belies warmth.
- Sound: Whisper of fabric moving, rustle under fingers, swish of hem.
- Texture: Impossibly smooth, cool at first touch, then warm. Slight resistance.
- Light: Directional and dramatic — a slight angle change transforms the color.
- Smell: Faint natural fiber, subtle dye, dry-cleaned freshness, atelier air.

---

### Paper / Origami

Flat surface with infinite dimensional potential. One fold changes everything. Creases hold memory. The page knows it started as a blank sheet and became something through intention.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Fold shadow | `box-shadow: 3px 3px 8px rgba(0,0,0,0.15), -1px -1px 3px rgba(0,0,0,0.08)` — shadow at fold edge creates dimensional paper illusion | Cards, containers, panels |
| Paper stack elevation | Multiple stacked `box-shadow` offsets (3px, 6px, 9px steps) in slightly different tones — layers of paper | Card groups, document stacks |
| Origami unfold reveal | `clip-path: polygon()` transforms from folded triangle/shape to full rectangle on scroll — paper unfolding | Section entry animations |
| Torn edge mask | Irregular SVG `clipPath` with jagged, hand-torn edge profile — paper torn apart | Image edges, section borders |
| Crease line divider | 1px line with `box-shadow` on one side only (depth of valley fold) — single paper crease | Section separators |
| Paper grain surface | `feTurbulence baseFrequency="0.65"` at 3-5% opacity on white/cream — paper fiber texture | Background surfaces |
| Corner curl | Pseudo-element `::after` with `border-radius: 0 0 0 100%` and shadow — page corner lifting | Interactive cards |
| Paper crane silhouette | SVG origami crane shape as decorative element — universal origami icon | Background art, section markers |
| Color block fold | Solid-color geometric fold patterns (triangles, diamonds) — flat origami geometry | Section backgrounds, cards |
| Pulp color variation | Subtle irregular patches of slightly different tone — handmade paper variation | Artisan backgrounds |

**Color schema (paper type dial):**
```css
/* White printer paper */
--paper-white: 0 0% 98%;            /* clean white */
--paper-white-shadow: 210 5% 88%;   /* cool paper shadow */
--paper-white-crease: 210 8% 78%;   /* fold crease line */

/* Craft / Kraft */
--paper-kraft: 35 45% 72%;          /* unbleached kraft */
--paper-kraft-dark: 30 40% 55%;     /* aged kraft shadow */
--paper-kraft-grain: 32 35% 60%;    /* kraft texture mid */

/* Origami spectrum */
--origami-red: 5 80% 52%;           /* origami red */
--origami-blue: 215 65% 48%;        /* origami blue */
--origami-yellow: 48 90% 58%;       /* origami yellow */
--origami-green: 145 55% 42%;       /* origami green */

/* Aged/Antique paper */
--paper-antique: 45 30% 82%;        /* yellowed old paper */
--paper-foxed: 32 25% 72%;          /* foxed/spotted age */
--paper-vellum: 42 35% 90%;         /* translucent vellum */

/* Ink on paper */
--paper-ink: 220 20% 15%;           /* blue-black ink */
--paper-pencil: 210 8% 45%;         /* graphite pencil */
```

**Font pairings that fit:**
- **Handmade press:** Lora (headings) + Merriweather (body) — letterpress weight
- **Origami minimal:** Nunito (300-400 weight, both) — clean, folded simplicity
- **Paper craft editorial:** Libre Baskerville (headings) + Crimson Text (body) — printed and precious

**NOT a locked theme.** Fold shadows work on any card element as a depth system. Paper stack elevation works on any layered content. Torn edge masks work on any organic brand's image treatment. Origami unfold reveals work on any section entry animation.

**Architectural short-schema:**
```
PAPER PAGE FLOW:
  [The Blank Sheet] — pure white hero, single crease line bisects it — potential
    ↓ paper grain resolves, first fold shadow appears
  [First Fold] — origami unfold reveals primary content
    ↓ color block folds as section backgrounds, stacking elevation
  [The Folding Table] — secondary content, crease line dividers, paper stack depth
    ↓ torn edge masks on images, craft paper shift
  [The Creation] — finished origami form — feature content as fully revealed shape
    ↓ paper crane silhouette marks completion
  [The Gift] — CTA on kraft paper, corner curl on the offer — wrapped for giving

Each section is a fold. The page is being built as you scroll.
```

**Sensory anchors:**
- Temperature: Neutral, slightly cool. No thermal memory.
- Sound: Crisp fold crack, paper slide, tearing, crinkle, printer hum.
- Texture: Smooth face with grain memory — tooth catches ink.
- Light: Diffuse reflection, no specular — paper absorbs more than it reflects.
- Smell: Fresh print chemical (new), vanilla-lignin (old), wet pulp (handmade).

---

### Chrome / Metal

Mirror finish. Your reflection but not quite right — elongated, color-shifted. Hard. Cold. Precise. The page does not bend. The page does not apologize.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Chrome reflection gradient | `linear-gradient(180deg, hsl(220,10%,90%) 0%, hsl(220,15%,55%) 30%, hsl(220,10%,85%) 50%, hsl(220,15%,40%) 70%, hsl(220,10%,75%) 100%)` — multi-band metallic gradient | Surfaces, buttons, containers |
| Brushed metal texture | `feTurbulence type="turbulence" baseFrequency="0.01 0.8" numOctaves="2"` + directional `feBlend` — unidirectional brushed grain | Metal panel backgrounds |
| Rivet dot pattern | Repeating `radial-gradient` dots (6-8px, 60px grid) at low opacity — mechanical fastener grid | Surface backgrounds |
| Metallic sheen on hover | `background-position` animation from `0% 50%` to `100% 50%` on gradient — light catching metal as it moves | Interactive elements |
| Cold specular highlight | Single-pixel horizontal white line in reflection gradient — razor-edge specular | Metal edges, beveled borders |
| Bevel edge | `box-shadow: 1px 1px 0 rgba(255,255,255,0.3), -1px -1px 0 rgba(0,0,0,0.4)` — machined bevel at container edge | Buttons, panels, containers |
| Anodized color layer | `hue-rotate` on top of chrome gradient — titanium, rose gold, or blue anodize | Accent elements, feature panels |
| Reflective elongation | `scaleY(0.15)` reflection below element, heavily `blur(3px)`, opacity 20% — elongated metal-surface reflection | Feature images, hero elements |
| Knurled texture | Dense `conic-gradient` diamond repeat — finger-grip knurling pattern | Grip zone backgrounds, button textures |
| Machine tolerance gap | `gap: 1px` between grid cells with `background: var(--chrome-dark)` showing — mechanical precision | Grid layouts, panels |

**Color schema (metal finish dial):**
```css
/* Polished chrome */
--chrome-high: 220 8% 95%;          /* highlight band */
--chrome-mid: 220 12% 68%;          /* mid reflection */
--chrome-low: 220 15% 35%;          /* shadow reflection */
--chrome-dark: 220 18% 12%;         /* deep shadow */

/* Brushed steel */
--steel-light: 210 10% 78%;         /* light brushed */
--steel-mid: 210 10% 55%;           /* mid brushed steel */
--steel-dark: 215 12% 25%;          /* dark steel */

/* Anodized titanium */
--titanium-blue: 210 40% 55%;       /* blue anodize */
--titanium-purple: 265 35% 48%;     /* purple anodize */
--titanium-gold: 42 55% 55%;        /* gold anodize */

/* Rose gold */
--rose-gold: 18 55% 65%;            /* rose gold highlight */
--rose-gold-deep: 15 50% 42%;       /* deep rose gold */

/* Universal */
--metal-void: 220 15% 5%;           /* pure dark metal shadow */
```

**Font pairings that fit:**
- **Precision machine:** Space Grotesk (headings) + IBM Plex Mono (body) — engineered exactness
- **Luxury hardware:** Futura PT (headings) + Barlow (body) — Swiss watch face
- **Cold editorial:** Bebas Neue (headings) + Inter (body) — cold modernism

**NOT a locked theme.** Chrome gradients work on any premium dark product site. Bevel edges work on any button or interactive element that needs tactile feedback. Brushed metal works on any industrial/precision background. Metallic sheen on hover works on any element that should feel physically responsive.

**Architectural short-schema:**
```
CHROME PAGE FLOW:
  [Cold Surface] — chrome gradient background, hard-cut entry, no softness
    ↓ brushed metal texture resolves, cold specular edge catches first
  [The Machine Room] — primary content on precision grid, machine tolerance gaps
    ↓ rivet patterns appear, bevel edges on all containers
  [The Mirror] — secondary content, reflective elongation below featured elements
    ↓ anodized color accent enters — single warm note in cold field
  [The Blade] — feature content, maximum chrome sheen, knurled texture accents
    ↓ metallic sheen animation on hover, every surface responds
  [The Function] — CTA, precise, bevel-edged, chromed — pure functional object

No warmth. No apology. The material is the message.
```

**Sensory anchors:**
- Temperature: Cold. Remains cold. Chrome does not warm to you.
- Sound: Click of machined parts, high-ring when struck, precision quiet otherwise.
- Texture: Smooth as liquid in polished areas, directional in brushed areas.
- Light: Specular, hard, directional — one bad angle and it blinds.
- Smell: Machine oil, ozone, metal tang on wet fingers.

---

### Ceramic / Pottery

Hand-shaped means no two are identical. The glaze pooled at the base. The kiln darkened one edge. These imperfections are the entire point — proof that human hands made it.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Glaze drip gradient | `linear-gradient` from opaque color at top to semi-transparent at bottom with irregular soft stop — glaze running down surface | Container backgrounds, section panels |
| Pottery wheel radius | Extreme `border-radius` variation (`60% 40% / 45% 55%`) — wheel-shaped organic roundness | Cards, containers, images |
| Crackle glaze texture | SVG network of fine irregular polygons with visible `stroke` — crazing in glaze surface | Overlay textures |
| Kiln fire accent | Toasted warm edge — `radial-gradient` from corner in deep amber/brown — heat mark from kiln contact | Container edges, image corners |
| Thumb indentation | `box-shadow: inset 2px 3px 8px rgba(0,0,0,0.2)` — finger press into clay body | Interactive containers, focus states |
| Glaze color pooling | Darker gradient pool at bottom of element — glaze gravity obeying physics | Card bottoms, section bases |
| Matte vs glossy zones | `background: hsl(...)` (matte) versus `background: linear-gradient(hsl(...), hsl(...))` (gloss) alternate on same element — uneven glaze coverage | Card surfaces |
| Thrown rim detail | Top `border` with slight variation — irregular rim of thrown vessel | Container top edges |
| Raku reduction pattern | Irregular dark patches (SVG organic shapes) at low opacity — smoke reduction marks | Dramatic background overlays |
| Celadon whisper | Very pale blue-green tint at very low saturation — Song Dynasty celadon glaze | Light background sections |

**Color schema (glaze type dial):**
```css
/* Celadon (Song Dynasty) */
--ceramic-celadon: 165 20% 72%;        /* pale jade green */
--ceramic-celadon-shadow: 165 25% 52%; /* deeper celadon depth */

/* Cobalt blue and white */
--ceramic-cobalt: 220 70% 35%;         /* cobalt blue glaze */
--ceramic-white-body: 35 15% 92%;      /* porcelain body white */

/* Terracotta earthenware */
--ceramic-terracotta: 18 65% 48%;      /* fired clay orange */
--ceramic-terra-shadow: 15 55% 30%;    /* shadow on earthenware */

/* Raku (dramatic contrast) */
--ceramic-raku-light: 45 20% 85%;      /* copper matte light */
--ceramic-raku-dark: 25 15% 12%;       /* carbon black raku */

/* Ash glaze */
--ceramic-ash: 100 15% 65%;            /* wood ash gray-green */
--ceramic-ash-dark: 95 12% 42%;        /* deeper ash glaze */

/* Kiln marks */
--ceramic-kiln-mark: 28 60% 28%;       /* where kiln touched */
--ceramic-flux: 35 40% 78%;            /* over-fired flux blush */
```

**Font pairings that fit:**
- **Studio pottery:** Crimson Pro (headings) + Nunito (300-400, body) — handmade warmth
- **Japanese ceramics:** Noto Serif JP (headings) + Noto Sans (body) — wabi-sabi precision
- **Contemporary craft:** Fraunces (headings) + DM Sans (body) — artisan modern

**NOT a locked theme.** Glaze drip gradients work on any artisan/craft brand section. Pottery wheel radius (extreme border-radius) works on any organic brand's containers. Thumb indentation box-shadow works on any interactive element. Kiln fire accents work on any warm-toned corner treatment.

**Architectural short-schema:**
```
CERAMIC PAGE FLOW:
  [The Clay] — unglazed earthenware tone, terracotta body, no surface treatment
    ↓ first glaze appears — drip gradient begins at section top
  [The Wheel] — primary content, pottery wheel radius on containers, organic forms
    ↓ cobalt blue pattern emerges on white body surface
  [The Kiln] — firing zone — raku reduction patches, kiln fire edges warm
    ↓ crackle glaze texture on secondary backgrounds
  [The Finished Vessel] — precious content, full glaze, celadon or cobalt, matte vs glossy
    ↓ thumb indentation on interactive elements, natural handling
  [The Table] — CTA, single vessel on clean surface, object-forward presentation

No perfect circles. No exact symmetry. The variation IS the quality mark.
```

**Sensory anchors:**
- Temperature: Body-warm when held. Cool when set down. Intimate weight.
- Sound: Clay slap, wheel hum, hollow thud when tapped, crockery click.
- Texture: Smooth glazed face, rough unglazed foot ring, glaze edge transition.
- Light: Diffuse off glaze, absorbed into matte — shifts dramatically under raking light.
- Smell: Wet clay, wood fire kiln, mineral iron oxide, cool earthenware.

---

### Rust / Patina

Time wrote this. Iron met oxygen met water and produced something richer than the original. Every shade of orange means a different year. The green patina on copper means decades of weather.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Rust bleed gradient | `radial-gradient` from fastener point: orange-red to burnt umber to dark iron — oxidation spreading from origin | Container corners, structural joints |
| Patina green overlay | `mix-blend-mode: color` or opacity overlay in desaturated verdigris — copper oxidation layer | Overlay effects on metal elements |
| Pitting texture | `feTurbulence` at high frequency + `feDisplacementMap` — pockmarked surface corrosion | Surface backgrounds |
| Oxidation spread animation | `clip-path` or `background-size` growing from corner — animated rust spreading on scroll | Section transitions, hover states |
| Blister layer | Raised bubble shapes (small circles with `box-shadow`) at irregular intervals — paint blistering over rust | Background texture details |
| Scale flake | Irregular jagged shapes lifting from surface — `clip-path` with lifted edges, slight shadow | Foreground texture elements |
| Iron stain streak | Vertical `linear-gradient` of rust color at 20-40% opacity — water carrying iron oxide down surface | Background overlays |
| Copper green drip | `linear-gradient` top-to-bottom in verdigris tones — patina dripping down | Section backgrounds, container tops |
| Raw iron surface | Very dark, near-black brown with slight red undertone — un-oxidized iron base | Dark section backgrounds |
| Structural joint rust | Concentrated rust `box-shadow` centered on structural junctions — where fasteners were | Grid intersections, card corners |

**Color schema (corrosion stage dial):**
```css
/* Fresh rust (early stage) */
--rust-fresh: 18 85% 48%;           /* bright new rust orange */
--rust-fresh-light: 28 75% 62%;     /* pale early oxidation */

/* Aged rust (mid stage) */
--rust-aged: 15 70% 35%;            /* deep mid-age rust */
--rust-aged-dark: 10 60% 22%;       /* brown old rust */

/* Deep corrosion (late stage) */
--rust-deep: 8 55% 18%;             /* deep iron brown */
--rust-base: 5 30% 12%;             /* raw iron under rust */

/* Copper patina */
--patina-light: 160 30% 55%;        /* early verdigris */
--patina-mid: 165 40% 38%;          /* mature patina */
--patina-dark: 170 45% 22%;         /* deep aged copper */

/* Mixed metals */
--bronze-oxidized: 30 35% 35%;      /* oxidized bronze */
--brass-tarnished: 42 40% 40%;      /* tarnished brass */

/* Environmental */
--rust-sky: 210 25% 18%;            /* industrial gray sky */
```

**Font pairings that fit:**
- **Industrial age:** Oswald (headings) + Barlow (body) — factory floor utility
- **Salvage yard:** Anton (headings) + Courier Prime (body) — stenciled metal marking
- **Weathered craft:** Alfa Slab One (headings) + Source Sans 3 (body) — cast iron weight

**NOT a locked theme.** Rust bleed gradients work on any industrial/aged aesthetic. Oxidation spread animations work on any dramatic section reveal. Iron stain streaks work on any dark atmospheric background. Patina green overlays work on any architectural/outdoor material brand.

**Architectural short-schema:**
```
RUST PAGE FLOW:
  [The Iron Surface] — raw iron base, dark and dense — before oxidation begins
    ↓ first rust spots appear at corners, bleed gradients spread
  [Year One] — light rust, bright orange-red, still structural integrity
    ↓ pitting texture resolves, blister layers form
  [Decades Pass] — primary content in deep rust territory, aged iron tones
    ↓ patina green enters on copper elements, oxidation spread animations
  [The Sculpture] — beauty is undeniable now — the corrosion IS the aesthetic
    ↓ structural joint rust marks every intersection, iron streaks on background
  [Still Standing] — CTA, deep rust patina, the structure that outlasted its purpose

The degradation story is told section by section. Entropy as narrative arc.
```

**Sensory anchors:**
- Temperature: Sun-hot surface, cold in shadow. Metal extremes.
- Sound: Scrape, flake fall, hollow ring of steel, rain on corrugated roof.
- Texture: Rough powdery rust, sharp flaking edge, smooth raw metal underneath.
- Light: Rust glows orange-red in direct sun, turns brown in shadow.
- Smell: Iron tang, wet rust, metal rain, the particular nose-sting of oxidation.

---

### Liquid Mercury

Not water. Not metal. Both. It pools, splits, merges, and reflects everything except itself. Touch it and it parts; stop touching and it reunites. Alien, impossible, beautiful.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Mercury blob morph | `border-radius` animated between irregular organic values — `60% 40% 70% 30% / 50% 60% 40% 50%` to `40% 60% 30% 70% / 60% 40% 50% 50%` at 4-8s ease-in-out infinite | Accent blobs, decorative elements |
| Liquid pool reflection | Element with `scaleY(-0.2)` + `blur(4px)` + opacity 25%, positioned directly below — mercury surface reflection | Below key elements |
| Metallic surface tension | `box-shadow: 0 0 0 1px rgba(255,255,255,0.3), 0 2px 8px rgba(0,0,0,0.6)` — meniscus edge where mercury meets air | All mercury blobs |
| Split and merge | Two blob elements that move toward and away from each other via `translate` animation — fission/fusion | Interactive decorative elements |
| Chrome-liquid gradient | `radial-gradient(circle at 35% 35%, hsl(220,5%,88%), hsl(220,12%,45%) 60%, hsl(220,18%,20%))` — spherical mercury drop lighting | Container fills |
| Ripple propagation | Concentric `box-shadow` rings animating outward from disturbance point — surface disturbance | CTAs, interaction points |
| Satellite droplet | Small child blob (15-25% size of parent) orbiting via `rotate()` with transform-origin at center — separated droplet | Accompanying decorations |
| Floor pooling | Wide, very flat blob at section bottom — mercury gathered by gravity | Section footers |
| Mirror surface | Perfect reflection gradient: top-right bright, mid dark, bottom-right bright — convex sphere lighting | Mercury ball elements |
| Viscosity drag | Hover interaction: blob deforms toward cursor, releases slowly with elastic ease — surface tension physics | Interactive mercury elements |

**Color schema:**
```css
/* Mercury core */
--mercury-highlight: 220 5% 92%;    /* specular highlight */
--mercury-mid: 220 10% 65%;         /* mid surface */
--mercury-shadow: 220 15% 28%;      /* shadow side */
--mercury-deep: 220 18% 10%;        /* deep shadow core */

/* Ambient color (mercury reflects surroundings) */
--mercury-warm: 35 15% 72%;         /* warm environment reflection */
--mercury-cool: 200 20% 62%;        /* cool environment reflection */
--mercury-void: 220 10% 8%;         /* dark environment */

/* Surface tension */
--mercury-meniscus: 220 5% 88% / 0.4; /* meniscus glow */
--mercury-pool-edge: 220 12% 18% / 0.6; /* pool shadow edge */

/* Contaminated variants */
--mercury-gold-tint: 40 30% 65%;    /* gold-tinted mercury */
--mercury-blue-tint: 210 30% 58%;   /* blue-tinted mercury */
```

**Font pairings that fit:**
- **Fluid tech:** Space Grotesk (headings) + Inter (body) — scientific precision
- **Alien luxury:** Syne (headings) + DM Sans (body) — otherworldly premium
- **Cold editorial:** Rajdhani (700, headings) + Barlow (body) — alien modernity

**NOT a locked theme.** Mercury blob morphing works on any fluid/organic brand accent. Chrome-liquid gradients work on any premium sphere or circular element. Ripple propagation works on any interaction point feedback. Split and merge works on any two complementary elements that need dynamic relationship.

**Architectural short-schema:**
```
MERCURY PAGE FLOW:
  [The Spill] — single large mercury blob, morphing, taking up hero space
    ↓ splits into smaller blobs as scroll begins
  [Pooling] — blobs gather into content zones, surface tension groups them
    ↓ reflections appear below key elements
  [Satellite System] — secondary content, smaller blobs orbit key elements
    ↓ split and merge animations mark section transitions
  [The Mirror] — featured content inside perfect chrome-liquid sphere reflection
    ↓ ripple propagation from CTA anticipation
  [Reunification] — all blobs merge toward final CTA, one pooled form

Physics drives the layout. Gravity and surface tension are actual constraints.
```

**Sensory anchors:**
- Temperature: Body temperature but radiates cold visually. Thermal confusion.
- Sound: Liquid metal slosh (heavy), droplet impact on pool surface, near silence.
- Texture: Impossible — you cannot touch it safely. The untouchability IS the texture.
- Light: Perfect reflection distorted by curvature — everything reflected and wrong.
- Smell: Metallic vapor — the kind that means danger, not craft.

---

### Ice / Frost

Water that stopped. Time crystallized. Each frost crystal is a unique decision by physics. The cold doesn't care about your comfort — it just is. The page is beautifully indifferent.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Frost crystal pattern | SVG dendritic branching pattern (recursive line branches at 60-degree angles) growing from edges inward | Border overlays, background edge treatments |
| Ice crack propagation | SVG `<path>` network of angular fractures, animated `stroke-dashoffset` growing from impact point | Section reveals, dramatic transitions |
| Frozen solid container | `backdrop-filter: blur(8px) brightness(1.1)` + very pale blue-white tint — frozen glass clarity | Cards, feature panels |
| Melt drip transition | SVG droplet shapes along element bottom edge, animated `translateY` downward — melting ice | Section bottom treatments |
| Ice bubble trapped | Circular shapes at 8-15% opacity — air trapped during freezing | Background texture accents |
| Frost edge spreading | `clip-path` or `background-image` frost pattern expanding from corners on hover/scroll | Interactive elements, section entries |
| Glacial gradient | `linear-gradient(180deg, hsl(200,30%,92%) 0%, hsl(195,40%,75%) 50%, hsl(200,25%,45%) 100%)` — deep ice column depth | Section backgrounds |
| Crystal facet reflections | `linear-gradient` at multiple sharp angles — faceted ice surface light reflection | Card surfaces |
| Rime texture | Dense tiny frost particle coverage — `feTurbulence` at high frequency + blue-white color map | Surface texture overlays |
| Sublimation glow | Very soft `radial-gradient` white glow, low opacity — ice sublimating in dry air | Around frozen elements |

**Color schema (temperature dial):**
```css
/* Pale winter ice */
--ice-surface: 200 30% 95%;         /* fresh ice surface */
--ice-shallow: 195 35% 85%;         /* shallow ice tint */
--ice-mid: 200 40% 70%;             /* mid-depth ice */
--ice-deep: 205 45% 45%;            /* deep glacial blue */
--ice-abyssal: 210 40% 20%;         /* deep ice darkness */

/* Frost whites */
--frost-bright: 195 15% 97%;        /* new frost, near-white */
--frost-blue: 200 25% 88%;          /* blue-tinted frost */
--frost-crystal: 0 0% 100%;         /* pure crystal face */

/* Cracked ice */
--crack-shadow: 210 30% 30%;        /* crack shadow depth */
--crack-light: 195 20% 75%;         /* light catching crack edge */

/* Environmental */
--frozen-sky: 210 35% 55%;          /* winter sky above ice */
--melt-water: 195 50% 60%;          /* melt pool blue */
--cold-dark: 215 20% 8%;            /* cold dark variant bg */
```

**Font pairings that fit:**
- **Arctic expedition:** Exo 2 (100-200 weight, headings) + Raleway (300, body) — thin and cold
- **Winter editorial:** Josefin Sans (100 weight, headings) + Lato (300, body) — bare ice clarity
- **Crystal precision:** Quicksand (light, headings) + Nunito (300, body) — crystalline lightness

**NOT a locked theme.** Frozen container `backdrop-filter` works on any glassmorphism card. Frost crystal patterns work on any cold/winter brand edge treatment. Ice crack propagation works on any dramatic section reveal. Glacial gradients work on any cool-toned atmospheric background.

**Architectural short-schema:**
```
ICE PAGE FLOW:
  [The Freeze] — dark cold background, first frost crystal appears at corners
    ↓ frost edge spreads inward, rime texture resolves across surface
  [The Ice Sheet] — primary content on glacial gradient, frozen solid containers
    ↓ ice bubbles trapped in background, crystal facet reflections on cards
  [The Crack] — secondary content, ice crack propagation on section entry
    ↓ light refracts through cracks, sublimation glow around key elements
  [Deep Ice] — feature content, deepest blue, maximum glacial depth
    ↓ melt drip transitions at section bottoms — warming begins
  [The Melt] — CTA, ice releasing — drips animate, cool becoming liquid

The cold is thinning as you reach the CTA. Urgency through temperature change.
```

**Sensory anchors:**
- Temperature: Below zero. Breath visible. Exposed skin burns.
- Sound: Ice crack (explosive), snow creak underfoot, wind across open ice, silence.
- Texture: Smooth sheet ice, rough rime frost, sharp crystal edge, cold burn on bare hand.
- Light: Blue-white, shadowless in overcast, blinding reflection on sunny days.
- Smell: Nothing — cold air has no smell. The absence of smell IS the cold.

---

## Mixes Well With

| Material Theme | Pairs With | Result |
|----------------|-----------|--------|
| Marble Stone | Museum Gallery White (urban file) | Precious objects on veined luxury surface |
| Wood Grain | Library Archive (urban file) | Warm knowledge, scholar's study |
| Leather Hide | Library Archive (urban file) | Bound tomes, masculine authority |
| Silk Fabric | Art Deco Lobby (urban file) | 1920s couture grandeur |
| Paper Origami | Japanese Zen Garden (urban file) | Folded silence, wabi-sabi craft |
| Chrome Metal | Brutalist Concrete (urban file) | Hard industrial precision, no softness |
| Ceramic Pottery | Moroccan Riad (urban file) | Zellige tile and hand-glazed richness |
| Rust Patina | Abandoned Decay (urban file) | Maximum entropy, iron and time |
| Liquid Mercury | Neon Tokyo (urban file) | Alien fluid pooling under neon |
| Ice Frost | Rooftop Skyline (urban file) | Winter rooftop, frozen breath, open sky |
| Marble + Chrome | Any dark premium brand | Cold luxury: veined stone meets mirror precision |
| Wood + Leather | Any artisan/craft brand | Workshop warmth: bench surface and bound tools |
| Silk + Ceramic | Any beauty/wellness brand | Soft drape and hand-shaped vessel |
| Rust + Paper | Any heritage/archive brand | Industrial age documents and oxidized storage |
| Ice + Chrome | Any tech/futurist brand | Frozen precision, cold future aesthetic |
