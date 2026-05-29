# AGENTS.md · Operating contract for AI agents working on `jamesalg/alg-website`

**Audience:** Any AI coding agent (Manus, Claude Code, Codex, future agents) doing work in this repository. Read this file **first**, on **every task**, before touching code. The instructions in the user's current task always take precedence over this file when they conflict, but everything not explicitly overridden by the current task is binding.

**Last updated:** 2026-05-29

---

## 1. Purpose

This file exists to stop a recurring failure mode: agents reinterpret design specs into the repo's component system, that reinterpretation introduces drift, and the live site diverges from the source-of-truth mockups. After enough iterations, what shipped no longer matches what was designed, and everyone is patching backward.

This file removes the reinterpretation step. Mockups are byte-canonical. Class names, CSS values, and markup structure in the source mockups are the spec. Your job is to host them in this repo, not to redesign them.

---

## 2. The Fidelity Contract (read this section twice)

When the user's task references a mockup file, datasheet HTML, or any pre-built fragment as the source:

**You MUST:**

- Copy the markup byte-for-byte from the source into the target component.
- Preserve every class name, every CSS value, every `data-*` attribute, every `aria-*` attribute, every comment.
- When the source uses `class="sec-eyebrow"`, the deployed page uses `class="sec-eyebrow"`. Not `class="eyebrow"`, not `class="SectionEyebrow"`, not `class="solutions-eyebrow"`.
- Preserve inline `<style>` blocks. If the mockup declares a scoped CSS class with specific values, deploy those values exactly. Do not "consolidate," "improve," or "normalize" them into existing design-system classes unless the user's task instructs you to.
- When changing an asset path (e.g., `assets/core/X.webp` → `/assets/homepage/core/X.webp`), change ONLY the path. Do not also change the `<img>` element's class, alt text, or surrounding markup.
- When the source HTML carries CSS for `:hover`, `::before`, `@media` queries, or animations — port them verbatim.

**You MUST NOT:**

- Rename classes for "consistency."
- Swap one canonical class for another based on what you think the design system uses.
- Reformat the markup or "clean up" indentation in ways that change rendered output.
- Move CSS from inline `<style>` blocks into separate component scope unless the user's task asks you to.
- Substitute icon libraries, font stacks, or color tokens.
- Re-author copy. Every visible string in the source is the published string.

**If a mockup file appears to use a class that doesn't exist in the global stylesheet** — that is a feature, not a bug. The mockup ships with its own scoped CSS in its `<style>` block. Deploy that CSS too.

**If you genuinely believe the mockup contains an error** — do not silently fix it. Report it back in your "done" message and ask. Do not let your judgment override the source.

---

## 3. Canonical Class Registry

The site has a small, intentional set of canonical classes. Reuse them. Do not invent new classes when these exist and apply.

### Section structure (every Solutions / Collections / homepage section uses these)

| Class | Element | Purpose | What it inherits |
|---|---|---|---|
| `sec-eyebrow` | `<div>` | Section eyebrow — the red mono small-caps label | JetBrains Mono 11px, font-weight 700, letter-spacing 2.2px, color #F32740, with a 84px red `::before` dash bar |
| `sec-title` | `<h2>` (or `<h3>` for sub-sections) | Section title — the big black headline | **Lato sans-serif** (NOT Cormorant Garamond), font-size clamp ~48px on desktop, font-weight 700, color #111 on light backgrounds |
| `section-inner` | `<div>` wrapper | Constrains content column to 1440px max-width, auto-centered, responsive horizontal padding | Standard column constraint |
| `mono` | inline class | Monospace label override | JetBrains Mono — applied to inline labels that are NOT eyebrows |

### Homepage CORE section

| Class | Purpose |
|---|---|
| `core-section` | Outer section · `background: #ffffff` · padding `96px 0 32px` |
| `core-grid` | The 4-panel CORE grid · `grid-template-columns: repeat(4, 1fr)` · `max-width: none` (full-bleed) |
| `core-panel`, `core-panel--c`, `core-panel--o`, `core-panel--r`, `core-panel--e` | Individual pillar panels with per-pillar letter color tints |
| `core-letter` | The big see-through letter glyph · `mix-blend-mode: screen` · per-pillar color/opacity |
| `core-tile-deck` | Per-tile descriptor line · Lato 13px, white-80, max-width 30ch |
| `core-sub-deck` | The mono cert/program bullets line under the deck · JetBrains Mono 13px |

### Homepage OEM strip

| Class | Purpose |
|---|---|
| `oem-strip` (with `id="oem"`) | Outer section · `background: #0a0a0d` (dark) · padding 96px |
| `oem-grid` | 3-panel grid · `grid-template-columns: repeat(3, 1fr)` |
| `oem-panel`, `oem-media`, `oem-panel-content`, `oem-panel-title`, `oem-panel-num` | OEM panel structure |

### Locator section (FIND YOUR LOCAL SUPPORT)

