"""
Composite script for Belgravia Victorian hero image.
Two bulbs: LTVC19V_MB (amber squirrel-cage) + LTVC19S_MB-SP (smoked spiral)
Same treatment as Edison: rembg background removal, base-aligned horizontal composite.
"""
from pathlib import Path
from rembg import remove
from PIL import Image
import io

UPLOAD = Path("/home/ubuntu/upload")
OUT_DIR = Path("/home/ubuntu/alg-website/public/images/vintage-decor")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SOURCES = [
    "LTVC19V_MB.png",
    "LTVC19S_MB-SP(1).png",
]

TARGET_H = 1200   # normalised bulb height
PADDING  = 60     # horizontal gap between bulbs
CANVAS_PAD = 80   # outer padding

def remove_bg(src: Path) -> Image.Image:
    print(f"Processing {src.name} ...")
    data = src.read_bytes()
    out  = remove(data)
    img  = Image.open(io.BytesIO(out)).convert("RGBA")
    # crop to tight bounding box
    bbox = img.getbbox()
    img  = img.crop(bbox)
    print(f"  Done  ({img.width}×{img.height})")
    return img

# --- remove backgrounds ---
bulbs = [remove_bg(UPLOAD / name) for name in SOURCES]

# --- scale to uniform height ---
scaled = []
for b in bulbs:
    ratio = TARGET_H / b.height
    new_w = int(b.width * ratio)
    scaled.append(b.resize((new_w, TARGET_H), Image.LANCZOS))

# --- base-align: find lowest non-transparent pixel for each ---
def base_y(img: Image.Image) -> int:
    """Row index of the lowest non-transparent pixel (0-indexed from top)."""
    alpha = img.split()[3]
    for y in range(img.height - 1, -1, -1):
        row = alpha.crop((0, y, img.width, y + 1))
        if row.getextrema()[1] > 10:
            return y
    return img.height - 1

bases = [base_y(b) for b in scaled]
max_base = max(bases)

# total canvas size
total_w = sum(b.width for b in scaled) + PADDING * (len(scaled) - 1) + 2 * CANVAS_PAD
total_h = max_base + CANVAS_PAD + 20   # a little below the lowest base

canvas = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))

x = CANVAS_PAD
for b, base in zip(scaled, bases):
    # align bases: shift up so each bulb's base sits at max_base row
    y_offset = max_base - base
    canvas.paste(b, (x, y_offset), b)
    x += b.width + PADDING

out_path = OUT_DIR / "belgravia-victorian-group.png"
canvas.save(out_path, "PNG")
print(f"Saved composite → {out_path.relative_to(Path('/home/ubuntu/alg-website'))}  ({canvas.width}×{canvas.height})")
