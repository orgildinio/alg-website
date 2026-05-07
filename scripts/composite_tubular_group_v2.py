"""
Composite script for Brighton Tubular hero image — v2.
Upscales small images before rembg for better edge quality.
Three bulbs: LTTB6V_CB (T6 candelabra amber), LTTB9V1_MB (T9 medium amber),
             LTTB10V_MB (T10 medium amber)
"""
from pathlib import Path
from rembg import remove
from PIL import Image
import io

UPLOAD = Path("/home/ubuntu/upload")
OUT_DIR = Path("/home/ubuntu/alg-website/public/images/vintage-decor")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = [
    "LTTB6V_CB.png",
    "LTTB9V1_MB.png",
    "LTTB10V_MB.png",
]

TARGET_H = 1300
PADDING  = 70
CANVAS_PAD = 80
MIN_DIM = 600   # upscale if smaller than this before rembg

def remove_bg(src: Path) -> Image.Image:
    print(f"Processing {src.name} ...")
    img_orig = Image.open(src).convert("RGB")
    # upscale if too small for rembg to work well
    if min(img_orig.size) < MIN_DIM:
        scale = MIN_DIM / min(img_orig.size)
        new_size = (int(img_orig.width * scale), int(img_orig.height * scale))
        img_orig = img_orig.resize(new_size, Image.LANCZOS)
        print(f"  Upscaled to {img_orig.width}×{img_orig.height} for rembg")
    buf = io.BytesIO()
    img_orig.save(buf, "PNG")
    out = remove(buf.getvalue())
    img = Image.open(io.BytesIO(out)).convert("RGBA")
    bbox = img.getbbox()
    img = img.crop(bbox)
    print(f"  Done  ({img.width}×{img.height})")
    return img

bulbs = [remove_bg(UPLOAD / name) for name in SOURCES]

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

out_path = OUT_DIR / "brighton-tubular-group.png"
canvas.save(out_path, "PNG")
print(f"Saved composite → {out_path.relative_to(Path('/home/ubuntu/alg-website'))}  ({canvas.width}×{canvas.height})")