| Class | Purpose |
|---|---|
| `locator-section` | Outer section |
| `map-grid` | `display: grid` · `grid-template-columns: 1fr 360px` · **`grid-template-rows: 600px`** (pinned — see §6 for why) |
| `iv-row`, `iv-row--{type}` | IN THIS VIEW list row · type ∈ {warehouse, rep, distributor} for color-dot variant |
| `iv-dot`, `iv-chip`, `iv-distance`, `iv-name`, `iv-line2` | List-row internals |
| `iv-sort-btn`, `iv-sort-row` | Sort toggle pill buttons |

### Anti-patterns (DO NOT use these — they're legacy or wrong)

- `core-eyebrow`, `core-title` — replaced by `sec-eyebrow` / `sec-title` (these caused a Cormorant Garamond regression)
- `oem-h1` — replaced by `sec-title`
- Any inline `font-family: Cormorant Garamond` or `font-family: serif` — forbidden by CFG-TYPE-1
- Custom `solutions-eyebrow`, `vertical-h2`, `hero-eyebrow` — use `sec-eyebrow` / `sec-title`

---

## 4. Voice & Copy Rules

### Voice (CFG-VOICE-1, CFG-VOICE-2)

- **Declarative, spec-writer voice.** "We return a zone-by-zone takeoff within 48 hours" — yes. "Get a stunning, world-class lighting layout that transforms your space" — no.
- **Plain English for non-technical audience; spec-grade for technical.** Trust readers to know basic terms.
- **Functional CTA verbs.** "View family", "Browse Retail", "Download Spec Pack." Not "Discover", "Unleash", "Transform."

### Copy (CFG-COPY-4, CFG-COPY-5, CFG-COPY-6)

- **No competitor brand names** in PDP / page copy. (Lutron / Leviton / RAB are out. DLC / UL / ETL / Title 24 are standards, not brands — those are fine.)
- **No vendor / supplier MPN numbers** in customer-facing copy. (BillDa / Bodine / BLD-* / Starlake / Mester / Cole etc.) Including comments in HTML / JS — View Source leaks count.
- **No OEM partner / contract manufacturer names.** "OEM" as a capability ALG offers is fine; specific factory names are not.

### Softened claims (CFG-VOICE-1 absolute-claim ban)

- **"No driver to fail"** → "designed to reduce failure points"
- **"No lamp replacements for over a decade"** → "long-life LED performance reduces relamping cycles"
- **"Eliminates flicker that causes headaches"** → "flicker-conscious performance"
- **"DLC Premium listed"** → "DLC-listed (where applicable)" — unless the specific SKU IS DLC Premium and you have proof
- **"BAA/TAA"** → "TAA/BAA" (consistent ordering)

### Forbidden phrases

- "customer journey" (retail marketing — replace with "sales floor experience" or similar)
- "ESSER-fundable" (too narrow / dated)
- "extended finance terms" (commitment risk)
- "stretched thin" (folksy — replace with "managing tight budgets" or similar)

---

## 5. Type & Layout Rules

### CFG-TYPE-1 · Lato is pinned on headings

Staging's global stylesheet pins `h1, h2, h3` to Lato. If a new component overrides this — explicitly or by inheriting from a third-party CSS — the headings will fall through to Cormorant Garamond serif. This is a regression. **Never declare `font-family` on headings without pinning Lato.**

Verify after any new section deploys: every `<h2>` should compute to `font-family: Lato, system-ui, sans-serif` in the browser inspector. If it shows Cormorant or Playfair, that's a bug.

### CFG-CANONICAL-1 · Reuse canonical classes

Before inventing any new CSS class for a Solutions / Collections / homepage section, check §3 of this file for an existing canonical class. The existing class likely already carries the right font-family, color, and spacing — using it avoids the Lato override problem entirely.

### CFG-MOBILE-1 v1.1 · Build-time responsive

Every new component ships with responsive breakpoints from the start:

```css
@media (max-width: 1024px) { /* tablet */ }
@media (max-width: 768px)  { /* small tablet */ }
@media (max-width: 480px)  { /* phone */ }
```

Touch targets ≥ 44px tall. Single-column layout at ≤ 480px. Container queries are fine.

### CFG-MAP-1 · Pin Leaflet grid row height

When a Leaflet map sits next to a sibling panel in a grid, **always set `grid-template-rows: 600px`** (or whatever the design calls for). Otherwise both columns track the taller sibling's content height, and dragging the map visibly resizes the section. Call `map.invalidateSize()` in `setTimeout(0)` after init. Apply scrollable overflow to the right-rail panel if its content might exceed the row height.

---

## 6. Data Rendering Rules

### CFG-DATA-1 · Normalize CRM data on display

When data comes from Zoho CRM, Zoho Books, or any external system into a customer-facing surface, **normalize at render time**:

