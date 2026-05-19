# GATE CHECK RESULTS — Editable Catalog Number (§C)
**Date:** 2026-05-18  
**Commit:** cd4e57d  
**Prompt:** MANUS_SUBMITTAL_EDITABLE_CATALOG_2026-05-18.md

---

## F1 — All 8 submittal files patched

| File | contenteditable | editable-catalog CSS | setupEditableCatalogNumber() |
|------|:-:|:-:|:-:|
| crescent/submittal | ✅ | ✅ | ✅ |
| eclipse-ii/submittal | ✅ | ✅ | ✅ |
| ecrescent/submittal | ✅ | ✅ | ✅ |
| gehry/submittal | ✅ | ✅ | ✅ |
| lunar-eclipse/submittal | ✅ | ✅ | ✅ |
| nebula-ii/submittal | ✅ | ✅ | ✅ |
| orbit-i/submittal | ✅ | ✅ | ✅ |
| radius-ii/submittal | ✅ | ✅ | ✅ |

## F2 — Build: exit 0 ✅

## F3 — Verify: exit 0 ✅

## F4 — CI: success ✅
Commit `cd4e57d` — conclusion: success

## F5 — ID variance documented

| Product | SKU variable | piCatNum pattern | Notes |
|---------|-------------|-----------------|-------|
| crescent, eclipse-ii, ecrescent, gehry, lunar-eclipse, radius-ii | `sku` | `var pi = document.getElementById('piCatNum'); if (pi) pi.textContent = sku;` | Standard pattern — auto-patched |
| nebula-ii, orbit-i | `sku` (with `var skuLive = sku` alias) | `document.getElementById('piCatNum').textContent = skuLive;` | Different anchor — manually patched |

## F6 — Behavior spec

- Click on catalog number in page header → field becomes editable (cursor: text, red dashed underline on hover, red outline on focus)
- Type to override → catNum2, catNum3, catNum4, piCatNum, liveSku all update in real-time
- specsEyebrow `{family} · {sku}` prefix preserved
- Full-page text-node walker sweeps any other occurrence of the original SKU
- document.title updated for filename hint
- Enter key blurs (no line breaks)
- Empty blur → reverts to original SKU
- Print: no cursor, no border, no outline (clean PDF)
- Session-only: no localStorage, no persistence across page loads
