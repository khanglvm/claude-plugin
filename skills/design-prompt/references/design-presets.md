# Design Presets

Aesthetic bundles, font pairings, and color palettes for auto-suggestion. Each bundle is a cohesive starting point the user can adopt or mix.

## Aesthetic Bundles

### Dark Premium (Apple-inspired)
- **Fonts:** Instrument Serif (italic, headings) + Barlow (300-600, body)
- **Colors:** Pure black bg, white text, white/60 body, white/40 muted
- **Effect:** Liquid glass morphism, blur transitions
- **Vibe:** Luxury tech, high-end agency, premium SaaS
- **CSS vars:** `--background: 0 0% 0%; --foreground: 0 0% 100%; --primary: 0 0% 100%;`

### Dark Minimal (Linear/Vercel-inspired)
- **Fonts:** Inter (400-600, headings) + Inter (300-400, body)
- **Colors:** Near-black bg (#0A0A0A), gray-200 text, gray-500 body
- **Effect:** Subtle gradient borders, soft glow on hover
- **Vibe:** Developer tools, technical products, clean SaaS
- **CSS vars:** `--background: 0 0% 4%; --foreground: 0 0% 87%; --primary: 220 70% 55%;`

### Dark Bold (Cyberpunk/Neon)
- **Fonts:** Space Grotesk (500-700, headings) + JetBrains Mono (300-400, body)
- **Colors:** Deep navy bg, electric blue/purple accents, white text
- **Effect:** Neon glow, gradient text, grain texture overlay
- **Vibe:** Gaming, crypto, futuristic tech
- **CSS vars:** `--background: 230 25% 7%; --foreground: 0 0% 95%; --primary: 250 90% 65%;`

### Light Minimal (Stripe-inspired)
- **Fonts:** Inter (500-700, headings) + Source Serif 4 (300-400, body)
- **Colors:** White bg, slate-900 text, slate-500 body, blue-600 accent
- **Effect:** Subtle shadows, smooth micro-animations
- **Vibe:** Fintech, professional SaaS, enterprise
- **CSS vars:** `--background: 0 0% 100%; --foreground: 222 47% 11%; --primary: 221 83% 53%;`

### Light Warm (Notion-inspired)
- **Fonts:** Georgia / Lora (headings) + Inter (body)
- **Colors:** Warm white (#FAFAF8), warm gray text, orange/amber accent
- **Effect:** Paper-like texture, rounded corners, gentle shadows
- **Vibe:** Productivity, docs, knowledge tools, creative tools
- **CSS vars:** `--background: 40 20% 98%; --foreground: 24 10% 10%; --primary: 25 95% 53%;`

### Light Clean (Apple.com-inspired)
- **Fonts:** SF Pro Display / Outfit (headings) + SF Pro Text / DM Sans (body)
- **Colors:** Pure white bg, near-black text, blue accent
- **Effect:** Large whitespace, hero product shots, smooth scroll
- **Vibe:** Consumer products, hardware, lifestyle tech
- **CSS vars:** `--background: 0 0% 100%; --foreground: 0 0% 7%; --primary: 211 100% 50%;`

### Colorful Playful
- **Fonts:** Bricolage Grotesque (headings) + DM Sans (body)
- **Colors:** Pastel gradients, multi-color accents, light bg
- **Effect:** Bento grid, rounded-3xl cards, bouncy animations
- **Vibe:** Creative agencies, startups, social apps
- **CSS vars:** `--background: 0 0% 98%; --foreground: 240 10% 10%; --primary: 270 80% 60%;`

### Bold Brutalist
- **Fonts:** Clash Display / Anton (headings) + Space Mono (body)
- **Colors:** High contrast, raw black/white, occasional neon accent
- **Effect:** Thick borders, no border-radius, monospace everywhere
- **Vibe:** Art, editorial, experimental, provocative
- **CSS vars:** `--background: 0 0% 100%; --foreground: 0 0% 0%; --primary: 0 0% 0%;`

### Soft Organic
- **Fonts:** Fraunces (headings) + Nunito Sans (body)
- **Colors:** Sage green, cream, earth tones, muted palette
- **Effect:** Soft blobs, organic SVG shapes, gentle parallax
- **Vibe:** Wellness, sustainability, organic brands, lifestyle
- **CSS vars:** `--background: 80 25% 96%; --foreground: 150 20% 15%; --primary: 150 40% 40%;`

### Glassmorphism
- **Fonts:** Plus Jakarta Sans (headings) + Figtree (body)
- **Colors:** Gradient bg (purple→blue→pink), white frosted glass cards
- **Effect:** backdrop-filter blur, translucent layers, gradient mesh bg
- **Vibe:** Modern apps, dashboards, creative portfolios
- **CSS vars:** `--background: 250 30% 12%; --foreground: 0 0% 100%; --primary: 260 80% 70%;`

## Font Pairings (Google Fonts)

| # | Heading | Body | Mood |
|---|---------|------|------|
| 1 | Instrument Serif (italic) | Barlow (300-600) | Premium editorial |
| 2 | Inter (500-700) | Inter (300-400) | Clean technical |
| 3 | Space Grotesk (500-700) | JetBrains Mono (300-400) | Techy monospace |
| 4 | Playfair Display (700) | Source Sans 3 (300-400) | Elegant editorial |
| 5 | Plus Jakarta Sans (600-800) | Figtree (300-400) | Modern friendly |
| 6 | Bricolage Grotesque (600-800) | DM Sans (300-500) | Playful geometric |
| 7 | Outfit (500-700) | DM Sans (300-400) | Clean consumer |
| 8 | Clash Display (600-700) | Space Mono (400) | Bold brutalist |
| 9 | Fraunces (600-800) | Nunito Sans (300-400) | Warm organic |
| 10 | Sora (500-700) | Work Sans (300-400) | Balanced modern |
| 11 | Poppins (600-700) | Lato (300-400) | Universal friendly |
| 12 | Manrope (600-800) | IBM Plex Sans (300-400) | Professional tech |
| 13 | Cabinet Grotesk (700) | General Sans (300-400) | Trendy startup |
| 14 | Lora (600-700, italic) | Roboto (300-400) | Classic serif + sans |
| 15 | Montserrat (600-700) | Open Sans (300-400) | Dependable corporate |

## Color Palette Templates

### Pure Black
```css
--background: 0 0% 0%;
--foreground: 0 0% 100%;
--primary: 0 0% 100%;
--primary-foreground: 0 0% 0%;
--secondary: 0 0% 8%;
--muted: 0 0% 15%;
--muted-foreground: 0 0% 64%;
--accent: 0 0% 15%;
--border: 0 0% 100% / 0.15;
```

### Slate Dark
```css
--background: 222 47% 4%;
--foreground: 210 40% 98%;
--primary: 217 91% 60%;
--primary-foreground: 0 0% 100%;
--secondary: 217 33% 17%;
--muted: 217 33% 17%;
--muted-foreground: 215 20% 65%;
--accent: 217 33% 17%;
--border: 217 33% 17%;
```

### Navy Deep
```css
--background: 230 25% 7%;
--foreground: 0 0% 95%;
--primary: 250 90% 65%;
--primary-foreground: 0 0% 100%;
--secondary: 230 20% 14%;
--muted: 230 15% 20%;
--muted-foreground: 230 10% 55%;
--accent: 280 80% 65%;
--border: 230 20% 18%;
```

### Clean White
```css
--background: 0 0% 100%;
--foreground: 222 47% 11%;
--primary: 221 83% 53%;
--primary-foreground: 0 0% 100%;
--secondary: 210 40% 96%;
--muted: 210 40% 96%;
--muted-foreground: 215 16% 47%;
--accent: 210 40% 96%;
--border: 214 32% 91%;
```

### Warm Cream
```css
--background: 40 20% 98%;
--foreground: 24 10% 10%;
--primary: 25 95% 53%;
--primary-foreground: 0 0% 100%;
--secondary: 40 15% 93%;
--muted: 40 15% 93%;
--muted-foreground: 24 5% 45%;
--accent: 40 15% 93%;
--border: 40 10% 88%;
```

### Gradient Mesh (for glassmorphism)
```css
--background: 250 30% 12%;
--foreground: 0 0% 100%;
--primary: 260 80% 70%;
--primary-foreground: 0 0% 100%;
--secondary: 280 40% 20%;
--muted: 260 20% 18%;
--muted-foreground: 260 10% 60%;
--accent: 310 80% 65%;
--border: 260 30% 25%;
```

---

## Immersive Atmospheric Bundles

These are environmental storytelling themes. NOT rigid templates — they are ingredient palettes. Mix freely: forest fog on a fire site, ember particles over dark premium, moss textures on organic layout. Each bundle lists building blocks, not a locked recipe.

### Deep in Forest

An immersive nature journey. The page IS a forest — users don't read a page, they walk through it.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Fog layers | 2-3 semi-transparent gradient layers that drift horizontally, opacity varies with scroll depth | Any dark/moody theme |
| Day-to-night shift | CSS `--time-hue` and `--time-lightness` custom properties that transition across scroll progress — top of page is golden dawn, middle is green daylight, bottom is blue moonlight | Section-based color systems |
| Canopy entrance | Hero starts zoomed into dense leaf texture (scale 3-5x), scrolling zooms out to reveal clearing with content | Cinematic close-in layout |
| Parallax forest layers | 3-5 PNG/SVG tree/branch silhouette layers at different scroll speeds — foreground branches partially occlude content | Any multi-section page |
| Content occlusion | Tree trunks, hanging vines, or leaf clusters positioned `absolute` over content edges — content peeks through gaps in foliage | Split layouts, cards |
| Ancient textures | Moss, bark, root overlays via `mix-blend-mode: multiply` on containers — aged stone for headers, cracked wood for dividers | Organic themes |
| Adventure path | No fixed background — each section is a location (clearing → river → cave → summit). Scroll IS the journey. Between sections: environment transitions (fog thickens, light changes, sounds shift) | Storytelling sites |
| Root borders | Section dividers are SVG tree roots that crawl across the page, not straight lines | Any section boundary |
| Leaf particles | Falling leaves (2-4 types, slow tumble with rotation, wind sway) — NOT small circles bobbing. Full leaf shapes with realistic fall physics | Atmospheric backgrounds |
| Light shafts | Diagonal gradient beams (gold/white, low opacity) simulating sunlight through canopy gaps. Shift position on scroll. | Forest, cathedral, fog themes |

**Color schema (flexible — shift the time-of-day dial):**
```css
/* Dawn (top sections) */
--forest-dawn-bg: 35 30% 8%;        /* warm dark brown */
--forest-dawn-fg: 40 40% 85%;       /* golden cream */
--forest-dawn-accent: 35 70% 55%;   /* amber gold */
--forest-dawn-mist: 35 20% 40% / 0.15;

/* Day (middle sections) */
--forest-day-bg: 140 25% 8%;        /* deep forest green-black */
--forest-day-fg: 80 20% 88%;        /* pale sage */
--forest-day-accent: 120 40% 45%;   /* moss green */
--forest-day-mist: 120 15% 50% / 0.1;

/* Night (bottom sections) */
--forest-night-bg: 220 20% 5%;      /* blue-black */
--forest-night-fg: 210 30% 80%;     /* moonlight blue-white */
--forest-night-accent: 200 50% 50%; /* cold blue */
--forest-night-mist: 220 20% 40% / 0.2;
```

**Font pairings that fit:**
- **Mystical editorial:** Fraunces (italic headings) + Nunito Sans (body) — warm, aged
- **Ancient carved:** Cormorant Garamond (headings) + Lato (body) — classical, stone-inscription feel
- **Adventure map:** Playfair Display (headings) + Source Sans 3 (body) — explorer journal

**NOT a locked theme.** Fog layers work on ANY dark site. Leaf particles work on organic brands. Day-to-night transitions work on storytelling pages that aren't forests. Root borders work anywhere you'd use a section divider.

**Architectural short-schema:**
```
FOREST PAGE FLOW:
  [Canopy Entrance] — hero, scale(5)→1, dense leaf texture zooms out
    ↓ fog thickens
  [First Clearing] — content visible through tree gaps, light shafts
    ↓ path curves, foreground branches slide in from sides
  [Deep Woods] — darker, content partially occluded by trunks/vines
    ↓ fog lifts, light changes (day→dusk)
  [River / Cave / Landmark] — environmental shift, new textures
    ↓ night falls, stars through canopy
  [Summit / Moonlit Clearing] — final CTA, open sky, fog below

Each transition: NOT hard section breaks. Environment elements (fog, light, foliage) continuously morph.
Foreground layers: branches/leaves in front of content (z-index above content)
Content: appears through gaps, clearings, openings in foliage
```

---

### On Fire

Destructive energy. The page burns, smolders, glows. Intensity is a dial — from gentle campfire warmth to full volcanic eruption.

**Core ingredients (pick & combine):**

| Ingredient | What it does | Combine with |
|-----------|-------------|-------------|
| Fire borders | CSS animated borders using conic-gradient with flame colors (red → orange → yellow → white core), flicker via randomized `hue-rotate` keyframes — replaces ALL boring solid/gradient borders | Any card, container, section divider |
| Ember particles | Small glowing dots (2-6px) that rise from bottom, glow orange-red, fade to gray ash, drift with slight wind. NOT bobbing circles — they rise, cool, and die | Dark backgrounds |
| Smoke columns | Large blurred gradient shapes (white/gray at 3-8% opacity) that rise slowly from fire sources, spread and dissipate. `filter: blur(40-80px)` | Headers, behind text |
| Ash fall | Tiny gray/white flakes falling slowly with tumble rotation — like snow but irregular, sparse | Dark sky sections |
| Heat distortion | `backdrop-filter` with subtle animated scale/translate on areas near fire — simulates heat haze ripple | Above fire borders, near bottom of fire sections |
| Charred edges | Content containers with irregular dark edges — `clip-path` with jagged polygon points, or burnt-paper SVG mask around content | Cards, images, sections |
| Crack glow | Hairline cracks in dark surfaces with orange/red glow bleeding through — SVG paths with animated `stroke-dashoffset` reveal + glow filter | Backgrounds, dividers |
| Environmental fire | Context-dependent: burning trees (SVG silhouettes with flame animation at crown), flags on fire (fabric wave + flame tip), volcanic glow (red radial gradient from below horizon), lava flows (slow-moving orange gradient strips) | Storytelling, themed sections |
| Dark sky | Deep charcoal/black with subtle red-orange tint from firelight below. Stars visible but dimmed by smoke haze | Background base |
| Scorched gradient | Bottom-to-top: white-hot (core) → orange → red → dark smoke → black sky. Used as section backgrounds or text gradient | Any fire-themed section |

**Color schema (intensity dial):**
```css
/* Ember (subtle warmth) */
--fire-ember-bg: 0 15% 5%;           /* near-black with warm tint */
--fire-ember-fg: 30 30% 85%;         /* warm white */
--fire-ember-accent: 25 90% 55%;     /* deep orange */
--fire-ember-glow: 15 100% 50% / 0.15;
--fire-ember-border: 20 80% 45%;     /* burnt orange */

/* Blaze (medium intensity) */
--fire-blaze-bg: 5 20% 4%;           /* dark red-black */
--fire-blaze-fg: 40 50% 90%;         /* hot white-yellow */
--fire-blaze-accent: 35 100% 55%;    /* bright orange */
--fire-blaze-glow: 25 100% 50% / 0.25;
--fire-blaze-core: 45 100% 70%;      /* yellow-white core */

/* Inferno (maximum) */
--fire-inferno-bg: 0 30% 3%;         /* deep crimson-black */
--fire-inferno-fg: 50 100% 95%;      /* white-hot */
--fire-inferno-accent: 0 100% 50%;   /* pure red */
--fire-inferno-glow: 30 100% 55% / 0.4;
--fire-inferno-core: 55 100% 80%;    /* blinding yellow */

/* Volcanic (earth + fire) */
--fire-volcanic-bg: 15 15% 6%;       /* dark volcanic rock */
--fire-volcanic-fg: 35 40% 80%;      /* ash-tinged white */
--fire-volcanic-accent: 10 90% 45%;  /* magma red */
--fire-volcanic-lava: 30 100% 50%;   /* flowing orange */
--fire-volcanic-obsidian: 0 0% 8%;   /* glass-black */
```

**Font pairings that fit:**
- **Apocalyptic bold:** Space Grotesk (700, headings) + Barlow (300, body) — strong, modern destruction
- **Ancient forge:** Cormorant Garamond (bold, headings) + Inter (body) — fire meets history
- **War banner:** Clash Display (headings) + Space Mono (body) — brutalist fire

**NOT a locked theme.** Fire borders replace boring CSS borders on ANY site. Ember particles add energy to dark premium. Charred edges work on grunge/editorial. Smoke columns work anywhere you need atmospheric depth.

**Architectural short-schema:**
```
FIRE PAGE FLOW:
  [Dark Sky] — hero, stars dimmed by distant glow on horizon
    ↓ ember particles begin rising from below viewport
  [First Flames] — fire borders appear on containers, warmth enters palette
    ↓ smoke columns rise behind text, heat distortion begins
  [The Blaze] — full fire environment: burning elements, crack glow on surfaces
    ↓ intensity peaks, charred edges on all containers
  [The Core] — hottest section: white-hot text, maximum glow, volcanic elements
    ↓ fire subsides, embers cool to gray ash
  [Aftermath] — cooled palette, ash fall, smoldering remains, CTA emerges from smoke

Intensity curve: subtle → building → peak → cooling
Fire sources: bottom of viewport, specific elements (trees, borders, dividers)
Smoke: rises from fire sources, spreads horizontally at top, thins and dissipates
Environmental elements are CONTEXTUAL — match the content:
  - Agency site: "ideas on fire" — abstract flame borders, no literal trees
  - Gaming/action: full environmental fire, burning landscapes
  - Restaurant/BBQ: controlled fire, campfire warmth, ember glow
  - Sale/urgency: fire borders on pricing, embers on CTAs
```

---

### Mix-and-Match Examples

These bundles are ingredients, not locked packages. Creative combinations:

| Mix | Result |
|-----|--------|
| Forest fog + Dark Premium glass | Luxury brand in misty atmosphere — glass cards float in fog |
| Fire borders + Glassmorphism | Frosted glass containers with animated flame perimeters |
| Forest canopy entrance + any hero | Any site can start with a zoom-through-nature reveal |
| Ember particles + Soft Organic | Warm, campfire-adjacent brand — cozy not destructive |
| Day-to-night shift + any multi-page | Color temperature shifts per page instead of per scroll |
| Charred edges + Bold Brutalist | Destroyed/deconstructed editorial aesthetic |
| Fog layers + Fire smoke | Competing atmospheres — mysterious burning forest |
| Root borders + Ancient textures + Dark Minimal | Tech product with ancient/timeless positioning |
| Leaf particles + Light Warm | Autumn/seasonal theme on warm productive brand |
| Volcanic palette + Neon Glow | Cyberpunk lava city aesthetic |
| Forest light shafts + any dark section | Cathedral/sacred feel without religious imagery |
| Fire crack glow + Gradient borders | Borders that appear to fracture and glow from within |

**Rule:** If the user mentions nature, organic, journey, exploration, ancient, moss, fog, mist → surface Forest ingredients. If they mention energy, intensity, urgency, destruction, power, heat, forge → surface Fire ingredients. If they mention both or something in between → mix. Never present these as all-or-nothing packages.

---

## Text Pattern Templates

### Dark backgrounds
```
Headings: font-heading italic text-white tracking-tight leading-[0.9]
Body: font-body font-light text-white/60 text-sm
Muted: font-body text-white/40 text-xs
Links: text-white/80 hover:text-white underline-offset-4
Buttons: font-body rounded-full
```

### Light backgrounds
```
Headings: font-heading text-foreground tracking-tight leading-tight
Body: font-body font-normal text-muted-foreground text-base
Muted: font-body text-muted-foreground/70 text-sm
Links: text-primary hover:text-primary/80 underline-offset-4
Buttons: font-body rounded-lg
```
