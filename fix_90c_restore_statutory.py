#!/usr/bin/env python3
"""
#90c: Restore § in statutory/code citations only.
fce1104 overshot — restore exactly the statutory rows from the #90b-addendum
before/after table. Internal §N refs stay banned.

Statutory patterns to restore:
  - Title 24 130.1 → Title 24 § 130.1  (all variants)
  - Title 24 140.7 → Title 24 §140.7   (spectra hero, no space before number)
  - ASHRAE 90.1 Section 9.4 → ASHRAE 90.1 § 9.4
  - IBC Section 711 → IBC § 711
  - 19 USC 2511 → 19 USC § 2511
"""

fixes = []

def fix(filepath, old, new, description):
    fixes.append((filepath, old, new, description))

# ══════════════════════════════════════════════════════════════════════════════
# Title 24 130.1 → Title 24 § 130.1
# ══════════════════════════════════════════════════════════════════════════════

# astra — 4 instances
fix('public/products/astra/index.html',
    'DLC NLC qualified \u00b7 Title 24 130.1',
    'DLC NLC qualified \u00b7 Title 24 \u00a7 130.1',
    'astra SVG text')

fix('public/products/astra/index.html',
    '<strong>DLC NLC-qualified</strong> for the Title 24 130.1 networked lighting control rebate adder.',
    '<strong>DLC NLC-qualified</strong> for Title 24 \u00a7 130.1 networked lighting control rebate adder.',
    'astra controls paragraph')

fix('public/products/astra/index.html',
    '<strong>DLC NLC-qualified</strong> for the Title 24 130.1 rebate adder.',
    '<strong>DLC NLC-qualified</strong> for the Title 24 \u00a7 130.1 rebate adder.',
    'astra closing paragraph')

fix('public/products/astra/index.html',
    'qualify for the Title 24 130.1 NLC rebate adder',
    'qualify for the Title 24 \u00a7 130.1 NLC rebate adder',
    'astra rebate paragraph')

# lara — 2 instances
fix('public/products/lara/index.html',
    '<strong>DLC NLC-qualified</strong> for Title 24 130.1 occupancy-reduction compliance.',
    '<strong>DLC NLC-qualified</strong> for Title 24 \u00a7 130.1 occupancy-reduction compliance.',
    'lara controls paragraph')

fix('public/products/lara/index.html',
    '<strong>DLC NLC-qualified</strong> for Title 24 130.1 rebate adders.',
    '<strong>DLC NLC-qualified</strong> for Title 24 \u00a7 130.1 rebate adders.',
    'lara closing paragraph')

# luna — 2 instances
fix('public/products/luna/index.html',
    '<strong>DLC NLC-qualified</strong> for Title 24 130.1.',
    '<strong>DLC NLC-qualified</strong> for Title 24 \u00a7 130.1.',
    'luna controls paragraph')

fix('public/products/luna/index.html',
    '<strong>DLC NLC-qualified</strong> for the Title 24 130.1 rebate adder.',
    '<strong>DLC NLC-qualified</strong> for the Title 24 \u00a7 130.1 rebate adder.',
    'luna closing paragraph')

# luxmark — 1 instance (was &sect; HTML entity, restore as § unicode for consistency)
fix('public/products/luxmark/index.html',
    'qualify for the Title 24 130.1 NLC rebate adder',
    'qualify for the Title 24 \u00a7 130.1 NLC rebate adder',
    'luxmark rebate paragraph')

# proarch — 5 instances (includes "Title 24 Part 6 § 130.1")
fix('public/products/proarch/index.html',
    'Title 24 Part 6 130.1 networked lighting controls (NLC) via the /SR port',
    'Title 24 Part 6 \u00a7 130.1 networked lighting controls (NLC) via the /SR port',
    'proarch controls paragraph — Title 24 Part 6')

fix('public/products/proarch/index.html',
    'Drop-in compliance for ASHRAE 90.1 Section 9.4 and Title 24 Part 6 130.1 occupancy reduction requirements.',
    'Drop-in compliance for ASHRAE 90.1 \u00a7 9.4 and Title 24 Part 6 \u00a7 130.1 occupancy reduction requirements.',
    'proarch bi-level callout — both citations in one sentence')

fix('public/products/proarch/index.html',
    'DLC NLC-qualified for the Ambient envelope (Title 24 130.1)',
    'DLC NLC-qualified for the Ambient envelope (Title 24 \u00a7 130.1)',
    'proarch accessories paragraph')

fix('public/products/proarch/index.html',
    'DLC NLC qualified \u00b7 Title 24 Part 6 130.1 compliant',
    'DLC NLC qualified \u00b7 Title 24 Part 6 \u00a7 130.1 compliant',
    'proarch sensor card')

