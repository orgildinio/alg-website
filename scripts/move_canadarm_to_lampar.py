"""
Move Canadarm family (SKUs + family record) from luxoarch → lampararch in sku-index.json.
Also updates the card_image path to lampararch directory.
"""
import json, copy

PATH = "src/data/sku-index.json"
with open(PATH) as f:
    data = json.load(f)

luxo = data['collections']['luxoarch']
lampar = data['collections']['lampararch']

# Move SKUs
canadarm_skus = [s for s in luxo['skus'] if s['family'] == 'Canadarm']
luxo['skus'] = [s for s in luxo['skus'] if s['family'] != 'Canadarm']
lampar['skus'].extend(canadarm_skus)
print(f"Moved {len(canadarm_skus)} SKUs to lampararch")

# Move family record, update card_image path
canadarm_fams = [f for f in luxo['families'] if f['family'] == 'Canadarm']
luxo['families'] = [f for f in luxo['families'] if f['family'] != 'Canadarm']
for fam in canadarm_fams:
    fam['card_image'] = fam.get('card_image','').replace('/luxoarch/', '/lampararch/')
    # Canadarm is a Dock Light — keep sub_category as-is for now
lampar['families'].extend(canadarm_fams)
print(f"Moved {len(canadarm_fams)} family record(s) to lampararch")
print("Family record:", json.dumps(canadarm_fams[0], indent=2))

with open(PATH, 'w') as f:
    json.dump(data, f, indent=2)
print("Done — sku-index.json updated.")
