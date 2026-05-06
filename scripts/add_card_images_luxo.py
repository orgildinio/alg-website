"""
Add card_image field to luxoARCH families in sku-index.json.
Maps family name -> /images/family-cards/luxoarch/{slug}.png
"""
import json
from pathlib import Path

SKU_INDEX = Path('/home/ubuntu/alg-website/src/data/sku-index.json')
CARD_BASE = '/images/family-cards/luxoarch'
AVAIL_DIR = Path('/home/ubuntu/alg-website/public/images/family-cards/luxoarch')

# Map family name -> slug used for the card image filename
FAMILY_SLUG_MAP = {
    'Heritage':    'heritage',
    'Liberty':     'liberty',
    'Navigator':   'navigator',
    'Pathfinder':  'pathfinder',
    'Aura':        None,  # no image
    'Canadarm':    None,
    'Everest':     'everest',
    'Illuminator': 'illuminator',
    'Radiator-I':  'radiator-i',
    'Radiator-II': 'radiator-ii',
    'Radiator-III':'radiator-iii',
    'Beacon-I':    None,
    'LSL Series':  None,
    'Anaheim':     'anaheim',
    'Guardian':    'guardian',
    'Ramparts':    'ramparts',
    'Shield':      None,
    'Watchtower':  'watchtower',
    'Wedge-I':     'wedge-i',
    'Atlanta':     'atlanta',
    'Nightwatch':  'nightwatch',
    'Sentinel':    'sentinel',
}

with open(SKU_INDEX) as f:
    data = json.load(f)

families = data['collections']['luxoarch']['families']
updated = 0
for fam in families:
    name = fam['family']
    slug = FAMILY_SLUG_MAP.get(name)
    if slug and (AVAIL_DIR / f'{slug}.png').exists():
        fam['card_image'] = f'{CARD_BASE}/{slug}.png'
        updated += 1
        print(f'  SET  {name} -> {fam["card_image"]}')
    else:
        fam['card_image'] = None
        print(f'  SKIP {name} — no image')

with open(SKU_INDEX, 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f'\nUpdated {updated}/{len(families)} families.')
