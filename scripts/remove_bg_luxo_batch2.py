#!/usr/bin/env python3
"""
Gentle background removal for luxoARCH product images.
Uses rembg with post-processing to preserve white optics/lenses.
"""
import os
import shutil
from pathlib import Path
from PIL import Image
import io

# Mapping: upload filename -> (family slug, output filename)
IMAGES = [
    ("LIBERTY_brown(5).webp",       "liberty",    "liberty-card.png"),
    ("LCNP-pendant-knock-out-1.webp","pathfinder", "pathfinder-card.png"),
    ("LDKT-CanadArm(2).webp",       "canadarm",   "canadarm-card.png"),
    ("LSPL-Black-Side01.webp",      "radiator-i", "radiator-i-card.png"),
    ("600W(2).webp",                "radiator-ii","radiator-ii-card.png"),
    ("600WLaserpointer.webp",       "radiator-iii","radiator-iii-card.png"),
    ("LWPF-Guardian.6.webp",        "guardian",   "guardian-card.png"),
    ("SENTINEL-02.webp",            "sentinel",   "sentinel-card.png"),
]

UPLOAD_DIR = Path("/home/ubuntu/upload")
OUT_DIR = Path("/home/ubuntu/alg-website/public/images/products/card-images")
OUT_DIR.mkdir(parents=True, exist_ok=True)

from rembg import remove, new_session

# Use u2net model - good balance of quality and speed
session = new_session("u2net")

for upload_name, slug, out_name in IMAGES:
    src = UPLOAD_DIR / upload_name
    dst = OUT_DIR / out_name
    
    print(f"Processing {upload_name} -> {out_name} ...", flush=True)
    
    with open(src, "rb") as f:
        input_data = f.read()
    
    # Remove background
    output_data = remove(
        input_data,
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=10,
    )
    
    # Open result and do a gentle cleanup pass
    img = Image.open(io.BytesIO(output_data)).convert("RGBA")
    
    # Restore near-white pixels that rembg may have made transparent
    # (preserves white optics/lenses)
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            # If pixel was near-white and got partially transparent, restore it
            # Only restore if it was originally a very light pixel
            if a < 200 and r > 200 and g > 200 and b > 200:
                # Check if this looks like a lens/optic pixel (high brightness)
                brightness = (r + g + b) / 3
                if brightness > 210:
                    pixels[x, y] = (r, g, b, 255)
    
    img.save(dst, "PNG", optimize=True)
    size_kb = dst.stat().st_size // 1024
    print(f"  -> Saved {out_name} ({img.size[0]}x{img.size[1]}, {size_kb}KB)", flush=True)

print("\nAll done!")
