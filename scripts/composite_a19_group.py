#!/usr/bin/env python3
"""
Remove backgrounds from 3 LTA19 bulb images and composite them into a
horizontal group shot matching the S.png reference layout.

Order (left to right):
  1. LTA19S  (silver-tip)
  2. LTA19F  (frosted)
  3. LTA19C  (clear)
"""
import io, os
from PIL import Image
from rembg import remove

SOURCES = [
    '/home/ubuntu/upload/pasted_file_IrJMLl_LTA19S.png',
    '/home/ubuntu/upload/pasted_file_D9clS6_LTA19F.png',
    '/home/ubuntu/upload/pasted_file_OaK0iz_LTA19C.png',
]

OUT_DIR = '/home/ubuntu/alg-website/public/images/nostalgic-decor'
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = f'{OUT_DIR}/eames-a19-group.png'

# --- Step 1: Remove backgrounds ---
bulbs = []
for src in SOURCES:
    print(f'Processing {os.path.basename(src)}...')
    with open(src, 'rb') as f:
        raw = f.read()
    out_bytes = remove(raw)
    img = Image.open(io.BytesIO(out_bytes)).convert('RGBA')
    bulbs.append(img)
    print(f'  size: {img.size}')

# --- Step 2: Normalize each bulb to a common slot height ---
SLOT_H = 600
normalized = []
for img in bulbs:
    w, h = img.size
    new_w = int(w * SLOT_H / h)
    resized = img.resize((new_w, SLOT_H), Image.LANCZOS)
    normalized.append(resized)

# --- Step 3: Composite side by side with slight overlap ---
OVERLAP = 0.08
total_w = 0
for i, img in enumerate(normalized):
    if i == 0:
        total_w += img.width
    else:
        total_w += int(img.width * (1 - OVERLAP))

PAD_X = 60
PAD_Y = 40
canvas_w = total_w + PAD_X * 2
canvas_h = SLOT_H + PAD_Y * 2

canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))

x = PAD_X
for i, img in enumerate(normalized):
    y = PAD_Y + (SLOT_H - img.height)
    canvas.paste(img, (x, y), img)
    if i < len(normalized) - 1:
        x += int(img.width * (1 - OVERLAP))
    else:
        x += img.width

canvas.save(OUT_PATH)
print(f'\nComposite saved: {OUT_PATH}  size={canvas.size}')
