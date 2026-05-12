# multi-fⒶMILY Visual Fix Report

**Date:** May 11, 2026
**Environment:** Staging

All three visual regressions identified on the staging site have been diagnosed and fixed. The code has been committed to `main` and the Netlify deployment is live.

## 1. Collection Page Cards Missing Images
**Issue:** The family cards on the `/collections/multi-family/` page were showing text watermarks (e.g., "GEHRY", "NEBULA-II") instead of the actual product photos.
**Root Cause:** The `card_image` field and `lineDrawing` field were missing from the JSON and TypeScript data structures that power the collection grid and featured section.
**Fix:**
- Extracted the hero product photos from the asset ZIP and copied them to a shared `/public/products/multi-family/card-images/` directory.
- Updated `sku-index.json` to include the `card_image` field for all 8 families.
- Updated `multifamily.ts` to include the `lineDrawing` field for the 3 featured families.
- **Result:** Both the Featured section and the All Families grid now render the correct product photos.

## 2. Faded First Slide in Hero Carousel
**Issue:** The first image in the hero carousel on product pages (like Orbit-I and Nebula-II) appeared washed out and faded.
**Root Cause:** The CSS class `.slide-img` had `mix-blend-mode: multiply` applied. This blend mode works well on light gray backgrounds to remove white photo backgrounds, but the carousel container had a pure white (`#FFFFFF`) background. This caused the white and light-gray areas of the product photos to blend into the white background, resulting in a faded appearance.
**Fix:**
- Removed the `mix-blend-mode: multiply` property from the `.slide-img` CSS block across all 8 multi-family PDPs.
- **Result:** The hero carousel images now render at full opacity with their natural colors.

## 3. Dimensions and Photometrics SVG Sizing
**Issue:** The photometric SVGs and inline dimension SVGs were rendering as tiny boxes or not filling their containers correctly.
**Root Cause:** The SVG files only contained a `viewBox` attribute (e.g., `viewBox="0 0 600 460"`) but lacked explicit `width` and `height` attributes. When loaded via an `<img>` tag without explicit dimensions, browsers fall back to a default intrinsic size (often 300x150px), which caused them to shrink inside their larger grid containers.
**Fix:**
- Added explicit `width="600"` and `height="460"` attributes to all 72 photometric SVG files in the public assets directory.
- Added explicit `width="600"` and `height="320"` attributes to the inline `<svg id="dimSvg">` elements across all 8 PDPs.
- **Result:** The SVGs now scale correctly to fill their designated layout containers while maintaining their aspect ratio.

---
The staging site is now rendering correctly. Please review the updated deployment at [staging.archipelagolighting.com](https://staging.archipelagolighting.com/collections/multi-family/).
