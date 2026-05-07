#!/usr/bin/env python3
"""Remove backgrounds from 6 series card bulb images for Nostalgic Décor collection page."""
import io, os
from PIL import Image
from rembg import remove

OUT_DIR = '/home/ubuntu/alg-website/public/images/nostalgic-decor'
os.makedirs(OUT_DIR, exist_ok=True)

images = [
    ('/home/ubuntu/upload/LTA19S.png',    'eames-a19-card.png'),
    ('/home/ubuntu/upload/LTB10C12.png',  'knoll-b10-card.png'),
    ('/home/ubuntu/upload/LTCA12C12.png', 'bauer-ca10-card.png'),
    ('/home/ubuntu/upload/LTG165C12.png', 'heath-g16-card.png'),
    ('/home/ubuntu/upload/LTG25S.png',    'eichler-g25-card.png'),
    ('/home/ubuntu/upload/LTS14C.webp',   'marshall-s14-card.png'),
]

for src, out_name in images:
    print(f'Processing {src}...')
    with open(src, 'rb') as f:
        raw = f.read()
    out_bytes = remove(raw)
    img = Image.open(io.BytesIO(out_bytes)).convert('RGBA')
    out_path = os.path.join(OUT_DIR, out_name)
    img.save(out_path)
    print(f'  Saved: {out_path} ({img.size})')

print('Done.')
