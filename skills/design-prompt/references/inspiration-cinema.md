# Cinema & Photography Inspiration Themes

Directors' visual languages translated into CSS ingredient palettes. NOT templates — directorial grammar for web design. Each ingredient works independently. Steal the frame, not the film.

---

### Film Noir

High contrast as moral position. Light is the detective; shadow is the truth.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Venetian blind shadow | `repeating-linear-gradient(90deg, transparent 0, transparent 18px, rgba(0,0,0,0.6) 18px, rgba(0,0,0,0.6) 20px)` pinned over content — hard diagonal light stripes through blinds | Hero sections, image overlays |
| Hard cast shadow | `box-shadow: 12px 12px 0 rgba(0,0,0,0.8)` (no blur radius) — noir shadows have no soft edges | Cards, containers |
| Cigarette smoke wisp | Large, slow SVG `feTurbulence` blob rising from bottom of frame, white at 4-8% opacity, slow upward drift | Background atmosphere |
| Rain on glass overlay | SVG with animated droplet paths streaming diagonally, `opacity: 0.15` — `stroke: white; stroke-width: 1px` | Full-screen hero backgrounds |
| High contrast B&W | `filter: grayscale(100%) contrast(140%)` on images, then `mix-blend-mode: luminosity` over dark bg | Photography, hero images |
| Spotlight radial | `radial-gradient(ellipse at 30% 40%, rgba(255,240,200,0.3) 0%, transparent 60%)` — single hard light source | Hero sections, product spotlights |
| Fedora shadow text | `text-shadow: 3px 3px 0 black, 6px 6px 0 rgba(0,0,0,0.5)` — type with weight and shadow | Display headings |

**Color schema:**
```css
/* Classic Noir */
--noir-bg: 0 0% 4%;               /* studio black */
--noir-fg: 0 0% 90%;              /* light-source white */
--noir-shadow: 0 0% 12%;          /* deep shadow zone */
--noir-highlight: 45 20% 80%;     /* tungsten warm white */
--noir-red: 0 70% 45%;            /* lipstick red accent */

/* Tinted Noir */
--noir-teal: 185 30% 15%;         /* cold blue shadow */
--noir-amber: 38 40% 25%;         /* warm noir amber */
--noir-sepia-bg: 30 15% 8%;       /* sepia-toned night */
```

**Font pairings:**
- **Crime column:** Special Elite (headings) + Courier Prime (body) — typewriter, dispatch, confession
- **Detective novel:** Playfair Display (italic headings) + EB Garamond (body) — literary, shadowy
- **Marquee lights:** Bebas Neue (display) + Barlow (body) — hard, vertical, unforgiving

**NOT a locked theme.** Venetian blind shadows work on any dark hero that needs dramatic lighting. Hard cast shadows (no blur) work as a design language on any bold UI. Spotlight radials work on any product photography section.

**Sensory anchors:** Rain on pavement that's been warm all day. A phone ringing in an empty office. The moment the light comes from the wrong angle and everything looks guilty.

---

### Wes Anderson

Every frame is a dollhouse. Symmetry is love; color is character.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Perfect bilateral symmetry | Flexbox/Grid with `justify-content: center; align-items: center` enforced at every level — every element centered, nothing left-aligned by accident | Full page layouts, hero sections |
| Centered-frame composition | `max-width: 680px; margin: 0 auto; text-align: center` enforced as default container — eye-level camera logic | All content blocks |
| Pastel field palette | Muted, de-saturated pastels — NOT candy. `hsl(n, 30-40%, 70-80%)` — colors that have aged gracefully | Background sections |
| Title card text | `font-family: serif; letter-spacing: 0.2em; text-transform: uppercase; font-size: 0.75rem` — every label reads like a film chapter card | Section labels, meta text |
| Shadow box frame | `box-shadow: 0 0 0 8px var(--bg), 0 0 0 10px var(--border)` — double-matted frame around images | Photography, portraits |
| Tableau horizontal reveal | Elements slide in from left at exact equal intervals (`animation-delay: 0.15s` increments) — the Wes pan reveal | Feature rows, team cards |
| Miniature detail border | `border: 2px solid hsl(var(--accent)); border-radius: 2px; padding: 2px` on ALL decorative elements — obsessive framing | Badges, tags, dividers |

