"""
Batch background removal for luxoARCH family hero images.
Outputs transparent PNGs to public/products/{family}/assets/card-nobg.png
"""
import os
import sys
from pathlib import Path
from rembg import remove
from PIL import Image
import io

BASE = Path('/home/ubuntu/alg-website/public/products')
OUT_DIR = Path('/home/ubuntu/alg-website/public/images/family-cards/luxoarch')
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Map: family_slug -> best hero image path
FAMILIES = {
    'heritage':    BASE / 'heritage/assets/hero/heritage-hero-1.webp',
    'liberty':     BASE / 'liberty/assets/hero/liberty-hero-3.webp',
    'navigator':   BASE / 'navigator/assets/hero/navigator-hero-1.webp',
    'pathfinder':  BASE / 'pathfinder/assets/hero/pathfinder-hero-1.webp',
    'aura':        None,  # no hero available
    'canadarm':    None,
    'everest':     BASE / 'everest/assets/hero/everest-hero-1.webp',
    'illuminator': BASE / 'illuminator/assets/hero/illuminator-hero-1.webp',
    'radiator-i':  BASE / 'radiator/assets/hero/radiator-hero-1.webp',
    'radiator-ii': BASE / 'radiator/assets/hero/radiator-hero-1.webp',
    'radiator-iii':BASE / 'radiator/assets/hero/radiator-hero-1.webp',
    'beacon-i':    None,
    'lsl-series':  None,
    'anaheim':     BASE / 'anaheim/assets/hero/anaheim-hero-1.webp',
    'guardian':    BASE / 'guardian/assets/hero/guardian-hero-1.webp',
    'ramparts':    BASE / 'ramparts/assets/hero/ramparts-hero-1.webp',
    'shield':      None,
    'watchtower':  BASE / 'watchtower/assets/hero/watchtower-hero-1.webp',
    'wedge-i':     BASE / 'wedge/assets/hero/wedge-hero-1-black.webp',
    'atlanta':     BASE / 'atlanta/assets/hero/atlanta-hero-1.webp',
    'nightwatch':  BASE / 'nightwatch/assets/hero/nightwatch-hero-1.webp',
    'sentinel':    BASE / 'sentinel/assets/hero/sentinel-hero-1.webp',
}

for slug, src in FAMILIES.items():
    out_path = OUT_DIR / f'{slug}.png'
    if src is None:
        print(f'SKIP  {slug} — no source image')
        continue
    if not src.exists():
        print(f'MISS  {slug} — {src} not found')
        continue
    print(f'Processing {slug}...', end=' ', flush=True)
    try:
        with open(src, 'rb') as f:
            img_bytes = f.read()
        result = remove(img_bytes)
        img = Image.open(io.BytesIO(result)).convert('RGBA')
        img.save(out_path, 'PNG')
        print(f'OK -> {out_path.name}')
    except Exception as e:
        print(f'ERROR: {e}')

print('\nDone.')
