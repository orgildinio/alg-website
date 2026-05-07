"""
Composite script for Brighton Tubular hero image — v6.
Output canvas is 4:3 landscape (1600×1200) so it fits the hero box exactly.
Bulbs are base-aligned, preserve relative size differences, centered vertically.
Three bulbs: LVTS-TB6 (short T6 candelabra), LVTS-TB9 (medium T9), LVTS-TB10 (tall T10)
"""
from pathlib import Path
from rembg import remove
from PIL import Image
import numpy as np
import io

UPLOAD = Path("/home/ubuntu/upload")
OUT_DIR = Path("/home/ubuntu/alg-website/public/images/vintage-decor")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = [
    "LVTS-TB6.png",
    "LVTS-TB9.png",
    "LVTS-TB10.png",
]

# 4:3 landscape canvas
CANVAS_W = 1600
CANVAS_H = 1200
PADDING  = 60   # gap between bulbs
ALPHA_THRESHOLD = 30

def remove_bg(src: Path) -> Image.Image:
    print(f"Processing {src.name} ...")
    data = src.read_bytes()
    out  = remove(data)
    img  = Image.open(io.BytesIO(out)).convert("RGBA")
    arr  = np.array(img)
    arr[arr[:, :, 3] < ALPHA_THRESHOLD, 3] = 0
    img  = Image.fromarray(arr)
    bbox = img.getbbox()
    img  = img.crop(bbox)
    print(f"  Done  ({img.width}×{img.height})")
    return img

raw_bulbs = [remove_bg(UPLOAD / name) for name in SOURCES]

# Scale so the tallest bulb fills 90% of canvas height, others scale proportionally
tallest_h = max(b.height for b in raw_bulbs)
scale = (CANVAS_H * 0.90) / tallest_h

scaled = []
for b in raw_bulbs:
    new_h = int(b.height * scale)
    new_w = int(b.width * scale)
    scaled.append(b.resize((new_w, new_h), Image.LANCZOS))

# Check total width fits; if not, reduce scale
total_content_w = sum(b.width for b in scaled) + PADDING * (len(scaled) - 1)
if total_content_w > CANVAS_W * 0.95:
    fit_scale = (CANVAS_W * 0.95) / total_content_w
    scaled = [b.resize((int(b.width * fit_scale), int(b.height * fit_scale)), Image.LANCZOS) for b in scaled]
    total_content_w = sum(b.width for b in scaled) + PADDING * (len(scaled) - 1)

def base_y(img: Image.Image) -> int:
    alpha = img.split()[3]
    for y in range(img.height - 1, -1, -1):
        row = alpha.crop((0, y, img.width, y + 1))
        if row.getextrema()[1] > 10:
            return y
    return img.height - 1

bases = [base_y(b) for b in scaled]
max_base = max(bases)

# Base sits at 95% of canvas height
base_y_canvas = int(CANVAS_H * 0.95)

canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))

# Center the group horizontally
start_x = (CANVAS_W - total_content_w) // 2
x = start_x
for b, base in zip(scaled, bases):
    y_pos = base_y_canvas - base
    canvas.paste(b, (x, y_pos), b)
    x += b.width + PADDING

out_path = OUT_DIR / "brighton-tubular-group.png"
canvas.save(out_path, "PNG")
print(f"Saved composite → {out_path.relative_to(Path('/home/ubuntu/alg-website'))}  ({canvas.width}×{canvas.height})")
