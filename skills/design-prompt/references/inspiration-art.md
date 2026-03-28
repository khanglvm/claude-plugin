# Art Movement Inspiration Themes

Visual art history translated into CSS ingredient palettes. NOT templates — loose aesthetic DNA. Each ingredient works independently. Borrow the soul of a movement without cosplaying it entirely.

---

### Impressionism

Soft light caught mid-moment. Color is emotion; edges are negotiable.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Soft-focus border bloom | `box-shadow: 0 0 40px 20px rgba(255,240,200,0.15)` on containers — edges that glow and dissolve rather than rule | Any card, image container |
| Dappled light overlay | SVG `<feTurbulence>` + `<feDiffuseLighting>` composite at 8-15% opacity — shifting light through leaves | Hero sections, photography |
| Brushstroke texture | CSS `background-image: url(noise.svg)` with `mix-blend-mode: overlay` at low opacity — visible surface, not digital flatness | All backgrounds |
| Color temperature shift | `filter: sepia(15%) saturate(120%) hue-rotate(-5deg)` on images — warm golden-hour cast | Photography, image sections |
| Visible water reflection | `background: linear-gradient(180deg, var(--sky) 0%, var(--sky-reflected) 50%)` with subtle ripple `@keyframes` on transform | Hero dividers, section joins |
| Soft type blur | `text-shadow: 0 1px 8px rgba(255,240,180,0.3)` on headings — type that vibrates with warm light | Hero text, display headings |
| Broken-color pointillism | `background-image: radial-gradient(circle at random, color1 1px, transparent 1px)` repeated — pointillist texture | Section backgrounds |

**Color schema:**
```css
/* Golden Hour */
--imp-bg: 40 20% 95%;             /* warm linen */
--imp-fg: 25 30% 15%;             /* warm near-black */
--imp-gold: 42 70% 65%;           /* afternoon light */
--imp-blue: 210 50% 60%;          /* Monet water blue */
--imp-green: 110 30% 55%;         /* garden green */
--imp-rose: 340 40% 65%;          /* impressionist pink */

/* Dusk palette */
--imp-dusk-bg: 250 25% 12%;       /* blue-violet dusk */
--imp-dusk-fg: 40 30% 85%;        /* warm cream light */
--imp-dusk-accent: 320 50% 65%;   /* rose-violet */
--imp-dusk-water: 200 60% 50%;    /* reflective blue */
```

**Font pairings:**
- **Garden light:** Cormorant Garamond (italic headings) + Lora (body) — soft, literary, warm
- **Plein air:** Playfair Display (headings) + Source Serif 4 (body) — painterly editorial
- **Soft editorial:** Libre Baskerville (headings) + Merriweather Light (body) — readable warmth

**NOT a locked theme.** Soft-focus border blooms work on any light-mode card. Dappled light overlays work on any nature or wellness brand. Color temperature filters unify photography across any site.

**Sensory anchors:** Warmth on the back of your neck in a garden. The blur between looking and remembering. Color that arrives before the object does.

---

### Bauhaus

Geometry is the only decoration you need. Form follows function; function IS beautiful.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Primary color blocks | `background: hsl(0 100% 50%)` / `hsl(210 100% 50%)` / `hsl(55 100% 50%)` flat sections — no gradient, no transition | Section backgrounds, card accents |
| Circle-triangle-square containers | `border-radius: 50%` for circles, `clip-path: polygon(50% 0%, 0% 100%, 100% 100%)` for triangles, squares as-is | Shape decorations, icon containers |
| Strict column grid | CSS Grid with visible column markers (`column-rule: 1px solid rgba(0,0,0,0.1)`) — scaffold made visible | Layout system |
| Black outline system | `border: 2px solid black` on ALL interactive elements — no box-shadow substitutes, just line | Buttons, cards, inputs |
| Geometric rule divider | `<hr>` replaced with alternating red/yellow/blue rectangles stacked horizontally — the Bauhaus band | Section separators |
| Asymmetric weight balance | Large geometric shape (circle or rectangle) floated to one side of layout, text balanced against it — visual fulcrum | Hero, feature sections |
| Workshop poster type | All-caps, tight `letter-spacing: 0.15em`, maximum weight contrast between heading and body | Typography system |

