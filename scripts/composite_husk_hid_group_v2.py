"""
Husk HID composite v2 — explicit size ratios.
Bulb order (left to right): 36W, 54W, 100W, 120W
Size ratios relative to the 4th (120W) bulb's rendered height:
  36W  = 50%
  54W  = 70%
  100W = 90%
  120W = 100%
Canvas: 1600×1200 (4:3 landscape), transparent bg.
Base-aligned.
"""
from pathlib import Path
from rembg import remove
from PIL import Image
import numpy as np
import io

UPLOAD = Path("/home/ubuntu/upload")
OUT_DIR = Path("/home/ubuntu/alg-website/public/images/signature")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = [
    ("LCRN_36WE39(2).webp",          0.50),
    ("LCRN_54WE39(5).webp",          0.70),
    ("LCRN_100WE39(2).webp",         0.90),
    ("LCRN_120WE39\uff082\uff09.webp", 1.00),
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

# Determine the target height for the 4th (100%) bulb so it fills ~90% of canvas height
target_100_h = int(CANVAS_H * 0.90)

# Scale each bulb: first scale to 100% height, then apply ratio
scaled = []
for img, ratio in raw_bulbs:
    # Scale image so that IF it were 100%, its height = target_100_h
    # Then apply the ratio to get the actual rendered height
    base_scale = target_100_h / img.height
    final_h = int(target_100_h * ratio)
    final_w = int(img.width * base_scale * ratio)
    resized = img.resize((final_w, final_h), Image.LANCZOS)
    scaled.append(resized)
    print(f"  Rendered: {resized.width}×{resized.height} (ratio {ratio})")

# Check total width fits; shrink if needed
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

out_path = OUT_DIR / "husk-hid-group.png"
canvas.save(out_path, "PNG")
print(f"\nSaved → {out_path}  ({canvas.width}×{canvas.height})")
