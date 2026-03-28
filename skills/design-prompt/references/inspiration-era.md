# Era & Time Period Inspiration Themes

Cultural epochs translated into CSS ingredient palettes. NOT templates — loose visual DNA for creative mixing. Each ingredient works independently. Raid these for atmosphere, not prescription.

---

### 1920s Art Deco

Gatsby grandeur made of geometry. Every surface earns its gold; every edge is a decision.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Sunburst radiator | `conic-gradient` repeating thin gold lines (1-2px) radiating from a center point — sunburst/clock-face pattern, applied behind hero text or as section dividers | Dark luxury, black backgrounds |
| Stepped pyramid border | Nested `box-shadow` with decreasing offsets in gold/champagne — creates stacked-tier frame effect without images | Card containers, modals |
| Geometric line-art overlay | SVG diamond lattice, chevron zigzags, or hexagon grids at 5-10% opacity over content | Any dark background |
| Champagne bubble particles | Tiny circles (3-8px) rising slowly, `border-radius: 50%`, gold-tinted, low opacity — irregular sizes, staggered timing | Hero sections, dark backgrounds |
| Gold ruled dividers | `border-image` with repeating diamond-dot pattern, or double-line rules (`border-top: 1px solid gold; margin-top: 3px; border-top: 3px solid gold`) | Section separators, any `<hr>` |
| Font geometric caps | All-caps headings with extreme `letter-spacing: 0.25em+`, set in geometric serif — every headline becomes a marquee | Headers, callouts |
| Black lacquer surface | `background: hsl(40 10% 4%)` with subtle warm undertone + gold `box-shadow` outlines on containers | Hero, nav, cards |
| Jazz shimmer | Fast `@keyframes hue-rotate` on a gold element cycling 0→30deg — barely perceptible shimmer | Accent borders, decorative elements |

**Color schema:**
```css
/* Black & Gold (classic) */
--deco-bg: 40 10% 4%;             /* near-black, warm */
--deco-fg: 45 60% 88%;            /* champagne cream */
--deco-gold: 43 80% 52%;          /* burnished gold */
--deco-gold-light: 48 90% 70%;    /* champagne highlight */
--deco-rule: 40 50% 40%;          /* aged gold line */

/* Ivory & Emerald (alternate) */
--deco-ivory-bg: 45 25% 92%;      /* old ivory */
--deco-ivory-fg: 160 20% 10%;     /* dark forest ink */
--deco-emerald: 155 50% 30%;      /* Gatsby green */

/* Midnight Navy (club) */
--deco-navy-bg: 230 40% 8%;       /* deep navy */
--deco-navy-accent: 43 80% 55%;   /* gold on navy */
--deco-navy-silver: 210 15% 75%;  /* silver chrome */
```

**Font pairings:**
- **Marquee glamour:** Playfair Display (italic headings) + Cormorant Garamond (body) — editorial luxury
- **Geometric authority:** Josefin Sans (all-caps headings) + Raleway (body) — pure Deco geometry
- **Broadway poster:** Poiret One (display) + Lato (body) — theatrical, high contrast

**NOT a locked theme.** Sunburst radiators work on any dark hero. Gold ruled dividers replace any `<hr>`. Stepped pyramid borders elevate plain cards. Champagne bubbles fit any premium product page.

**Sensory anchors:** Weight of cut crystal. The geometry of a clock face at midnight. A ballroom seen through cigarette smoke. Gold that catches light without asking permission.

---

### 1960s Psychedelic

