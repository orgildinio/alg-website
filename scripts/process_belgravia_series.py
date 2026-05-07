"""
Process the Belgravia Victorian series card image for the collection page.
Remove background, save as PNG.
"""
from pathlib import Path
from rembg import remove
from PIL import Image
import io

src = Path("/home/ubuntu/upload/LTVC19V_MB-SP(2).jpg")
out = Path("/home/ubuntu/alg-website/public/images/vintage-decor/series-belgravia-victorian.png")

print(f"Processing {src.name} ...")
data = src.read_bytes()
result = remove(data)
img = Image.open(io.BytesIO(result)).convert("RGBA")
bbox = img.getbbox()
img = img.crop(bbox)
print(f"  Cropped to {img.width}×{img.height}")
img.save(out, "PNG")
print(f"Saved → {out.relative_to(Path('/home/ubuntu/alg-website'))}")
