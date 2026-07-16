#!/usr/bin/env python3
"""
#90b addendum: § symbol purge from all rendered copy, site-wide.
45 hits across 19 files. Every § replaced with plain English.
Rule: § banned from all customer-facing rendered copy. Code comments exempt.
"""

fixes = []

def fix(filepath, old, new, description):
    fixes.append((filepath, old, new, description))

# ══════════════════════════════════════════════════════════════════════════════
# astra/index.html — 4 hits
# ══════════════════════════════════════════════════════════════════════════════

# L5446: SVG text "Title 24 § 130.1"
fix('public/products/astra/index.html',
    'DLC NLC qualified \u00b7 Title 24 \u00a7 130.1',
    'DLC NLC qualified \u00b7 Title 24 130.1',
    'astra SVG text: § 130.1 → 130.1')

# L5452: paragraph "Title 24 § 130.1 networked lighting control rebate adder"
fix('public/products/astra/index.html',
    '<strong>DLC NLC-qualified</strong> for Title 24 \u00a7 130.1 networked lighting control rebate adder.',
    '<strong>DLC NLC-qualified</strong> for the Title 24 130.1 networked lighting control rebate adder.',
    'astra controls paragraph: § 130.1 → 130.1')

# L5523: paragraph "Title 24 § 130.1 rebate adder"
fix('public/products/astra/index.html',
    '<strong>DLC NLC-qualified</strong> for the Title 24 \u00a7 130.1 rebate adder.',
    '<strong>DLC NLC-qualified</strong> for the Title 24 130.1 rebate adder.',
    'astra closing controls paragraph: § 130.1 → 130.1')

# L6744: rebate paragraph "Title 24 § 130.1 NLC rebate adder"
fix('public/products/astra/index.html',
    'qualify for the Title 24 \u00a7 130.1 NLC rebate adder',
    'qualify for the Title 24 130.1 NLC rebate adder',
    'astra rebate paragraph: § 130.1 → 130.1')

# ══════════════════════════════════════════════════════════════════════════════
# lara/index.html — 2 hits
# ══════════════════════════════════════════════════════════════════════════════

# L4134
fix('public/products/lara/index.html',
    '<strong>DLC NLC-qualified</strong> for Title 24 \u00a7 130.1 occupancy-reduction compliance.',
    '<strong>DLC NLC-qualified</strong> for Title 24 130.1 occupancy-reduction compliance.',
    'lara controls paragraph: § 130.1 → 130.1')

# L4193
fix('public/products/lara/index.html',
    '<strong>DLC NLC-qualified</strong> for Title 24 \u00a7 130.1 rebate adders.',
    '<strong>DLC NLC-qualified</strong> for Title 24 130.1 rebate adders.',
    'lara closing paragraph: § 130.1 → 130.1')

# ══════════════════════════════════════════════════════════════════════════════
# lptp-symmetry-post-top/submittal/index.html — 1 hit
# ══════════════════════════════════════════════════════════════════════════════

fix('public/products/lptp-symmetry-post-top/submittal/index.html',
    'Per-cell .ies bundle linked from \u00a76 Photometrics',
    'Per-cell .ies bundle linked from the Photometrics section',
    'lptp-symmetry submittal: §6 → the Photometrics section')

# ══════════════════════════════════════════════════════════════════════════════
# lptp-unity-post-top/submittal/index.html — 1 hit
# ══════════════════════════════════════════════════════════════════════════════

fix('public/products/lptp-unity-post-top/submittal/index.html',
    'Per-cell .ies bundle linked from \u00a76 Photometrics',
    'Per-cell .ies bundle linked from the Photometrics section',
    'lptp-unity submittal: §6 → the Photometrics section')

# ══════════════════════════════════════════════════════════════════════════════
# luna/index.html — 2 hits
# ══════════════════════════════════════════════════════════════════════════════

# L4581
fix('public/products/luna/index.html',
    '<strong>DLC NLC-qualified</strong> for Title 24 \u00a7 130.1.',
    '<strong>DLC NLC-qualified</strong> for Title 24 130.1.',
    'luna controls paragraph: § 130.1 → 130.1')