Reality softens at the edges, colors negotiate with each other, and the ground is optional.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Op-art repeating field | `repeating-radial-gradient` or `repeating-linear-gradient` with high-contrast color bands (2-8px) — optical vibration without animation | Section backgrounds, hero pattern |
| Lava-lamp blob | Large SVG `<feTurbulence>` + `<feDisplacementMap>` on circular shapes, slow morph animation — organic pulsing | Behind text, accent shapes |
| Rainbow spectrum shift | `@keyframes` animating `filter: hue-rotate(0deg→360deg)` on a gradient element — full spectrum slowly cycles | Accent borders, dividers |
| Warped container | `clip-path: path()` with gentle sine-wave top/bottom edges — sections that undulate rather than rectangle | Section wrappers |
| Kaleidoscope overlay | `conic-gradient` with 12+ color stops at low opacity as radial vignette | Hero backgrounds |
| Concentric circle pulse | `box-shadow` with 4-6 layered rings in alternating colors — bullseye that radiates | CTAs, focal points |
| Color-field blocks | Large flat color panels, no gradient, no texture — pure hue collision inspired by Color Field painting | Full-bleed section backgrounds |

**Color schema:**
```css
/* Electric Day */
--psych-yellow: 55 100% 55%;      /* chrome yellow */
--psych-magenta: 310 90% 55%;     /* hot pink */
--psych-cyan: 185 90% 50%;        /* electric teal */
--psych-green: 120 70% 45%;       /* acid green */
--psych-purple: 270 80% 55%;      /* lysergic violet */

/* Earth Psychedelic */
--psych-earth-bg: 30 40% 10%;     /* dark saffron */
--psych-earth-orange: 20 90% 55%; /* tangerine */
--psych-earth-teal: 175 60% 40%;  /* mineral teal */
--psych-earth-gold: 45 85% 55%;   /* warm gold */
```

**Font pairings:**
- **Poster acid:** Boogaloo (headings) + Nunito (body) — rounded, bouncy, slightly unhinged
- **Underground press:** Abril Fatface (headlines) + IBM Plex Mono (body) — bold slab meets typewriter
- **Groovy editorial:** Righteous (headings) + Quicksand (body) — curved, optimistic

**NOT a locked theme.** Op-art gradients work on any vibrant brand. Rainbow spectrum shift adds life to any accent element. Lava-lamp blobs fit wellness, creative, or experimental products.

**Sensory anchors:** The moment your eyes adjust to a darkroom. Velvet black light posters. Color that vibrates before you touch it. Time moving slower than it should.

---

### 1970s Disco / Funk

The room remembers every body that ever danced in it. Warm, analog, kinetic.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Disco-ball scatter | Multiple tiny `radial-gradient` hotspots (white → transparent, 8-20px) at random coordinates, slow rotation on parent — scattered mirror reflections | Dark backgrounds |
| Warm film grain | SVG `<feTurbulence type="fractalNoise">` overlay at 4-8% opacity — analog warmth, not digital noise | Photography sections |
| Vinyl groove circles | `repeating-radial-gradient` with near-identical dark bands (1-2px gap) — vinyl record texture on circular elements | Circular containers, hero |
| Sunburst burst rays | `conic-gradient` with alternating brown/gold thin slices — 1970s starburst wall decoration | Behind product shots, CTAs |
| Warm panel gradient | Large horizontal bands of warm browns, oranges, avocado greens — shag-carpet color logic | Section backgrounds |
| Platform shimmer | `linear-gradient(135deg)` in gold/bronze with animated `background-position` — glittery platform shoe effect on buttons | CTAs, interactive elements |
| Prism lens flare | Thin `radial-gradient` rainbow streak (2-4px tall, wide) crossing the hero focal point | Hero images, product photos |

**Color schema:**
```css
/* Harvest Gold */
--disco-bg: 25 20% 8%;            /* dark walnut */
--disco-fg: 40 50% 85%;           /* warm cream */
--disco-gold: 38 75% 55%;         /* harvest gold */
--disco-orange: 22 80% 52%;       /* burnt orange */
--disco-brown: 20 40% 35%;        /* saddle brown */

/* Midnight Floor */
--disco-floor-bg: 260 30% 8%;     /* deep plum */
--disco-floor-mirror: 0 0% 90%;   /* mirror white */
--disco-floor-hot: 330 80% 55%;   /* hot pink accent */
--disco-floor-laser: 185 90% 55%; /* laser teal */
```

