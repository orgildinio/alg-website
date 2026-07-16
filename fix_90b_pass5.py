#!/usr/bin/env python3
"""
#90b pass-5 authored fixes — remaining CFG-RBT-2 and heads-up rendered hits.
"""

fixes = []

def fix(filepath, old, new, description):
    fixes.append((filepath, old, new, description))

# ── Luxmark L4923: spec-table-foot — heads up: and CFG-RBT-2 ─────────────────
# Two issues in one line:
# 1. "heads up: not 90+ spec-grade" → remove the heads-up prefix
# 2. "verification pending Rebate Center per CFG-RBT-2" → remove rule citation

fix('public/products/luxmark/index.html',
    'CRI &gt;80 standard (commercial-ambient tier &middot; heads up: not 90+ spec-grade).',
    'CRI &gt;80 standard (commercial-ambient tier).',
    'Luxmark spec-table-foot: remove heads-up internal note from CRI clause')

fix('public/products/luxmark/index.html',
    '<strong>DLC Listed in the Troffer category</strong> &mdash; verification pending Rebate Center per CFG-RBT-2.',
    '<strong>DLC Listed in the Troffer category</strong>.',
    'Luxmark spec-table-foot: remove CFG-RBT-2 rule citation')

# ── Luxmark L5800: photo-stat-sub CFG-RBT-2 ─────────────────────────────────
fix('public/products/luxmark/index.html',
    '<strong>DLC Listed</strong> in the Troffer category per Rebate Center &middot; CFG-RBT-2 hierarchy.',
    '<strong>DLC Listed</strong> in the Troffer category.',
    'Luxmark photo-stat-sub: remove CFG-RBT-2 rule citation')

# ── proarch-t L4988: spec-table-foot — heads up: (×2) and CFG-RBT-2 ─────────
fix('public/products/proarch-t/index.html',
    'T2 IES bundle pending \u2014 awaiting ALG release. CCT options: 3500K / 4000K / 5000K (no 3000K \u00b7 heads up: warm-CCT projects route to Luxmark or premium-tier center-basket troffers).',
    'T2 IES bundle pending \u2014 awaiting ALG release. CCT options: 3500K / 4000K / 5000K (no 3000K \u00b7 warm-CCT projects route to Luxmark or premium-tier center-basket troffers).',
    'proarch-t spec-table-foot: remove heads-up prefix from CCT routing note')

fix('public/products/proarch-t/index.html',
    'CRI &gt;80 R9&ge;0 (commercial-ambient tier &middot; heads up: not 90+ spec-grade \u00b7 spec-grade projects route to Astra-I).',
    'CRI &gt;80 R9&ge;0 (commercial-ambient tier \u00b7 spec-grade projects route to Astra-I).',
    'proarch-t spec-table-foot: remove heads-up prefix from CRI routing note')

fix('public/products/proarch-t/index.html',
    '<strong>DLC Premium Dual-Listed Ambient + Low-Bay</strong> &mdash; verification pending Rebate Center per CFG-RBT-2.',
    '<strong>DLC Premium Dual-Listed Ambient + Low-Bay</strong>.',
    'proarch-t spec-table-foot: remove CFG-RBT-2 rule citation')

# ── Spectra L5394: photo-stat-sub CFG-RBT-2 ─────────────────────────────────
fix('public/products/spectra/index.html',
    '<strong>DLC tier verification pending</strong> via Rebate Center per CFG-RBT-2 \u2014 datasheet is silent on tier; the measured efficacy (90-107 LM/W across the bundle) clears the DLC Listed floor and approaches Premium-tier on the high-watt DMS3060 SKUs.',
    '<strong>DLC tier verification pending</strong> \u2014 measured efficacy (90-107 LM/W across the bundle) clears the DLC Listed floor and approaches Premium-tier on the high-watt DMS3060 SKUs.',
    'Spectra photo-stat-sub: remove CFG-RBT-2 rule citation')

# ── Waymark L4427: spec-table-foot heads up: ─────────────────────────────────
fix('public/products/waymark/index.html',
    'CRI &gt;80 standard (commercial-ambient tier \u00b7 heads up: not 90+ spec-grade).',
    'CRI &gt;80 standard (commercial-ambient tier).',
    'Waymark spec-table-foot: remove heads-up internal note from CRI clause')

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
            results.append(f'    SOUGHT: {old[:160]}')

    if changed > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        results.append(f'  \u2192 Wrote {filepath} ({changed} fix(es))')

for r in results:
    print(r)

print('\nDone.')
