<!-- SUMMARY: Forbidden AI design signatures (badge above headline, decorative blobs, uniform grid cards) with mandatory replacement patterns. Load ONLY in Phase 6 pre-output scan. -->

# AI Design Anti-Patterns — Forbidden Code Signatures

Reference file for `SKILL.md`. If any of these patterns appear in a generated prompt, delete or replace them.

---

## 1. Badge/Tag Above Heading

```html
<!-- ANY of these above a heading = REJECT -->
<span class="... text-xs ... rounded-full ... uppercase tracking-widest ...">Label</span>
<div class="badge ...">Feature</div>
<p class="text-primary text-sm font-semibold ...">Why Choose Us</p>
```

**Replace with:** Integrate context into the heading itself, use oversized section numbers, side-aligned labels, or omit labels entirely.

---

## 2. Decorative Bob/Float Animation

```css
/* BOB ANIMATION — FORBIDDEN */
@keyframes bob { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
@keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-20px); } }
/* class="animate-bounce" on decorative divs — FORBIDDEN */
/* class="w-4 h-4 rounded-full bg-primary/20 absolute ... animate-" — FORBIDDEN */
```

**Replace with:** Background mesh gradients that shift, grain/noise texture overlays, scroll-linked parallax, or cursor-reactive elements.

---

## 3. Generic Grid Cards

```html
<!-- GRID-3 CARD PATTERN — FORBIDDEN -->
<div class="grid grid-cols-3 gap-6">
  <div class="rounded-lg border shadow-md p-6">...</div>
  <div class="rounded-lg border shadow-md p-6">...</div>
  <div class="rounded-lg border shadow-md p-6">...</div>
</div>
<!-- Uniform grid-cols-2/3/4 with identical card markup = FORBIDDEN -->
<!-- grid gap-N with every child having rounded-lg border p-6 = FORBIDDEN -->
```

**Replace with:** Stacked folders, cascade overlap, irregular clip-path shapes, gradient-bordered containers, masonry with varied sizes, or radial/orbital layouts.

---

## 4. Generic Hero Layout

```html
<!-- CENTERED STACK HERO — FORBIDDEN -->
<section class="flex flex-col items-center text-center">
  <span class="badge">Tag</span>
  <h1>Heading</h1>
  <p>Subtext</p>
  <button>CTA</button>
</section>
```

**Replace with:** Split asymmetric layout, full-screen headline, cinematic close-in, text wrapping around a visual element.

---

## 5. Generic Container Shape

Pattern: `rounded-lg shadow-md border p-6` as the only container shape in a design.

**Replace with:** Add `clip-path`, gradient border mask, cascade overlap, or organic curve edges.
