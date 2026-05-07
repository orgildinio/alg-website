"""
Provence Globe composite v3 — explicit size ratios.
Order (left to right): G16.5 CB, G16.5 MB, G25, G40
Ratios relative to 4th (G40) rendered height:
  G16.5 CB = 50%
  G16.5 MB = 50%
  G25      = 70%
  G40      = 100%
Canvas: 1600×1200 (4:3), transparent bg, base-aligned.
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
    ("LTG165V_CB.png",       0.50),
    ("LTG165V_MB.png",       0.50),
    ("LTG25V_MB.png",        0.70),
    ("LTG40V_MB-SV(1).png",  1.00),
]

CANVAS_W = 1600
CANVAS_H = 1200
PADDING  = 40
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
    print(f"  Cropped: {img.width}×{img.height}")
    return img

raw_bulbs = [(remove_bg(UPLOAD / name), ratio) for name, ratio in SOURCES]

# Target height for the 100% bulb = 90% of canvas height
target_100_h = int(CANVAS_H * 0.90)

scaled = []
for img, ratio in raw_bulbs:
    base_scale = target_100_h / img.height
    final_h = int(target_100_h * ratio)
    final_w = int(img.width * base_scale * ratio)
    resized = img.resize((final_w, final_h), Image.LANCZOS)
    scaled.append(resized)
    print(f"  Rendered: {resized.width}×{resized.height} (ratio {ratio})")

# Shrink if total width exceeds canvas
total_w = sum(b.width for b in scaled) + PADDING * (len(scaled) - 1)
if total_w > CANVAS_W * 0.96:
    fit = (CANVAS_W * 0.96) / total_w
    scaled = [b.resize((int(b.width * fit), int(b.height * fit)), Image.LANCZOS) for b in scaled]
    total_w = sum(b.width for b in scaled) + PADDING * (len(scaled) - 1)

def base_y(img: Image.Image) -> int:
    alpha = img.split()[3]
    for y in range(img.height - 1, -1, -1):
        row = alpha.crop((0, y, img.width, y + 1))
        if row.getextrema()[1] > 10:
            return y
    return img.height - 1

base_y_canvas = int(CANVAS_H * 0.97)

canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))

start_x = (CANVAS_W - total_w) // 2
x = start_x
for b in scaled:
    base = base_y(b)
    y_pos = base_y_canvas - base
    canvas.paste(b, (x, y_pos), b)
    x += b.width + PADDING

out_path = OUT_DIR / "provence-globe-group.png"
canvas.save(out_path, "PNG")
print(f"\nSaved → {out_path}  ({canvas.width}×{canvas.height})")
