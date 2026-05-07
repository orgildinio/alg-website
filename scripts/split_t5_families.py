#!/usr/bin/env python3
"""
Split the single 't5' family record in tubulararch into 3 sub-families:
  - t5-de5  | sub_category: T5HE/T5HO (mixed) | display_echelon: UL-B   | DE5 Series
  - t5-u5   | sub_category: T5HE/T5HO (mixed) | display_echelon: UL-A+B | U5 Series
  - t5-k5   | sub_category: T5HE              | display_echelon: UL-A   | K5/K Series

Also fix DE5 SKU sub_categories from 'T5' to the correct T5HE/T5HO based on SKU name.

For the All Families filter: the T5 app tile should select both T5HE and T5HO.
We'll handle that in the component separately.
"""
import json, re

with open('src/data/sku-index.json') as f:
    data = json.load(f)

ta = data['collections']['tubulararch']
skus = ta['skus']
families = ta['families']

# Fix DE5 SKU sub_categories: 'T5' → T5HE or T5HO based on SKU name
for sku in skus:
    if sku.get('family') == 't5' and sku.get('sub_category') == 'T5':
        name = sku.get('sku', '')
        if 'T5HE' in name:
            sku['sub_category'] = 'T5HE'
        elif 'T5HO' in name:
            sku['sub_category'] = 'T5HO'

# Count SKUs per suffix group
de5_skus = [s for s in skus if s.get('family') == 't5' and 'DE5' in s.get('sku', '')]
u5_skus  = [s for s in skus if s.get('family') == 't5' and ('U5' in s.get('sku', '') or s.get('display_echelon') == 'UL-A+B')]
k5_skus  = [s for s in skus if s.get('family') == 't5' and s.get('display_echelon') == 'UL-A']

print(f'DE5 SKUs: {len(de5_skus)}, U5 SKUs: {len(u5_skus)}, K5 SKUs: {len(k5_skus)}')

# Update family slugs in SKUs
for sku in skus:
    if sku.get('family') != 't5':
        continue
    echelon = sku.get('display_echelon', '')
    sku_name = sku.get('sku', '')
    if 'DE5' in sku_name:
        sku['family'] = 't5-de5'
    elif echelon == 'UL-A+B':
        sku['family'] = 't5-u5'
    elif echelon == 'UL-A':
        sku['family'] = 't5-k5'

# Remove old t5 family record, add 3 new ones
families = [f for f in families if f['family'] != 't5']

families.append({
    "family": "t5-de5",
    "sub_category": "T5HE · T5HO",
    "display_echelon": "UL-B",
    "max_wattage": 24,
    "sku_count": len(de5_skus),
    "dlc": False,
    "ccts": [],
    "voltages": [],
    "mount_types": [],
    "taa": False,
    "comingSoon": False
})

families.append({
    "family": "t5-u5",
    "sub_category": "T5HE · T5HO",
    "display_echelon": "UL-A+B",
    "max_wattage": 24,
    "sku_count": len(u5_skus),
    "dlc": False,
    "ccts": [],
    "voltages": [],
    "mount_types": [],
    "taa": False,
    "comingSoon": False
})

families.append({
    "family": "t5-k5",
    "sub_category": "T5HE",
    "display_echelon": "UL-A",
    "max_wattage": 24,
    "sku_count": len(k5_skus),
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

print("Done. New families:")
for fam in ta['families']:
    print(f"  {fam['family']} | sub_category: {fam['sub_category']} | echelon: {fam['display_echelon']} | sku_count: {fam['sku_count']}")