# L4657
fix('public/products/luna/index.html',
    '<strong>DLC NLC-qualified</strong> for the Title 24 \u00a7 130.1 rebate adder.',
    '<strong>DLC NLC-qualified</strong> for the Title 24 130.1 rebate adder.',
    'luna closing paragraph: § 130.1 → 130.1')

# ══════════════════════════════════════════════════════════════════════════════
# luna/submittal/index.html — 2 hits
# ══════════════════════════════════════════════════════════════════════════════

# L886: "PDP §6 Photometrics card"
fix('public/products/luna/submittal/index.html',
    'ships from WorkDrive (link on the PDP \u00a76 Photometrics card).',
    'ships from WorkDrive (link on the Photometrics section of the product page).',
    'luna submittal: §6 Photometrics card → Photometrics section of the product page')

# L1007: "configured in §9 of the product page"
fix('public/products/luna/submittal/index.html',
    'in the LUNA SKU above; this BOM lists only the optional add-ons configured in &sect;9 of the product page.',
    'in the LUNA SKU above; this BOM lists only the optional add-ons configured in the Configurator on the product page.',
    'luna submittal: &sect;9 → the Configurator on the product page')

# ══════════════════════════════════════════════════════════════════════════════
# luxmark/index.html — 1 hit (uses &sect; HTML entity)
# ══════════════════════════════════════════════════════════════════════════════

fix('public/products/luxmark/index.html',
    'qualify for the Title 24 &sect; 130.1 NLC rebate adder',
    'qualify for the Title 24 130.1 NLC rebate adder',
    'luxmark rebate paragraph: &sect; 130.1 → 130.1')

# ══════════════════════════════════════════════════════════════════════════════
# multi-family/radius-safezone/submittal/index.html — 1 hit
# ══════════════════════════════════════════════════════════════════════════════

fix('public/products/multi-family/radius-safezone/submittal/index.html',
    'authority-having-jurisdiction (AHJ) submittal acceptance across IBC \u00a7 711, NFPA 5000, and most state codes',
    'authority-having-jurisdiction (AHJ) submittal acceptance across IBC Section 711, NFPA 5000, and most state codes',
    'radius-safezone submittal: IBC § 711 → IBC Section 711')

# ══════════════════════════════════════════════════════════════════════════════
# proarch-t/submittal/index.html — 1 hit
# ══════════════════════════════════════════════════════════════════════════════

fix('public/products/proarch-t/submittal/index.html',
    'ASHRAE 90.1 \u00a7 9.4 drop-in',
    'ASHRAE 90.1 Section 9.4 drop-in',
    'proarch-t submittal: ASHRAE § 9.4 → Section 9.4')

# ══════════════════════════════════════════════════════════════════════════════
# proarch/index.html — 4 hits
# ══════════════════════════════════════════════════════════════════════════════

# L4329: two § refs in one sentence
fix('public/products/proarch/index.html',
    'Title 24 Part 6 \u00a7 130.1 networked lighting controls (NLC) via the /SR port',
    'Title 24 Part 6 130.1 networked lighting controls (NLC) via the /SR port',
    'proarch controls paragraph: § 130.1 → 130.1 (first instance)')

fix('public/products/proarch/index.html',
    'ASHRAE 90.1 \u00a7 9.4 occupancy / bi-level requirements via Bi-Level standalone',
    'ASHRAE 90.1 Section 9.4 occupancy / bi-level requirements via Bi-Level standalone',
    'proarch controls paragraph: ASHRAE § 9.4 → Section 9.4')

# L4346
fix('public/products/proarch/index.html',
    'Drop-in compliance for ASHRAE 90.1 \u00a7 9.4 and Title 24 Part 6 \u00a7 130.1 occupancy reduction requirements.',
    'Drop-in compliance for ASHRAE 90.1 Section 9.4 and Title 24 Part 6 130.1 occupancy reduction requirements.',
    'proarch bi-level callout: § 9.4 → Section 9.4 and § 130.1 → 130.1')