**Color schema:**
```css
/* Primary Workshop */
--bh-red: 0 100% 50%;             /* Bauhaus red */
--bh-blue: 210 100% 50%;          /* Bauhaus blue */
--bh-yellow: 55 100% 50%;         /* Bauhaus yellow */
--bh-black: 0 0% 5%;              /* printing black */
--bh-white: 0 0% 98%;             /* paper white */
--bh-grey: 0 0% 65%;              /* neutral mid */

/* Extended Bauhaus */
--bh-orange: 25 100% 50%;         /* Klee orange */
--bh-green: 140 60% 40%;          /* Itten green */
```

**Font pairings:**
- **Workshop authority:** Bebas Neue (headings) + Barlow (body) — industrial, no apology
- **Geometric purist:** Josefin Sans (headings) + DM Sans (body) — clean, functional
- **Typography lab:** Archivo Black (headings) + Archivo (body) — same family, weight contrast

**NOT a locked theme.** Primary color blocks work on any brand that needs visual authority. Strict column grids work on any data-heavy layout. Black outline systems work on any design system that needs clarity.

**Sensory anchors:** The smell of fresh rubber on linoleum. A lamp that is also a sculpture. The decision that a right angle is enough.

---

### Art Nouveau

The plant is the architect. Every line borrowed from something alive.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Vine-curve SVG border | SVG `<path>` with spiraling tendrils and leaf terminals along container edges — organic frame growth | Cards, section containers, panels |
| Whiplash line divider | SVG `<path>` with dramatic S-curve sweep across full width — the signature Art Nouveau stroke | Section separators |
| Stained-glass color panels | `background: hsl(var(--color) / 0.5)` with `border: 2px solid hsl(var(--color))` on content blocks — lead-lined glass panels | Feature cards, stat blocks |
| Botanical silhouette overlay | SVG botanical illustrations (iris, lily, peacock feather) at 5-10% opacity as background layers | Section backgrounds |
| Organic container shape | `clip-path: path('M...')` with flowing curved top and bottom — no hard rectangle corners | Hero containers, callout sections |
| Gradient lustre | `linear-gradient(135deg, hsl(40,80%,70%), hsl(140,50%,60%), hsl(200,60%,65%))` — peacock iridescence | Border gradients, accents |
| Letterform flourish | CSS `::before` pseudo-element with serif letter scaled large, `opacity: 0.06` — wallpaper letter background | Behind headings, section bg |

**Color schema:**
```css
/* Mucha Gold */
--an-gold: 43 70% 60%;            /* poster gold */
--an-olive: 80 35% 40%;           /* botanical olive */
--an-teal: 175 50% 40%;           /* peacock teal */
--an-rose: 340 45% 55%;           /* organic rose */
--an-cream: 42 40% 92%;           /* vellum ground */
--an-brown: 25 35% 30%;           /* earth line */

/* Twilight palette */
--an-dusk-bg: 260 20% 12%;        /* violet dusk */
--an-dusk-gold: 43 80% 60%;       /* lit gold */
--an-dusk-teal: 175 70% 45%;      /* deep peacock */
```

**Font pairings:**
- **Belle Epoque:** Cinzel Decorative (headings) + IM Fell English (body) — ornate, period-accurate
- **Poster femme:** Abril Fatface (headings) + Crimson Text (body) — Mucha poster energy
- **Organic editorial:** Cormorant Garamond (italic headings) + Lora (body) — living letterforms

**NOT a locked theme.** Vine-curve borders work on any botanical, wellness, or heritage brand. Whiplash dividers replace any horizontal rule. Stained-glass panels work on any site with distinct feature sections.

**Sensory anchors:** The weight of a wrought iron gate. Lily stems bending without breaking. A poster where the woman IS the frame.

---

### Surrealism

Dream logic applies. Rules of physics are advisory. The familiar made stranger than the strange.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Impossible shadow direction | `box-shadow` cast in the wrong direction relative to the implied light source — cognitive dissonance at the container level | Cards, images |
| Melting element | `@keyframes` that slowly deforms `border-radius` and `clip-path` on hover — solid things becoming liquid | CTAs, interactive containers |
| Floating disconnected shadow | Detached `::after` shadow element positioned offset from parent, not aligned — shadow left behind | Product cards, avatars |
| Scale inversion | Small things large, large things small — `font-size: 0.5rem` for "important" labels, `font-size: 4rem` for "minor" details | Typography as visual disruption |
| Window within window | Nested `overflow: hidden` containers with different `background-attachment: fixed` values — infinite interior depth | Hero sections, modals |
| Mirrored landscape | CSS `transform: scaleY(-1)` on a faded copy of an image, positioned beneath it — Magritte reflection | Below-fold section joins |
| Clock-face time text | Circular `letter-spacing` using SVG `textPath` on a circle — text that orbits | Time/date displays, decorative text |

