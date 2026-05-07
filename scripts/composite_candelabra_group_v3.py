"""
Composite script for Glasgow Candelabra hero image — v3.
Uses higher alpha threshold to eliminate halo on LTCA10V_CB.
Two bulbs: LTCA10V_CB (CA10 candelabra base amber), LTCA10V_MB (CA10 medium base amber)
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
    "LTCA10V_CB.png",
    "LTCA10V_MB.png",
]

# Per-bulb alpha thresholds — CB needs more aggressive cleanup
THRESHOLDS = [80, 30]

TARGET_H = 1200
PADDING  = 80
CANVAS_PAD = 80

def remove_bg(src: Path, threshold: int) -> Image.Image:
    print(f"Processing {src.name} (threshold={threshold}) ...")
    data = src.read_bytes()
    out  = remove(data)
    img  = Image.open(io.BytesIO(out)).convert("RGBA")
    arr  = np.array(img)
    arr[arr[:, :, 3] < threshold, 3] = 0
    img  = Image.fromarray(arr)
    bbox = img.getbbox()
    img  = img.crop(bbox)
    print(f"  Done  ({img.width}×{img.height})")
    return img

bulbs = [remove_bg(UPLOAD / name, t) for name, t in zip(SOURCES, THRESHOLDS)]

scaled = []
for b in bulbs:
    ratio = TARGET_H / b.height
    new_w = int(b.width * ratio)
    scaled.append(b.resize((new_w, TARGET_H), Image.LANCZOS))

def base_y(img: Image.Image) -> int:
    alpha = img.split()[3]
    for y in range(img.height - 1, -1, -1):
        row = alpha.crop((0, y, img.width, y + 1))
        if row.getextrema()[1] > 10:
            return y
    return img.height - 1

bases = [base_y(b) for b in scaled]
max_base = max(bases)

total_w = sum(b.width for b in scaled) + PADDING * (len(scaled) - 1) + 2 * CANVAS_PAD
total_h = max_base + CANVAS_PAD + 20

canvas = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))

x = CANVAS_PAD
for b, base in zip(scaled, bases):
    y_offset = max_base - base
    canvas.paste(b, (x, y_offset), b)
    x += b.width + PADDING

out_path = OUT_DIR / "glasgow-candelabra-group.png"
canvas.save(out_path, "PNG")
print(f"Saved composite → {out_path.relative_to(Path('/home/ubuntu/alg-website'))}  ({canvas.width}×{canvas.height})")
