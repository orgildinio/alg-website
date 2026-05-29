#!/usr/bin/env python3
"""
CFG-NAMING-1 v2 — planoARCH -I suffix drop + app code fixes
Patches 1-6 + 8 from PROMPT.md 2026-05-29 PM
"""
import re
import sys

BASE = "/home/ubuntu/alg-website-src/public/products"

patches = [
    # (slug, list of (old_string, new_string, description))
    ("trackstar", [
        # Patch 1: Trackstar-I → Trackstar (everywhere)
        ("Trackstar-I", "Trackstar", "drop -I suffix"),
        # Also catch any LCTS that might have crept in (gate shows 0 already, but be safe)
        ("LCTS · Trackstar", "LTRK · Trackstar", "app code LCTS→LTRK"),
        ("LCTS", "LTRK", "app code LCTS→LTRK bare"),
    ]),
    ("lara", [
        # Patch 2: LARA-I → Lara, Lara-I → Lara, LARA → Lara
        ("LARA-I", "Lara", "drop -I + title case"),
        ("Lara-I", "Lara", "drop -I"),
        ("LARA", "Lara", "title case all-caps"),
    ]),
    ("luna", [
        # Patch 3: LUNA-I → Luna, Luna-I → Luna, LUNA → Luna
        ("LUNA-I", "Luna", "drop -I + title case"),
        ("Luna-I", "Luna", "drop -I"),
        ("LUNA", "Luna", "title case all-caps"),
    ]),
    ("waymark", [
        # Patch 4: Waymark-I → Waymark
        ("Waymark-I", "Waymark", "drop -I suffix"),
    ]),
    ("astra", [
        # Patch 5: Astra-I → Astra
        ("Astra-I", "Astra", "drop -I suffix"),
    ]),
    ("spectra", [
        # Patch 6: Spectra-I → Spectra
        ("Spectra-I", "Spectra", "drop -I suffix"),
    ]),
    ("solstice-safezone", [
        # Patch 8: LCDL/SZ → LCDL
        ("LCDL/SZ", "LCDL", "fix app code LCDL/SZ→LCDL"),
    ]),
]

total_changes = 0

for slug, replacements in patches:
    path = f"{BASE}/{slug}/index.html"
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"ERROR: {path} not found")
        sys.exit(1)

    original = content
    slug_changes = 0

    for old, new, desc in replacements:
        count = content.count(old)
        if count > 0:
            content = content.replace(old, new)
            print(f"  [{slug}] {desc}: '{old}' → '{new}' ({count} replacements)")
            slug_changes += count
        else:
            print(f"  [{slug}] {desc}: '{old}' NOT FOUND (0 replacements)")

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [{slug}] ✅ Written ({slug_changes} total replacements)")
        total_changes += slug_changes
    else:
        print(f"  [{slug}] ⚠️  No changes made")

print(f"\nTotal replacements across all files: {total_changes}")
