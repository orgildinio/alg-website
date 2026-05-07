"""
Remove background from LSL Series (string light) and Pathfinder (canopy) images.
Uses gentle alpha matting to preserve white/clear optics.
"""
from rembg import remove, new_session
from PIL import Image
import io, os

session = new_session(
    model_name="u2net",
    alpha_matting=True,
    alpha_matting_foreground_threshold=240,
    alpha_matting_background_threshold=10,
    alpha_matting_erode_size=10,
)

OUT_DIR = "/home/ubuntu/alg-website/public/images/family-cards/luxoarch"
os.makedirs(OUT_DIR, exist_ok=True)

jobs = [
    ("/home/ubuntu/upload/pasted_file_0AJ1bx_InsertPic_9310(0(05-11-09-59-07).jpg", "lsl-series.png"),
    ("/home/ubuntu/upload/Pathfinder.webp", "pathfinder.png"),
]

for src_path, out_name in jobs:
    print(f"Processing {src_path} ...")
    with open(src_path, "rb") as f:
        data = f.read()
    result = remove(
        data,
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=10,
    )
    img = Image.open(io.BytesIO(result)).convert("RGBA")
    out_path = os.path.join(OUT_DIR, out_name)
    img.save(out_path, "PNG")
    print(f"  Saved → {out_path}  ({img.size})")

print("Done.")