**Font pairings:**
- **Funk poster:** Bebas Neue (headings) + DM Sans (body) — wide, strutting, confident
- **Soul album:** Lobster (headings) + Source Sans 3 (body) — rounded warmth, album liner notes
- **Studio session:** Oswald (headings) + Open Sans (body) — no-nonsense, workhorse

**NOT a locked theme.** Warm film grain works on any photography site. Vinyl groove texture fits music, podcast, or audio brands. Disco-ball scatter fits any nightlife or event aesthetic.

**Sensory anchors:** The floor vibrating under bass. Warm amber through amber glass. Mirror light that never lands in the same place twice.

---

### 1980s Synthwave

The future that 1982 imagined. Neon on black velvet. Chrome that bleeds pink.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Perspective grid floor | `linear-gradient` horizontal lines + `perspective: 500px; rotateX(60deg)` on a grid container — infinite road-to-horizon illusion | Hero sections, full-bleed backgrounds |
| Chrome text gradient | `background: linear-gradient(180deg, #fff 0%, #f0f 40%, #00f 100%); -webkit-background-clip: text` — metallic chrome with pink-purple cast | Display headings, logos |
| Scan-line overlay | `repeating-linear-gradient(transparent 0, transparent 1px, rgba(0,0,0,0.3) 1px, rgba(0,0,0,0.3) 2px)` fixed over content — CRT effect | Any dark-mode section |
| Sunset tri-gradient | `linear-gradient(180deg, hsl(280,80%,15%) 0%, hsl(320,80%,40%) 50%, hsl(350,90%,55%) 100%)` — iconic synthwave sky | Hero backgrounds |
| VHS glitch | `@keyframes` alternating `clip-path` horizontal slices + `transform: translateX(±5px)` rapid frames — tape-tracking error | Loading states, hover on images |
| Neon glow text | `text-shadow: 0 0 10px currentColor, 0 0 30px currentColor, 0 0 60px currentColor` — phosphor tube glow | Any heading element |
| Laser grid lines | `box-shadow` or SVG diagonal lines in pink/cyan — 80s vector graphics aesthetic | Cards, section borders |

**Color schema:**
```css
/* Classic Synthwave */
--synth-bg: 270 60% 4%;           /* deep space purple-black */
--synth-fg: 0 0% 95%;             /* near-white */
--synth-pink: 320 90% 60%;        /* hot pink neon */
--synth-cyan: 185 100% 55%;       /* electric cyan */
--synth-purple: 270 80% 55%;      /* laser violet */
--synth-orange: 25 100% 60%;      /* sunset orange */

/* Outrun (warm variant) */
--synth-out-sky: 280 70% 15%;     /* dusk purple */
--synth-out-horizon: 330 80% 45%; /* sunset pink */
--synth-out-sun: 40 100% 60%;     /* chrome gold */
--synth-out-grid: 185 80% 50%;    /* teal grid lines */
```

**Font pairings:**
- **80s arcade:** Orbitron (headings) + Rajdhani (body) — angular, digital, futuristic
- **VHS cover:** Audiowide (headings) + Exo 2 (body) — sci-fi film title energy
- **Retro future:** Electrolize (headings) + IBM Plex Sans (body) — technical, readable

**NOT a locked theme.** Perspective grid floors work on any product landing. Scan-line overlays add authenticity to any dark UI. Neon glow text works on any dark hero heading.

**Sensory anchors:** The hum before a synthesizer breathes. Highway at 2am with no other cars. Chrome that reflects a sunset that isn't there.

---

### 1990s Grunge