**Color schema:**
```css
/* Grand Budapest */
--wa-pink: 340 35% 78%;           /* dusty rose */
--wa-purple: 270 25% 55%;         /* muted plum */
--wa-red: 0 60% 50%;              /* Mendl's red */
--wa-cream: 42 30% 92%;           /* aged paper */
--wa-fg: 220 20% 15%;             /* near-navy text */

/* Isle of Dogs */
--wa-amber: 35 55% 55%;           /* warm amber */
--wa-khaki: 70 20% 55%;           /* military olive */
--wa-steel: 210 20% 45%;          /* steel grey */

/* Moonrise Kingdom */
--wa-tan: 35 30% 70%;             /* camp tan */
--wa-forest: 130 25% 35%;         /* scout green */
--wa-orange: 25 70% 55%;          /* adventure orange */
```

**Font pairings:**
- **Futura first:** Futura PT (all text, weight variation only) — Wes Anderson's actual typeface
- **European storybook:** Libre Baskerville (headings) + Lato (body) — dignified warmth
- **Title card:** Josefin Slab (headings) + Josefin Sans (body) — same family, slab vs sans contrast

**NOT a locked theme.** Perfect bilateral symmetry works as a design system on any brand that wants to feel precise. Centered-frame compositions work on any hero that needs calm authority. Pastel field palettes work on any brand that wants to feel curated.

**Sensory anchors:** A lobby that was designed by someone who loved it. The color of a hotel that used to be the best hotel. Everything exactly where it said it would be.

---

### Blade Runner

Neon light in rain. Every surface reflects something. The city is alive and doesn't notice you.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Dense neon layer stack | Multiple `box-shadow` colors on one element — `0 0 10px #ff0080, 0 0 30px #ff0080, 0 0 60px rgba(255,0,128,0.4)` — light bleeds onto itself | Headings, borders, cards |
| Perpetual rain overlay | SVG animated streaks (thin diagonal lines, `opacity: 0.08-0.15`), continuous loop — city never dries | Hero backgrounds, dark sections |
| Hologram flicker | `@keyframes` rapid opacity oscillation (`1 → 0.7 → 1 → 0.85 → 1`) with `hue-rotate` micro-shifts — unstable projection | CTAs, accent elements |
| Wet street reflection | `element::after` with `transform: scaleY(-1); opacity: 0.15; filter: blur(4px)` — puddle mirror below content | Cards, images |
| Smog horizon gradient | `linear-gradient(180deg, hsl(240,40%,3%) 0%, hsl(270,50%,10%) 40%, hsl(300,60%,15%) 60%, hsl(0,0%,5%) 100%)` — the BR sky | Hero backgrounds |
| Language-layer text | Japanese/Korean characters at 3-5% opacity behind English text — megacity information density | Hero backgrounds |
| Data corruption artifact | `@keyframes` brief `clip-path` slice displacement on hover — data integrity error | Interactive elements, images |

**Color schema:**
```css
/* Replicant City */
--br-bg: 240 40% 3%;              /* night black */
--br-neon-red: 350 100% 55%;      /* blood neon */
--br-neon-blue: 190 100% 55%;     /* cyan neon */
--br-neon-gold: 40 90% 55%;       /* amber advertisement |
--br-smog: 280 30% 15%;           /* purple smog */
--br-rain: 200 20% 60%;           /* rain grey |

/* 2049 Variant */
--br-orange: 25 90% 55%;          /* desert orange */
--br-cold: 210 50% 40%;           /* cold corporate blue */
--br-holo: 175 80% 55%;           /* hologram cyan */
```

**Font pairings:**
- **Megacity signage:** Orbitron (headings) + IBM Plex Sans (body) — future bureaucratic
- **Street level:** Share Tech Mono (headings) + Barlow (body) — terminal + field manual
- **Replicant ID:** Rajdhani (headings) + Source Sans 3 (body) — geometric, slightly alien

**NOT a locked theme.** Dense neon layer stacks work on any dark premium UI. Perpetual rain overlays add atmosphere to any dark hero. Hologram flicker works on any tech or sci-fi brand's interactive elements.

**Sensory anchors:** Neon that reflects on everything except what you're looking for. The warmth of a screen in the cold. A city that was built on top of another city on top of another city.

---

### Studio Ghibli

