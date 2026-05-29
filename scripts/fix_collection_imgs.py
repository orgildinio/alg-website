#!/usr/bin/env python3
"""
Fix the fam-card img src pattern in the collection page:
1. Use slug_001_white.png (underscore) as primary for most SKUs
2. Use slug-001_white.png (dash) for em20-hmb135ac, em15-pmb120ac, em25-pmb120ac
3. Add data-output and data-family attributes to fam-cards for filter support
4. Fix the featured card image path for em20-cmb260dc
"""
import re

COLLECTION = 'src/pages/collections/constant/index.astro'

with open(COLLECTION, 'r') as f:
    content = f.read()

# --- Fix 1: Fix the img src pattern in fam-cards ---
# Current (broken): removes dashes from dir name
# /products/${sku.id.replace('sku-','').replace(/-q$/,'').replace(/-/g,'').replace(/\//g,'')}/assets/${sku.id.replace('sku-','').replace(/-q$/,'')}-001_white.png
# 
# New: use the sku.pdp path to derive the dir slug, and use underscore pattern
# But we need to handle the 3 exceptions. Best approach: add a `photo` field to the SKU data.

# --- Fix 2: Add photo field to each SKU in the data array ---
# Map from sku id to photo filename
photo_map = {
    'sku-em07-cmb-150dc':   '/products/em07-cmb150dc/assets/em07-cmb150dc_001_white.png',
    'sku-em07-cmb-260dc':   '/products/em07-cmb260dc/assets/em07-cmb260dc_001_white.png',
    'sku-em08-amb-48dc':    '/products/em08-amb48dc/assets/em08-amb48dc_001_white.png',
    'sku-em08-hmb-170dc':   '/products/em08-hmb170dc/assets/em08-hmb170dc_001_white.png',
    'sku-em08-mt-150dc':    '/products/em08-mt150dc/assets/em08-mt150dc_001_white.png',
    'sku-em08-ytb-60dc':    '/products/em08-ytb60dc/assets/em08-ytb60dc_001_white.png',
    'sku-em15-hmb-170dc':   '/products/em15-hmb170dc/assets/em15-hmb170dc_001_white.png',
    'sku-em15-pmb-120ac':   '/products/em15-pmb120ac/assets/em15-pmb-120ac-001_white.png',  # placeholder
    'sku-em20-cmb-150dc':   '/products/em20-cmb150dc/assets/em20-cmb150dc_001_white.png',
    'sku-em20-cmb-260dc':   '/products/em20-cmb260dc/assets/em20-cmb260dc_001_white.png',
    'sku-em20-cmb-260dc-q': '/products/em20-cmb260dc/assets/em20-cmb260dc_001_white.png',
    'sku-em20-hmb-135ac':   '/products/em20-hmb135ac/assets/em20-hmb-135ac-001_white.png',  # dash pattern
    'sku-em25-hmb-170dc':   '/products/em25-hmb170dc/assets/em25-hmb170dc_001_white.png',
    'sku-em25-pmb-120ac':   '/products/em25-pmb120ac/assets/em25-pmb-120ac-001_white.png',  # placeholder
    'sku-em30-umb-170dc':   '/products/em30-umb170dc/assets/em30-umb170dc_001_white.png',
    'sku-em40-rmb-170dc':   '/products/em40-rmb170dc/assets/em40-rmb170dc_001_white.png',
    'sku-em60-gmb-170dc':   '/products/em60-gmb170dc/assets/em60-gmb170dc_001_white.png',
    'sku-em60-umb-170dc':   '/products/em60-umb170dc/assets/em60-umb170dc_001_white.png',
    'sku-crcu-em24-jbm':    '/products/crcu-em24-jbm/assets/crcu-em24-jbm_001_white.png',
    'sku-crc6-em24-jbs-b':  '/products/crc6-em24-jbs-b/assets/crc6-em24-jbs-b_001_white.png',
    'sku-crc6-em24-jbs-w':  '/products/crc6-em24-jbs-w/assets/crc6-em24-jbs-w_001_white.png',
}

# Also map data-output and data-family for each SKU
output_map = {
    'sku-em07-cmb-150dc':   'dc',
    'sku-em07-cmb-260dc':   'dc',
    'sku-em08-amb-48dc':    'dc',
    'sku-em08-hmb-170dc':   'dc',
    'sku-em08-mt-150dc':    'dc',
    'sku-em08-ytb-60dc':    'dc',
    'sku-em15-hmb-170dc':   'dc',
    'sku-em15-pmb-120ac':   'ac',
    'sku-em20-cmb-150dc':   'dc',
    'sku-em20-cmb-260dc':   'dc',
    'sku-em20-cmb-260dc-q': 'dc',
    'sku-em20-hmb-135ac':   'ac',
    'sku-em25-hmb-170dc':   'dc',
    'sku-em25-pmb-120ac':   'ac',
    'sku-em30-umb-170dc':   'dc',
    'sku-em40-rmb-170dc':   'dc',
    'sku-em60-gmb-170dc':   'dc',
    'sku-em60-umb-170dc':   'dc',
    'sku-crcu-em24-jbm':    'dc',
    'sku-crc6-em24-jbs-b':  'dc',
    'sku-crc6-em24-jbs-w':  'dc',
}

