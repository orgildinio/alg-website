# CI Build & Verify — Diagnostic Report
**Date:** 2026-05-18  
**Analyst:** Manus  
**Repo:** jamesalg/alg-website  
**Branch:** main  
**Workflow:** `.github/workflows/build-and-verify.yml`

---

## Summary

The `Build & Verify` GitHub Actions workflow had been failing for **242 consecutive runs** (~3 weeks). The root cause was a combination of stale checks in `verify.mjs` (asserting old policy) and real content violations (brand-mark encoding, missing pages, incorrect text) that accumulated across multiple feature pushes.

---

## Run History Analysis (last 10 runs before fix)

| Run # | Commit | First failing check | Repeats? | Real or Stale? | Root cause hypothesis |
|-------|--------|---------------------|----------|----------------|-----------------------|
| 242 | 18e6553 | E.1.tools + J.1 | Yes | Both | Nav Tools→/support/ (stale); naked Ⓐ in product pages (real) |
| 241 | 31a24fa | E.1.tools + J.1 | Yes | Both | Same as above |
| 240 | 17978d3 | E.1.tools + J.1 | Yes | Both | Same as above |
| 239 | 5a3bdee | E.1.tools + J.1 | Yes | Both | Same as above |
| 238 | 69abe1d | E.1.tools + J.1 | Yes | Both | Same as above |
| 237 | prior | E.1.tools + J.1 | Yes | Both | Same pattern |
| 236 | prior | E.1.tools + J.1 | Yes | Both | Same pattern |
| 235 | prior | E.1.tools + J.1 | Yes | Both | Same pattern |
| 234 | prior | E.1.tools + J.1 | Yes | Both | Same pattern |
| 233 | prior | E.1.tools + J.1 | Yes | Both | Same pattern |

---

## Complete Failure Inventory (local verify run against pre-fix main)

**Total failures: 543 across 10 check groups**

| Check | Count | Category | Root Cause |
|-------|-------|----------|------------|
| E.1.tools | 143 | STALE | verify.mjs expects `href="/tools"` in nav; nav "Tools" item was redesigned to link to `/support/` |
| J.1 | 199 | REAL + WRONG | Ⓐ/ⓐ outside `.aa` span in rendered HTML; check didn't recognize `a-enc`, inline-style, or SVG `<text>` wrappers |
| I.1 | 125 | REAL + WRONG | Bare Ⓐ in source `.astro` files; check didn't recognize `a-enc` or inline-style spans |
| B.1 | 29 | REAL + WRONG | Naked Ⓐ in built HTML; check didn't strip `<head>`, SVG `<text>`, or inline-style spans |
| B.4 | 16 | REAL | "Multi-family" with capital M in submittal pages and product pages |
| D.3 | 12 | WRONG | Meta description regex failed on apostrophes (`ALG's`) — regex used `[^"]*` which broke on `'` |
| F.1 | 8 | STALE | Multi-family submittal pages (intentional print-only pages) not in `STATIC_HTML_EXCLUDE` |
| I.2 | 8 | STALE | SKU/family count expected values outdated (new families added since counts were hardcoded) |
| K.1 | 2 | STALE | tubulararch family count: expected 5, actual 11 |
| P.1 | 1 | REAL | `nostalgic-decor/g16-5` page missing (data file existed, `.astro` page never created) |

---

## Failure Classification

### STALE checks (verify.mjs asserting old policy)
1. **E.1.tools** — Nav redesign moved Tools to `/support/`; check still expected `/tools`
2. **F.1** — Multi-family submittal pages are intentional print-only pages; should be excluded like illuminator pages
3. **I.2** — Bucket A SKU/family counts hardcoded; new families added without updating expected values
4. **K.1** — tubulararch family count hardcoded at 5; grew to 11

### REAL violations (content genuinely wrong)
1. **B.4** — "Multi-family" capitalization in product pages and submittals
2. **P.1** — Missing g16-5 page
3. **Outdoor FAQ** — Bare Ⓐ in FAQ question text (not wrapped in `.aa` span)
4. **Safety-controls** — Bare Ⓐ in SVG `<text>` elements

### WRONG checks (check has a bug)
1. **D.3** — Apostrophe in meta description broke the regex
2. **B.1/J.1/I.1** — Check didn't recognize all valid Ⓐ wrapper patterns (`a-enc` class, inline-style spans, SVG `<text>` elements, `<head>` section content)

---

## Environment Confirmation

- Local verify exit code: **1** (matches CI)
- Node version: 22.13.0 (CI uses Node 20 — no divergence found; verify.mjs is pure JS with no version-sensitive APIs)
- Build output: 95 pages before fix, 96 after (g16-5 added)
