<!-- SUMMARY: 4 named narrative arc templates (Emergence/Awakening/Descent/Revelation) with useTransform chains, scroll ranges, and audio atmosphere cues. Load ONLY in Phase 4. -->

# Animation Storytelling

A page scroll is a narrative arc. The user is the audience. Each section is a scene. Animation should tell a story — not decorate elements.

## Core Concept: The Scroll Journey

Every page has a **narrative state** — where the user is emotionally and informationally in the story. Animation must reflect and advance that state. Per-element fade-ins are not storytelling. A scroll journey is.

> Instead of: "hero fades in, features slide up, CTA fades in"
> Think: "world awakens → product emerges from darkness → user is invited into the light"

---

## Narrative Arc Templates

### 1. Emergence — *Void → Light → Reveal*
**Story:** The world begins in darkness. A signal appears. The product emerges from nothingness.

**Scroll progression:**
- `0%–15%` — Pure black. A single point of light appears at center (radial gradient, 1px → 200px). Sound: deep silence broken by a single low tone.
- `15%–35%` — Light expands into a warm glow. Background color shifts from `hsl(0,0%,2%)` to `hsl(220,15%,8%)`. First word of headline bleeds in through light.
- `35%–60%` — Full headline revealed character by character through the brightening. Environment fills with ambient color.
- `60%–80%` — Supporting content materializes as the world becomes solid. Fog/grain clears progressively.
- `80%–100%` — Environment is fully lit. Call to action pulses with the same warm light that started the journey.

**CSS chain (scroll 0→1):**
```jsx
const bgLightness = useTransform(scrollYProgress, [0, 0.15, 0.4, 1], [2, 4, 8, 10]);
const glowRadius = useTransform(scrollYProgress, [0, 0.15, 0.35], [0, 80, 400]);
const heroOpacity = useTransform(scrollYProgress, [0.1, 0.4], [0, 1]);
const heroBlur = useTransform(scrollYProgress, [0.1, 0.45], [20, 0]);
// Background radial glow expands as headline reveals
```

**Audio atmosphere:** Low drone → harmonic tone → ambient melody entrance (use Web Audio API oscillator or `<audio>` autoplay at scroll threshold 0.15)

---

### 2. Awakening — *Still → Alive → Energy*
**Story:** A product asleep. You arrive. It wakes up for you.

**Scroll progression:**
- `0%–10%` — Frozen scene. All elements static, monochromatic, slightly blurred. Like a photograph.
- `10%–30%` — Color bleeds in from top-left. Elements desaturate → resaturate. A subtle pulse begins (scale 1.0 → 1.002 → 1.0, 3s loop).
- `30%–55%` — Motion multiplies. Text begins animating. UI elements light up sequentially like switches being thrown.
- `55%–75%` — Full kinetic state. Everything in motion, vibrant. The product is alive.
- `75%–100%` — Energy settles into confident stillness. The product is awake and ready.

**CSS chain (scroll 0→1):**
```jsx
const saturation = useTransform(scrollYProgress, [0, 0.1, 0.35, 0.6], [0, 0, 100, 100]);
const globalFilter = useMotionTemplate`saturate(${saturation}%) blur(0px)`;
const pulseScale = useTransform(scrollYProgress, [0.1, 0.3], [1, 1.002]);
// Apply saturation filter to entire page wrapper, not individual elements
```

**Audio atmosphere:** Silence → soft breath/heartbeat sound at 10% → layered ambient beat at 35% → full atmospheric score at 55%

---

### 3. Descent — *Surface → Depth → Core*
**Story:** You dive beneath the surface. The deeper you go, the more you understand.

**Scroll progression:**
- `0%–20%` — Bright surface. Light blue/white. Content is simple, approachable. Background: sky.
- `20%–45%` — Color darkens as if diving into water. Blue deepens `hsl(210,60%,80%)` → `hsl(220,60%,20%)`. Grain increases. Pressure builds.
- `45%–70%` — Deep zone. Near-black environment. Only the essential glows. Complex features revealed here — the "core truth" of the product.
- `70%–90%` — Return to surface with new understanding. Color brightens again but warmer than start — changed by the journey.
- `90%–100%` — Surfaced. CTA presented as the conclusion of the dive.

**CSS chain:**
```jsx
const bgHue = useTransform(scrollYProgress, [0, 0.2, 0.5, 0.75, 1], [210, 215, 220, 220, 30]);
const bgLightness = useTransform(scrollYProgress, [0, 0.2, 0.5, 0.75, 1], [80, 50, 8, 8, 15]);
const grainOpacity = useTransform(scrollYProgress, [0, 0.3, 0.55, 0.8], [0.02, 0.04, 0.08, 0.03]);
```

**Audio atmosphere:** Open air sound → underwater murmur at 25% → deep resonance at 50% → re-emergence breath at 75%

---

### 4. Revelation — *Obscured → Hinted → Unveiled*
**Story:** Something important is hidden. Each scroll gesture pulls back the curtain.

**Scroll progression:**
- `0%–25%` — Heavy blur/frost over everything. Shapes barely visible. Intrigue builds.
- `25%–50%` — Frost clears from center outward. Text emerges character by character. Vignette pulls back.
- `50%–75%` — Sharp clarity. Color temperature shifts from cold to warm (product revealed = warmth).
- `75%–100%` — Aftermath of revelation: environment is fully visible, user has seen everything, CTAs emerge.

