# Effects Catalog

CSS effects, animation patterns, background techniques, and element composition for web design prompts.

## CRITICAL: Animation Anti-Patterns

Before suggesting ANY animation, verify it is NOT:
- ❌ Small decorative shape (circle, dot, blob) with up/down bob animation
- ❌ Abstract floating elements that don't interact with content or user
- ❌ Scattered geometric shapes drifting aimlessly
- ❌ Ornamental particles with no atmospheric purpose
- ❌ Pulsing dots/rings as section decoration

**Every animated element must pass this test:** "If I remove this animation, does the page lose meaning, atmosphere, or usability?" If no → cut it.

---

## Element Composition & Blending

### Rotation as Layout Tool
Elements with intentional rotation create visual energy and break AI-template rigidity.

```css
/* Card rotation in a stack */
.card-stack > *:nth-child(1) { transform: rotate(-2deg); }
.card-stack > *:nth-child(2) { transform: rotate(1.5deg); }
.card-stack > *:nth-child(3) { transform: rotate(-3deg); }
.card-stack > *:nth-child(4) { transform: rotate(0.5deg); }

/* Image rotation with overflow bleed */
.rotated-visual {
  transform: rotate(4deg) scale(1.1);
  transform-origin: center center;
  /* scale(1.1) prevents corner gaps from rotation */
}

/* Text block rotation */
.diagonal-text {
  transform: rotate(-3deg);
  transform-origin: left center;
  /* Entire text block tilts — creates editorial energy */
}
```
**Use for:** Card stacks, image galleries, testimonial layouts, feature showcases. Vary rotation per element (never uniform).

### Mix-Blend-Mode Compositions
Elements that visually merge with backgrounds and each other.

```css
/* Text that inverts over any background */
.blend-difference {
  mix-blend-mode: difference;
  color: white;
  /* Text appears white on dark areas, dark on light areas */
}

/* Image that blends into dark background */
.blend-luminosity {
  mix-blend-mode: luminosity;
  opacity: 0.7;
  /* Image becomes monochromatic, toned by background */
}

/* Overlay element that tints content below */
.blend-overlay {
  mix-blend-mode: overlay;
  /* Enhances contrast of content beneath */
}

/* Soft merge — element fades into background */
.blend-soft {
  mix-blend-mode: soft-light;
  opacity: 0.6;
}

/* Multiply — darkens, great for layered images */
.blend-multiply {
  mix-blend-mode: multiply;
  /* Dark areas absorb, light areas become transparent */
}

/* Screen — lightens, great for glow effects */
.blend-screen {
  mix-blend-mode: screen;
  /* Light areas glow, dark areas become transparent */
}
```
**Use for:** Large headline text over images/video, overlapping visual elements, atmospheric layers, typographic compositions.

### Element Overlap & Intersection
Elements that intentionally bleed into each other's space.

```css
/* Overlapping cards with depth */
.overlap-cascade > * {
  position: relative;
}
.overlap-cascade > *:nth-child(2) { margin-top: -80px; z-index: 2; }
.overlap-cascade > *:nth-child(3) { margin-top: -80px; z-index: 3; }
/* Each card overlaps the one above, creating physical depth */

/* Element bleeding beyond its container */
.bleed-right {
  margin-right: -10vw;
  /* Visual extends beyond grid/container boundary */
}

/* Overlapping text and image */
.overlap-composition {
  display: grid;
  grid-template-columns: 1fr;
}
.overlap-composition > * {
  grid-area: 1 / 1; /* All children overlap */
}
.overlap-composition .text { z-index: 2; align-self: end; padding: 2rem; }
.overlap-composition .image { z-index: 1; }
```

### Gradient Mask Transitions
Elements that fade INTO each other rather than having hard edges.