- **Title Case names + state-code preservation.** Don't display raw CRM all-caps strings like `BOWLING GREEN WINLECTRIC CO`. Use a helper that title-cases ≥ 70%-uppercase strings while preserving 2-letter state codes.
- **Tabular numerics.** Apply `font-variant-numeric: tabular-nums` to every numeric column for column alignment.
- **`tel:` link formatting.** Strip non-digits for the href.
- **URL cleanup.** Add `https://` if missing; force `target="_blank" rel="noopener"`.
- **Hidden-when-null.** Never render `· null`, `Phone: (empty)`, or empty `<a></a>` for missing fields.

### CFG-LIST-1 · Data-list polish defaults (ship these on first pass)

Any list of CRM/external-data items ships with all of these from day one, not iterated:

1. Fixed-width numeric column (e.g., distance, count) right-aligned with `min-width`.
2. Tabular nums on numbers.
3. Title Case display names + state-code preservation.
4. Color-coded type chip with dot.
5. 1px row divider (`rgba(255,255,255,0.10)` on dark; `rgba(0,0,0,0.08)` on light).
6. 2-line max format: line 1 = name + numeric · line 2 = city + type.
7. Hover background tint (`rgba(255,255,255,0.035)` or equivalent).
8. Empty-state copy when filtered to zero results.

If sort matters and count > 4 items: include sort pill buttons (default Nearest, plus A–Z and Type).

---

## 7. Verification Gate Template (CFG-COWORK-12 v2 + CFG-COWORK-13 + CFG-MANUS-1)

Every "done" report you generate **must include all six** of these, or the work is not considered complete:

1. **Merge commit SHA.** Not a preview branch — the SHA on `main` after merge.
2. **Build-hash badge on the deployed page rolled to that SHA.** The footer of every staging page shows `build {sha}`. Confirm it matches your merge SHA. If it hasn't rolled yet, the deploy isn't done.
3. **Curl-grep verification gate output.** For every spec in the user's task, run a `curl -s {url} | grep -c "{string}"` check. Required strings should return 1+; forbidden / old strings should return 0.
4. **Title + h1 verification.** Cloudflare Pages soft-falls 404s to the homepage stub. A `200 OK` does NOT mean the right content is there. Always grep the deployed page's `<title>` and `<h1>` against expected values per CFG-COWORK-12 v2.
5. **CTA click verification.** Per CFG-COWORK-13: a CTA href can return 200 OK and still be broken (configurator state dropped, wrong query string, missing fragment). Click every new CTA in a real browser and confirm the resulting UX matches intent. URL HEAD is the floor, not the ceiling.
6. **Preview URL.** Cloudflare Pages generates a preview URL on every PR. Include it in your report so PM can audit visually before merge.

### CFG-MANUS-1 · Every spec is REQUIRED, not optional

Treat every numbered patch in a user's task as binary. There is no "suggested" or "optional" or "nice to have." If a spec has unclear scope, stop and ask the user before partial-implementing. Half-shipping a polish pass is worse than not shipping it — the next prompt has to spell out what's missing on top of what's wrong.

---

## 8. "Done" Definition

- "Built and tested locally" = **not done**.
- "Deployed to preview URL" = **not done**.
- "Merged to main, build-hash badge rolled, verification gate passes" = **done**.
- "Reported back to PM with the §7 six-item checklist" = **fully done**.

Do not claim done at any earlier stage.

---

## 9. Anti-patterns (DO NOT)

| ❌ Anti-pattern | ✅ Correct |
|---|---|
| Rename mockup classes to match the design system | Use mockup classes verbatim; if they don't exist in the design system, port the mockup's inline CSS too |
| Substitute `<h2 class="oem-h1">` → `<h2 class="display-large">` because "display-large" is what your design system calls it | Keep `<h2 class="sec-title">` from the mockup; do not substitute |
| Move inline `<style>` into a separate `.module.css` file | Keep inline; the mockup IS the spec |
| Add `font-family: serif` to override what looks like a missing font declaration | Trust the global Lato pin; do not declare font-family on h2 in component scope |
| Mark a task done after the preview URL renders correctly | Wait for merge + build-hash badge roll, then mark done |
| Report "24/24 routes 200 OK" as proof of correctness | Also report the title + h1 grep results per CFG-COWORK-12 |
| Ship a list / row UI without colored dots, dividers, Title Case, tabular nums | Ship all CFG-LIST-1 defaults from the first pass |
| Use raw CRM strings (`BOWLING GREEN, KY`) in customer-facing displays | Normalize at render time per CFG-DATA-1 |
| Invent a `solutions-eyebrow` class for a new Solutions section | Use the canonical `sec-eyebrow` |

---

## 10. When in doubt

- **Check this file first.** Most "should I do X?" questions are answered above.
- **If not above, ask the user.** Do not improvise.
- **If the user's instruction conflicts with this file, the user wins for that task.** But report the conflict in your "done" message so this file can be updated.

This file is the operating contract. It should be updated as we learn — but it should not be silently bypassed.
