#!/usr/bin/env python3
"""
add_canonical_classes.py — Patch 2: Add sec-eyebrow, sec-title, section-inner
canonical classes to all 8 multi-family PDPs.

Strategy:
1. Add 'sec-eyebrow' to all *-eyebrow class elements (p, div with *-eyebrow class)
2. Add 'sec-title' to all section h2 elements (first h2 in each section)
3. Add 'section-inner' to the first div inside each <section class="*-section">

This adds the canonical classes WITHOUT removing the existing product-specific ones.
"""
import re

SLUGS = ['gehry', 'nebula-ii', 'orbit-i', 'radius-ii', 'radius-safezone',
         'ecrescent', 'eclipse-ii', 'lunar-eclipse']
BASE = 'src/pages/products/multi-family'

def read(path):
    with open(path) as f: return f.read()

def write(path, content):
    with open(path, 'w') as f: f.write(content)

for slug in SLUGS:
    f = f'{BASE}/{slug}/index.astro'
    content = read(f)
    original = content
    
    # 1. Add sec-eyebrow to all *-eyebrow elements
    # Pattern: class="hf-eyebrow" → class="hf-eyebrow sec-eyebrow"
    # But NOT if it already has sec-eyebrow
    content = re.sub(
        r'class="([^"]*-eyebrow)(?!\s+sec-eyebrow)([^"]*)"',
        lambda m: f'class="{m.group(1)} sec-eyebrow{m.group(2)}"'
        if 'sec-eyebrow' not in m.group(0) else m.group(0),
        content
    )
    
    # 2. Add sec-title to h2 elements inside sections
    # Pattern: <h2 class="X"> → <h2 class="X sec-title">
    # Only h2 elements that don't already have sec-title
    content = re.sub(
        r'<h2 class="([^"]*)"(?![^>]*sec-title)',
        lambda m: f'<h2 class="{m.group(1)} sec-title">'
        if 'sec-title' not in m.group(0) else m.group(0),
        content
    )
    
    # Also handle h2 without class
    content = re.sub(
        r'<h2>',
        '<h2 class="sec-title">',
        content
    )
    
    # 3. Add section-inner to first div inside each <section class="*-section">
    # Pattern: <section class="X-section" ...>\n  <div class="Y"> → add section-inner
    content = re.sub(
        r'(<section class="[^"]*-section[^"]*"[^>]*>\s*\n\s*)(<div class=")(?!section-inner)',
        lambda m: m.group(1) + m.group(2) + 'section-inner ',
        content
    )
    
    if content != original:
        write(f, content)
        # Count canonical classes
        ec = content.count('sec-eyebrow')
        tc = content.count('sec-title')
        ic = content.count('section-inner')
        print(f'  ✅ {slug}: sec-eyebrow={ec}, sec-title={tc}, section-inner={ic}')
    else:
        print(f'  — {slug}: no changes')

print("Done.")