```css
/* Fade element into background at edges */
.gradient-mask-bottom {
  -webkit-mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
  mask-image: linear-gradient(to bottom, black 60%, transparent 100%);
}

/* Fade left and right edges */
.gradient-mask-sides {
  -webkit-mask-image: linear-gradient(to right, transparent, black 15%, black 85%, transparent);
  mask-image: linear-gradient(to right, transparent, black 15%, black 85%, transparent);
}

/* Radial fade — element visible in center, fades at edges */
.gradient-mask-radial {
  -webkit-mask-image: radial-gradient(ellipse at center, black 40%, transparent 70%);
  mask-image: radial-gradient(ellipse at center, black 40%, transparent 70%);
}

/* Section transition — bottom of section A fades into top of section B */
.section-fade-out {
  -webkit-mask-image: linear-gradient(to bottom, black 70%, transparent 100%);
  mask-image: linear-gradient(to bottom, black 70%, transparent 100%);
}
```
**Use for:** Section transitions, image edges, overlapping content areas, creating depth without borders.

---

## Signature CSS Effects

### Liquid Glass (Apple-inspired)
Two variants: `.liquid-glass` (subtle) and `.liquid-glass-strong` (prominent).

```css
.liquid-glass {
  background: rgba(255, 255, 255, 0.01);
  background-blend-mode: luminosity;
  backdrop-filter: blur(4px);
  border: none;
  box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1);
  position: relative;
  overflow: hidden;
}
.liquid-glass::before {
  content: '';
  position: absolute; inset: 0;
  border-radius: inherit;
  padding: 1.4px;
  background: linear-gradient(180deg,
    rgba(255,255,255,0.45) 0%, rgba(255,255,255,0.15) 20%,
    rgba(255,255,255,0) 40%, rgba(255,255,255,0) 60%,
    rgba(255,255,255,0.15) 80%, rgba(255,255,255,0.45) 100%);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
.liquid-glass-strong {
  backdrop-filter: blur(50px);
  box-shadow: 4px 4px 4px rgba(0,0,0,0.05),
    inset 0 1px 1px rgba(255,255,255,0.15);
}
```
**Use for:** Navbar pills, buttons, stat containers. NOT for generic cards (use creative shapes instead).

### Glassmorphism (Classic)
```css
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.18);
  border-radius: 16px;
}
```
**Use for:** Modals, floating panels. Combine with irregular clip-path for non-rectangular glass shapes.

### Gradient Border (Animated)
```css
.gradient-border {
  position: relative;
  background: var(--background);
}
.gradient-border::before {
  content: '';
  position: absolute; inset: 0;
  border-radius: inherit;
  padding: 1px;
  background: conic-gradient(from var(--angle, 0deg), var(--primary), var(--accent), var(--primary));
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  animation: rotate-border 4s linear infinite;
}
@property --angle {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}
@keyframes rotate-border {
  to { --angle: 360deg; }
}
```
**Use for:** Featured/highlighted elements. The border rotates continuously — feels alive.

### Neon Glow
```css
.neon-glow {
  box-shadow: 0 0 15px rgba(var(--primary-rgb), 0.3),
    0 0 45px rgba(var(--primary-rgb), 0.1);
  border: 1px solid rgba(var(--primary-rgb), 0.3);
}
.neon-text {
  text-shadow: 0 0 10px rgba(var(--primary-rgb), 0.5),
    0 0 40px rgba(var(--primary-rgb), 0.2);
}
```

### Grain Texture Overlay
```css
.grain::after {
  content: '';
  position: absolute; inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.03;
  pointer-events: none;
  mix-blend-mode: overlay;
}
```
**Use for:** Adding tactile quality. This is atmospheric (covers entire section), NOT a small floating decoration.

### Aurora / Mesh Gradient
```css
.aurora-bg {
  background:
    radial-gradient(ellipse at 20% 50%, rgba(120,80,255,0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 20%, rgba(255,80,120,0.1) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 80%, rgba(80,200,255,0.12) 0%, transparent 50%);
  animation: aurora-shift 25s ease-in-out infinite alternate;
}
@keyframes aurora-shift {
  0% { background-position: 0% 0%, 100% 0%, 50% 100%; }
  100% { background-position: 100% 100%, 0% 100%, 50% 0%; }
}
```

---

## Creative Text Effects

