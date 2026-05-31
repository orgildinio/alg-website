Liberty contrⒶLS section · device imagery drop point
===========================================================

The Liberty PDP Section 6 (contrⒶLS) tab switcher swaps between two
sensor product photos based on the active tab. The HTML + JS wiring is
canonical (`mockup_liberty_pdp_v1.html` lines ~5036-5046 + the tac-section
tab-switcher script at ~5095-5160).

REQUIRED FILES — drop here with these exact names:

  1. sensor-bls.webp
     Image: PIR dome sensor with hexagonal Fresnel lens + two mounting
     screws (the dome-on-cap fixture-mount sensor).
     Used by: contrⒶLS Bi-Level tab (/BLS · /BLS-5D).

  2. sensor-acs.webp
     Image: Two-piece socket + dome sensor module (the spring-loaded
     three-pin socket on the bottom + the dome assembly on the right).
     Used by: contrⒶLS by ⒶCS tab AND contrⒶLS by SILVAIR tab.
     (Same physical hardware — different firmware/protocol stack.)

NOTES:
- WebP preferred for production (smaller payload, transparent bg support).
- PNG with transparent or matte-black background also fine — change
  `.webp` to `.png` in the <img src=> in mockup_liberty_pdp_v1.html
  around lines 5037, 5041, 5045 if you save as PNG instead of WebP.
- Aspect ratio: ~3:2 to 4:3 fits the .tac-sensor-area panel (60% width,
  max 380px, drop-shadow filter applied via CSS).
- The page renders both images side-by-side in the DOM; the active tab's
  image gets `.is-active` class (opacity 0.96 + scale 1.0), inactives
  fade to opacity 0 + scale 0.94 via CSS transition.

If you upload to a different filename, update the <img src=> attributes
in mockup_liberty_pdp_v1.html at the lines noted above.