Everything is hand-drawn: the wind, the soot, the kindness. Nature is a character with dialogue.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Watercolor wash background | `background: hsl(var(--sky))` + SVG `feTurbulence` displacement at low scale — soft, wet paper color | Hero sections, section backgrounds |
| Hand-drawn line border | SVG `<rect>` with `stroke-dasharray` set to irregular values + slight `stroke-width` variation — pencil, not ruler | Cards, image frames, containers |
| Cloud-billowing animation | Large `border-radius: 50% 60% 50% 60%` shapes with slow `@keyframes` border-radius morph — cumulus clouds that breathe | Hero backgrounds, section accents |
| Totoro forest palette | Deep teals, warm ochres, dusk purples — nature at the moment light changes | Section backgrounds |
| Dust bunny particles | Tiny circular elements (4-8px), dark grey at low opacity, drifting slowly with slight rotation — soot sprites | Dark backgrounds, loading states |
| Painted texture overlay | `mix-blend-mode: multiply` on a `feTurbulence`-based canvas texture over backgrounds — color-pencil background | All backgrounds |
| Soft horizon line | `border-bottom: 2px solid hsl(var(--horizon))` with `filter: blur(1px)` — a horizon drawn by hand | Section separators |

**Color schema:**
```css
/* Totoro Summer */
--ghibli-sky: 200 60% 70%;        /* afternoon sky */
--ghibli-grass: 100 45% 45%;      /* deep summer grass */
--ghibli-earth: 30 40% 55%;       /* warm earth */
--ghibli-shadow: 240 25% 35%;     /* cool tree shadow */
--ghibli-cream: 40 35% 92%;       /* warm cloud white */

/* Spirited Away */
--ghibli-lantern: 35 90% 60%;     /* paper lantern amber */
--ghibli-bathhouse: 0 60% 45%;    /* red gate vermillion */
--ghibli-deep: 220 35% 15%;       /* night river dark */
--ghibli-spirit: 270 40% 60%;     /* spirit purple */
```

**Font pairings:**
- **Storybook hand:** Klee One (headings) + Noto Sans (body) — hand-lettered warmth, bilingual
- **Adventure journal:** Architects Daughter (headings) + Lato (body) — hand-drawn notebook
- **Ghibli world:** M PLUS Rounded 1c (headings) + Source Han Sans (body) — Japanese digital warmth

**NOT a locked theme.** Watercolor wash backgrounds work on any nature, wellness, or children's brand. Cloud-billowing animations work on any site that needs organic motion. Hand-drawn line borders work on any brand that wants to feel crafted.

**Sensory anchors:** Grass that has been walked on by something larger than you. Warmth from a bath house seen across a lake at night. The feeling that the forest remembers your name.

---

### Kubrick

Geometry as threat. Symmetry that watches back. The frame knows you're there.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| One-point perspective layout | CSS perspective grid centered on single vanishing point — corridor, tunnel, or room receding to center | Hero sections, full-bleed backgrounds |
| Cold bilateral symmetry | Strict `display: grid; grid-template-columns: 1fr 1fr` with mirror content — not Wes Anderson's warm symmetry, this is cold | Hero, feature sections |
| Floor pattern repeat | `repeating-linear-gradient` or `conic-gradient` checkerboard in perspective — the Overlook floor | Backgrounds, hero floors |
| Cold blue-white palette | `hsl(210-220, 20-30%, 85-95%)` — not warm white. Institutional, fluorescent | Section backgrounds |
| Slow zoom tension | `@keyframes { from { transform: scale(1) } to { transform: scale(1.03) } }` over 8-12 seconds — almost imperceptible approach | Hero backgrounds |
| Extreme close-up crop | `object-fit: cover; object-position: center` on portrait images at 2:1 ratio — faces cropped to just eyes | Profile images, testimonials |
| Red as the only color | Single red accent in otherwise monochromatic cold palette — the door, the carpet, the detail | Accent system — one element only |

**Color schema:**
```css
/* 2001 Cold */
--kub-bg: 0 0% 96%;               /* white room */
--kub-fg: 220 15% 10%;            /* cold dark */
--kub-cold-white: 210 20% 92%;    /* fluorescent white */
--kub-red: 0 80% 45%;             /* the only red */
--kub-grey: 210 10% 55%;          /* steel mid-tone */

/* The Shining */
--kub-gold: 38 60% 50%;           /* Overlook carpet gold */
--kub-blood: 0 70% 35%;           /* that red */
--kub-floor: 38 20% 80%;          /* hex tile tan */
```

**Font pairings:**
- **Institutional:** Helvetica Neue (all text, weights only) — the actual Kubrick typeface
- **Future cold:** Futura PT (headings) + IBM Plex Sans (body) — 2001 rational
- **Document authority:** DM Serif Text (headings) + DM Sans (body) — precise, no warmth added