### Cinematic Close-In (Scroll-linked Scale)
Heading starts massively zoomed in, scales down to reveal full text on scroll.
```jsx
const { scrollYProgress } = useScroll({ target: ref });
const scale = useTransform(scrollYProgress, [0, 1], [5, 1]);
const opacity = useTransform(scrollYProgress, [0.6, 1], [0, 1]); // content appears late

<motion.div ref={ref} className="min-h-[200vh]">
  <motion.h1
    style={{ scale, position: 'sticky', top: '40%' }}
    className="text-[6vw] font-heading text-center"
  >
    We Build Digital Futures
  </motion.h1>
  <motion.div style={{ opacity }} className="relative z-10">
    {/* Rest of content appears as heading reaches scale 1 */}
  </motion.div>
</motion.div>
```
**Deps:** `motion`

### Circular Text Around Element
Text arranged along a circular path around a central visual.
```jsx
// SVG approach
<svg viewBox="0 0 500 500" className="w-[500px] h-[500px] animate-spin-slow">
  <defs>
    <path id="circle" d="M 250,250 m -200,0 a 200,200 0 1,1 400,0 a 200,200 0 1,1 -400,0" />
  </defs>
  <text>
    <textPath href="#circle" className="text-sm fill-white/40 tracking-[0.3em]">
      DIGITAL SOLUTIONS · E-COMMERCE · WEB SERVICES · CREATIVE AGENCY ·
    </textPath>
  </text>
</svg>
// Center: absolutely positioned visual element

// CSS: @keyframes spin-slow { to { transform: rotate(360deg); } }
// .animate-spin-slow { animation: spin-slow 30s linear infinite; }
```

### Per-Word Typographic Art
Each word in a headline has different size, weight, or position.
```jsx
<h1 className="font-heading tracking-tight leading-[0.85]">
  <span className="block text-[10vw] font-light italic text-white/40">We</span>
  <span className="block text-[14vw] font-bold text-white">Build</span>
  <span className="block text-[8vw] font-normal text-primary ml-[10vw]">Digital</span>
  <span className="block text-[12vw] font-bold italic text-white">Futures</span>
</h1>
// Each word: different size, weight, indent — creates typography as art
```

### Text with Gradient Reveal on Scroll
Text starts muted, color fills in as user scrolls past.
```jsx
const { scrollYProgress } = useScroll({ target: ref });
const gradientPosition = useTransform(scrollYProgress, [0, 1], ['0%', '100%']);

<motion.p
  style={{
    backgroundImage: 'linear-gradient(to right, white 50%, rgba(255,255,255,0.2) 50%)',
    backgroundSize: '200% 100%',
    backgroundPositionX: gradientPosition,
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
  }}
>
  Your paragraph text here...
</motion.p>
```

---

## Animation Patterns

### Blur-to-Clear Text (BlurText)
Word-by-word reveal using Framer Motion + IntersectionObserver.
- Split text by words
- Each word: `filter: blur(10px) → blur(0px)`, `opacity: 0 → 1`, `y: 50 → 0`
- Stagger: 100ms per word, step duration 0.35s
- **Deps:** `motion`

### Fade In Up with Blur (Section Reveal)
```jsx
<motion.div
  initial={{ opacity: 0, y: 40, filter: 'blur(10px)' }}
  whileInView={{ opacity: 1, y: 0, filter: 'blur(0px)' }}
  transition={{ duration: 0.8, ease: 'easeOut' }}
  viewport={{ once: true }}
/>
```
Duration: 0.6-1.0s minimum. Never snappy — always slow and blended.

### Staggered Children (with rotation)
```jsx
const container = { hidden: {}, show: { transition: { staggerChildren: 0.15 } } }
const item = {
  hidden: { opacity: 0, y: 30, rotate: -2, filter: 'blur(8px)' },
  show: { opacity: 1, y: 0, rotate: 0, filter: 'blur(0px)', transition: { duration: 0.6 } }
}
```
Items arrive with slight rotation that straightens — more organic than pure vertical slide.

### Counter Animation (Stats)
Count up numbers on scroll intersection. Use `useInView` + `useMotionValue` + `useTransform`.
```jsx
const count = useMotionValue(0);
const rounded = useTransform(count, Math.round);
useEffect(() => {
  if (inView) {
    const controls = animate(count, target, { duration: 2, ease: 'easeOut' });
    return controls.stop;
  }
}, [inView]);
```