**CSS chain:**
```jsx
const globalBlur = useTransform(scrollYProgress, [0, 0.25, 0.5], [20, 8, 0]);
const vignetteOpacity = useTransform(scrollYProgress, [0, 0.3, 0.6], [0.9, 0.5, 0]);
const colorTemp = useTransform(scrollYProgress, [0.3, 0.7], [0, 1]); // 0=cold, 1=warm
const warmFilter = useMotionTemplate`blur(0px) sepia(${useTransform(colorTemp, [0,1], [0,20])}%)`;
```

---

## Chained Multi-Property Scroll Sequences

Unlike simple fade-in, narrative sequences chain 4–6 properties across defined scroll ranges.

### Full-Page Entrance Chain
```jsx
// Properties that chain across scroll progress 0→1
const scale     = useTransform(scrollYProgress, [0,    0.15, 0.4,  1   ], [1.2,  1.05, 1.0,  1.0 ]);
const blur      = useTransform(scrollYProgress, [0,    0.2,  0.45, 1   ], [15,   8,    0,    0   ]);
const opacity   = useTransform(scrollYProgress, [0,    0.1,  0.4,  1   ], [0,    0.4,  1,    1   ]);
const y         = useTransform(scrollYProgress, [0,    0.3,  0.6,  1   ], [40,   20,   0,    0   ]);
const saturation= useTransform(scrollYProgress, [0,    0.25, 0.5,  1   ], [0,    40,   100,  100 ]);
const brightness= useTransform(scrollYProgress, [0,    0.15, 0.4,  0.8 ], [60,   80,   100,  110 ]);

// Combine into single filter string
const filterChain = useMotionTemplate`blur(${blur}px) saturate(${saturation}%) brightness(${brightness}%)`;
```

### Section-Level Story Chain (per section scroll)
Each section has its own scroll progress from 0 (entering viewport) to 1 (leaving viewport):
```jsx
// Section enters: compressed → expands → normal
const sectionScale   = useTransform(sectionProgress, [0, 0.3, 0.6], [0.92, 1.02, 1.0]);
// Background: dark as section enters, lightens when centered, darkens as it leaves
const sectionBg      = useTransform(sectionProgress, [0, 0.4, 0.6, 1], [4, 10, 10, 4]);
// Text: dim → full → dim
const textOpacity    = useTransform(sectionProgress, [0, 0.25, 0.75, 1], [0.3, 1, 1, 0.3]);
// Depth: blurred → sharp → blurred
const sectionBlur    = useTransform(sectionProgress, [0, 0.3, 0.7, 1], [8, 0, 0, 8]);
```

---

## Sound Design & Audio Atmosphere

Audio cues tied to scroll position make animations feel cinematic, not decorative. Trigger via Web Audio API or `<audio>` elements at scroll thresholds.

### Implementation Pattern
```jsx
const { scrollYProgress } = useScroll();

useMotionValueEvent(scrollYProgress, "change", (latest) => {
  if (latest > 0.1 && latest < 0.12 && !audioTriggered.chapter1) {
    ambientAudio.play(); // Trigger once at 10% scroll
    audioTriggered.chapter1 = true;
  }
  // Volume follows scroll position
  if (ambientAudio) {
    ambientAudio.volume = Math.min(latest * 2, 0.6);
  }
});
```

### Audio by Narrative Arc

| Arc | 0% | 25% | 50% | 75% | 100% |
|-----|----|----|----|----|-----|
| **Emergence** | Silence | Single drone tone | Harmonic layer | Ambient melody | Resolution chord |
| **Awakening** | Silence | Soft breath | Heartbeat + texture | Full ambient beat | Fade to gentle pulse |
| **Descent** | Open air | Water murmur | Deep resonance | Echo chamber | Re-emergence breath |
| **Revelation** | White noise | Crystalline tone | Warmth tone | Full clarity | Confident chord |

### Suggested Audio Texture Keywords
When specifying audio in design prompts, use these descriptors:
- **Atmospheric drones:** low frequency hum, sub-bass presence, harmonic overtones
- **Spatial cues:** reverb tail, hall echo, intimate dry close-mic
- **Rhythm cues:** heartbeat pulse, breath cycle (4s inhale/4s exhale), tempo 60–80 BPM
- **Tonal warmth:** major key for revelation/emergence, minor for descent/mystery, modal for ambiguity

---

## Applying Narrative to Phase 4

When suggesting animation style in Phase 4, ask:

> "What is the emotional journey of this page? What does the user feel at the top vs. the bottom?"

Then select a narrative arc and apply it as the **page-level animation layer** — ABOVE individual section animations. Individual section animations (fade-in, slide-up) are micro-level. The narrative arc is macro-level. Both exist simultaneously.

**In the design prompt output, include:**
```
## Animation Narrative Arc
Arc: [Emergence / Awakening / Descent / Revelation / custom]
Scroll journey: [0%] state → [50%] state → [100%] state
Chained properties: scale + blur + opacity + saturation + brightness
Audio atmosphere: [description of sound at each chapter]
Implementation: useScroll + useTransform chain on page wrapper
```