**NOT a locked theme.** One-point perspective layouts work on any hero that needs psychological weight. Slow zoom tension works on any background image for ambient dread or authority. Cold blue-white palettes work on any SaaS or medical brand.

**Sensory anchors:** A hallway that is exactly as long as you feared. White that has been cleaned too many times. Something at the end of the room that was always there.

---

### Wong Kar-Wai

Time is a texture. Longing has a frame rate. Colors remember things the people don't say.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Heavy color saturation | `filter: saturate(160%) contrast(110%)` on images — memories are more saturated than reality | Photography, hero images |
| Motion blur trailing | `@keyframes` with `filter: blur(3px)` at mid-animation, clearing to sharp at end — step-printed movement | Page transitions, hover animations |
| Narrow color temperature shift | Alternating sections: warm amber → cool blue-green — emotional temperature as color temperature | Section backgrounds |
| Clock stopped detail | Analog clock SVG with `animation-play-state: paused` or zero velocity — time that isn't moving | Hero details, decorative elements |
| Venetian blind light repeat | `repeating-linear-gradient(0deg, transparent 0, transparent 20px, rgba(255,200,100,0.08) 20px, rgba(255,200,100,0.08) 22px)` — warm horizontal light bands | Photography overlays |
| Overexposed memory | `filter: brightness(120%) contrast(85%) saturate(130%)` — burned-in recollection | Hero images, flashback sections |
| Rain-blurred text | `filter: blur(0.5px)` on secondary text — things on the periphery don't need to be sharp | Subheadings, captions |

**Color schema:**
```css
/* Chungking Express */
--wkw-amber: 35 80% 50%;          /* noodle shop amber */
--wkw-green: 140 40% 35%;         /* Hong Kong green */
--wkw-neon-pink: 330 80% 60%;     /* Midnight Express pink */
--wkw-dark: 220 30% 8%;           /* corridor black */
--wkw-warm-white: 38 20% 88%;     /* warm lamp light */

/* In the Mood */
--wkw-red: 5 75% 40%;             /* cheongsam red */
--wkw-gold: 42 70% 55%;           /* hallway gold */
--wkw-shadow: 240 30% 12%;        /* stairwell blue */
```

**Font pairings:**
- **Midnight dispatch:** Noto Serif CJK (headings) + Source Han Sans (body) — Hong Kong bilingual weight
- **Longing editorial:** Playfair Display (italic headings) + Source Serif 4 (body) — the diary font
- **Corridor silence:** DM Serif Display (headings) + DM Sans Light (body) — loaded restraint

**NOT a locked theme.** Heavy color saturation works on any photography brand. Motion blur trailing works as a page transition on any site. Narrow color temperature shifts work as a section system on any emotional brand.

**Sensory anchors:** A number you memorized but never used. The sound of rain on air conditioning. Amber light from a kitchen that belongs to someone else.

---

### Terrence Malick

The camera never looks at the thing; it looks at the thing the thing is near. Golden hour is not a filter — it is a philosophy.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Perpetual golden hour | `filter: sepia(20%) saturate(130%) brightness(105%) hue-rotate(-10deg)` on all images — the sun is always setting | All photography |
| Lens flare accent | SVG radial gradient white→transparent, thin ellipse, positioned at light source angle — not added, found | Hero images, photography |
| Flowing text overlay | Italic quote text (`font-style: italic; font-weight: 300`) at large size, low opacity, over landscape photography | Hero sections, full-bleed imagery |
| Grass/wheat field motion | `background-attachment: fixed` on landscape image + `@keyframes` subtle horizontal sway on foreground element | Hero backgrounds |
| Whispering caption style | `font-size: 0.8rem; font-style: italic; color: rgba(255,255,255,0.5); max-width: 300px` — not exposition, poetry | Image captions, pull quotes |
| Sky-dominant crop | `object-position: center 30%` on landscape images — more sky than ground, always | Hero images, section backgrounds |
| Memory dissolve transition | `@keyframes` from `opacity: 0; filter: blur(8px)` to `opacity: 1; filter: blur(0)` — not a fade, a recognition | Page transitions, section reveals |

