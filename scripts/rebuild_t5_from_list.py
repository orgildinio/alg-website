#!/usr/bin/env python3
"""
Rebuild T5 SKUs and families in sku-index.json from the authoritative list.
Groups:
  CSselect UL-A+B  → sub_category: T5HE or T5HO (per SKU), display_echelon: UL-A+B, family: t5-cs-u5
  CSselect UL-B    → sub_category: T5HE or T5HO (per SKU), display_echelon: UL-B,   family: t5-cs-de5
  T5HE UL-A+B      → sub_category: T5HE,                   display_echelon: UL-A+B, family: t5-he-u5
  T5HE UL-A        → sub_category: T5HE,                   display_echelon: UL-A,   family: t5-he-k5
  T5HO UL-A+B      → sub_category: T5HO,                   display_echelon: UL-A+B, family: t5-ho-u5
  T5HO UL-A        → sub_category: T5HO,                   display_echelon: UL-A,   family: t5-ho-k5
  T5HO UL-B        → sub_category: T5HO,                   display_echelon: UL-B,   family: t5-ho-de5
"""
import json

# Authoritative SKU list
# (sku_number, description, sub_category, display_echelon, family_slug)
T5_SKUS = [
    # CSselect UL-A+B
    ("LT5F2CS4/HE/U5",  "T5HE | 2FT | Type A-B | 7W | 4-CCTselect | U5 Series",  "T5HE", "UL-A+B", "t5-cs-u5"),
    ("LT5F2CS4/HO/U5",  "T5HO | 2FT | Type A-B | 11W | 4-CCTselect | U5 Series", "T5HO", "UL-A+B", "t5-cs-u5"),
    ("LT5F3CS4/HE/U5",  "T5HE | 3FT | Type A-B | 10W | 4-CCTselect | U5 Series", "T5HE", "UL-A+B", "t5-cs-u5"),
    ("LT5F3CS4/HO/U5",  "T5HO | 3FT | Type A-B | 17W | 4-CCTselect | U5 Series", "T5HO", "UL-A+B", "t5-cs-u5"),
    ("LT5F4CS4/HE/U5",  "T5HE | 4FT | Type A-B | 13W | 4-CCTselect | U5 Series", "T5HE", "UL-A+B", "t5-cs-u5"),
    ("LT5F4CS4/HO/U5",  "T5HO | 4FT | Type A-B | 24W | 4-CCTselect | U5 Series", "T5HO", "UL-A+B", "t5-cs-u5"),
    # CSselect UL-B
    ("LT5F2CS4/HE/DE5", "T5HE | 2FT | Type-B | 7W | 4-CCTselect | DE5 Series",   "T5HE", "UL-B",   "t5-cs-de5"),
    ("LT5F2CS4/HO/DE5", "T5HO | 2FT | Type-B | 12W | 4-CCTselect | DE5 Series",  "T5HO", "UL-B",   "t5-cs-de5"),
    ("LT5F3CS4/HE/DE5", "T5HE | 3FT | Type-B | 12W | 4-CCTselect | DE5 Series",  "T5HE", "UL-B",   "t5-cs-de5"),
    ("LT5F3CS4/HO/DE5", "T5HO | 3FT | Type-B | 18W | 4-CCTselect | DE5 Series",  "T5HO", "UL-B",   "t5-cs-de5"),
    ("LT5F4CS4/HE/DE5", "T5HE | 4FT | Type-B | 15W | 4-CCTselect | DE5 Series",  "T5HE", "UL-B",   "t5-cs-de5"),
    ("LT5F4CS4/HO/DE5", "T5HO | 4FT | Type-B | 24W | 4-CCTselect | DE5 Series",  "T5HO", "UL-B",   "t5-cs-de5"),
    # T5HE UL-A+B (Clearance)
    ("LT5F160035K1",    "T5HE | 4FT | Type-A | 13W/3500K | K Series",             "T5HE", "UL-A+B", "t5-he-u5"),
    ("LT5F21241U5",     "T5HE | 2FT | Type A+B | 12W/4100K | U5 Series",          "T5HE", "UL-A+B", "t5-he-u5"),
    ("LT5F31841U5",     "T5HE | 3FT | Type A+B | 18W/4100K | U5 Series",          "T5HE", "UL-A+B", "t5-he-u5"),
    ("LT5F41330BP1",    "T5HE | 4FT | Type-B | 13W/3000K | BP Series",            "T5HE", "UL-A+B", "t5-he-u5"),
    ("LT5F41341BP1",    "T5HE | 4FT | Type-B | 13W/4100K | BP Series",            "T5HE", "UL-A+B", "t5-he-u5"),
    ("LT5F41530U5",     "T5HE | 4FT | Type A+B | 15W/3000K | U5 Series",          "T5HE", "UL-A+B", "t5-he-u5"),
    ("LT5F41541U5",     "T5HE | 4FT | Type A+B | 15W/4100K | U5 Series",          "T5HE", "UL-A+B", "t5-he-u5"),
    # T5HE UL-A (Clearance)
    ("LT5F090435K5",    "T5HE | 9in | Type-A | 4W/3500K | K5 Series",             "T5HE", "UL-A",   "t5-he-k5"),
    ("LT5F120435K5",    "T5HE | 12in | Type-A | 4W/3500K | K5 Series",            "T5HE", "UL-A",   "t5-he-k5"),
    ("LT5F211235K5",    "T5HE | 21in | Type-A | 12W/3500K | K5 Series",           "T5HE", "UL-A",   "t5-he-k5"),
    ("LT5F241235K5",    "T5HE | 24in | Type-A | 12W/3500K | K5 Series",           "T5HE", "UL-A",   "t5-he-k5"),
    ("LT5F341835K5",    "T5HE | 34in | Type-A | 18W/3500K | K5 Series",           "T5HE", "UL-A",   "t5-he-k5"),
    ("LT5F361835K5",    "T5HE | 36in | Type-A | 18W/3500K | K5 Series",           "T5HE", "UL-A",   "t5-he-k5"),
    ("LT5F482435K5",    "T5HE | 48in | Type-A | 24W/3500K | K5 Series",           "T5HE", "UL-A",   "t5-he-k5"),
    ("LT5F602435K5",    "T5HE | 60in | Type-A | 24W/3500K | K5 Series",           "T5HE", "UL-A",   "t5-he-k5"),
    # T5HO UL-A+B (Clearance)
    ("LT5F42435U5",     "T5HO | 4FT | Type A+B | 24W/3500K | U5 Series",          "T5HO", "UL-A+B", "t5-ho-u5"),
    ("LT5F42441U5",     "T5HO | 4FT | Type A+B | 24W/4100K | U5 Series",          "T5HO", "UL-A+B", "t5-ho-u5"),
    ("LT5F42450U5",     "T5HO | 4FT | Type A+B | 24W/5000K | U5 Series",          "T5HO", "UL-A+B", "t5-ho-u5"),
    # T5HO UL-A (Clearance)
    ("LT5F330035K2",    "T5HO | 4FT | Type-A | 24W/3500K | K Series",             "T5HO", "UL-A",   "t5-ho-k5"),
    ("LT5F330041K2",    "T5HO | 4FT | Type-A | 24W/4100K | K Series",             "T5HO", "UL-A",   "t5-ho-k5"),
    # T5HO UL-B (Clearance)
    ("LT5F42530BP1",    "T5HO | 4FT | Type-B | 25W/3000K | BP Series",            "T5HO", "UL-B",   "t5-ho-de5"),
]