# L4464
fix('public/products/proarch/index.html',
    'DLC NLC-qualified for the Ambient envelope (Title 24 \u00a7 130.1)',
    'DLC NLC-qualified for the Ambient envelope (Title 24 130.1)',
    'proarch accessories paragraph: § 130.1 → 130.1')

# L5693
fix('public/products/proarch/index.html',
    'DLC NLC qualified \u00b7 Title 24 Part 6 \u00a7 130.1 compliant',
    'DLC NLC qualified \u00b7 Title 24 Part 6 130.1 compliant',
    'proarch sensor card: § 130.1 → 130.1')

# ══════════════════════════════════════════════════════════════════════════════
# proarch/submittal/index.html — 1 hit (uses &sect; HTML entity)
# ══════════════════════════════════════════════════════════════════════════════

fix('public/products/proarch/submittal/index.html',
    'ASHRAE 90.1 &sect; 9.4 drop-in',
    'ASHRAE 90.1 Section 9.4 drop-in',
    'proarch submittal: &sect; 9.4 → Section 9.4')

# ══════════════════════════════════════════════════════════════════════════════
# retroarch-p1/index.html — 6 hits
# ══════════════════════════════════════════════════════════════════════════════

# L4717: SVG text "19 USC § 2511"
fix('public/products/retroarch-p1/index.html',
    '19 USC \u00a7 2511 \u00b7 TAA-DESIGNATED',
    '19 USC 2511 \u00b7 TAA-DESIGNATED',
    'retroarch-p1 TAA SVG text: § 2511 → 2511')

# L4938: paragraph "Title 24 § 130.1 + NYC LL97"
fix('public/products/retroarch-p1/index.html',
    'factory-locks for Title 24 \u00a7 130.1 + NYC LL97 compliance baked in at order.',
    'factory-locks for Title 24 130.1 + NYC LL97 compliance baked in at order.',
    'retroarch-p1 SKU paragraph: § 130.1 → 130.1')

# L5146: SVG text "CA TITLE 24 § 130.1 DIM-TO-OFF"
fix('public/products/retroarch-p1/index.html',
    'CA TITLE 24 \u00a7 130.1 DIM-TO-OFF \u00b7 WAREHOUSE / PARKING / CORRIDOR LATE-NIGHT',
    'CA TITLE 24 130.1 DIM-TO-OFF \u00b7 WAREHOUSE / PARKING / CORRIDOR LATE-NIGHT',
    'retroarch-p1 dim-to-off SVG text: § 130.1 → 130.1')

# L5152: paragraph "California Title 24 § 130.1"
fix('public/products/retroarch-p1/index.html',
    'Clears California Title 24 \u00a7 130.1 area-controls dim-to-off scenarios.',
    'Clears California Title 24 130.1 area-controls dim-to-off scenarios.',
    'retroarch-p1 dim-to-off paragraph: § 130.1 → 130.1')

# L5288: paragraph "Title 24 § 130.1 rebate adders"
fix('public/products/retroarch-p1/index.html',
    'All DLC NLC qualified for Title 24 \u00a7 130.1 rebate adders.',
    'All DLC NLC qualified for Title 24 130.1 rebate adders.',
    'retroarch-p1 controls paragraph: § 130.1 → 130.1')

# L7000: anchor link &sect;4 in href text
fix('public/products/retroarch-p1/index.html',
    '(<a href="#highlights" style="color:#F32740;">&sect;4</a>)',
    '(<a href="#highlights" style="color:#F32740;">Highlights</a>)',
    'retroarch-p1 rebate paragraph: &sect;4 anchor → Highlights')

# ══════════════════════════════════════════════════════════════════════════════
# retroarch-p1/submittal/index.html — 1 hit (uses &sect; HTML entity)
# ══════════════════════════════════════════════════════════════════════════════

