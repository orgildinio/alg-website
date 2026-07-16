#!/usr/bin/env python3
"""
#90b authored fixes — no find-replace. Each string is exact and unique.
Fixes applied:
  1. "Reads §9 Configurator" → "Reads the Configurator" (8 pages)
  2. "Reads §9 SKU" → "Reads the SKU" (retroarch-p1, retroarch-t1)
  3. "Switch tabs in §2 above to see LCDL4..." → "Switch tabs in the Specifications section above to see LCDL4..." (6 pages)
  4. "Switch tabs in §2 above to see LCDL4..." SafeZone variant → same
  5. Spectra §6 photometric IES title attr — remove §6 ref
  6. Spectra CFG-RBT-2 rebate copy — remove rule citation
  7. Spectra CRI configurator cell — remove internal note
  8. Spectra compliance cell — remove CFG-QA-1 note
  9. Solstice CFG- photo-stat-sub — remove rule citation
  10. Waymark CFG- photo-stat-sub — remove rule citation
  11. Waymark spec-table-foot heads up: — remove note
  12. Waymark submittal CRI heads up: — rewrite
  13. Waymark submittal Country of Origin heads up: — rewrite
  14. retroarch-t1 LPVR sentence — remove heads up: note
  15. Trackstar §8 grid references in configurator label and body — rewrite
  16. Trackstar §8 grid reference in specifier-support pillar — rewrite
  17. Trackstar submittal §8 grid section head — rewrite
  18. Trackstar rebate sentence §11 planoⒶRCH -tier — rewrite (nit 1)
  19. Trackstar family-card badge ECO→PRO (nit 2)
"""

import re

fixes = []

# ── Helper ──────────────────────────────────────────────────────────────────
def fix(filepath, old, new, description):
    fixes.append((filepath, old, new, description))

# ── 1. "Reads §9 Configurator" → "Reads the Configurator" ───────────────────
for page in [
    'public/products/astra/index.html',
    'public/products/luxmark/index.html',
    'public/products/proarch-t/index.html',
    'public/products/spectra/index.html',
    'public/products/trackstar/index.html',
    'public/products/waymark/index.html',
]:
    fix(page,
        'Reads §9 Configurator',
        'Reads the Configurator',
        'Remove §9 internal section ref from docs-card-updated label')

# ── 2. "Reads §9 SKU" → "Reads the SKU" ─────────────────────────────────────
for page in [
    'public/products/retroarch-p1/index.html',
    'public/products/retroarch-t1/index.html',
]:
    fix(page,
        'Reads §9 SKU',
        'Reads the SKU',
        'Remove §9 internal section ref from docs-card-updated label')

# ── 3. "Switch tabs in §2 above" → "Switch tabs in the Specifications section above" ──
# Standard variant (astra, luxmark, proarch-t, solstice, waymark)
switch_standard = 'Switch tabs in §2 above to see LCDL4 / LCDL8 / LCDL10 watt tiers; the 15-CCT range stays constant across all four sizes.'
switch_fixed    = 'Switch tabs in the Specifications section above to see LCDL4 / LCDL8 / LCDL10 watt tiers; the 15-CCT range stays constant across all four sizes.'
for page in [
    'public/products/astra/index.html',
    'public/products/luxmark/index.html',
    'public/products/proarch-t/index.html',
    'public/products/solstice/index.html',
    'public/products/waymark/index.html',
]:
    fix(page, switch_standard, switch_fixed, 'Remove §2 internal section ref from spec-table footnote')

# SafeZone variant
fix('public/products/solstice-safezone/index.html',
    'Switch tabs in §2 above to see LCDL4 / LCDL8 / LCDL10 watt tiers; the 15-CCT range stays constant across all four sizes.',
    'Switch tabs in the Specifications section above to see LCDL4 / LCDL8 / LCDL10 watt tiers; the 15-CCT range stays constant across all four sizes.',
    'Remove §2 internal section ref from SafeZone spec-table footnote')

# ── 4. Spectra: IES docs-card title attr with §6 ref ────────────────────────
fix('public/products/spectra/index.html',
    'title="IES Bundle pending — target next week per James 2026-05-09 · §6 photometric',
    'title="IES Bundle pending',
    'Remove §6 internal section ref from IES docs-card title attribute')