**Color schema:**
```css
/* Dali Desert */
--sur-bg: 40 25% 88%;             /* bleached sand */
--sur-fg: 25 40% 15%;             /* dark umber */
--sur-sky: 200 50% 65%;           /* Magritte blue */
--sur-red: 5 75% 50%;             /* Dali red */
--sur-shadow: 230 20% 30%;        /* detached shadow */

/* Magritte Night */
--sur-night-bg: 220 40% 15%;      /* twilight blue */
--sur-night-fg: 40 20% 85%;       /* pale light */
--sur-night-green: 140 40% 40%;   /* bowler hat green */
--sur-night-cloud: 210 30% 75%;   /* cloud white */
```

**Font pairings:**
- **Dream text:** Spectral (headings) + Lora (body) — literary, slightly unsettling
- **Bureau poster:** Anton (headings) + Karla (body) — bold authority in strange context
- **Museum label:** DM Serif Display (headings) + DM Sans (body) — clinical, matter-of-fact about impossible things

**NOT a locked theme.** Impossible shadows work on any dark card as unexpected delight. Melting element transforms add dreaminess to any interactive element. Scale inversion works as editorial typography contrast on any site.

**Sensory anchors:** The exact moment before sleep. Clocks that remember they were made of metal. A door that opens onto another door.

---

### Pop Art

Mass production made loud. The billboard became the painting. Everything shouts and that's the point.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Halftone dot pattern | `radial-gradient(circle, black 1px, transparent 1px)` with `background-size: 8px 8px` — Ben-Day printing dots | Backgrounds, image overlays |
| Thick black outline | `box-shadow: 4px 4px 0 black` or `outline: 3px solid black; outline-offset: 2px` on all interactive elements | Buttons, cards, badges |
| Speech bubble container | `clip-path` or SVG shape with tail pointer — thought/speech bubble for callouts | Tooltips, callout boxes, CTAs |
| Flat color separation | CSS Grid with hard-edge color blocks, no gradient transitions — color separated like screen printing | Layout, section backgrounds |
| Dot-matrix overlay | `filter: url(#halftone-svg-filter)` on images — converts photography to printed newsprint | Hero images, product photos |
| Roy's blue/yellow palette | Exact Lichtenstein palette: `#003087` (comic blue) + `#FFD700` (yellow) + white + black | Color system |
| Bold exclamation typography | `font-weight: 900; text-transform: uppercase; font-size: clamp(3rem, 10vw, 10rem)` — BANG. POW. | Hero headings, section labels |

**Color schema:**
```css
/* Lichtenstein Primary */
--pop-blue: 220 100% 27%;         /* comic book blue */
--pop-yellow: 48 100% 50%;        /* flat yellow */
--pop-red: 0 100% 50%;            /* pure red */
--pop-black: 0 0% 5%;             /* outline black */
--pop-white: 0 0% 98%;            /* page white */
--pop-pink: 340 80% 65%;          /* Warhol pink */
--pop-green: 120 80% 45%;         /* screen print green */
```

**Font pairings:**
- **Comic authority:** Bangers (headings) + Lato Bold (body) — comic book caption box
- **Warhol print:** Anton (headings) + Source Sans 3 (body) — silkscreen, repetitive weight
- **Pop editorial:** Impact (display) + Open Sans (body) — maximum contrast, maximum legibility

**NOT a locked theme.** Halftone dot patterns work on any retro or print-inspired brand. Thick black outlines work as a design system on any bold brand. Speech bubble containers work as unique callout boxes anywhere.

**Sensory anchors:** A can of soup that's also the price of a can of soup. The color that was too expensive to print so they didn't. Noise that makes the silence next to it quieter.

---

### Japanese Ukiyo-e

The world is flat, layered, and moving. Every wave knows it will break.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Flat color layer planes | No gradient fill — pure flat `background-color` blocks stacked in composition, like woodblock color layers | Layout sections, illustration areas |
| Wave pattern border | SVG `<path>` with repeated sine-wave curves in Hokusai proportions — the great wave as a CSS motif | Section dividers, card borders |
| Layered depth parallax | 3-5 PNG/SVG flat-color layers (sky, distant mountain, mid-ground, foreground) at different scroll speeds | Hero sections, storytelling pages |
| Diagonal composition cut | `clip-path: polygon(0 0, 100% 0, 100% 80%, 0 100%)` — section floors cut at angle, like woodblock horizon lines | Section backgrounds |
| Ink brush stroke | SVG path with variable-width stroke (thick-to-thin), used as heading underline or section accent | Typography accents, dividers |
| Woodblock texture | Paper texture overlay + `filter: contrast(110%) saturate(80%)` — aged print on kozo paper | Background treatment |
| Sparse negative space | Intentional emptiness — `padding: 15vh 10vw` with minimal elements — the ma (negative space) principle | Layout breathing room |

