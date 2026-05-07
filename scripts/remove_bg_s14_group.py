#!/usr/bin/env python3
"""Remove background from S14 group photo and save for use as hero image."""
import io, os
from PIL import Image
from rembg import remove

SRC = '/home/ubuntu/upload/S.webp'
OUT_DIR = '/home/ubuntu/alg-website/public/images/nostalgic-decor'
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = f'{OUT_DIR}/s14-group.png'

print('Processing S.webp...')
with open(SRC, 'rb') as f:
    raw = f.read()
out_bytes = remove(raw)
img = Image.open(io.BytesIO(out_bytes)).convert('RGBA')
print(f'  size: {img.size}')
img.save(OUT_PATH)
print(f'Saved: {OUT_PATH}')
