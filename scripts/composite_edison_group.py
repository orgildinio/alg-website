"""Remove backgrounds from 3 Edison ST19 bulbs and composite into horizontal group shot."""
import subprocess, sys, io, os

try:
    from rembg import remove
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rembg[gpu]", "-q"])
    from rembg import remove

from PIL import Image

inputs = [
    "/home/ubuntu/upload/LTST19V_MB.webp",
    "/home/ubuntu/upload/LTST19M_MB-SV(1).png",
    "/home/ubuntu/upload/LTST19V_MB-SC(1).png",
]

os.makedirs("public/images/vintage-decor", exist_ok=True)

bulbs = []
for src in inputs:
    print(f"Processing {os.path.basename(src)} ...")
    with open(src, "rb") as f:
        data = f.read()
    result = remove(data)
    img = Image.open(io.BytesIO(result)).convert("RGBA")
    bulbs.append(img)
    print(f"  Done  ({img.size[0]}×{img.size[1]})")

# Normalize heights — scale each to a common height, align bases
TARGET_H = 900
PADDING = 60  # px padding around each bulb
OVERLAP = 0   # no overlap

resized = []
for b in bulbs:
    ratio = TARGET_H / b.height
    new_w = int(b.width * ratio)
    resized.append(b.resize((new_w, TARGET_H), Image.LANCZOS))

canvas_w = sum(r.width for r in resized) + PADDING * (len(resized) + 1)
canvas_h = TARGET_H + PADDING * 2

canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

x = PADDING
for r in resized:
    # Align bases: paste so bottom of bulb sits at bottom of canvas area
    y = PADDING + (TARGET_H - r.height)
    canvas.paste(r, (x, y), r)
    x += r.width + PADDING

out_path = "public/images/vintage-decor/foundry-edison-group.png"
canvas.save(out_path, "PNG")
print(f"\nSaved composite → {out_path}  ({canvas.width}×{canvas.height})")