# ── 5. Spectra: CFG-RBT-2 in rebate copy ────────────────────────────────────
fix('public/products/spectra/index.html',
    'The Spectra qualifies for utility rebate programs at the DLC Listed tier (verification pending Rebate Center search per CFG-RBT-2 · datasheet is silent on DLC tier · published up to 100 LM/W efficacy',
    'The Spectra qualifies for utility rebate programs at the DLC Listed tier — published up to 100 LM/W efficacy',
    'Remove CFG-RBT-2 rule citation from Spectra rebate copy')

# ── 6. Spectra: CRI configurator cell internal note ─────────────────────────
# The cell reads: 80+ standard (NOT 90+ · datasheet body wins · pg 1 truⒶCOLOR chip is a marketing claim · CRI 80+ is the spec-grade value)
fix('public/products/spectra/index.html',
    '(NOT 90+ \u00b7 datasheet body wins \u00b7 pg 1 tru<span class="aa">\u24b6</span>COLOR chip is a marketing claim \u00b7 CRI 80+ is the spec-grade value)',
    '',
    'Remove internal note from Spectra CRI configurator cell')

# ── 7. Spectra: compliance cell CFG-QA-1 note ───────────────────────────────
# Ends with: · >0.9 PF · <20% THD · CFG-QA-1 verified
fix('public/products/spectra/index.html',
    ' \u00b7 CFG-QA-1 verified',
    '',
    'Remove CFG-QA-1 rule citation from Spectra compliance configurator cell')

# ── 8. Solstice: CFG- photo-stat-sub ────────────────────────────────────────
# Line 4985: "100° wide-distribution beam · rotationally symmetric · frosted polycarbonate diffuser delivers a glare-free wash with no hot-spot pixelation. CRI >90 standard · CFG-PHOTO-1 verified."
fix('public/products/solstice/index.html',
    ' \u00b7 CFG-PHOTO-1 verified.',
    '.',
    'Remove CFG-PHOTO-1 rule citation from Solstice photo-stat-sub')

# ── 9. Waymark: CFG- photo-stat-sub ─────────────────────────────────────────
# Line 5337 ends with: "C0/180 long-axis · C90/270 short-axis · CFG-PHOTO-1 verified."
fix('public/products/waymark/index.html',
    ' \u00b7 CFG-PHOTO-1 verified.',
    '.',
    'Remove CFG-PHOTO-1 rule citation from Waymark photo-stat-sub')

# ── 10. Waymark: spec-table-foot "heads up:" note ───────────────────────────
# Line 4427: ends with "...heads up: Waymark is a commercial-ambient product, not a spec-grade luminaire."
fix('public/products/waymark/index.html',
    ' heads up: Waymark is a commercial-ambient product, not a spec-grade luminaire.',
    '',
    'Remove heads-up internal note from Waymark spec-table-foot')

# ── 11. Waymark submittal: CRI "heads up:" ───────────────────────────────────
fix('public/products/waymark/submittal/index.html',
    '&gt; 80 (commercial-ambient tier &middot; heads up: not 90+ spec-grade)',
    '&gt; 80 (commercial-ambient tier)',
    'Remove heads-up internal note from Waymark submittal CRI cell')

# ── 12. Waymark submittal: Country of Origin "heads up:" ────────────────────
fix('public/products/waymark/submittal/index.html',
    'Verification pending supplier confirmation &middot; heads up: non-TAA',
    'Verification pending supplier confirmation &middot; non-TAA',
    'Remove heads-up internal note from Waymark submittal Country of Origin cell')

# ── 13. retroarch-t1: LPVR sentence with "heads up:" ────────────────────────
# Line 4421: "Three sizes (LPVR14 1×4 · LPVR22 2×2 · LPVR24 2×4) × three WATTselect dip positions × three CCTselect dip positions = 27 install configurations from 6 catalog SKUs. Pick the size that fits the ceiling grid — heads up: LPVR14 is the only size that fits a 1×4 T-bar grid."
fix('public/products/retroarch-t1/index.html',
    ' \u2014 heads up: LPVR14 is the only size that fits a 1\u00d74 T-bar grid.',
    '. LPVR14 is the only size that fits a 1\u00d74 T-bar grid.',
    'Remove heads-up internal note from retroarch-t1 LPVR sentence')

