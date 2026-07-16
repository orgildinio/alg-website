#!/usr/bin/env python3
"""
#90b pass-3 authored fixes — remaining rendered CFG-RBT-2 and § hits found in sweep.
All fixes: remove the rule citation, keep the factual claim.
"""

fixes = []

def fix(filepath, old, new, description):
    fixes.append((filepath, old, new, description))

# ── Astra L5671: photo-stat-sub CFG-RBT-2 ───────────────────────────────────
fix('public/products/astra/index.html',
    '<strong>DLC tier verification pending</strong> via Rebate Center per CFG-RBT-2 \u2014 SellSheet shows \u201cDLC LISTED\u201d badge but datasheet is silent on tier; the published efficacy numbers (95-100 LM/W on DMS1830/3050) clear the DLC Listed floor and approach Premium-tier.',
    '<strong>DLC tier verification pending</strong> \u2014 SellSheet shows \u201cDLC LISTED\u201d badge; the published efficacy numbers (95-100 LM/W on DMS1830/3050) clear the DLC Listed floor and approach Premium-tier.',
    'Astra photo-stat-sub: remove CFG-RBT-2 rule citation')

# ── Astra L6263: compliance cell CFG-RBT-2 ──────────────────────────────────
fix('public/products/astra/index.html',
    ' \u00b7 DLC tier verification pending Rebate Center per CFG-RBT-2',
    '',
    'Astra compliance cell: remove CFG-RBT-2 rule citation')

# ── Astra L6744: rebate paragraph CFG-RBT-2 and Title 24 § 130.1 ────────────
# "§ 130.1" here is a California Title 24 code section — this is a real external
# regulatory reference, NOT an internal section number. Keep it.
# Only remove the CFG-RBT-2 reference.
fix('public/products/astra/index.html',
    '(verification pending Rebate Center search per CFG-RBT-2 \u00b7 published 95-100 LM/W efficacy clears the DLC Listed floor and approaches Premium)',
    '(published 95-100 LM/W efficacy clears the DLC Listed floor and approaches Premium)',
    'Astra rebate paragraph: remove CFG-RBT-2 rule citation')

# ── Luxmark L7010: rebate paragraph CFG-RBT-2 ───────────────────────────────
# "(DLC Premium tier verification per CFG-RBT-2 pending Rebate Center search.)"
# Title 24 § 130.1 here is a real external code ref — keep it.
fix('public/products/luxmark/index.html',
    ' <em>(DLC Premium tier verification per CFG-RBT-2 pending Rebate Center search.)</em>',
    '',
    'Luxmark rebate paragraph: remove CFG-RBT-2 rule citation parenthetical')

# ── Spectra L4525: spec-table-foot CFG-RBT-2 and §6 / §13 refs ──────────────
# The spec-table-foot has multiple internal refs:
# "§6 Photometrics will populate..." → "the Photometrics section will populate..."
# "knowledge pack §13" → remove that clause
# "per CFG-RBT-2" → remove
fix('public/products/spectra/index.html',
    '\u00a76 Photometrics will populate with real polar plots once delivered.',
    'the Photometrics section will populate with real polar plots once delivered.',
    'Spectra spec-table-foot: remove §6 internal section ref')

fix('public/products/spectra/index.html',
    ' (datasheet body \u00b7 marketing collateral inconsistency on page 1 tru\u24b6COLOR chip flagged in knowledge pack \u00a713).',
    '.',
    'Spectra spec-table-foot: remove knowledge pack §13 internal note')

fix('public/products/spectra/index.html',
    ' \u00b7 DLC tier verification pending Rebate Center per CFG-RBT-2.',
    '.',
    'Spectra spec-table-foot: remove CFG-RBT-2 rule citation')

# ── Spectra L4610/4664/4718: SVG text §6 ref ─────────────────────────────────
# Three identical SVG text elements: "◇ IES bundle PENDING (James 2026-05-09: target next week) · §6 polar plots will populate when delivered"
# Rewrite: remove §6 ref
fix('public/products/spectra/index.html',
    '\u25c7 IES bundle PENDING (James 2026-05-09: target next week) \u00b7 \u00a76 polar plots will populate when delivered',
    '\u25c7 IES bundle PENDING \u00b7 polar plots will populate when delivered',
    'Spectra IES pending SVG text: remove §6 internal section ref (first instance)')

# The replace above only hits the first instance; run for all 3
# We'll use a loop in the apply section below

# ── Spectra L6006: compliance cell CFG-RBT-2 (second pass didn't catch it) ───
# Already confirmed full text ends with: · DLC tier verification pending Rebate Center per CFG-RBT-2
# This was the pass-2 fix target — re-check if it was applied
# (If already applied, this will be NOT FOUND — harmless)
fix('public/products/spectra/index.html',
    ' \u00b7 DLC tier verification pending Rebate Center per CFG-RBT-2',
    '',
    'Spectra compliance cell: remove CFG-RBT-2 rule citation (re-check)')

# ── Solstice L4985: photo-stat-sub CFG-RBT-2 ────────────────────────────────
fix('public/products/solstice/index.html',
    '<strong>DLC tier verification pending</strong> via Rebate Center per CFG-RBT-2 (datasheet does not commit to DLC Premium \u00b7 the published efficacy numbers \u2014 100-110 LM/W on the 6\u201d \u2014 clear the DLC Listed floor and approach Premium-tier).',
    '<strong>DLC tier verification pending</strong> (published efficacy 100-110 LM/W on the 6\u201d clears the DLC Listed floor and approaches Premium-tier).',
    'Solstice photo-stat-sub: remove CFG-RBT-2 rule citation')

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
            # Replace ALL occurrences for the SVG text (3 identical lines)
            count = content.count(old)
            content = content.replace(old, new)
            changed += count
            results.append(f'  FIXED x{count} [{filepath}]: {desc}')
        else:
            results.append(f'  NOT FOUND [{filepath}]: {desc}')
            results.append(f'    SOUGHT: {old[:120]}')

    if changed > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        results.append(f'  \u2192 Wrote {filepath} ({changed} fix(es))')

for r in results:
    print(r)

print('\nDone.')
