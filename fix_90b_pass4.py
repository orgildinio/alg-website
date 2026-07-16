#!/usr/bin/env python3
"""
#90b pass-4 authored fixes — 2 remaining photo-stat-sub CFG-RBT-2 hits.
The quote characters in the sought strings are curly/smart quotes, not straight.
"""

fixes = []

def fix(filepath, old, new, description):
    fixes.append((filepath, old, new, description))

# ── Astra L5671: photo-stat-sub CFG-RBT-2 ───────────────────────────────────
# Exact string uses \u2014 em-dash and \u201c/\u201d curly quotes
fix('public/products/astra/index.html',
    '<strong>DLC tier verification pending</strong> via Rebate Center per CFG-RBT-2 \u2014 SellSheet shows \u201cDLC LISTED\u201d badge but datasheet is silent on tier; the published efficacy numbers (95-100 LM/W on DMS1830/3050) clear the DLC Listed floor and approach Premium-tier.',
    '<strong>DLC tier verification pending</strong> \u2014 published efficacy (95-100 LM/W on DMS1830/3050) clears the DLC Listed floor and approaches Premium-tier.',
    'Astra photo-stat-sub: remove CFG-RBT-2 rule citation')

# ── Solstice L4985: photo-stat-sub CFG-RBT-2 ────────────────────────────────
# Exact string uses &quot; HTML entity and \u2014 em-dash
fix('public/products/solstice/index.html',
    '<strong>DLC tier verification pending</strong> via Rebate Center per CFG-RBT-2 (datasheet does not commit to DLC Premium \u00b7 the published efficacy numbers \u2014 100-110 LM/W on the 6&quot; \u2014 clear the DLC Listed floor and approach Premium-tier).',
    '<strong>DLC tier verification pending</strong> (published efficacy 100-110 LM/W on the 6&quot; clears the DLC Listed floor and approaches Premium-tier).',
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