The refusal to be polished. Texture as ideology. Imperfection as the only honest aesthetic.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Photocopy noise | `filter: contrast(150%) grayscale(30%)` on a `feTurbulence` SVG overlay — xerox machine had a bad day | Any background, image treatment |
| Torn collage edges | `clip-path: polygon()` with irregular, slightly-off-right-angle vertices — torn paper on containers | Cards, images, hero sections |
| Stamp overlay | Semi-transparent text at angle (`transform: rotate(-15deg)`), `mix-blend-mode: multiply` — used/handled object aesthetic | Anywhere over content |
| Type collision | Deliberate `letter-spacing: -0.05em` paired with oversized line-height — type crashes into itself | Display headings |
| Marker underline | `text-decoration: underline wavy 3px` in contrasting ink color | Links, emphasized text |
| Dirty white | Off-white backgrounds with `hsl(45 10% 90%)` + subtle noise overlay — photocopied, not printed | Light-mode sections |
| Scotch tape highlight | `::before` pseudo-element, 20px tall, semi-transparent yellow, `transform: rotate(-1deg)` — literal tape mark | Pull quotes, headings |

**Color schema:**
```css
/* Xerox Black */
--grunge-bg: 40 5% 92%;           /* dirty white */
--grunge-fg: 0 0% 10%;            /* near-black ink */
--grunge-red: 0 80% 45%;          /* band flyer red */
--grunge-yellow: 50 90% 55%;      /* highlighter */
--grunge-noise: 40 10% 40% / 0.1; /* grime layer */

/* Dark Flannel */
--grunge-dark-bg: 220 10% 10%;    /* slate black */
--grunge-dark-fg: 40 10% 80%;     /* worn grey-white */
--grunge-dark-accent: 340 60% 45%;/* dark crimson */
```

**Font pairings:**
- **Flyer stack:** Special Elite (headings) + Courier Prime (body) — typewriter, photocopied, DIY
- **Zine cut:** Black Han Sans (headings) + Inconsolata (body) — rough, stacked, aggressive
- **Pacific NW:** Oswald (headings) + Lora (body) — flannel plaid energy, readable

**NOT a locked theme.** Torn collage edges work on editorial/portfolio. Photocopy noise works on any photography treatment. Stamp overlays add authenticity to handmade or craft brands.

**Sensory anchors:** Paper that's been folded and unfolded too many times. Marker on skin. A flyer pulled from a telephone pole in the rain.

---

### Y2K / Bubble

Everything is inflated, glossy, and optimistic about a future that turned out differently.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Bubble gloss button | `background: radial-gradient(ellipse at 30% 25%, rgba(255,255,255,0.6) 0%, transparent 60%)` over saturated color — candy-pill 3D effect | Any CTA, tag, badge |
| Iridescent shift | `linear-gradient(135deg, hsl(180,70%,70%), hsl(270,70%,75%), hsl(330,70%,70%))` with animated `background-position` — soap bubble color shift | Card borders, overlays |
| Inflated shape | `border-radius: 40% 60% 60% 40% / 40% 40% 60% 60%` — organic blob that reads as pressurized, 3D-squeezable | Containers, avatars |
| Frosted info panel | `background: rgba(255,255,255,0.2); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.4)` — Windows XP glass | Any card on colored bg |
| Translucent candy panel | Saturated color at 50-60% opacity over white — jellybean panels | Pricing blocks, feature cards |
| Star burst badge | `clip-path: polygon(...)` 12-16 point star shape | Promo labels, CTAs |
| Digital chrome | `linear-gradient(135deg, #c0c0c0, #ffffff, #c0c0c0)` with `background-size: 200%` animated — spinning CD surface | Decorative elements |

**Color schema:**
```css
/* Candy Internet */
--y2k-bg: 220 30% 97%;            /* almost white */
--y2k-fg: 220 30% 15%;            /* deep blue-black */
--y2k-blue: 210 90% 60%;          /* hyperlink blue */
--y2k-pink: 330 90% 65%;          /* bubble gum */
--y2k-lime: 80 80% 55%;           /* acid lime */
--y2k-silver: 210 10% 75%;        /* chrome silver */

/* Translucent OS */
--y2k-glass: 210 60% 60% / 0.4;   /* glass tint */
--y2k-shadow: 210 50% 30% / 0.2;  /* soft OS shadow */
```

