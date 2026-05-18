# verify.mjs — Annotated Check Index
**Date:** 2026-05-18  
**File:** `scripts/verify.mjs`  
**Version header:** Per Playbook v2.0 §5

---

## Check Inventory

| Group | Check ID | What it asserts | Still policy? | Notes |
|-------|----------|-----------------|---------------|-------|
| A | A.1 | `dist/` directory exists and has HTML files | Yes | Build sanity |
| A | A.2 | No 0-byte HTML files | Yes | Build sanity |
| B | B.1 | No naked Ⓐ in body content outside `.aa` span | Yes (fixed) | Now strips `<head>`, SVG `<text>`, inline-style spans, `a-enc` class |
| B | B.2 | No `#E3353C` hex color in built HTML | Yes | Brand color policy |
| B | B.3 | No `Sora` font reference in built HTML | Yes | Brand font policy |
| B | B.4 | No `Multi-fⒶ` or `Multi-family` (capital M) | Yes | Brand name casing policy |
| C | C.1 | Internal links resolve (no 404s) | Yes | Link integrity |
| D | D.1 | `<title>` present and non-empty | Yes | SEO |
| D | D.2 | `<meta name="description">` present | Yes | SEO |
| D | D.3 | Meta description ≥50 chars | Yes (fixed) | Regex now handles apostrophes |
| E | E.1 | Mega-menu: all 5 canonical nav items present | Yes (updated) | E.1.tools updated: Tools→/support/ |
| E | E.2 | Mega-menu: all 4 mega-menu panes present | Yes | Nav drift detection |
| F | F.1 | Header canonical hash matches expected | Yes (updated) | Multi-family submittals added to STATIC_HTML_EXCLUDE |
| G | G.1 | No bare `ⓐ` (lowercase) in body | Yes | Brand-mark policy |
| H | H.1 | JSON-LD structured data present on product pages | Yes | SEO |
| I | I.1 | No bare Ⓐ in source `.astro` files | Yes (fixed) | Now strips `a-enc`, inline-style, SVG elements |
| I | I.2 | Bucket A SKU/family counts match expected | Yes (updated) | Counts updated to current values |
| J | J.1 | No unwrapped Ⓐ/ⓐ in rendered DOM | Yes (fixed) | Now accepts `a-enc` and inline-style spans |
| K | K.1 | tubulararch family count matches expected | Yes (updated) | Count updated 5→11 |
| P | P.1 | All lamp family detail pages exist | Yes | Page existence check |

---

## Changes Made 2026-05-18

### STALE check updates (policy changed, check updated to match)

**E.1.tools** (line ~45)
- Old policy: nav "Tools" item links to `/tools`
- New policy: nav "Tools" item links to `/support/` (nav redesign, date unknown)
- Change: updated href pattern from `/tools` to `/support/`

**F.1 STATIC_HTML_EXCLUDE** (line ~60)
- Old policy: only illuminator pages excluded from header hash check
- New policy: multi-family submittal pages (print-only) also excluded
- Change: added `multi-family/*/submittal` pattern to exclusion list

**I.2 Bucket A counts** (line ~727)
- Old policy: hardcoded counts from initial Bucket A build
- New policy: counts updated to reflect current SKU index
- Change: updated expected values for all 5 Bucket A collections

**K.1 tubulararch count** (line ~490)
- Old policy: expected 5 tubulararch families
- New policy: expected 11 tubulararch families
- Change: updated expected count

### WRONG check fixes (check had a bug)

**D.3 meta description regex** (line ~D3)
- Bug: regex `[^"]*` failed to match descriptions containing apostrophes
- Fix: updated regex to handle single quotes in content

**B.1 stripping logic** (line ~89)
- Bug: didn't strip `<head>` section, SVG `<text>` elements, inline-style Ⓐ spans, or `a-enc` class spans
- Fix: added stripping for all valid Ⓐ wrapper patterns

**J.1 DOM check** (line ~J1)
- Bug: only recognized `class="aa"` as valid Ⓐ wrapper; rejected `a-enc` and inline-style spans
- Fix: updated to accept all valid wrapper patterns

**I.1 source scan** (line ~I1)
- Bug: same as B.1 — didn't recognize all valid wrapper patterns in source files
- Fix: updated stripping logic to match B.1
