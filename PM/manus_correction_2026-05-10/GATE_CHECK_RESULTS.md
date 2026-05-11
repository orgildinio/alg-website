# Gate Check Results — MANUS_GATE_CHECKS_2026-05-10
**Commit:** `af60665` · **Branch:** `main` · **Repo:** `jamesalg/alg-website`
**Verified against:** `https://staging.archipelagolighting.com`
**Date:** 2026-05-11

---

## §F1 — URL Canonicalization

| Route | Expected | Actual | Result |
|---|---|---|---|
| `/collections/indoor/` | 200 | 200 | **PASS** |
| `/collections/outdoor/` | 200 | 200 | **PASS** |
| `/collections/lamps/` | 200 | 200 | **PASS** |
| `/collections/residential/` | 200 | 200 | **PASS** |
| `/collections/safety-controls/` | 200 | 200 | **PASS** |
| `/solutions/cold-storage-grocery/` | 200 | 200 | **PASS** |
| `/solutions/data-center/` | 200 | 200 | **PASS** |
| `/solutions/education/` | 200 | 200 | **PASS** |
| `/solutions/healthcare/` | 200 | 200 | **PASS** |
| `/solutions/hospitality/` | 200 | 200 | **PASS** |
| `/solutions/industrial-manufacturing/` | 200 | 200 | **PASS** |
| `/solutions/warehouse-logistics/` | 200 | 200 | **PASS** |
| `/solutions/government-military/` | 200 | 200 | **PASS** |
| `/support/rebate-center/` | 200 | 200 | **PASS** |

---

## §F2 — Breadcrumb Parity

| Page | Home link | Parent link | Current label | Result |
|---|---|---|---|---|
| `/collections/indoor/` | ✓ Home | ✓ Products | ✓ Indoor | **PASS** |
| `/solutions/cold-storage-grocery/` | ✓ Home | ✓ Solutions | ✓ Cold Storage & Grocery | **PASS** |
| `/support/rebate-center/` | ✓ Home | ✓ Support | ✓ Rebate Center | **PASS** |

---

## §F3 — 301 Redirects

| Legacy URL | Canonical URL | Redirect fires | Result |
|---|---|---|---|
| `/products/indoor` | `/collections/indoor/` | ✓ | **PASS** |
| `/products/outdoor` | `/collections/outdoor/` | ✓ | **PASS** |
| `/products/lamps` | `/collections/lamps/` | ✓ | **PASS** |
| `/products/residential` | `/collections/residential/` | ✓ | **PASS** |
| `/products/safety-controls` | `/collections/safety-controls/` | ✓ | **PASS** |
| `/verticals/cold-storage` | `/solutions/cold-storage-grocery/` | ✓ | **PASS** |
| `/solutions/safety-controls` | `/collections/safety-controls/` | ✓ | **PASS** |
| `/pages/rebate-center` | `/support/rebate-center/` | ✓ | **PASS** |

---

## §F4 — ApplicationFinder JS Hydration

Verified on `/collections/indoor/` via browser console:

| Check | Value | Result |
|---|---|---|
| `[data-coll]` chips found | 10 | **PASS** |
| `[data-coll-card]` cards found | 2 | **PASS** |
| Click WAREHOUSE chip → `app-chip--active` | `true` | **PASS** |
| lamparARCH card → `coll-card-wrap--highlight` | `true` | **PASS** |
| planoARCH card → `coll-card-wrap--dim` | `true` | **PASS** |
| Keyboard accessible (`Enter`/`Space`) | Implemented | **PASS** |
| Toggle off (second click) → deactivate | Implemented | **PASS** |

All 5 collection pages carry the same JS island and `data-coll` / `data-coll-card` attributes.

---

## §F5 — Token Hygiene

| Check | Result |
|---|---|
| No `#E3353C` in `/collections/indoor/` DOM | **PASS** |
| No `Sora` font in `/collections/indoor/` styles | **PASS** |
| No `#E3353C` in `/support/rebate-center/` DOM | **PASS** |
| `#F32740` is the only brand red in `src/` | **PASS** |

---

## §F6 — Rebate Center Light Theme

| Check | Value | Result |
|---|---|---|
| `document.body` background | `rgb(255, 255, 255)` | **PASS** |
| Page wrapper background | `rgba(0, 0, 0, 0)` (transparent over white) | **PASS** |
| Breadcrumb: Home › Support › Rebate Center | ✓ | **PASS** |
| Dark Layer-B overrides stripped | ✓ | **PASS** |
| Brand-only widget overrides retained | ✓ | **PASS** |

---

## §F7 — Rebate Widget Integrity

| Check | Value | Result |
|---|---|---|
| `#ee_widget_container` present | ✓ | **PASS** |
| `#ee_widget_main` present | ✓ | **PASS** |
| Widget tabs (`[role="tab"]`) | 3 (Home, Controls, Settings) | **PASS** |
| ag-Grid column headers | 14 | **PASS** |
| Data rows visible on load | ✓ (11+ rows) | **PASS** |
| `widget_base.js` script tag | ✓ | **PASS** |

---

## Summary

All **7 gate check categories** pass on staging commit `af60665`.

**Items remaining for manual QA before prod cutover:**
1. Rebate Center interactive tests: ZIP filter, column toggle, sort, pagination, download
2. Mobile 375×812 visual check on all 14 new pages
3. ApplicationFinder on remaining 4 collection pages (outdoor, lamps, residential, safety-controls) — same JS island, spot-check recommended
