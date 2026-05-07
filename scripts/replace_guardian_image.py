"""Replace guardian.png with background-removed version of the new source image."""
from rembg import remove
from PIL import Image
import io, shutil

src = "/home/ubuntu/upload/Generatedimage.png"
dst = "/home/ubuntu/alg-website/public/images/family-cards/luxoarch/guardian.png"

with open(src, "rb") as f:
    raw = f.read()

result = remove(raw)
img = Image.open(io.BytesIO(result)).convert("RGBA")

# Trim transparent border
bbox = img.getbbox()
if bbox:
    img = img.crop(bbox)

# Save with transparency
img.save(dst, "PNG")
print(f"Saved {img.size} → {dst}")