**Color schema:**
```css
/* Hokusai Blue */
--uke-blue: 205 80% 35%;          /* Prussian blue */
--uke-foam: 200 20% 90%;          /* white foam */
--uke-sand: 38 45% 75%;           /* beach sand */
--uke-bark: 20 35% 30%;           /* pine bark brown */
--uke-red: 5 80% 45%;             /* woodblock red */

/* Spring Blossom */
--uke-spring-bg: 35 30% 95%;      /* washi paper */
--uke-spring-pink: 340 50% 70%;   /* sakura */
--uke-spring-green: 130 35% 40%;  /* bamboo */
--uke-spring-ink: 220 25% 8%;     /* sumi ink */
```

**Font pairings:**
- **Woodblock editorial:** Noto Serif JP (headings) + Noto Sans JP (body) — authentic bilingual
- **Western adaptation:** IM Fell English (headings) + Merriweather (body) — old-press sensibility
- **Modern ukiyo:** Shippori Mincho (headings) + Source Han Sans (body) — digital woodblock

**NOT a locked theme.** Flat color layer planes work on any illustration-forward brand. Wave pattern borders work on ocean, sports, or Japanese-inspired brands. Sparse negative space works as layout discipline on any minimal site.

**Sensory anchors:** A mountain seen from 30 miles away with no haze. Ink that dries before you can change your mind. A wave that is also a wall.

---

### De Stijl / Mondrian

All the curves have been removed. What remains is exactly enough.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Mondrian grid layout | CSS Grid with `gap: 4-8px` filled with black — gap IS the grid line. Cells filled with primary colors or white | Hero sections, feature grids |
| Black border divisions | `border: 4-6px solid black` as the primary layout element — every division is explicit | Section containers, cards |
| Asymmetric primary fill | Unequal grid cell sizes — one large red cell, small blue accent, large white field — never equal | Any grid composition |
| Primary color accent strips | `height: 6px; background: var(--mondrian-red)` used as heading underline or section marker | Typography accents, progress bars |
| Whitespace as element | Intentional empty white cells in grid — whitespace given the same weight as filled cells | Grid compositions |
| Right-angle typography | `font-weight: 900; line-height: 1; letter-spacing: -0.02em` — type as geometry, not decoration | Display headings |
| Single-color focus | Per section: only ONE accent color in use, rest is black/white — no color mixing within a zone | Section-based color system |

**Color schema:**
```css
/* Mondrian Classic */
--stijl-red: 0 100% 40%;          /* De Stijl red */
--stijl-blue: 210 100% 40%;       /* De Stijl blue */
--stijl-yellow: 50 100% 50%;      /* De Stijl yellow */
--stijl-black: 0 0% 8%;           /* grid line */
--stijl-white: 0 0% 97%;          /* field white */

/* Modern Extension */
--stijl-grey: 0 0% 82%;           /* Rietveld grey */
```

**Font pairings:**
- **Geometric manifesto:** Bebas Neue (headings) + Barlow Condensed (body) — the Stijl proclamation
- **De Stijl rational:** Futura PT (headings) + DM Sans (body) — rationalist beauty
- **Grid master:** Space Grotesk (headings) + Space Grotesk Light (body) — same family, weight only

**NOT a locked theme.** Mondrian grid layouts work as hero compositions on any bold brand. Black border divisions work as a card system on any product page. Primary color accent strips work as universal typography accents.

**Sensory anchors:** The satisfaction of a right angle that doesn't apologize. Red that knows it is red. The grid underneath everything, finally visible.

---

### Constructivism