**Color schema:**
```css
/* Tree of Life */
--mal-gold: 40 80% 60%;           /* golden hour primary */
--mal-sky: 200 50% 65%;           /* afternoon sky */
--mal-earth: 25 35% 40%;          /* warm earth */
--mal-green: 100 35% 40%;         /* wheat field green */
--mal-light: 40 30% 92%;          /* sunlit white */
--mal-shadow: 25 20% 15%;         /* warm shadow */

/* Badlands */
--mal-dust: 30 30% 65%;           /* dusty plains */
--mal-horizon: 15 25% 35%;        /* dusk horizon brown */
--mal-flame: 20 90% 55%;          /* burning orange */
```

**Font pairings:**
- **Voiceover whisper:** Cormorant Garamond (italic headings) + Lato Light (body) — interior monologue
- **Nature documentary:** Libre Baskerville (headings) + Source Serif 4 (body) — literary observation
- **Field notes:** IM Fell DW Pica (headings) + Lora (body) — hand-written world

**NOT a locked theme.** Perpetual golden hour treatment works on any photography-heavy site. Flowing text overlays work on any brand that wants to feel meditative. Memory dissolve transitions work on any site's page navigation.

**Sensory anchors:** Light that arrives from one direction only. Grass that moves while everything else stands still. A question asked to no one that the landscape answers.

---

### David Lynch

The suburb is where the strange sleeps. Velvet and static. Something is wrong and it has been wrong for a long time.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Red velvet texture | `background: hsl(0 60% 20%)` + noise overlay + `background-blend-mode: multiply` — fabric that absorbs light | Hero sections, curtain panels |
| Flickering light instability | `@keyframes` with `opacity: 1 → 0.92 → 1 → 0.97 → 1` at irregular intervals (not `step-end`) — bulb about to fail | Background lighting elements |
| Dual reality split | CSS Grid two-column with `filter: saturate(0)` on one side, full color other side — two worlds occupying same frame | Hero layouts, before/after sections |
| Slow sine wave drift | `@keyframes` with `transform: translateY(sin-wave)` on background element over 8-12 seconds — something beneath the surface | Background layers |
| Suburban color under noir | Bright pastel colors (`hsl(200 40% 75%)`) rendered on dark background — the cheerful and the sinister co-present | Color system |
| Industrial sound visual | Heavy `letter-spacing: 0.3em; text-transform: uppercase` on small text — like a safety label in a mill | Labels, meta text |
| Coffee cup steam | Small SVG wisp rising from element, `opacity: 0.2`, slow upward drift — the mundane detail that anchors the uncanny | Decorative elements |

**Color schema:**
```css
/* Twin Peaks */
--lynch-red: 0 60% 35%;           /* velvet red */
--lynch-black: 0 0% 3%;           /* lodge black */
--lynch-white: 0 0% 95%;          /* fluorescent white */
--lynch-yellow: 48 80% 55%;       /* diner yellow */
--lynch-green: 150 30% 35%;       /* Douglas fir green */

/* Blue Velvet */
--lynch-blue: 220 50% 30%;        /* suburban night */
--lynch-ear: 25 40% 45%;          /* earth, severed */
--lynch-fire: 20 80% 50%;         /* LOG LADY fire */
```

**Font pairings:**
- **Diner menu:** Special Elite (headings) + Courier Prime (body) — 1950s American, slightly wrong
- **Log lady:** Libre Baskerville (headings) + Georgia (body) — suburban domesticity with weight
- **Industrial dream:** Space Mono (headings) + Inconsolata (body) — mill town bureaucratic

**NOT a locked theme.** Red velvet textures work on any dark luxury brand. Flickering light instability works on any atmospheric dark site. Dual reality splits work as hero layouts on any brand with a before/after or product contrast story.

**Sensory anchors:** The red curtain. The feeling that the backwards-talking has always been happening, you just couldn't hear it. A cup of coffee that has been there exactly the right amount of time.

---

### Mixes well with

| Cinema combo | Result |
|-------------|--------|
| Film Noir shadows + Terminal green | Cyberpunk noir — hacker detective aesthetic |
| Wes Anderson symmetry + Art Deco gold | Grand Hotel — precise luxury, every tile counted |
| Blade Runner neon + Vaporwave pastels | Retro-dystopia — neon nostalgia in the megacity |
| Ghibli watercolor + Impressionism blur | Dreamed landscape — hand-painted memory |
| Kubrick cold white + Bauhaus primary | Total control — institutional with color authority |
| Wong Kar-Wai amber + Film Noir rain | Hong Kong midnight — saturated longing in the rain |
| Malick golden hour + Art Nouveau organics | Sacred nature — botanical light, everything alive |
| Lynch velvet + 1990s Grunge | Small town darkness — suburban psychedelia |
