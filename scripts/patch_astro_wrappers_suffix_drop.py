#!/usr/bin/env python3
"""
Patch Astro wrappers for planoARCH -I suffix drop + app code fixes.
Updates hardcoded title= and description= props in each wrapper.
"""
import re

BASE = "/home/ubuntu/alg-website-src/src/pages/products"

patches = {
    "trackstar": {
        "old_title": 'title="LCTS · Trackstar-I — Archipelago Lighting Group"',
        "new_title": 'title="LTRK · Trackstar — Archipelago Lighting Group"',
        "old_desc": 'description="LCTS Trackstar-I · planoⒶRCH PRO · Commercial Track Head · 3 sizes · DLC Premium · CRI 90+."',
        "new_desc": 'description="LTRK Trackstar · planoⒶRCH PRO · Commercial Track Head · 3 sizes · DLC Premium · CRI 90+."',
    },
    "lara": {
        "old_title": 'title="LUXA · Lara-I — Archipelago Lighting Group"',
        "new_title": 'title="LUXA · Lara — Archipelago Lighting Group"',
        "old_desc": 'description="LUXA Lara-I · planoⒶRCH PRO · Architectural Linear · 2/4/8 ft · DLC Premium · CRI 90+."',
        "new_desc": 'description="LUXA Lara · planoⒶRCH PRO · Architectural Linear · 2/4/8 ft · DLC Premium · CRI 90+."',
    },
    "luna": {
        "old_title": 'title="LUXA · Luna-I — Archipelago Lighting Group"',
        "new_title": 'title="LUXA · Luna — Archipelago Lighting Group"',
        "old_desc": 'description="LUXA Luna-I · planoⒶRCH PRO · Architectural Linear · 2/3/4/8 ft · DLC Premium · CRI 90+."',
        "new_desc": 'description="LUXA Luna · planoⒶRCH PRO · Architectural Linear · 2/3/4/8 ft · DLC Premium · CRI 90+."',
    },
    "waymark": {
        "old_title": 'title="LWRL · Waymark-I — Archipelago Lighting Group"',
        "new_title": 'title="LWRL · Waymark — Archipelago Lighting Group"',
        "old_desc": 'description="LWRL Waymark-I · planoⒶRCH PRO · Commercial Wall-Wash Linear · 2/4 ft · DLC Premium · CRI 90+."',
        "new_desc": 'description="LWRL Waymark · planoⒶRCH PRO · Commercial Wall-Wash Linear · 2/4 ft · DLC Premium · CRI 90+."',
    },
    "solstice-safezone": {
        "old_title": 'title="LCDL/SZ · Solstice SafeZone — Archipelago Lighting Group"',
        "new_title": 'title="LCDL · Solstice SafeZone — Archipelago Lighting Group"',
        "old_desc": 'description="LCDL/SZ Solstice SafeZone · planoⒶRCH PRO · Wet-Location Surface-Mount Downlight · IP65 · DLC Premium."',
        "new_desc": 'description="LCDL Solstice SafeZone · planoⒶRCH PRO · Wet-Location Surface-Mount Downlight · IP65 · DLC Premium."',
    },
}

# Also do a general -I sweep on all 7 wrappers for any remaining -I in the wrapper text
all_slugs = ["trackstar", "lara", "luna", "waymark", "astra", "spectra", "solstice-safezone"]
names = ["Astra", "Spectra", "Trackstar", "Lara", "Luna", "Waymark", "LARA", "LUNA"]

for slug in all_slugs:
    path = f"{BASE}/{slug}/index.astro"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    # Apply specific patches
    if slug in patches:
        p = patches[slug]
        if p["old_title"] in content:
            content = content.replace(p["old_title"], p["new_title"])
            print(f"  [{slug}] title: patched")
        else:
            print(f"  [{slug}] title: NOT FOUND (already correct?)")
        if p["old_desc"] in content:
            content = content.replace(p["old_desc"], p["new_desc"])
            print(f"  [{slug}] description: patched")
        else:
            print(f"  [{slug}] description: NOT FOUND (already correct?)")

    # General -I sweep
    for name in names:
        old = f"{name}-I"
        if old in content:
            count = content.count(old)
            content = content.replace(old, name)
            print(f"  [{slug}] {old} → {name}: {count} replacements")

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [{slug}] ✅ Written")
    else:
        print(f"  [{slug}] no changes")