**Font pairings:**
- **Portal startup:** Trebuchet MS (headings) + Verdana (body) — the authentic Y2K web stack
- **Future friendly:** Varela Round (headings) + Nunito (body) — rounded, approachable, inflated
- **Optimistic tech:** Fredoka One (headings) + Poppins (body) — cheerful authority

**NOT a locked theme.** Bubble gloss buttons elevate any modern UI. Frosted panels work with any colorful background. Iridescent shifts fit fashion, beauty, or NFT aesthetics.

**Sensory anchors:** The weight of a clear plastic handbag. A CD that turns prism when angled. Everything was loading and we believed it would load.

---

### Medieval Manuscript

The slowest possible medium made luminous. Every page is a garden.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Illuminated drop cap | First letter: `font-size: 5em`, colored gold/deep red, `float: left`, SVG border frame around it | Blog posts, long-form content |
| Vine border frame | SVG `<path>` with organic spiral/leaf curves along container edges — border that grows rather than rules | Cards, section containers |
| Parchment texture | `background: hsl(40 40% 88%)` + noise overlay + `filter: sepia(20%)` — aged paper | Full page, hero backgrounds |
| Rubrication accent | Red used exclusively for headings, initials, key terms — medieval typographic hierarchy | Typography system |
| Folio margin notes | `position: absolute; left: -200px` italic text, smaller size — marginalia annotation style | Pull quotes, annotations |
| Gold leaf shimmer | `linear-gradient(135deg, #c8a951, #f0d060, #c8a951)` with `background-size: 200%` slow animation — beaten gold | Headings, borders, icons |
| Gothic arch container | `clip-path` or SVG shape with pointed arch top — medieval window/doorway framing | Images, featured content |

**Color schema:**
```css
/* Illuminated Page */
--ms-parchment: 40 40% 88%;       /* aged vellum */
--ms-ink: 220 30% 10%;            /* iron gall ink */
--ms-gold: 43 70% 52%;            /* burnished gold */
--ms-red: 0 80% 40%;              /* vermillion */
--ms-blue: 220 70% 35%;           /* ultramarine */
--ms-green: 130 40% 30%;          /* verdigris */

/* Dark Codex */
--ms-dark-bg: 25 20% 8%;          /* worn leather */
--ms-dark-gold: 43 80% 55%;       /* lit gold */
--ms-dark-vellum: 40 30% 70%;     /* aged paper */
```

**Font pairings:**
- **Abbey scriptorium:** UnifrakturMaguntia (display) + IM Fell English (body) — authentic blackletter
- **Illuminated modern:** MedievalSharp (headings) + Crimson Text (body) — readable with manuscript soul
- **Scholarly:** Palatino Linotype (headings) + Garamond (body) — academic, enduring

**NOT a locked theme.** Illuminated drop caps transform any long-form article. Vine borders work on botanical or heritage brands. Parchment texture fits food, history, craft, legal brands.

**Sensory anchors:** The weight of a page that can't be deleted. Ink ground from stone. A margin note written 600 years ago to no one in particular.

---

### Retro Computing / Terminal

The authority of a machine that doesn't apologize for being a machine.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| CRT scan-line | `repeating-linear-gradient(transparent 0, transparent 2px, rgba(0,0,0,0.15) 2px, rgba(0,0,0,0.15) 3px)` over screen content | Any dark section |
| Phosphor glow text | `color: hsl(120 100% 55%); text-shadow: 0 0 8px currentColor, 0 0 20px currentColor` — green phosphor tube | Headings, code blocks |
| Blinking cursor | `::after { content: '█'; animation: blink 1s step-end infinite }` at end of headline | Hero text, form labels |
| Boot sequence reveal | Text appears character by character via `@keyframes` width expansion — typewriter at OS speed | Hero headings, loading states |
| Terminal container | `background: #0a0a0a; font-family: monospace; border: 1px solid #1a1a1a` — black shell window | Code snippets, data displays |
| Prompt prefix | `::before { content: '> '; color: hsl(120 80% 50%) }` on list items — command line aesthetics | Feature lists, instructions |
| Screen curvature | `border-radius: 20px; box-shadow: inset 0 0 80px rgba(0,0,0,0.5)` — CRT barrel distortion | Full-screen sections |

