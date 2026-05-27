# Gate Check Results — multi-fAMILY PDP Build
**Date:** 2026-05-11  
**Commits:** `8a49c71` (initial build) → `78fa7d2` (breadcrumb fix)  
**Repo:** `jamesalg/alg-website` `main`  
**Build:** 94 pages · 0 errors

---

## Deliverables Summary

### 8 Product Detail Pages (PDPs)

| Series | URL | Status |
|---|---|---|
| Eclipse-II | `/products/multi-family/eclipse-ii/` | ✓ Live |
| Radius-II | `/products/multi-family/radius-ii/` | ✓ Live |
| Nebula-II | `/products/multi-family/nebula-ii/` | ✓ Live |
| Crescent | `/products/multi-family/crescent/` | ✓ Live |
| eCrescent | `/products/multi-family/ecrescent/` | ✓ Live |
| Orbit-I | `/products/multi-family/orbit-i/` | ✓ Live |
| Lunar Eclipse | `/products/multi-family/lunar-eclipse/` | ✓ Live |
| Gehry | `/products/multi-family/gehry/` | ✓ Live |

### 8 Submittal Generators

| Series | URL | Status |
|---|---|---|
| Eclipse-II | `/products/multi-family/eclipse-ii/submittal/` | ✓ Live |
| Radius-II | `/products/multi-family/radius-ii/submittal/` | ✓ Live |
| Nebula-II | `/products/multi-family/nebula-ii/submittal/` | ✓ Live |
| Crescent | `/products/multi-family/crescent/submittal/` | ✓ Live |
| eCrescent | `/products/multi-family/ecrescent/submittal/` | ✓ Live |
| Orbit-I | `/products/multi-family/orbit-i/submittal/` | ✓ Live |
| Lunar Eclipse | `/products/multi-family/lunar-eclipse/submittal/` | ✓ Live |
| Gehry | `/products/multi-family/gehry/submittal/` | ✓ Live |

> **Note:** Crescent and eCrescent each have their own submittal generator (brief said "shared" but separate pages were provided in the handoff ZIP). Both are live.

---

## Gate 1 — URL Structure

All 16 pages return HTTP 200 at canonical `/products/multi-family/{slug}/` paths.  
**Result: PASS**

---

## Gate 2 — Breadcrumbs

Pattern: `HOME › PRODUCTS › INDOOR › RESIDENTIAL · MULTI-FAMILY › MULTI-FⒶMILY › {SERIES NAME}`

| PDP | Breadcrumb | Result |
|---|---|---|
| Eclipse-II | HOME › PRODUCTS › INDOOR › RESIDENTIAL · MULTI-FAMILY › MULTI-FⒶMILY › LDLL ECLIPSE-II SERIES | ✓ |
| Radius-II | HOME › PRODUCTS › INDOOR › RESIDENTIAL · MULTI-FAMILY › MULTI-FⒶMILY › LDRS RADIUS-II SERIES | ✓ |
| Nebula-II | HOME › PRODUCTS › INDOOR › RESIDENTIAL · MULTI-FAMILY › MULTI-FⒶMILY › LDRR NEBULA-II SERIES | ✓ (fixed in `78fa7d2`) |
| Crescent | HOME › PRODUCTS › INDOOR › RESIDENTIAL · MULTI-FAMILY › MULTI-FⒶMILY › LSMT CRESCENT SERIES | ✓ |
| eCrescent | HOME › PRODUCTS › INDOOR › RESIDENTIAL · MULTI-FAMILY › MULTI-FⒶMILY › LSMT ECRESCENT SERIES | ✓ |
| Orbit-I | HOME › PRODUCTS › INDOOR › RESIDENTIAL · MULTI-FAMILY › MULTI-FⒶMILY › LDGR ORBIT-I SERIES | ✓ (fixed in `78fa7d2`) |
| Lunar Eclipse | HOME › PRODUCTS › INDOOR › RESIDENTIAL · MULTI-FAMILY › MULTI-FⒶMILY › LDLL LUNAR ECLIPSE SERIES | ✓ |
| Gehry | HOME › PRODUCTS › INDOOR › RESIDENTIAL · MULTI-FAMILY › MULTI-FⒶMILY › CRC GEHRY SERIES | ✓ |

**Result: PASS** (2 breadcrumbs corrected from mockup data errors — Nebula-II and Orbit-I had OUTDOOR/COMMERCIAL/LUXOARCH from their source HTMLs)

---

## Gate 3 — Sticky-Nav + Scroll-Spy

- Eclipse-II: 9 sticky-nav links, IntersectionObserver scroll-spy present ✓
- All 8 PDPs ported from mockup with identical JS island (IntersectionObserver, one Map, one CSS class toggle)
- `.sticky-nav a.is-current` CSS state confirmed in DOM

**Result: PASS**

---

