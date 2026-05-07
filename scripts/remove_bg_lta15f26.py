#!/usr/bin/env python3
"""Remove background from LTA15F26.png and save to nostalgic-decor image directory."""
import subprocess, sys, os

src = '/home/ubuntu/upload/LTA15F26.png'
out_dir = '/home/ubuntu/alg-website/public/images/family-cards/nostalgic-decor'
os.makedirs(out_dir, exist_ok=True)
out = f'{out_dir}/saarinen-a15.png'

# Try rembg first
try:
    result = subprocess.run(
        ['python3.11', '-c', f"""
from rembg import remove
from PIL import Image
import io

with open('{src}', 'rb') as f:
    inp = f.read()
out_bytes = remove(inp)
img = Image.open(io.BytesIO(out_bytes)).convert('RGBA')
img.save('{out}')
print('rembg done:', img.size)
"""],
        capture_output=True, text=True, timeout=120
    )
    print(result.stdout)
    if result.returncode != 0:
        print('rembg error:', result.stderr)
        raise Exception('rembg failed')
except Exception as e:
    print(f'rembg failed: {e}, trying PIL threshold...')
    from PIL import Image
    img = Image.open(src).convert('RGBA')
    data = img.getdata()
    new_data = []
    for r, g, b, a in data:
        # White/near-white background removal
        if r > 230 and g > 230 and b > 230:
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    img.save(out)
    print('PIL threshold done:', img.size)

print(f'Saved to: {out}')
