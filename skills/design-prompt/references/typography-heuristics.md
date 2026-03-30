<!-- SUMMARY: Enforced type constraints: single-family default, tracking-tight on headings, leading-[1.1–1.2], 6-size max scale, weight contrast over size variety. Load ONLY in Phase 3. -->

# Typography Heuristics

Professional typography rules enforced by every design prompt. These override defaults.

## Rule 1: Single Font Family (MANDATORY)

**Use ONE font family with different weights for hierarchy. Do NOT mix serif headings with sans-serif body.**

The default mode is single-family:
- `Inter 800` headings + `Inter 400` body
- `Space Grotesk 700` headings + `Space Grotesk 400` body
- `Outfit 700` headings + `Outfit 400` body

Dual-family (serif+sans) is a **deliberate stylistic choice** requiring explicit user intent — not the default auto-suggestion.

**Why:** Mixing Playfair Display headings with Inter body creates visual tension that usually looks unpolished. Single-family achieves hierarchy cleanly through weight contrast.

**Exception:** Only suggest serif+sans when the user explicitly requests editorial, literary, or classic aesthetic AND the combination is intentionally art-directed.

### Single-Family Weight Distribution

| Role | Weight | Tailwind Class |
|------|--------|---------------|
| Display / Hero heading | 800–900 | `font-black` / `font-extrabold` |
| Section heading (H2) | 700 | `font-bold` |
| Sub-heading (H3) | 600 | `font-semibold` |
| Body text | 400 | `font-normal` |
| Captions / muted | 300–400 | `font-light` / `font-normal` |

---

## Rule 2: Header Letter-Spacing — -2% to -3%

Headings must use tight letter-spacing. The target range is **-0.02em to -0.03em** (-2% to -3%).

| Tailwind Class | Value | Use |
|---------------|-------|-----|
| `tracking-tight` | `-0.025em` (~-2.5%) | Standard heading default ✅ |
| `tracking-tighter` | `-0.05em` (~-5%) | Only for very large display text |
| `[-0.02em]` | `-0.02em` | Minimum heading tracking |
| `[-0.03em]` | `-0.03em` | Maximum standard heading tracking |

**Never use `tracking-normal` or `tracking-wide` on headings.** Headings at small/medium scale look amateurish with default or loose tracking.

```css
/* Correct — heading letter-spacing */
.heading { letter-spacing: -0.025em; }  /* Tailwind: tracking-tight */

/* Wrong — too loose for headings */
.heading { letter-spacing: 0; }         /* Tailwind: tracking-normal */
```

---

## Rule 3: Header Line-Height — 110% to 120%

Headings must use condensed line-height. The target range is **1.1 to 1.2** (110% to 120%).

| Tailwind Class | Value | Use |
|---------------|-------|-----|
| `leading-none` | `1.0` (100%) | Display-only, single-line heroes |
| `leading-[1.1]` | `1.1` (110%) | Multi-line H1 default ✅ |
| `leading-[1.15]` | `1.15` (115%) | H2 sections ✅ |
| `leading-tight` | `1.25` (125%) | H3 and smaller headings |
| `leading-snug` | `1.375` | Body text with short lines |
| `leading-normal` | `1.5` | Body text default |

**Never use `leading-[0.9]` on multi-line headings** — sub-100% causes descenders to overlap ascenders. Use only on single-word/line display text.

```css
/* Correct — heading line-height */
h1 { line-height: 1.1; }   /* Tailwind: leading-[1.1] */
h2 { line-height: 1.15; }  /* Tailwind: leading-[1.15] */

/* Wrong — too tight for multi-line */
h1 { line-height: 0.9; }   /* Tailwind: leading-[0.9] — only safe for single-line display */

/* Wrong — too loose for headings */
h1 { line-height: 1.5; }   /* Tailwind: leading-normal — body text rhythm, not headings */
```

---

## Rule 4: Maximum 6 Font Sizes

**Web and landing pages must not exceed 6 distinct font sizes.** More than 6 creates visual chaos and broken rhythm.

### Recommended 6-Size Scale

| Role | Size | Tailwind Class |
|------|------|---------------|
| Display hero | 72–96px | `text-7xl` / `text-8xl` |
| Section heading (H2) | 40–48px | `text-4xl` / `text-5xl` |
| Sub-heading (H3) | 24–28px | `text-2xl` / `text-3xl` |
| Body / paragraphs | 16–18px | `text-base` / `text-lg` |
| Caption / metadata | 14px | `text-sm` |
| Label / eyebrow | 12px | `text-xs` |

**Enforcement:** Before finalizing a design prompt, count distinct font sizes. If > 6, consolidate by:
- Merging roles (e.g., use H3 size for both sub-headings and card titles)
- Using weight contrast instead of size contrast for same-level hierarchy
- Removing intermediate sizes added "just to be safe"

---

## Rule 5: Font Pairing Default Priority

When auto-suggesting font pairings, prioritize in this order:

1. **Single-family (preferred)** — same typeface, weight contrast only
2. **Same-style dual-family** — both sans-serif, compatible geometric/humanist styles
3. **Intentional serif+sans** — only when editorial contrast is the explicit design goal

### Quick Reference: Single-Family Pairings

| Family | Display/H1 | H2/H3 | Body | Vibe |
|--------|-----------|-------|------|------|
| Inter | 800 | 600–700 | 400 | Clean technical, SaaS |
| Space Grotesk | 700 | 600 | 400 | Techy, geometric |
| Outfit | 700 | 600 | 400 | Friendly consumer |
| Plus Jakarta Sans | 800 | 700 | 400 | Modern, bold |
| Sora | 700 | 600 | 400 | Balanced, professional |
| Bricolage Grotesque | 800 | 600 | 400 | Expressive, editorial |
| Manrope | 800 | 700 | 400 | Professional tech |
| DM Sans | 700 | 600 | 400 | Approachable, warm |

---

## Checklist (Run Before Finalizing Any Typography Section)

- [ ] Single font family used? (or dual-family explicitly justified by user request)
- [ ] Heading letter-spacing: `-0.02em` to `-0.03em` (`tracking-tight` minimum)
- [ ] Heading line-height: `1.1` to `1.2` (`leading-[1.1]` to `leading-[1.2]`)
- [ ] Total font sizes ≤ 6
- [ ] Weight hierarchy defined (e.g., 800/700/600/400/300 — not just bold/normal)
- [ ] No `tracking-normal` or `tracking-wide` on headings
- [ ] No `leading-normal` (1.5) on headings