family_map = {
    'sku-em07-cmb-150dc':   'multifamily',
    'sku-em07-cmb-260dc':   'multifamily',
    'sku-em08-amb-48dc':    'cityarch',
    'sku-em08-hmb-170dc':   'planoarch',
    'sku-em08-mt-150dc':    'multifamily',
    'sku-em08-ytb-60dc':    'multifamily',
    'sku-em15-hmb-170dc':   'planoarch',
    'sku-em15-pmb-120ac':   'lamparch',
    'sku-em20-cmb-150dc':   'universal',
    'sku-em20-cmb-260dc':   'universal',
    'sku-em20-cmb-260dc-q': 'universal',
    'sku-em20-hmb-135ac':   'luxoarch',
    'sku-em25-hmb-170dc':   'lamparch',
    'sku-em25-pmb-120ac':   'lamparch',
    'sku-em30-umb-170dc':   'universal',
    'sku-em40-rmb-170dc':   'lamparch',
    'sku-em60-gmb-170dc':   'lamparch',
    'sku-em60-umb-170dc':   'universal',
    'sku-crcu-em24-jbm':    'universal',
    'sku-crc6-em24-jbs-b':  'luxoarch',
    'sku-crc6-em24-jbs-w':  'luxoarch',
}

adder_map = {
    'sku-em07-cmb-150dc':   '',
    'sku-em07-cmb-260dc':   'ag',
    'sku-em08-amb-48dc':    '',
    'sku-em08-hmb-170dc':   '',
    'sku-em08-mt-150dc':    '',
    'sku-em08-ytb-60dc':    '',
    'sku-em15-hmb-170dc':   '',
    'sku-em15-pmb-120ac':   'cl',
    'sku-em20-cmb-150dc':   '',
    'sku-em20-cmb-260dc':   '',
    'sku-em20-cmb-260dc-q': 'ag',
    'sku-em20-hmb-135ac':   'cl',
    'sku-em25-hmb-170dc':   '',
    'sku-em25-pmb-120ac':   'cl',
    'sku-em30-umb-170dc':   '',
    'sku-em40-rmb-170dc':   'cl',
    'sku-em60-gmb-170dc':   '',
    'sku-em60-umb-170dc':   '',
    'sku-crcu-em24-jbm':    '',
    'sku-crc6-em24-jbs-b':  '',
    'sku-crc6-em24-jbs-w':  '',
}

# Add photo, output, family, adder fields to the SKU data array
# Find each SKU entry and add the fields
for sku_id, photo in photo_map.items():
    output = output_map.get(sku_id, 'dc')
    family = family_map.get(sku_id, 'universal')
    adder = adder_map.get(sku_id, '')
    
    # Find the SKU entry: { id: 'sku-em07-cmb-150dc', tier: ...
    pattern = rf"(\{{ id: '{re.escape(sku_id)}',[^}}]+\}})"
    
    def add_fields(m):
        entry = m.group(1)
        # Remove trailing }
        entry = entry.rstrip().rstrip('}')
        # Add new fields
        entry += f",\n    photo: '{photo}', output: '{output}', family: '{family}', adder: '{adder}'"
        entry += ' }'
        return entry
    
    new_content = re.sub(pattern, add_fields, content, flags=re.DOTALL)
    if new_content != content:
        content = new_content
    else:
        print(f"WARNING: Could not find SKU entry for {sku_id}")

# --- Fix 3: Replace the img src expression in fam-cards ---
# Replace the complex template literal with {sku.photo}
old_img = r'''                  <img
                    src={`/products/${sku.id.replace('sku-','').replace(/-q$/,'').replace(/-/g,'').replace(/\//g,'')}/assets/${sku.id.replace('sku-','').replace(/-q$/,'')}-001_white.png`}
                    alt={sku.name}
                    loading="lazy"
                    style="max-width:100%;max-height:100%;object-fit:contain;opacity:0.85;"
                    onerror="this.style.display='none';this.nextElementSibling.style.display='block';"
                  />'''

new_img = '''                  <img
                    src={sku.photo}
                    alt={sku.name}
                    loading="lazy"
                    style="max-width:100%;max-height:100%;object-fit:contain;opacity:0.85;"
                    onerror="this.style.display='none';this.nextElementSibling.style.display='block';"
                  />'''

if old_img in content:
    content = content.replace(old_img, new_img)
    print("Fixed img src in fam-cards")
else:
    print("WARNING: Could not find old img src pattern")

# --- Fix 4: Add data-output and data-family to fam-card <a> element ---
old_card_open = '''              <a
                href={sku.pdp}
                class="fam-card"
                id={sku.id}
                data-tier={sku.tier}
                data-sku={sku.name}
              >'''

new_card_open = '''              <a
                href={sku.pdp}
                class="fam-card"
                id={sku.id}
                data-tier={sku.tier}
                data-sku={sku.name}
                data-output={sku.output}
                data-family={sku.family}
                data-adder={sku.adder}
              >'''

if old_card_open in content:
    content = content.replace(old_card_open, new_card_open)
    print("Added data-output, data-family, data-adder to fam-cards")
else:
    print("WARNING: Could not find old fam-card <a> opening")

# --- Fix 5: Fix featured card image path for em20-cmb260dc ---
# The featured array has cardImage: '/products/em20-cmb260dc/assets/em20-cmb-260dc-001_white.png'
# but the real photo is em20-cmb260dc_001_white.png (underscore)
old_feat_img = "cardImage: '/products/em20-cmb260dc/assets/em20-cmb-260dc-001_white.png',"
new_feat_img = "cardImage: '/products/em20-cmb260dc/assets/em20-cmb260dc_001_white.png',"
if old_feat_img in content:
    content = content.replace(old_feat_img, new_feat_img)
    print("Fixed featured card image path for em20-cmb260dc")

with open(COLLECTION, 'w') as f:
    f.write(content)

print("Done.")
