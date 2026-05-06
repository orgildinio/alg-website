#!/usr/bin/env python3
"""
fix_lampar_subcats.py — Update lamparARCH sub_category values in sku-index.json
to match the correct application taxonomy:
  Linear High Bay:      Tiny-I, Titan-II
  Round High Bay:       Icarus-III, Jupiter-II
  Linear Strip:         Hallmark
  Retrofit Linear Strip: retroⒶRCH-L1
  Vapor-Tight:          Eureka-I, Eureka-II
"""
import json

path = '/home/ubuntu/alg-website/src/data/sku-index.json'
with open(path) as f:
    data = json.load(f)

# Mapping: family name -> correct sub_category
FAMILY_SUBCATS = {
    'Tiny-I':           'Linear High Bay',
    'Titan-II':         'Linear High Bay',
    'Icarus-III':       'Round High Bay',
    'Jupiter-II':       'Round High Bay',
    'Hallmark':         'Linear Strip',
    'retroⒶRCH-L1':    'Retrofit Linear Strip',
    'Eureka-I':         'Vapor-Tight',
    'Eureka-II':        'Vapor-Tight',
    # Vanguard-I was already "Linear Strip" — keep it
    'Vanguard-I':       'Linear Strip',
}

lampar = data['collections']['lampararch']

# Update families
changed_families = []
for fam in lampar['families']:
    name = fam.get('family')
    if name in FAMILY_SUBCATS:
        old = fam.get('sub_category')
        new = FAMILY_SUBCATS[name]
        if old != new:
            fam['sub_category'] = new
            changed_families.append(f'  {name}: {old} -> {new}')

# Update SKUs
changed_skus = 0
for sku in lampar['skus']:
    name = sku.get('family')
    if name in FAMILY_SUBCATS:
        old = sku.get('sub_category')
        new = FAMILY_SUBCATS[name]
        if old != new:
            sku['sub_category'] = new
            changed_skus += 1

with open(path, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')

print('✅ lamparARCH sub_category updates:')
for line in changed_families:
    print(line)
print(f'  SKUs updated: {changed_skus}')
print('Done.')