The diagonal is a weapon. Everything leans forward, toward the future.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Diagonal slash layout | `clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%)` — section floors tilted forward, not horizontal | Section backgrounds, hero |
| Bold wedge composition | Large SVG triangle or parallelogram overlaid on hero — pointed toward CTA or focal point | Hero sections |
| Red/black palette lock | Binary palette: `hsl(0 100% 40%)` + `hsl(0 0% 5%)` — no softening, no third color without justification | Color system |
| Propaganda typography | Uppercase, maximum weight, `letter-spacing: 0.05em`, slight italic lean (`font-style: italic`) — forward motion in type | All headings |
| Star/gear decorative element | SVG constructivist motifs (gear, red star, factory silhouette) at low opacity as background layer | Section backgrounds |
| Overlapping plane stack | Multiple absolutely-positioned color blocks at different `z-index`, deliberately overlapping — depth without shadow | Hero layouts |
| Industrial rule stripe | `background: repeating-linear-gradient(45deg, red 0, red 2px, transparent 2px, transparent 10px)` — construction barrier stripe | Warnings, CTAs, borders |

**Color schema:**
```css
/* Revolutionary Red */
--con-red: 0 95% 42%;             /* Soviet red */
--con-black: 0 0% 5%;             /* ink black */
--con-white: 0 0% 96%;            /* paper */
--con-grey: 0 0% 40%;             /* steel grey */

/* Extended Palette */
--con-orange: 20 100% 50%;        /* propaganda orange */
--con-blue: 215 80% 30%;          /* industrial blue */
```

**Font pairings:**
- **Rodchenko bold:** Oswald (headings) + Barlow Condensed (body) — narrow, stacked, insistent
- **Soviet manifesto:** Bebas Neue (display) + IBM Plex Sans (body) — mass communication
- **Agitprop:** Anton (headings) + Open Sans (body) — placard weight, clear body

**NOT a locked theme.** Diagonal slash layouts work on any brand that wants forward momentum. Red/black palettes work on any bold tech or media brand. Overlapping plane stacks work as hero art direction on any site.

**Sensory anchors:** A poster that has to be read from across a square. The angle of a crane against sky. Words that arrive before the sentence does.

---

### Islamic Geometric Art

Infinite pattern as meditation. The divine expressed through mathematics. No beginning, no end — just the tessellation of the cosmos.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Star polygon tile | `repeating-conic-gradient` or SVG 8/10/12-point star tessellation — Islamic arabesque tiling | Section backgrounds, hero patterns |
| Girih interlace | SVG overlapping pentagonal/decagonal straps with `mix-blend-mode: multiply` — interlaced geometric ribbon | Card borders, dividers |
| Muqarnas shadow depth | Nested `box-shadow` creating stalactite-vault layering — honeycomb depth without 3D | Hero sections, decorative headers |
| Arabesque vine | SVG organic spiral with geometric leaf terminals, low opacity — botanical geometry | Section backgrounds, card overlays |
| Geometric color field | Flat mosaic cells in deep jewel tones — each tile a pure saturated color, no gradient | Feature blocks, pricing sections |
| Zellige gradient border | `border-image` using repeating diamond/star tile in earth tones — handmade ceramic tile frame | Cards, modals |

**Color schema:**
```css
/* Isfahan Blue */
--isg-bg: 200 15% 8%;              /* dark lapis ground */
--isg-tile-blue: 210 70% 45%;      /* cobalt tile */
--isg-tile-teal: 175 55% 40%;      /* turquoise glaze */
--isg-gold: 43 75% 55%;            /* gilded accent */
--isg-ivory: 40 35% 90%;           /* bone white */
--isg-red: 5 65% 40%;              /* terracotta earth */
```

**NOT a locked theme.** Star polygon tiles work on any dark premium brand. Girih interlace works as a section divider on any site. Geometric color fields work on any brand that needs structured visual richness.

**Sensory anchors:** A courtyard seen from above that is also a prayer. Tile that was cut to fit a shape that hasn't changed in 900 years. The geometry of stars, brought down to earth.

---

### Mixes well with

| Art movement combo | Result |
|-------------------|--------|
| Bauhaus grid + Constructivism diagonals | Geometric power — organized dynamism |
| Impressionism blur + Art Nouveau vine borders | Garden editorial — soft nature meets organic structure |
| Pop Art halftone + Ukiyo-e flat planes | Print culture collision — Western dots on Eastern planes |
| Surrealism impossible shadows + Dark Premium | Luxury with unsettling depth |
| De Stijl grid + Y2K gloss | Mondrian gets inflated — primary colors in bubble form |
| Constructivism red/black + Terminal phosphor | Revolutionary tech — propaganda meets command line |
| Art Nouveau organics + Impressionism blur | Belle Epoque full immersion — soft, growing, golden |
| Ukiyo-e negative space + Dark minimal | Maximum restraint — Japanese minimalism on dark ground |
