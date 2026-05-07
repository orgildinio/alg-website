"""Replace guardian.png with background-removed version, with alpha cleanup."""
from rembg import remove
from PIL import Image
import numpy as np
import io

src = "/home/ubuntu/upload/Generatedimage.png"
dst = "/home/ubuntu/alg-website/public/images/family-cards/luxoarch/guardian.png"

with open(src, "rb") as f:
    raw = f.read()

result = remove(raw)
img = Image.open(io.BytesIO(result)).convert("RGBA")

# Aggressive alpha cleanup: push semi-transparent pixels to fully transparent
arr = np.array(img)
alpha = arr[:, :, 3]
# Any pixel with alpha < 200 becomes fully transparent
arr[alpha < 200, 3] = 0
# Any pixel with alpha >= 200 becomes fully opaque
arr[alpha >= 200, 3] = 255
img = Image.fromarray(arr, "RGBA")

# Trim transparent border
bbox = img.getbbox()
if bbox:
    img = img.crop(bbox)

img.save(dst, "PNG")
print(f"Saved {img.size} → {dst}")
