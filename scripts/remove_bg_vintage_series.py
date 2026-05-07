"""Remove backgrounds from 6 Vintage Décor series images and save to public directory."""
import subprocess, sys, os

# Install rembg if needed
try:
    from rembg import remove
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rembg[gpu]", "-q"])
    from rembg import remove

from PIL import Image
import io

inputs = [
    ("/home/ubuntu/upload/LVTS-ED19-pendant.png",  "public/images/vintage-decor/series-foundry-edison.png"),
    ("/home/ubuntu/upload/LVTS-VC19-pendant.png",  "public/images/vintage-decor/series-belgravia-victorian.png"),
    ("/home/ubuntu/upload/LVTS-G25-pendant2.png",  "public/images/vintage-decor/series-provence-globe.png"),
    ("/home/ubuntu/upload/LVTS-RD10-pendant.png",  "public/images/vintage-decor/series-marconi-radio.png"),
    ("/home/ubuntu/upload/LVTS-TB10-pendant.png",  "public/images/vintage-decor/series-brighton-tubular.png"),
    ("/home/ubuntu/upload/LVTZ-CA12.png",          "public/images/vintage-decor/series-glasgow-candelabra.png"),
]

os.makedirs("public/images/vintage-decor", exist_ok=True)

for src, dst in inputs:
    print(f"Processing {os.path.basename(src)} ...")
    with open(src, "rb") as f:
        data = f.read()
    result = remove(data)
    img = Image.open(io.BytesIO(result)).convert("RGBA")
    img.save(dst, "PNG")
    print(f"  Saved → {dst}  ({img.size[0]}×{img.size[1]})")

print("Done.")