# retroarch-p1 — 3 instances (Title 24 only; TAA and anchor handled separately)
fix('public/products/retroarch-p1/index.html',
    'factory-locks for Title 24 130.1 + NYC LL97 compliance baked in at order.',
    'factory-locks for Title 24 \u00a7 130.1 + NYC LL97 compliance baked in at order.',
    'retroarch-p1 SKU paragraph')

fix('public/products/retroarch-p1/index.html',
    'CA TITLE 24 130.1 DIM-TO-OFF \u00b7 WAREHOUSE / PARKING / CORRIDOR LATE-NIGHT',
    'CA TITLE 24 \u00a7 130.1 DIM-TO-OFF \u00b7 WAREHOUSE / PARKING / CORRIDOR LATE-NIGHT',
    'retroarch-p1 dim-to-off SVG text')

fix('public/products/retroarch-p1/index.html',
    'Clears California Title 24 130.1 area-controls dim-to-off scenarios.',
    'Clears California Title 24 \u00a7 130.1 area-controls dim-to-off scenarios.',
    'retroarch-p1 dim-to-off paragraph')

fix('public/products/retroarch-p1/index.html',
    'All DLC NLC qualified for Title 24 130.1 rebate adders.',
    'All DLC NLC qualified for Title 24 \u00a7 130.1 rebate adders.',
    'retroarch-p1 controls paragraph')

# retroarch-p1/submittal — 1 instance
fix('public/products/retroarch-p1/submittal/index.html',
    'DLC NLC qualified for Title 24 130.1 rebate adder',
    'DLC NLC qualified for Title 24 \u00a7 130.1 rebate adder',
    'retroarch-p1 submittal')

# retroarch-t1 — 4 instances
fix('public/products/retroarch-t1/index.html',
    'factory-locks for Title 24 130.1 + NYC LL97 compliance baked in at order.',
    'factory-locks for Title 24 \u00a7 130.1 + NYC LL97 compliance baked in at order.',
    'retroarch-t1 SKU paragraph')

fix('public/products/retroarch-t1/index.html',
    'CA TITLE 24 130.1 DIM-TO-OFF \u00b7 WAREHOUSE / PARKING / CORRIDOR LATE-NIGHT',
    'CA TITLE 24 \u00a7 130.1 DIM-TO-OFF \u00b7 WAREHOUSE / PARKING / CORRIDOR LATE-NIGHT',
    'retroarch-t1 dim-to-off SVG text')

fix('public/products/retroarch-t1/index.html',
    'Clears California Title 24 130.1 area-controls dim-to-off scenarios.',
    'Clears California Title 24 \u00a7 130.1 area-controls dim-to-off scenarios.',
    'retroarch-t1 dim-to-off paragraph')

fix('public/products/retroarch-t1/index.html',
    'All DLC NLC qualified for Title 24 130.1 rebate adders.',
    'All DLC NLC qualified for Title 24 \u00a7 130.1 rebate adders.',
    'retroarch-t1 controls paragraph')

# solstice — 3 instances
fix('public/products/solstice/index.html',
    'DLC NLC qualified \u00b7 Title 24 130.1 networked lighting control rebate adder',
    'DLC NLC qualified \u00b7 Title 24 \u00a7 130.1 networked lighting control rebate adder',
    'solstice SVG text')

fix('public/products/solstice/index.html',
    'DLC NLC-qualified for Title 24 130.1.',
    'DLC NLC-qualified for Title 24 \u00a7 130.1.',
    'solstice controls paragraph')

fix('public/products/solstice/index.html',
    '<strong>DLC NLC-qualified</strong> for the Title 24 130.1 rebate adder.',
    '<strong>DLC NLC-qualified</strong> for the Title 24 \u00a7 130.1 rebate adder.',
    'solstice closing paragraph')

# solstice-safezone — 3 instances
fix('public/products/solstice-safezone/index.html',
    'DLC NLC qualified \u00b7 Title 24 130.1 networked lighting control rebate adder',
    'DLC NLC qualified \u00b7 Title 24 \u00a7 130.1 networked lighting control rebate adder',
    'solstice-safezone SVG text')

fix('public/products/solstice-safezone/index.html',
    'DLC NLC-qualified for Title 24 130.1.',
    'DLC NLC-qualified for Title 24 \u00a7 130.1.',
    'solstice-safezone controls paragraph')

fix('public/products/solstice-safezone/index.html',
    '<strong>DLC NLC-qualified</strong> for the Title 24 130.1 rebate adder.',
    '<strong>DLC NLC-qualified</strong> for the Title 24 \u00a7 130.1 rebate adder.',
    'solstice-safezone closing paragraph')

