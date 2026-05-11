# Gate Check Report — G1–G4 Multi-fAMILY Punchlist
**Project:** ALG Staging Site — multi-fⒶMILY Collection  
**Punchlist:** MANUS_MULTIFAMILY_2026-05-11.md  
**Checked by:** Manus  
**Date:** 2026-05-11  
**Commits:** 74196a5, 94447a4 on `main`  
**Staging URL:** https://staging.archipelagolighting.com

---

## F9 — Collection Page: Hero, Stats, and Headlines

| Check | Expected | Result | Status |
|---|---|---|---|
| Browse-by-Application tiles | 4 tiles: Housing Cans, Recessed Downlights, SafeZone Downlights, Surface Mount | All 4 present with correct SKU counts (8, 22, 8, 21) | ✅ PASS |
| Stat strip — Families | 8 Families | 8 Families | ✅ PASS |
| Stat strip — Active SKUs | 59 Active SKUs | 59 Active SKUs | ✅ PASS |
| Stat strip — Applications | 4 Applications | 4 Applications | ✅ PASS |
| Featured section headline | "Three flagship families from the multi-fⒶMILY collection." | Correct | ✅ PASS |
| All Families section headline | "Eight families from the multi-fⒶMILY collection." | Correct | ✅ PASS |
| Hero badge strip | VALUE-ENGINEERED · CODE-COMPLIANT · JA8 / TITLE 24 · 48-HR LAYOUTS · 5-YR WARRANTY | All 5 present | ✅ PASS |

---

## F10 — All Families Grid: 8 Cards, Sub-categories, Echelons, VIEW Links

| Family | Application | Echelon | Max Wattage | SKU Count | VIEW → Link | Status |
|---|---|---|---|---|---|---|
| Gehry | Housing Cans | PRO | — | 8 | /products/multi-family/gehry/ | ✅ PASS |
| Nebula-II | Recessed Downlights | ECO | 15W | 12 | /products/multi-family/nebula-ii/ | ✅ PASS |
| Orbit-I | Recessed Downlights | ECO | 15W | 4 | /products/multi-family/orbit-i/ | ✅ PASS |
| Radius-II | Recessed Downlights | PRO | 18W | 6 | /products/multi-family/radius-ii/ | ✅ PASS |
| Radius SafeZone | SafeZone Downlights | PRO+ | 19W | 8 | /products/multi-family/radius-safezone/ | ✅ PASS |
| eCrescent | Surface Mount | ECO | 15W | 5 | /products/multi-family/ecrescent/ | ✅ PASS |
| Eclipse-II | Surface Mount | PRO | 24W | 13 | /products/multi-family/eclipse-ii/ | ✅ PASS |
| Lunar Eclipse | Surface Mount | PRO | 18W | 3 | /products/multi-family/lunar-eclipse/ | ✅ PASS |

All 8 VIEW → links resolve to correct `/products/multi-family/{slug}/` PDPs. Filter controls (Application, Echelon, Max Wattage, CCT, Voltage, Mount Type) all present and functional.

---

## F11 — Radius SafeZone PDP

| Check | Expected | Result | Status |
|---|---|---|---|
| HTTP status | 200 OK | 200 OK | ✅ PASS |
| URL | /products/multi-family/radius-safezone/ | Live at correct URL | ✅ PASS |
| H1 | "Radius SafeZone" | Correct | ✅ PASS |
| Breadcrumb | HOME › PRODUCTS › RESIDENTIAL › MULTI-FAMILY › RADIUS SAFEZONE | Correct | ✅ PASS |
| Stub notice | "Full spec sheet coming soon" or equivalent | Present | ✅ PASS |

---

## F12 — Mega-Menu: 4 Applications, Hover Panel

| Check | Expected | Result | Status |
|---|---|---|---|
| Application items | Housing Cans, Recessed Downlights, SafeZone Downlights, Surface Mount | All 4 present | ✅ PASS |
| Hover panel | Right-side panel fires on hover with family tier cards | Functional | ✅ PASS |
| Old "Wally" entry | Removed | Not present | ✅ PASS |
| Links | Each application item links to /collections/multi-family/ with correct anchor | Correct | ✅ PASS |

---

## Summary

All G1–G4 punchlist items pass gate checks F9–F12. The multi-fⒶMILY collection page, All Families grid, Radius SafeZone PDP, and mega-menu are all live and correct on staging.

---

## Escalation Items

The following items require stakeholder input or additional assets before production launch.

### ESC-01 — Eclipse-II maxWattage discrepancy (CONFIRM WITH ENGINEERING)

- **Featured card** shows **18W max** (value sourced from `featured[]` array in `multifamily.ts`)
- **All Families card** shows **24W max** (value sourced from `sku-index.json`, `maxWattage: 24`)
- The two data sources are out of sync. Engineering should confirm the correct rated maximum wattage for Eclipse-II and one source should be updated to match.

### ESC-02 — Nebula-II maxWattage discrepancy (CONFIRM WITH ENGINEERING)

- **Featured card** shows **20W max** (value sourced from `featured[]` array in `multifamily.ts`)
- **All Families card** shows **15W max** (value sourced from `sku-index.json`, `maxWattage: 15`)
- Same root cause as ESC-01. Engineering should confirm and a single authoritative value should be set in `sku-index.json`; the `featured[]` override in `multifamily.ts` should then be removed or aligned.

### ESC-03 — Product photography missing for all 8 PDPs

All 8 multi-fⒶMILY PDPs are live as stub pages. No product photography has been supplied. PDPs currently render with placeholder image blocks. Photography assets are needed before production launch.

### ESC-04 — WorkDrive datasheet URLs still placeholder

At least 3 family PDPs reference placeholder Zoho WorkDrive datasheet URLs (e.g., `#` or `https://workdrive.zoho.com/...` with a stub path). Final datasheet PDF links must be supplied and updated in the relevant PDP source files before production launch.

---

*Report generated from staging verification on 2026-05-11. All checks performed against commit 94447a4.*