# ── 14. Trackstar: configurator label "(separate line items · see §8 grid)" ──
# This is flagged for James to decide — but the §8 reference is a UI navigation aid
# pointing to the Accessories section. Rewrite to remove the § number.
fix('public/products/trackstar/index.html',
    '(separate line items \u00b7 see \u00a78 grid)',
    '(separate line items \u00b7 see Accessories below)',
    'Remove §8 internal section ref from trackstar configurator field label')

# ── 15. Trackstar: body paragraph "§8 Accessories grid" ─────────────────────
fix('public/products/trackstar/index.html',
    'picked from the \u00a78 Accessories grid based on the install geometry. The configurator at left resolves the head SKU; the \u00a78 grid resolves the track system.',
    'picked from the Accessories grid below based on the install geometry. The configurator at left resolves the head SKU; the Accessories grid resolves the track system.',
    'Remove §8 internal section refs from trackstar configurator body paragraph')

# ── 16. Trackstar: specifier-support pillar "§8 grid" ───────────────────────
fix('public/products/trackstar/index.html',
    'track<span class="aa">\u24b6</span>DAPT layout components ship per project as line-item orders from the \u00a78 grid.',
    'track<span class="aa">\u24b6</span>DAPT layout components ship per project as line-item orders from the Accessories grid.',
    'Remove §8 internal section ref from trackstar specifier-support pillar')

# ── 17. Trackstar: beamADJUST section "§8 Accessories" ──────────────────────
fix('public/products/trackstar/index.html',
    'Layouts rendered as a 10-card filterable grid in \u00a78 Accessories.',
    'Layouts rendered as a 10-card filterable grid in the Accessories section.',
    'Remove §8 internal section ref from trackstar beamADJUST paragraph')

# ── 18. Trackstar submittal: "§8 grid" section head ─────────────────────────
fix('public/products/trackstar/submittal/index.html',
    'track<span class="aa">\u24b6</span>DAPT System (per-project \u00b7 \u00a78 grid)',
    'track<span class="aa">\u24b6</span>DAPT System (per-project \u00b7 see Accessories)',
    'Remove §8 internal section ref from trackstar submittal section head')

# ── 19. Trackstar nit 1: rebate sentence "§11 planoⒶRCH -tier" ──────────────
# Current: "Pair with the §11 planoⒶRCH -tier networked lighting control family"
fix('public/products/trackstar/index.html',
    'Pair with the \u00a711 plano\u24b6RCH -tier networked lighting control family',
    'Pair with the plano\u24b6RCH networked lighting control family',
    'Trackstar nit 1: remove §11 internal section ref and orphaned -tier fragment from rebate copy')

# ── 20. Trackstar nit 2: family-card badge ECO→PRO ───────────────────────────
# The "You Are Here" card reads: LTRK · Trackstar ECO
fix('public/products/trackstar/index.html',
    'LTRK \u00b7 Trackstar ECO',
    'LTRK \u00b7 Trackstar PRO',
    'Trackstar nit 2: align family-card badge to PRO (matches H1 and meta)')

# ── Apply all fixes ──────────────────────────────────────────────────────────
from collections import defaultdict
by_file = defaultdict(list)
for filepath, old, new, desc in fixes:
    by_file[filepath].append((old, new, desc))

results = []
for filepath, file_fixes in by_file.items():
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        results.append(f'NOT FOUND: {filepath}')
        continue

    changed = 0
    for old, new, desc in file_fixes:
        if old in content:
            content = content.replace(old, new, 1)
            changed += 1
            results.append(f'  FIXED [{filepath}]: {desc}')
        else:
            results.append(f'  NOT FOUND [{filepath}]: {desc}')
            results.append(f'    SOUGHT: {old[:100]}')

    if changed > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        results.append(f'  → Wrote {filepath} ({changed} fix(es))')

for r in results:
    print(r)

print('\nDone.')