### Marquee / Infinite Scroll
CSS-only horizontal scroll for text strips or partner names:
```css
@keyframes marquee { from { transform: translateX(0); } to { transform: translateX(-50%); } }
.marquee { animation: marquee 30s linear infinite; }
/* Duplicate content inside to create seamless loop */
```

### Parallax Scroll (Multi-layer)
Three-layer depth system:
```jsx
const { scrollY } = useScroll();
const bgY = useTransform(scrollY, [0, 1000], [0, -100]);     // 0.1x — slow
const contentY = useTransform(scrollY, [0, 1000], [0, 0]);    // 1x — normal
const fgY = useTransform(scrollY, [0, 1000], [0, -300]);      // 0.3x — fast

// Background blobs/gradients move slowly
// Content stays normal
// Foreground accents (if any) move faster — creates depth
```

### Hover Glass Shimmer
White gradient sweep across surface on hover.
```css
.shimmer {
  position: relative;
  overflow: hidden;
}
.shimmer::after {
  content: '';
  position: absolute;
  top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: linear-gradient(
    to right,
    transparent 0%,
    rgba(255,255,255,0.05) 45%,
    rgba(255,255,255,0.1) 50%,
    rgba(255,255,255,0.05) 55%,
    transparent 100%
  );
  transform: rotate(25deg) translateX(-100%);
  transition: transform 0.6s ease;
}
.shimmer:hover::after {
  transform: rotate(25deg) translateX(100%);
}
```

### Scroll-Linked Section Transitions
Sections blend into each other as user scrolls.
```jsx
// Current section fades and blurs as next section approaches
const opacity = useTransform(scrollYProgress, [0.7, 1], [1, 0]);
const blur = useTransform(scrollYProgress, [0.7, 1], [0, 10]);
const filterValue = useMotionTemplate`blur(${blur}px)`;
```

---

## Background Techniques

### MP4 Video Background
```jsx
<video autoPlay loop muted playsInline className="absolute inset-0 w-full h-full object-cover z-0"
  poster="/images/fallback.jpeg">
  <source src="/video.mp4" type="video/mp4" />
</video>
```

### HLS Video Background (hls.js)
```jsx
useEffect(() => {
  if (Hls.isSupported()) {
    const hls = new Hls();
    hls.loadSource(src);
    hls.attachMedia(videoRef.current);
  } else if (videoRef.current.canPlayType('application/vnd.apple.mpegurl')) {
    videoRef.current.src = src;
  }
}, [src]);
```
**Deps:** `hls.js`

### Video Fade Overlays (top + bottom)
```jsx
<div className="absolute top-0 left-0 right-0 h-[200px] bg-gradient-to-b from-black to-transparent z-[1]" />
<div className="absolute bottom-0 left-0 right-0 h-[200px] bg-gradient-to-t from-black to-transparent z-[1]" />
```

### Desaturated Video
```jsx
<video style={{ filter: 'saturate(0)' }} ... />
```

### Gradient Overlay on Image
```jsx
<div className="relative">
  <img src="..." className="w-full h-full object-cover" />
  <div className="absolute inset-0 bg-gradient-to-b from-transparent via-black/50 to-black" />
</div>
```

### Animated Mesh Gradient Background
Slow-moving gradient that creates atmospheric depth.
```css
.mesh-bg {
  background:
    radial-gradient(at 40% 20%, hsla(260,80%,50%,0.15) 0px, transparent 50%),
    radial-gradient(at 80% 0%, hsla(310,80%,50%,0.1) 0px, transparent 50%),
    radial-gradient(at 0% 50%, hsla(200,80%,50%,0.12) 0px, transparent 50%),
    radial-gradient(at 80% 80%, hsla(260,80%,50%,0.08) 0px, transparent 50%);
  animation: mesh-drift 20s ease-in-out infinite alternate;
}
@keyframes mesh-drift {
  0% { background-size: 100% 100%; background-position: 0% 0%; }
  50% { background-size: 120% 120%; background-position: 50% 50%; }
  100% { background-size: 100% 100%; background-position: 100% 100%; }
}
```

---

## Atmospheric Environment Effects

Immersive environmental techniques from `design-presets.md` atmospheric bundles. Each technique is standalone — use individually or combine.