with open('src/data/sku-index.json') as f:
    data = json.load(f)

ta = data['collections']['tubulararch']

# Remove all old T5 SKUs
ta['skus'] = [s for s in ta['skus'] if not (s.get('family', '').startswith('t5') or s.get('family') == 't5')]

# Add new T5 SKUs
for sku_num, desc, sub_cat, echelon, family in T5_SKUS:
    ta['skus'].append({
        "sku": desc,
        "sku_number": sku_num,
        "family": family,
        "sub_category": sub_cat,
        "display_echelon": echelon,
        "max_wattage": None,
        "dlc": False,
        "ccts": [],
        "voltages": [],
        "mount_types": [],
        "taa": False,
    })

# Remove all old T5 family records
ta['families'] = [f for f in ta['families'] if not f['family'].startswith('t5')]

# Count SKUs per family
from collections import defaultdict
fam_counts = defaultdict(int)
for s in ta['skus']:
    fam = s.get('family', '')
    if fam.startswith('t5'):
        fam_counts[fam] += 1

# Family definitions
FAMILIES = [
    # family_slug,    sub_category,   display_echelon, max_watt
    ("t5-cs-u5",   "T5HE · T5HO",  "UL-A+B",        24),
    ("t5-cs-de5",  "T5HE · T5HO",  "UL-B",          24),
    ("t5-he-u5",   "T5HE",         "UL-A+B",        15),
    ("t5-he-k5",   "T5HE",         "UL-A",          24),
    ("t5-ho-u5",   "T5HO",         "UL-A+B",        24),
    ("t5-ho-k5",   "T5HO",         "UL-A",          24),
    ("t5-ho-de5",  "T5HO",         "UL-B",          25),
]

for slug, sub_cat, echelon, max_watt in FAMILIES:
    ta['families'].append({
        "family": slug,
        "sub_category": sub_cat,
        "display_echelon": echelon,
        "max_wattage": max_watt,
        "sku_count": fam_counts[slug],
        "dlc": False,
        "ccts": [],
        "voltages": [],
        "mount_types": [],
        "taa": False,
        "comingSoon": False
    })

with open('src/data/sku-index.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Done. T5 families:")
for fam in ta['families']:
    if fam['family'].startswith('t5'):
        print(f"  {fam['family']:15} | sub_category: {fam['sub_category']:12} | echelon: {fam['display_echelon']:7} | sku_count: {fam['sku_count']}")

print(f"\nTotal T5 SKUs: {sum(fam_counts.values())}")
