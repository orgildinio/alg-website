#!/usr/bin/env python3
"""Update card_image paths for 8 luxoARCH families in sku-index.json."""
import json
from pathlib import Path

SKU_INDEX = Path("/home/ubuntu/alg-website/src/data/sku-index.json")

# family slug -> new card image path
UPDATES = {
    "liberty":     "/images/products/card-images/liberty-card.png",
    "pathfinder":  "/images/products/card-images/pathfinder-card.png",
    "canadarm":    "/images/products/card-images/canadarm-card.png",
    "radiator-i":  "/images/products/card-images/radiator-i-card.png",
    "radiator-ii": "/images/products/card-images/radiator-ii-card.png",
    "radiator-iii":"/images/products/card-images/radiator-iii-card.png",
    "guardian":    "/images/products/card-images/guardian-card.png",
    "sentinel":    "/images/products/card-images/sentinel-card.png",
}

with open(SKU_INDEX) as f:
    data = json.load(f)

updated = []
for family in data.get("families", []):
    slug = family.get("slug", "")
    if slug in UPDATES:
        family["card_image"] = UPDATES[slug]
        updated.append(slug)

with open(SKU_INDEX, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Updated {len(updated)} families: {updated}")