fix('public/products/retroarch-p1/submittal/index.html',
    'DLC NLC qualified for Title 24 &sect; 130.1 rebate adder',
    'DLC NLC qualified for Title 24 130.1 rebate adder',
    'retroarch-p1 submittal: &sect; 130.1 → 130.1')

# ══════════════════════════════════════════════════════════════════════════════
# retroarch-t1/index.html — 6 hits
# ══════════════════════════════════════════════════════════════════════════════

# L4722: SVG text "19 USC § 2511"
fix('public/products/retroarch-t1/index.html',
    '19 USC \u00a7 2511 \u00b7 TAA-DESIGNATED',
    '19 USC 2511 \u00b7 TAA-DESIGNATED',
    'retroarch-t1 TAA SVG text: § 2511 → 2511')

# L4943: paragraph "Title 24 § 130.1 + NYC LL97"
fix('public/products/retroarch-t1/index.html',
    'factory-locks for Title 24 \u00a7 130.1 + NYC LL97 compliance baked in at order.',
    'factory-locks for Title 24 130.1 + NYC LL97 compliance baked in at order.',
    'retroarch-t1 SKU paragraph: § 130.1 → 130.1')

# L5151: SVG text "CA TITLE 24 § 130.1 DIM-TO-OFF"
fix('public/products/retroarch-t1/index.html',
    'CA TITLE 24 \u00a7 130.1 DIM-TO-OFF \u00b7 WAREHOUSE / PARKING / CORRIDOR LATE-NIGHT',
    'CA TITLE 24 130.1 DIM-TO-OFF \u00b7 WAREHOUSE / PARKING / CORRIDOR LATE-NIGHT',
    'retroarch-t1 dim-to-off SVG text: § 130.1 → 130.1')

# L5157: paragraph "California Title 24 § 130.1"
fix('public/products/retroarch-t1/index.html',
    'Clears California Title 24 \u00a7 130.1 area-controls dim-to-off scenarios.',
    'Clears California Title 24 130.1 area-controls dim-to-off scenarios.',
    'retroarch-t1 dim-to-off paragraph: § 130.1 → 130.1')

# L5293: paragraph "Title 24 § 130.1 rebate adders"
fix('public/products/retroarch-t1/index.html',
    'All DLC NLC qualified for Title 24 \u00a7 130.1 rebate adders.',
    'All DLC NLC qualified for Title 24 130.1 rebate adders.',
    'retroarch-t1 controls paragraph: § 130.1 → 130.1')

# L6991: anchor link &sect;4 in href text
fix('public/products/retroarch-t1/index.html',
    '(<a href="#highlights" style="color:#F32740;">&sect;4</a>)',
    '(<a href="#highlights" style="color:#F32740;">Highlights</a>)',
    'retroarch-t1 rebate paragraph: &sect;4 anchor → Highlights')

# ══════════════════════════════════════════════════════════════════════════════
# retroarch-t1/submittal/index.html — 1 hit
# ══════════════════════════════════════════════════════════════════════════════

fix('public/products/retroarch-t1/submittal/index.html',
    'ASHRAE 90.1 \u00a7 9.4 drop-in',
    'ASHRAE 90.1 Section 9.4 drop-in',
    'retroarch-t1 submittal: ASHRAE § 9.4 → Section 9.4')

# ══════════════════════════════════════════════════════════════════════════════
# solstice-safezone/index.html — 3 hits
# ══════════════════════════════════════════════════════════════════════════════

# L4867: SVG text
fix('public/products/solstice-safezone/index.html',
    'DLC NLC qualified \u00b7 Title 24 \u00a7 130.1 networked lighting control rebate adder',
    'DLC NLC qualified \u00b7 Title 24 130.1 networked lighting control rebate adder',
    'solstice-safezone SVG text: § 130.1 → 130.1')

# L4873: paragraph
fix('public/products/solstice-safezone/index.html',
    'DLC NLC-qualified for Title 24 \u00a7 130.1.',
    'DLC NLC-qualified for Title 24 130.1.',
    'solstice-safezone controls paragraph: § 130.1 → 130.1')