**Color schema:**
```css
/* Green Phosphor */
--term-bg: 120 10% 3%;            /* true black, green tint */
--term-green: 120 100% 55%;       /* phosphor green */
--term-green-dim: 120 60% 35%;    /* dim text */
--term-green-glow: 120 100% 55% / 0.3;

/* Amber Phosphor */
--term-amber: 38 100% 55%;        /* amber tube */
--term-amber-dim: 35 70% 40%;     /* dim amber */

/* Modern Dark Terminal */
--term-modern-bg: 220 15% 6%;     /* VS Code dark */
--term-modern-fg: 210 20% 85%;    /* cool grey */
--term-modern-accent: 175 80% 55%;/* mint green */
--term-modern-string: 25 90% 60%; /* orange strings */
```

**Font pairings:**
- **Pure terminal:** IBM Plex Mono (all text) — the authentic choice, nothing else needed
- **Hacker news:** Share Tech Mono (headings) + Share Tech (body) — slightly warmer
- **Developer docs:** JetBrains Mono (code) + Inter (prose) — modern, respectful

**NOT a locked theme.** CRT scan-lines work on any dark UI. Blinking cursors work on any tech hero. Boot sequence reveals work on any site that wants to feel like it's initializing.

**Sensory anchors:** Warmth of a monitor left on overnight. Click of a mechanical keyboard in an empty office. The certainty that the machine knows more than it's saying.

---

### Vaporwave / Digital Nostalgia

Consumer culture on pause. Roman busts in a pink mall that closed in 1997.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Pastel gradient wash | `linear-gradient(135deg, hsl(300,60%,75%), hsl(200,70%,70%), hsl(240,65%,72%))` — signature pink-blue-lavender field | Hero backgrounds, full-bleed sections |
| Glitch artifact | `@keyframes` applying `clip-path` horizontal slices + `filter: hue-rotate(90deg)` on alternate frames — digital compression noise | Image hover, section transitions |
| Greek column frame | SVG column capitals positioned left/right of content area — classical architecture in a mall atrium | Feature sections, hero flanking |
| Checkerboard floor | `repeating-conic-gradient(#fff 0 25%, #ddd 0 50%)` in `perspective` transform — mallwave tile floor | Hero backgrounds |
| VHS timestamp | Monospace text, top-right corner, `color: rgba(255,255,255,0.7)` — REC indicator aesthetic | Image overlays, hero corner |
| Slowed-down text | Extra-wide `letter-spacing: 0.3em`, soft hover `filter: blur(1px)` — time stretching | Display headings |
| Japanese text overlay | Katakana characters positioned decoratively at low opacity — not translation, purely aesthetic | Background decoration |

**Color schema:**
```css
/* Classic Vaporwave */
--vapor-pink: 310 70% 75%;        /* bubblegum pink */
--vapor-purple: 270 60% 70%;      /* lavender */
--vapor-blue: 200 70% 70%;        /* sky pool blue */
--vapor-teal: 175 65% 60%;        /* seafoam */
--vapor-bg: 270 40% 15%;          /* deep twilight */
--vapor-white: 0 0% 95%;          /* mall white */

/* Night City */
--vapor-night-bg: 260 50% 5%;     /* deep space */
--vapor-night-pink: 320 90% 65%;  /* hot pink neon */
--vapor-night-cyan: 185 100% 55%; /* neon cyan */
--vapor-night-gold: 45 90% 60%;   /* 24k gold */
```

**Font pairings:**
- **Digital sunset:** Righteous (headings) + Raleway Light (body) — geometric calm, languid
- **Aesthetics:** Josefin Sans (headings, wide tracking) + Lato Light (body) — spaced out
- **Mall loop:** Viga (headings) + Arial (body) — the nostalgic stack