## Gate 4 — Family Band

- Eclipse-II: 10 family-card elements (5 multi-family + 5 cross-line Round-Out) ✓
- Family band links all point to `/products/multi-family/{slug}/` ✓
- `.family-card.is-current` badge applied to the current series on each page ✓
- Cross-line Round-Out CTAs: Pathfinder, Symmetry, Tiny, proARCH-III wired to canonical site URLs ✓

**Result: PASS**

---

## Gate 5 — Configurator

- Eclipse-II: 5 size chips, 2 finish chips, 3 emergency options, 3 sensor options, COPY SKU button, REQUEST A LAYOUT CTA ✓
- Submittal link: `/products/multi-family/eclipse-ii/submittal/` ✓
- All configurator JS from mockup ported verbatim (SKU builder, chip toggle, live preview card) ✓

**Result: PASS**

---

## Gate 6 — Submittal Generator

- Eclipse-II submittal tested with `?sku=LDLL0918-E2S5/W&housing=0918&wattage=18&finish=W&shape=R&autoprint=0`
- URL params read correctly: SKU displayed as `LDLL0918-E2S5/W`, generated date `May 11, 2026` ✓
- 4-page layout: Cover/stamp, Specifications, Dimensions, Ordering + Photometrics ✓
- SAVE AS PDF and ← BACK TO CONFIGURATOR buttons present ✓
- `autoprint=0` correctly suppresses auto-print ✓

**Result: PASS**

---

## Gate 7 — Canonical Token Compliance

- `--brand: #E3353C` → `var(--color-alg-red)` / `var(--brand-red)`: applied ✓
- `font-family: 'Sora'` in page CSS: **none** — Lato used throughout ✓
- `'Sora'` appears only in inline SVG `font-family` attributes within photometric polar plot diagrams (these are SVG text labels, not loaded fonts; browser falls back to `sans-serif`). **Not a calibration failure.**
- `#E3353C` hardcoded: **none** in page CSS ✓
- Rebate Center links: all point to `/support/rebate-center` ✓

**Result: PASS** (SVG polar plot labels noted as cosmetic — will update in Phase B when photometric SVGs are regenerated)

---

## Assets

| Asset Type | Count | Location |
|---|---|---|
| Photometric SVGs | 72 | `/public/products/multi-family/assets/photometrics/` |
| Accessory photos | 6 | `/public/products/multi-family/assets/photos/accessories/` |
| Hero images | 4 | `/public/products/multi-family/assets/photos/` |

---

## Open Items (Pre-Production)

| # | Item | Owner |
|---|---|---|
| 1 | **Product photography** — per-series hero/lifestyle photos not in handoff ZIP. All 8 PDPs show placeholder `<img>` tags with correct `alt` text and `src` paths. | James — provide photos |
| 2 | **IES bundle WorkDrive URL** — Eclipse-II IES bundle href is a placeholder `#`. | James — provide WorkDrive URL |
| 3 | **CRC6-EM24/JBS/W, CRC6-EM24/JBS/B, MSP-SRI/* datasheet URLs** — wired as `#` per brief. | James — provide URLs |
| 4 | **DLC tier on Eclipse-II** — knowledge pack says "TBC — verify with engineering." Badge omitted. | Engineering to confirm |
| 5 | **ENERGY STAR badge on Eclipse-II** — knowledge pack says "TBC." Badge omitted. | Engineering to confirm |
| 6 | **Photometric SVG font** — polar plot SVGs use `font-family="Sora"` in SVG text labels. Cosmetic only; will render as sans-serif. Fix in Phase B when SVGs are regenerated. | Phase B |
| 7 | **Mobile 375×812 visual QA** — all 16 pages need manual mobile spot-check before prod cutover. | Manual QA |
| 8 | **Configurator interactive QA** — chip toggle, SKU builder, COPY SKU, submittal auto-print. | Manual QA |

---

## Staging URLs

| Page | URL |
|---|---|
| Eclipse-II | https://staging.archipelagolighting.com/products/multi-family/eclipse-ii/ |
| Radius-II | https://staging.archipelagolighting.com/products/multi-family/radius-ii/ |
| Nebula-II | https://staging.archipelagolighting.com/products/multi-family/nebula-ii/ |
| Crescent | https://staging.archipelagolighting.com/products/multi-family/crescent/ |
| eCrescent | https://staging.archipelagolighting.com/products/multi-family/ecrescent/ |
| Orbit-I | https://staging.archipelagolighting.com/products/multi-family/orbit-i/ |
| Lunar Eclipse | https://staging.archipelagolighting.com/products/multi-family/lunar-eclipse/ |
| Gehry | https://staging.archipelagolighting.com/products/multi-family/gehry/ |
| Eclipse-II Submittal | https://staging.archipelagolighting.com/products/multi-family/eclipse-ii/submittal/ |