# L4943: paragraph
fix('public/products/solstice-safezone/index.html',
    '<strong>DLC NLC-qualified</strong> for the Title 24 \u00a7 130.1 rebate adder.',
    '<strong>DLC NLC-qualified</strong> for the Title 24 130.1 rebate adder.',
    'solstice-safezone closing paragraph: § 130.1 → 130.1')

# ══════════════════════════════════════════════════════════════════════════════
# solstice/index.html — 3 hits
# ══════════════════════════════════════════════════════════════════════════════

# L4770: SVG text
fix('public/products/solstice/index.html',
    'DLC NLC qualified \u00b7 Title 24 \u00a7 130.1 networked lighting control rebate adder',
    'DLC NLC qualified \u00b7 Title 24 130.1 networked lighting control rebate adder',
    'solstice SVG text: § 130.1 → 130.1')

# L4776: paragraph
fix('public/products/solstice/index.html',
    'DLC NLC-qualified for Title 24 \u00a7 130.1.',
    'DLC NLC-qualified for Title 24 130.1.',
    'solstice controls paragraph: § 130.1 → 130.1')

# L4846: paragraph
fix('public/products/solstice/index.html',
    '<strong>DLC NLC-qualified</strong> for the Title 24 \u00a7 130.1 rebate adder.',
    '<strong>DLC NLC-qualified</strong> for the Title 24 130.1 rebate adder.',
    'solstice closing paragraph: § 130.1 → 130.1')

# ══════════════════════════════════════════════════════════════════════════════
# spectra/index.html — 4 hits
# ══════════════════════════════════════════════════════════════════════════════

# L4021: hero description "§140.7"
fix('public/products/spectra/index.html',
    'Title 24 \u00a7140.7 compliant.',
    'Title 24 140.7 compliant.',
    'spectra hero description: §140.7 → 140.7')

# L5160: SVG text
fix('public/products/spectra/index.html',
    'DLC NLC qualified \u00b7 Title 24 \u00a7 130.1',
    'DLC NLC qualified \u00b7 Title 24 130.1',
    'spectra SVG text: § 130.1 → 130.1')

# L5166: paragraph
fix('public/products/spectra/index.html',
    '<strong>DLC NLC-qualified</strong> for Title 24 \u00a7 130.1 networked lighting control rebate adder.',
    '<strong>DLC NLC-qualified</strong> for the Title 24 130.1 networked lighting control rebate adder.',
    'spectra controls paragraph: § 130.1 → 130.1')

# L6488: rebate paragraph
fix('public/products/spectra/index.html',
    'qualify for the Title 24 \u00a7 130.1 NLC rebate adder',
    'qualify for the Title 24 130.1 NLC rebate adder',
    'spectra rebate paragraph: § 130.1 → 130.1')

# ══════════════════════════════════════════════════════════════════════════════
# waymark/index.html — 1 hit (uses &sect; HTML entity)
# ══════════════════════════════════════════════════════════════════════════════

fix('public/products/waymark/index.html',
    'qualify for the Title 24 &sect; 130.1 NLC rebate adder',
    'qualify for the Title 24 130.1 NLC rebate adder',
    'waymark rebate paragraph: &sect; 130.1 → 130.1')

# ══════════════════════════════════════════════════════════════════════════════
# Apply all fixes
# ══════════════════════════════════════════════════════════════════════════════
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
        results.append(f'NOT FOUND FILE: {filepath}')
        continue

    changed = 0
    for old, new, desc in file_fixes:
        if old in content:
            content = content.replace(old, new, 1)
            changed += 1
            results.append(f'  FIXED [{filepath}]: {desc}')
        else:
            results.append(f'  NOT FOUND [{filepath}]: {desc}')
            results.append(f'    SOUGHT: {old[:140]}')

    if changed > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        results.append(f'  \u2192 Wrote {filepath} ({changed} fix(es))')

for r in results:
    print(r)

print(f'\nTotal fixes attempted: {len(fixes)}')
print('Done.')