**NOT a locked theme.** Pastel gradient washes work on any dreamy or nostalgic brand. Glitch artifacts work on tech or gaming sites. Checkerboard floors in perspective work on fashion or 3D product pages.

**Sensory anchors:** Air-conditioned mall at 2pm on a Tuesday in 1994. The pause between cassette tracks. A sunset that refuses to end.

---

### Mughal Miniature / Persian Court

The jeweled page. Every element earns its border. Gold doesn't decorate — it defines what is sacred.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Geometric medallion field | `repeating-conic-gradient` with 8-12 point star interlace at 5% opacity — Mughal arabesque tiling | Section backgrounds, hero patterns |
| Cartouche container | SVG arch frame with knotwork border — manuscript panel that frames royalty | Feature cards, hero sections |
| Jewel-tone panel | Deep lapis `hsl(210 80% 25%)`, ruby `hsl(0 75% 35%)`, emerald `hsl(145 55% 28%)` flat blocks — precious stone as color system | Section backgrounds, pricing blocks |
| Double gold margin | `border: 1px solid var(--mug-gold); outline: 2px solid var(--mug-gold-dim); outline-offset: 4px` — Mughal manuscript double rule | Cards, images, content blocks |
| Calligraphic watermark | Naskh letterform SVG at 4% opacity behind headings — manuscript page ground | Section backgrounds, hero text zones |
| Diaper pattern fill | `repeating-conic-gradient` tiny diamond motif at 3-5% opacity — woven silk repeat | Card backgrounds, subtle texture |
| Flat garden cartography | Layered flat-color rectangles (no shadow, no perspective) with botanical SVG motifs — Mughal garden seen from above | Hero sections, illustrated features |

**Color schema:**
```css
/* Lapis & Gold */
--mug-lapis: 210 80% 25%;         /* ultramarine lapis */
--mug-gold: 43 85% 55%;           /* burnished Mughal gold */
--mug-ruby: 0 75% 35%;            /* deep ruby red */
--mug-emerald: 145 55% 28%;       /* forest emerald */
--mug-ivory: 40 35% 92%;          /* manuscript ivory */
--mug-gold-dim: 43 60% 45%;       /* aged gold rule */

/* Sunset Durbar */
--mug-dusk-bg: 20 30% 8%;         /* dark amber court */
--mug-dusk-saffron: 35 90% 55%;   /* saffron gold */
--mug-dusk-teal: 175 55% 35%;     /* Mughal tile teal */
```

**Font pairings:**
- **Court manuscript:** Cinzel Decorative (headings) + Crimson Text (body) — ornate and legible
- **Modern durbar:** Cormorant Upright (headings) + IM Fell English (body) — classical with court weight
- **Heritage luxury:** Playfair Display (headings) + Lora (body) — editorial court grandeur

**NOT a locked theme.** Jewel-tone panels work on any heritage or luxury brand. Double gold margins elevate any card system. Diaper pattern fills work on any premium textile or fashion brand.

**Sensory anchors:** The weight of a page that cost more than a horse. Ink ground from lapis hauled across a continent. A garden that is also a map of paradise.

---

### Mixes well with

| Era combo | Result |
|----------|--------|
| Art Deco + Dark Premium glass | Gatsby speakeasy — gold geometry behind frosted panels |
| Synthwave grid + Cyberpunk neon | Full retro-futurism, neon city with perspective depth |
| Terminal green + Grunge noise | Hacker zine — code culture meets punk DIY |
| Medieval manuscript + Dark minimal | Ancient knowledge in a modern vessel |
| Y2K gloss + blurred photography | Dreamy early web — a memory of the internet |
| Disco warm grain + Art Deco gold | Soul food, jazz club, upscale warmth |
| Vaporwave pastels + Japanese flat planes | Lo-fi study, calm digital orientalism |
| 1960s op-art + Bold outlines | Maximum visual noise, graphic energy overload |
| Mughal Miniature + Islamic Geometric Art | Sacred opulence — jeweled geometry in court manuscript |
