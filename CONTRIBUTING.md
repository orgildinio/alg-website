# Contributing to alg-website

## Before pushing to `main`

**This is mandatory.** Every push to `main` must pass the full build and verify suite locally before pushing. No exceptions.

```bash
npm ci                  # clean install
npm run build           # full build
npm run verify          # full verify suite
echo "exit code: $?"    # must be 0
```

If `npm run verify` exits with code `1`, **do not push**. Fix the violations first.

This rule was codified on **2026-05-18** after 242 consecutive CI failures caused by pushes that skipped local verification. The Cloudflare Pages deploy succeeds regardless of CI status — a green staging site does NOT mean CI is green.

---

## Why this matters

The `Build & Verify` GitHub Actions workflow runs `npm run verify` against the built output. It checks:

- Brand-mark encoding (Ⓐ must be wrapped in `.aa` spans)
- Mega-menu drift (all canonical nav items present on every page)
- Header canonical hash (header HTML matches expected structure)
- SEO fields (title, meta description present and valid)
- Internal link integrity (no 404s)
- SKU/family counts (Bucket A collections match expected values)
- Page existence (all expected lamp/product pages exist)

A red CI X on `main` means one or more of these checks failed. It emails James. Fix it.

---

## Verify suite

The verification suite is in `scripts/verify.mjs`. It runs against `dist/` (the built output). If you update site policy (nav structure, brand-mark rules, page slugs, SKU counts), update `verify.mjs` to match — and add a comment block explaining what changed, when, and why.

**Do not silence checks.** Do not add `continue-on-error: true` to the workflow. Do not comment out checks. Fix the root cause.
