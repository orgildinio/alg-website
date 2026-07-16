#!/usr/bin/env python3
"""
#90b pass-2 authored fixes — exact strings confirmed from file reads.
Applies the 6 remaining NOT FOUND items (2 were already clean/in comments).
"""

fixes = []

def fix(filepath, old, new, description):
    fixes.append((filepath, old, new, description))

# ── 1. Spectra L5990: CRI cell internal note ─────────────────────────────────
# Remove the entire span with the internal note, leaving "80+ standard"
fix('public/products/spectra/index.html',
    ' <span style="color:var(--text-muted);font-size:11px;">(NOT 90+ \u00b7 datasheet body wins \u00b7 pg 1 tru<span class="aa">\u24b6</span>COLOR chip is a marketing inconsistency \u00b7 KP \u00a713)</span>',
    '',
    'Spectra CRI cell: remove internal note span (NOT 90+ · KP §13)')

# ── 2. Spectra L6006: compliance cell CFG-RBT-2 note ─────────────────────────
# Remove " · DLC tier verification pending Rebate Center per CFG-RBT-2" from end
fix('public/products/spectra/index.html',
    ' \u00b7 DLC tier verification pending Rebate Center per CFG-RBT-2',
    '',
    'Spectra compliance cell: remove CFG-RBT-2 rule citation')

# ── 3. Waymark L5337: photo-stat-sub CFG-RBT-2 reference ─────────────────────
# Remove " · CFG-RBT-2 hierarchy" from the DLC Listed sentence
fix('public/products/waymark/index.html',
    ' \u00b7 CFG-RBT-2 hierarchy',
    '',
    'Waymark photo-stat-sub: remove CFG-RBT-2 rule citation')

# ── 4. retroarch-t1 L4421: LPVR sentence "heads up:" ─────────────────────────
# Current: "...No drywall patch.</strong> heads up: <strong>door-kit install requires an existing troffer housing</strong> (GT8/2GT8/equivalent fluorescent troffer frame with ceiling cutout + J-Box). Won't work in unimproved ceilings &mdash; spec Luxmark (new-construction center-basket troffer) for that brief."
# Rewrite: remove "heads up:" prefix, keep the factual content
fix('public/products/retroarch-t1/index.html',
    ' heads up: <strong>door-kit install requires an existing troffer housing</strong>',
    ' <strong>Door-kit install requires an existing troffer housing</strong>',
    'retroarch-t1 LPVR: remove heads-up prefix, capitalize sentence start')

# ── 5. Trackstar L6321: rebate sentence §11 planoⒶRCH -tier ─────────────────
# Current: "Pair with the §11 plano<span class="aa">Ⓐ</span>RCH -tier networked lighting control family for a coherent rebate-eligible package across the install."
# Rewrite: remove §11 and orphaned "-tier" fragment
fix('public/products/trackstar/index.html',
    'Pair with the \u00a711 plano<span class="aa">\u24b6</span>RCH -tier networked lighting control family for a coherent rebate-eligible package across the install.',
    'Pair with the plano<span class="aa">\u24b6</span>RCH networked lighting control family for a coherent rebate-eligible package across the install.',
    'Trackstar nit 1: remove §11 internal section ref and orphaned -tier fragment from rebate copy')

# ── 6. Trackstar L6068: family-card tier badge ECO → PRO ─────────────────────
# Current: <span class="tier-badge tier-eco" style="margin-left:auto;">ECO</span>
# Fix: change class and label to PRO
fix('public/products/trackstar/index.html',
    '<span class="tier-badge tier-eco" style="margin-left:auto;">ECO</span>',
    '<span class="tier-badge tier-pro" style="margin-left:auto;">PRO</span>',
    'Trackstar nit 2: family-card tier badge ECO → PRO (matches H1, meta, and family-card-tag)')

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
            results.append(f'    SOUGHT: {old[:120]}')

    if changed > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        results.append(f'  → Wrote {filepath} ({changed} fix(es))')

for r in results:
    print(r)

print('\nDone.')