### Fog / Mist Layers
Multiple semi-transparent gradient layers that drift horizontally, creating depth.
```css
.fog-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
}
.fog-layer-1 {
  background: linear-gradient(90deg,
    transparent 0%, rgba(200,210,220,0.06) 20%,
    rgba(200,210,220,0.12) 50%, rgba(200,210,220,0.06) 80%,
    transparent 100%);
  animation: fog-drift-1 25s ease-in-out infinite alternate;
}
.fog-layer-2 {
  background: linear-gradient(90deg,
    transparent 10%, rgba(180,190,200,0.08) 40%,
    rgba(180,190,200,0.15) 60%, transparent 90%);
  animation: fog-drift-2 35s ease-in-out infinite alternate-reverse;
}
.fog-layer-3 {
  background: radial-gradient(ellipse at 30% 50%,
    rgba(200,210,220,0.1) 0%, transparent 60%);
  animation: fog-drift-3 20s ease-in-out infinite alternate;
}
@keyframes fog-drift-1 {
  0% { transform: translateX(-5%) scaleX(1.1); opacity: 0.6; }
  100% { transform: translateX(5%) scaleX(0.9); opacity: 1; }
}
@keyframes fog-drift-2 {
  0% { transform: translateX(8%) translateY(-2%); }
  100% { transform: translateX(-8%) translateY(2%); }
}
@keyframes fog-drift-3 {
  0% { transform: translateX(-10%); opacity: 0.4; }
  100% { transform: translateX(10%); opacity: 0.8; }
}
```
**Scroll-linked variant:** Fog opacity/density increases as user scrolls deeper:
```jsx
const fogOpacity = useTransform(scrollYProgress, [0, 0.5, 1], [0.3, 0.8, 0.2]);
```
**Use for:** Forest, horror, mystery, atmospheric luxury, cathedral interiors.

### Day-to-Night Scroll Transition
CSS custom properties that shift hue/lightness based on scroll position, creating time-of-day changes.
```jsx
const { scrollYProgress } = useScroll();
const hue = useTransform(scrollYProgress, [0, 0.3, 0.7, 1], [35, 140, 220, 240]);
const lightness = useTransform(scrollYProgress, [0, 0.3, 0.7, 1], [12, 10, 6, 4]);
const accentHue = useTransform(scrollYProgress, [0, 0.3, 0.7, 1], [35, 120, 200, 210]);

// Apply to root or section container
<motion.div style={{
  '--env-hue': hue,
  '--env-lightness': useMotionTemplate`${lightness}%`,
  '--env-accent-hue': accentHue,
  backgroundColor: useMotionTemplate`hsl(${hue}, 25%, ${lightness}%)`,
}}>
```
Sections automatically shift from warm dawn → green day → blue dusk → dark night as user scrolls.
**Use for:** Journey/storytelling sites, forest themes, timeline pages, day-in-the-life narratives.

### Canopy / Tunnel Entrance (Scroll-Zoom-Through)
Hero starts deep inside a texture (leaves, clouds, abstract), zooming out to reveal content.
```jsx
const { scrollYProgress } = useScroll({ target: heroRef });
const scale = useTransform(scrollYProgress, [0, 0.6], [5, 1]);
const textureOpacity = useTransform(scrollYProgress, [0, 0.4, 0.7], [1, 0.6, 0]);
const contentOpacity = useTransform(scrollYProgress, [0.5, 0.8], [0, 1]);
const blur = useTransform(scrollYProgress, [0, 0.3, 0.7], [0, 3, 0]);

<section ref={heroRef} className="min-h-[250vh] relative">
  {/* Texture layer that zooms out */}
  <motion.div
    style={{ scale, opacity: textureOpacity, filter: useMotionTemplate`blur(${blur}px)` }}
    className="sticky top-0 h-screen w-full"
  >
    <img src="/canopy-texture.jpg" className="w-full h-full object-cover" />
  </motion.div>
  {/* Content reveals as texture clears */}
  <motion.div style={{ opacity: contentOpacity }} className="sticky top-0 h-screen flex items-center justify-center z-10">
    {/* Your content */}
  </motion.div>
</section>
```
**Deps:** `motion`. Texture can be: leaf canopy, cloud tunnel, abstract fractal, smoke, water surface.