# spectra — 3 instances of § 130.1 + 1 of §140.7
fix('public/products/spectra/index.html',
    'Title 24 140.7 compliant.',
    'Title 24 \u00a7140.7 compliant.',
    'spectra hero description — §140.7 (no space)')

fix('public/products/spectra/index.html',
    'DLC NLC qualified \u00b7 Title 24 130.1',
    'DLC NLC qualified \u00b7 Title 24 \u00a7 130.1',
    'spectra SVG text')

fix('public/products/spectra/index.html',
    '<strong>DLC NLC-qualified</strong> for the Title 24 130.1 networked lighting control rebate adder.',
    '<strong>DLC NLC-qualified</strong> for Title 24 \u00a7 130.1 networked lighting control rebate adder.',
    'spectra controls paragraph')

fix('public/products/spectra/index.html',
    'qualify for the Title 24 130.1 NLC rebate adder',
    'qualify for the Title 24 \u00a7 130.1 NLC rebate adder',
    'spectra rebate paragraph')

# waymark — 1 instance
fix('public/products/waymark/index.html',
    'qualify for the Title 24 130.1 NLC rebate adder',
    'qualify for the Title 24 \u00a7 130.1 NLC rebate adder',
    'waymark rebate paragraph')

# ══════════════════════════════════════════════════════════════════════════════
# ASHRAE 90.1 Section 9.4 → ASHRAE 90.1 § 9.4
# ══════════════════════════════════════════════════════════════════════════════

# proarch — 1 standalone instance (the other was handled in the bi-level callout above)
fix('public/products/proarch/index.html',
    'ASHRAE 90.1 Section 9.4 occupancy / bi-level requirements via Bi-Level standalone',
    'ASHRAE 90.1 \u00a7 9.4 occupancy / bi-level requirements via Bi-Level standalone',
    'proarch controls paragraph — ASHRAE standalone')

# proarch-t/submittal
fix('public/products/proarch-t/submittal/index.html',
    'ASHRAE 90.1 Section 9.4 drop-in',
    'ASHRAE 90.1 \u00a7 9.4 drop-in',
    'proarch-t submittal')

# proarch/submittal
fix('public/products/proarch/submittal/index.html',
    'ASHRAE 90.1 Section 9.4 drop-in',
    'ASHRAE 90.1 \u00a7 9.4 drop-in',
    'proarch submittal')

# retroarch-t1/submittal
fix('public/products/retroarch-t1/submittal/index.html',
    'ASHRAE 90.1 Section 9.4 drop-in',
    'ASHRAE 90.1 \u00a7 9.4 drop-in',
    'retroarch-t1 submittal')

# ══════════════════════════════════════════════════════════════════════════════
# IBC Section 711 → IBC § 711
# ══════════════════════════════════════════════════════════════════════════════

fix('public/products/multi-family/radius-safezone/submittal/index.html',
    'IBC Section 711, NFPA 5000',
    'IBC \u00a7 711, NFPA 5000',
    'radius-safezone submittal')

# ══════════════════════════════════════════════════════════════════════════════
# 19 USC 2511 → 19 USC § 2511  (TAA SVG text)
# ══════════════════════════════════════════════════════════════════════════════

fix('public/products/retroarch-p1/index.html',
    '19 USC 2511 \u00b7 TAA-DESIGNATED',
    '19 USC \u00a7 2511 \u00b7 TAA-DESIGNATED',
    'retroarch-p1 TAA SVG text')

fix('public/products/retroarch-t1/index.html',
    '19 USC 2511 \u00b7 TAA-DESIGNATED',
    '19 USC \u00a7 2511 \u00b7 TAA-DESIGNATED',
    'retroarch-t1 TAA SVG text')

# ══════════════════════════════════════════════════════════════════════════════
# Apply all fixes
# ══════════════════════════════════════════════════════════════════════════════
from collections import defaultdict
by_file = defaultdict(list)
for filepath, old, new, desc in fixes:
    by_file[filepath].append((old, new, desc))

results = []
total_fixed = 0
for filepath, file_fixes in sorted(by_file.items()):
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
            total_fixed += 1
            results.append(f'  FIXED [{filepath}]: {desc}')
        else:
            results.append(f'  NOT FOUND [{filepath}]: {desc}')
            results.append(f'    SOUGHT: {old[:160]}')

    if changed > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        results.append(f'  \u2192 Wrote {filepath} ({changed} fix(es))')

for r in results:
    print(r)

print(f'\nTotal applied: {total_fixed} / {len(fixes)} attempted')
print('Done.')
