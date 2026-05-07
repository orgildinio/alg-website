#!/usr/bin/env python3
"""
Remove backgrounds from 4 LTA15 bulb images and composite them into a
horizontal group shot matching the S.png reference layout.

Order (left to right, matching S.png style):
  1. LTA15C12 (clear, E12 candelabra)
  2. LTA15C26 (clear, E26 medium)
  3. LTA15F12 (frosted, E12 candelabra)
  4. LTA15F26 (frosted, E26 medium)
"""
import io, os
from PIL import Image
from rembg import remove

SOURCES = [
    '/home/ubuntu/upload/pasted_file_oZoPNG_LTA15C12.png',
    '/home/ubuntu/upload/pasted_file_tJyTfy_LTA15C26.png',
    '/home/ubuntu/upload/pasted_file_YktdMC_LTA15F12.png',
    '/home/ubuntu/upload/pasted_file_S7PHow_LTA15F26.png',
]

OUT_DIR = '/home/ubuntu/alg-website/public/images/nostalgic-decor'
os.makedirs(OUT_DIR, exist_ok=True)
OUT_PATH = f'{OUT_DIR}/saarinen-a15-group.png'

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
# Target slot: 600px tall, keep aspect ratio
SLOT_H = 600
normalized = []
for img in bulbs:
    w, h = img.size
    new_w = int(w * SLOT_H / h)
    resized = img.resize((new_w, SLOT_H), Image.LANCZOS)
    normalized.append(resized)

# --- Step 3: Composite side by side with slight overlap (like S.png) ---
# Overlap each bulb by 10% of its width for a natural grouped look
OVERLAP = 0.08
total_w = 0
for i, img in enumerate(normalized):
    if i == 0:
        total_w += img.width
    else:
        total_w += int(img.width * (1 - OVERLAP))

# Add padding: 60px left/right, 40px top/bottom
PAD_X = 60
PAD_Y = 40
canvas_w = total_w + PAD_X * 2
canvas_h = SLOT_H + PAD_Y * 2

# Transparent canvas
canvas = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))

x = PAD_X
for i, img in enumerate(normalized):
    # Align all bulbs to bottom of slot so bases line up
    y = PAD_Y + (SLOT_H - img.height)
    canvas.paste(img, (x, y), img)
    if i < len(normalized) - 1:
        x += int(img.width * (1 - OVERLAP))
    else:
        x += img.width

canvas.save(OUT_PATH)
print(f'\nComposite saved: {OUT_PATH}  size={canvas.size}')