### Parallax Foliage Layers (Content Occlusion)
Tree branches/leaves positioned in front of content at different scroll speeds.
```jsx
// 5-layer system: far bg → mid bg → content → near fg → closest fg
const layer1Y = useTransform(scrollY, [0, 2000], [0, -60]);   // far trees
const layer2Y = useTransform(scrollY, [0, 2000], [0, -120]);  // mid branches
const layer4Y = useTransform(scrollY, [0, 2000], [0, -250]);  // near leaves
const layer5Y = useTransform(scrollY, [0, 2000], [0, -400]);  // closest branch

// Foreground layers sit ABOVE content (z-30, z-40)
<motion.img src="/branch-left.png" style={{ y: layer4Y }}
  className="absolute top-[20%] left-0 w-[300px] z-30 pointer-events-none opacity-80" />
<motion.img src="/vine-right.png" style={{ y: layer5Y }}
  className="absolute top-[40%] right-0 w-[200px] z-40 pointer-events-none" />

// Content sits at z-10
// Gradient masks on foreground elements so they fade at edges:
// mask-image: linear-gradient(to right, black 50%, transparent 100%);
```
**Effect:** Content peeks through gaps in foliage. Scrolling shifts the layers at different rates. Some content is partially hidden behind branches — creates discovery.

### Light Shafts
Diagonal beams of light simulating sunlight through gaps (canopy, windows, clouds).
```css
.light-shaft {
  position: absolute;
  width: 200px;
  height: 150%;
  background: linear-gradient(
    180deg,
    rgba(255, 230, 150, 0.08) 0%,
    rgba(255, 230, 150, 0.02) 60%,
    transparent 100%
  );
  transform: rotate(-25deg);
  transform-origin: top center;
  filter: blur(30px);
  pointer-events: none;
  animation: shaft-sway 15s ease-in-out infinite alternate;
}
.light-shaft:nth-child(2) {
  left: 40%;
  width: 150px;
  animation-delay: -5s;
  opacity: 0.6;
  transform: rotate(-20deg);
}
@keyframes shaft-sway {
  0% { transform: rotate(-25deg) translateX(-20px); opacity: 0.6; }
  100% { transform: rotate(-22deg) translateX(20px); opacity: 1; }
}
```
**Use for:** Forest, cathedral, spiritual, atmospheric dark sections. Shift position with scroll for parallax effect.

### Organic Dividers (Root/Vine Borders)
SVG paths as section dividers instead of straight lines.
```jsx
// Between sections — replaces <hr> or border-t
<svg viewBox="0 0 1200 80" className="w-full h-[80px] -mt-1" preserveAspectRatio="none">
  <path
    d="M0,40 C100,10 200,60 350,35 C500,10 600,55 750,30 C900,5 1050,50 1200,40"
    fill="none"
    stroke="rgba(120,100,80,0.2)"
    strokeWidth="2"
    className="animate-root-grow"
  />
  {/* Secondary thinner root */}
  <path
    d="M200,45 C300,25 400,55 550,30 C700,15 850,45 1000,35"
    fill="none"
    stroke="rgba(120,100,80,0.1)"
    strokeWidth="1"
  />
</svg>
// animate-root-grow: stroke-dasharray/dashoffset animation on scroll
```
**Use for:** Forest/nature themes, organic brands. Replace ANY straight-line section divider.

### Fire Border Animation
Replaces static CSS borders with animated flame effect using conic-gradient + hue flicker.
```css
.fire-border {
  position: relative;
  z-index: 0;
}
.fire-border::before {
  content: '';
  position: absolute;
  inset: -3px;
  border-radius: inherit;
  background: conic-gradient(
    from var(--fire-angle, 0deg),
    hsl(0, 100%, 50%),
    hsl(30, 100%, 55%),
    hsl(45, 100%, 60%),
    hsl(55, 100%, 70%),
    hsl(45, 100%, 60%),
    hsl(30, 100%, 55%),
    hsl(0, 100%, 50%)
  );
  z-index: -1;
  animation: fire-rotate 3s linear infinite, fire-flicker 0.15s ease-in-out infinite alternate;
  filter: blur(4px);
}
.fire-border::after {
  content: '';
  position: absolute;
  inset: 1px;
  border-radius: inherit;
  background: var(--background);
  z-index: -1;
}
@property --fire-angle {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}
@keyframes fire-rotate {
  to { --fire-angle: 360deg; }
}
@keyframes fire-flicker {
  0% { filter: blur(3px) brightness(0.9); }
  100% { filter: blur(5px) brightness(1.1); }
}
```
**Intensity dial:** Adjust `inset` (-3px subtle, -8px blazing), blur (3-8px), flicker speed (0.15-0.3s).
**Use for:** Replace ANY boring border. Cards, containers, section dividers, buttons, images.

