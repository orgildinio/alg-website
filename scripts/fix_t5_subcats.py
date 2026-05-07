#!/usr/bin/env python3
"""
Fix T5 sub-family sub_categories so filter checkboxes show T5HE / T5HO properly.
- t5-de5: has both T5HE and T5HO SKUs → keep two separate family records:
    t5-de5-he (T5HE, UL-B) and t5-de5-ho (T5HO, UL-B)
- t5-u5: has both T5HE and T5HO SKUs → two records:
    t5-u5-he (T5HE, UL-A+B) and t5-u5-ho (T5HO, UL-A+B)
- t5-k5: only T5HE → one record: t5-k5 (T5HE, UL-A)

Actually, simpler: just give each family the most representative sub_category
and let the T5 app-tile click select BOTH T5HE and T5HO.

Strategy:
- t5-de5 → sub_category: "T5HE" (primary) but also add a t5-de5-ho for T5HO DE5 SKUs
- Actually: split into t5-he (all T5HE across all series) and t5-ho (all T5HO across all series)
  grouped by echelon. But that's complex.

Simplest correct approach:
- Create 6 family records: {T5HE, T5HO} × {UL-A, UL-A+B, UL-B}
- Each family card shows the right sub_category and echelon badge
- T5 app tile selects both T5HE and T5HO

Let's count SKUs per (sub_category, echelon) combo:
"""
import json

with open('src/data/sku-index.json') as f:
    data = json.load(f)

ta = data['collections']['tubulararch']
skus = ta['skus']

# Count per (sub_category, echelon)
from collections import defaultdict
counts = defaultdict(int)
for sku in skus:
    fam = sku.get('family', '')
    if not fam.startswith('t5'):
        continue
    sub = sku.get('sub_category', '')
    echelon = sku.get('display_echelon', '')
    counts[(sub, echelon)] += 1

print("SKU counts per (sub_category, echelon):")
for k, v in sorted(counts.items()):
    print(f"  {k}: {v}")
