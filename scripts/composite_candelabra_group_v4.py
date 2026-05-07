"""
Candelabra hero image — v4.
Single bulb: LVTZ-CA12 (CA10 smoked candelabra base)
White background source — rembg removal, centered on dark canvas.
"""
from pathlib import Path
from rembg import remove
from PIL import Image
import numpy as np
import io

UPLOAD = Path("/home/ubuntu/upload")
OUT_DIR = Path("/home/ubuntu/alg-website/public/images/vintage-decor")
OUT_DIR.mkdir(parents=True, exist_ok=True)

SOURCE = "LVTZ-CA12.png"
ALPHA_THRESHOLD = 30
TARGET_H = 1300
CANVAS_PAD = 120

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

bulb = remove_bg(UPLOAD / SOURCE)

# Scale to target height
ratio = TARGET_H / bulb.height
new_w = int(bulb.width * ratio)
bulb = bulb.resize((new_w, TARGET_H), Image.LANCZOS)

canvas_w = new_w + 2 * CANVAS_PAD
canvas_h = TARGET_H + 2 * CANVAS_PAD

canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
canvas.paste(bulb, (CANVAS_PAD, CANVAS_PAD), bulb)

out_path = OUT_DIR / "glasgow-candelabra-group.png"
canvas.save(out_path, "PNG")
print(f"Saved → {out_path.relative_to(Path('/home/ubuntu/alg-website'))}  ({canvas.width}×{canvas.height})")