### Ember & Ash Particles
Rising ember particles using pure CSS (no JS library needed).
```css
.ember-field {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
}
.ember {
  position: absolute;
  bottom: -10px;
  width: var(--size, 4px);
  height: var(--size, 4px);
  background: radial-gradient(circle,
    hsl(40, 100%, 70%) 0%,
    hsl(25, 100%, 55%) 40%,
    hsl(10, 100%, 40%) 70%,
    transparent 100%);
  border-radius: 50%;
  animation:
    ember-rise var(--duration, 8s) ease-out infinite,
    ember-sway var(--sway, 3s) ease-in-out infinite alternate,
    ember-fade var(--duration, 8s) ease-out infinite;
  animation-delay: var(--delay, 0s);
}
@keyframes ember-rise {
  0% { transform: translateY(0) scale(1); }
  100% { transform: translateY(-100vh) scale(0.3); }
}
@keyframes ember-sway {
  0% { margin-left: -20px; }
  100% { margin-left: 20px; }
}
@keyframes ember-fade {
  0% { opacity: 1; }
  60% { opacity: 0.8; }
  100% { opacity: 0; }
}
/* Spawn 15-25 embers with varied --size (2-6px), --duration (6-12s), --delay (0-8s), left positions */
```
**Ash variant:** Same structure but: gray colors (`hsl(0,0%,60%)` → `hsl(0,0%,30%)`), larger size (3-8px), slower rise (12-18s), slight tumble rotation added.

### Smoke Rising Effect
Large blurred gradient elements that rise and spread.
```css
.smoke-column {
  position: absolute;
  bottom: 0;
  width: 300px;
  height: 600px;
  background: radial-gradient(ellipse at 50% 100%,
    rgba(200,200,200,0.08) 0%,
    rgba(180,180,180,0.04) 40%,
    transparent 70%);
  filter: blur(40px);
  animation: smoke-rise 15s ease-out infinite;
  transform-origin: bottom center;
}
@keyframes smoke-rise {
  0% {
    transform: translateY(0) scaleX(1);
    opacity: 0.6;
  }
  50% {
    transform: translateY(-40%) scaleX(1.8);
    opacity: 0.3;
  }
  100% {
    transform: translateY(-80%) scaleX(3);
    opacity: 0;
  }
}
```
**Use for:** Behind text in fire sections, rising from fire-bordered elements. 2-3 columns at different positions/timings.

### Heat Distortion
Subtle ripple effect above fire sources simulating hot air.
```css
.heat-distortion {
  position: absolute;
  bottom: 100%; /* sits above the fire source */
  left: -10%;
  width: 120%;
  height: 200px;
  backdrop-filter: blur(0.5px);
  animation: heat-ripple 2s ease-in-out infinite;
  pointer-events: none;
}
@keyframes heat-ripple {
  0%, 100% { transform: scaleY(1) translateY(0); }
  25% { transform: scaleY(1.02) translateY(-1px); }
  75% { transform: scaleY(0.98) translateY(1px); }
}
```
**Use for:** Above fire borders, above ember sources. Very subtle — 0.5-1px blur only.

