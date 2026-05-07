#!/usr/bin/env python3
"""
Create 6 T5 family records: {T5HE, T5HO} × {UL-A, UL-A+B, UL-B}
Update each SKU's family slug to match.
"""
import json
from collections import defaultdict

with open('src/data/sku-index.json') as f:
    data = json.load(f)

ta = data['collections']['tubulararch']
skus = ta['skus']
families = ta['families']

# Remove old t5-* family records
families = [f for f in families if not f['family'].startswith('t5')]

# Build new family records
combos = defaultdict(list)
for sku in skus:
    fam = sku.get('family', '')
    if not fam.startswith('t5'):
        continue
    sub = sku.get('sub_category', '')
    echelon = sku.get('display_echelon', '')
    combos[(sub, echelon)].append(sku)

# Slug map: (sub_category, echelon) → family slug
slug_map = {
    ('T5HE', 'UL-A'):   't5-he-k5',
    ('T5HE', 'UL-A+B'): 't5-he-u5',
    ('T5HE', 'UL-B'):   't5-he-de5',
    ('T5HO', 'UL-A'):   't5-ho-k5',
    ('T5HO', 'UL-A+B'): 't5-ho-u5',
    ('T5HO', 'UL-B'):   't5-ho-de5',
}

# Update SKU family slugs
for sku in skus:
    fam = sku.get('family', '')
    if not fam.startswith('t5'):
        continue
    sub = sku.get('sub_category', '')
    echelon = sku.get('display_echelon', '')
    new_slug = slug_map.get((sub, echelon))
    if new_slug:
        sku['family'] = new_slug

# Create family records
max_watts = {
    ('T5HE', 'UL-A'):   24,
    ('T5HE', 'UL-A+B'): 15,
    ('T5HE', 'UL-B'):   15,
    ('T5HO', 'UL-A'):   24,
    ('T5HO', 'UL-A+B'): 24,
    ('T5HO', 'UL-B'):   24,
}

for (sub, echelon), sku_list in sorted(combos.items()):
    slug = slug_map[(sub, echelon)]
    families.append({
        "family": slug,
        "sub_category": sub,
        "display_echelon": echelon,
        "max_wattage": max_watts.get((sub, echelon), 24),
        "sku_count": len(sku_list),
        "dlc": False,
        "ccts": [],
        "voltages": [],
        "mount_types": [],
        "taa": False,
        "comingSoon": False
    })

ta['families'] = families
ta['skus'] = skus

with open('src/data/sku-index.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Done. T5 families:")
for fam in families:
    if fam['family'].startswith('t5'):
        print(f"  {fam['family']} | sub_category: {fam['sub_category']} | echelon: {fam['display_echelon']} | sku_count: {fam['sku_count']}")

print("\nAll families:")
for fam in families:
    print(f"  {fam['family']} | sub_category: {fam['sub_category']} | echelon: {fam['display_echelon']}")