### Charred / Burnt Edge Mask
Content containers with irregular burnt-paper edges.
```css
.charred-edge {
  -webkit-mask-image: url('/masks/burnt-edge.svg');
  mask-image: url('/masks/burnt-edge.svg');
  -webkit-mask-size: cover;
  mask-size: cover;
}
/* CSS-only fallback with clip-path: */
.charred-edge-poly {
  clip-path: polygon(
    2% 0%, 8% 1%, 15% 0%, 22% 2%, 30% 0%, 38% 1%,
    45% 0%, 52% 2%, 60% 0%, 68% 1%, 75% 0%, 82% 2%,
    90% 0%, 95% 1%, 100% 3%, 100% 97%, 98% 100%,
    92% 98%, 85% 100%, 78% 98%, 70% 100%, 62% 98%,
    55% 100%, 48% 98%, 40% 100%, 32% 98%, 25% 100%,
    18% 98%, 10% 100%, 5% 98%, 0% 97%
  );
}
/* Orange glow at charred edges: */
.charred-edge::before {
  content: '';
  position: absolute;
  inset: -2px;
  background: radial-gradient(ellipse at var(--glow-x, 50%) var(--glow-y, 50%),
    rgba(255, 100, 0, 0.15) 0%, transparent 50%);
  filter: blur(8px);
  z-index: -1;
}
```
**Use for:** Cards, images, section boundaries in fire/destructive themes. Combine with fire-border for double effect.

### Crack Glow
Hairline fractures in dark surfaces with ember light bleeding through.
```css
.crack-glow {
  position: relative;
}
.crack-glow::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url('/textures/cracks.svg');
  background-size: cover;
  opacity: 0;
  animation: crack-reveal 0.8s ease-out forwards;
  /* SVG has thin white paths on transparent bg */
  filter: drop-shadow(0 0 4px rgba(255,100,0,0.8)) drop-shadow(0 0 12px rgba(255,50,0,0.4));
}
@keyframes crack-reveal {
  to { opacity: 1; }
}
/* CSS-only: use repeating-linear-gradient at various angles with very thin (1px) lines */
.crack-glow-css::before {
  background:
    linear-gradient(73deg, transparent 49.5%, rgba(255,120,0,0.3) 49.5%, rgba(255,120,0,0.3) 50.5%, transparent 50.5%),
    linear-gradient(127deg, transparent 49.7%, rgba(255,80,0,0.2) 49.7%, rgba(255,80,0,0.2) 50.3%, transparent 50.3%);
  filter: blur(0.5px);
  mix-blend-mode: screen;
}
```
**Use for:** Dark backgrounds, section transitions (cracks spread as user scrolls), interactive (cracks radiate from cursor). Combine with ember particles leaking through cracks.

### Falling Leaves (Nature Particle)
CSS-only realistic leaf fall — NOT small circles bobbing.
```css
.leaf {
  position: absolute;
  top: -40px;
  width: var(--leaf-w, 20px);
  height: var(--leaf-h, 30px);
  background: var(--leaf-color, hsl(100, 30%, 35%));
  clip-path: ellipse(50% 50% at 50% 50%);
  opacity: var(--leaf-opacity, 0.6);
  animation:
    leaf-fall var(--fall-duration, 12s) linear infinite,
    leaf-sway var(--sway-duration, 4s) ease-in-out infinite alternate,
    leaf-tumble var(--tumble-duration, 6s) linear infinite;
  animation-delay: var(--delay, 0s);
}
@keyframes leaf-fall {
  0% { top: -40px; }
  100% { top: calc(100vh + 40px); }
}
@keyframes leaf-sway {
  0% { transform: translateX(-30px) rotate(0deg); }
  100% { transform: translateX(30px) rotate(15deg); }
}
@keyframes leaf-tumble {
  0% { transform: rotateX(0deg) rotateZ(0deg); }
  100% { transform: rotateX(360deg) rotateZ(360deg); }
}
/* 4-8 leaves with varied: --leaf-w (15-35px), --leaf-h (20-45px),
   --leaf-color (greens, browns, amber for autumn),
   left positions, --fall-duration (8-18s), --delay (0-10s) */
```
**Key difference from bad floating decorations:** Leaves have realistic fall physics (tumble + sway + gravity), varied shapes, and serve atmospheric purpose. NOT small dots bobbing in place.

---

## Common Dependencies

| Package | Purpose |
|---------|---------|
| `hls.js` | HLS video streaming |
| `motion` | Framer Motion animations (scroll-linked, stagger, layout) |
| `lucide-react` | Icon library |
| `tailwindcss-animate` | Tailwind animation utilities |
| `clsx` / `tailwind-merge` | Class merging utilities |
| `embla-carousel-react` | Carousels/sliders |
