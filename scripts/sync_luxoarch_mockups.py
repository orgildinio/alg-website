#!/usr/bin/env python3
"""
Sync luxoARCH mockups into Astro wrappers.

For each PDP:
1. Keep the Astro wrapper's frontmatter + BaseLayout + JSON-LD header
2. Replace <style is:global>...</style> with mockup's <style>...</style>
3. Replace body content with mockup's <body> content
4. Convert relative asset paths to absolute /products/{slug}/assets/ paths
5. Convert relative sentinel roundout paths to /products/sentinel/assets/roundout/
6. Apply Wedge-specific fix: strip id="photometrics" div content
7. Apply R5 fix: ENGINEERING IN MOTION uppercase in Illuminator + Sentinel

Strategy: preserve everything before the first <style is:global> in the Astro wrapper,
then replace from there to </BaseLayout> with the mockup content.
"""

import re
import os

REPO = "/home/ubuntu/alg-website-src"
MOCKUP_DIR = "/home/ubuntu/upload/luxoARCH_bundle/source/mockups"

# Mapping: mockup filename → Astro slug
MOCKUP_MAP = {
    "mockup_illuminator_pdp_v2.html": "illuminator",
    "mockup_anaheim_pdp_v1.html": "anaheim",
    "mockup_atlanta_pdp_v1.html": "atlanta",
    "mockup_aura_pdp_v1.html": "aura",
    "mockup_everest_pdp_v1.html": "everest",
    "mockup_guardian_pdp_v1.html": "guardian",
    "mockup_heritage_pdp_v1.html": "heritage",
    "mockup_liberty_pdp_v1.html": "liberty",
    "mockup_navigator_pdp_v1.html": "navigator",
    "mockup_nightwatch_pdp_v1.html": "nightwatch",
    "mockup_pathfinder_pdp_v1.html": "pathfinder",
    "mockup_radiator_pdp_v1.html": "radiator",
    "mockup_ramparts_pdp_v1.html": "ramparts",
    "mockup_sentinel_pdp_v1.html": "sentinel",
    "mockup_watchtower_pdp_v1.html": "watchtower",
    "mockup_wedge_pdp_v1.html": "wedge",
}

def extract_astro_header(astro_content):
    """Extract everything from start to (but not including) <style is:global>"""
    idx = astro_content.find('<style is:global>')
    if idx == -1:
        raise ValueError("Could not find <style is:global> in Astro wrapper")
    return astro_content[:idx]

def extract_astro_footer(astro_content):
    """Extract </BaseLayout> at the end"""
    idx = astro_content.rfind('</BaseLayout>')
    if idx == -1:
        raise ValueError("Could not find </BaseLayout> in Astro wrapper")
    return astro_content[idx:]

def extract_mockup_style(mockup_content):
    """Extract the content of the <style> block from the mockup head"""
    m = re.search(r'<style[^>]*>([\s\S]*?)</style>', mockup_content, re.IGNORECASE)
    if not m:
        raise ValueError("Could not find <style> in mockup")
    return m.group(1)

def extract_mockup_body(mockup_content):
    """Extract the content between <body ...> and </body>"""
    m = re.search(r'<body[^>]*>([\s\S]*)</body>', mockup_content, re.IGNORECASE)
    if not m:
        raise ValueError("Could not find <body> in mockup")
    return m.group(1)

def fix_asset_paths(content, slug):
    """
    Convert relative asset paths to absolute /products/{slug}/assets/ paths.
    Patterns to fix:
    - src="assets/{slug}/..." → src="/products/{slug}/assets/..."
    - src="assets/sentinel/roundout/..." → src="/products/sentinel/assets/roundout/..."
    - href="assets/..." → href="/products/{slug}/assets/..."
    """
    # Fix sentinel roundout paths (used across multiple PDPs)
    content = re.sub(
        r'(src|href)="assets/sentinel/roundout/',
        r'\1="/products/sentinel/assets/roundout/',
        content
    )
    # Fix product-specific asset paths
    content = re.sub(
        r'(src|href)="assets/' + re.escape(slug) + r'/',
        r'\1="/products/' + slug + r'/assets/',
        content
    )
    # Fix generic "assets/" paths that don't have a product prefix
    # These are typically: assets/hero/..., assets/dimensions/..., etc.
    # Convert to /products/{slug}/assets/...
    content = re.sub(
        r'(src|href)="assets/(?!' + re.escape(slug) + r'|sentinel)',
        r'\1="/products/' + slug + r'/assets/',
        content
    )
    return content

def fix_photometric_paths(content, slug):
    """
    Fix polar SVG paths from ../../luxoARCH_PolarPlots/{Slug}-I/ 
    to /products/{slug}/assets/photometrics/
    """
    # Pattern: ../../luxoARCH_PolarPlots/Anaheim-I/LWPA40_3000K.svg
    content = re.sub(
        r'[./]*luxoARCH_PolarPlots/[^/]+/',
        f'/products/{slug}/assets/photometrics/',
        content
    )
    # Also fix any remaining relative photometrics paths
    content = re.sub(
        r"'[./]*assets/" + re.escape(slug) + r"/photometrics/",
        f"'/products/{slug}/assets/photometrics/",
        content
    )
    # Fix quoted paths in JS objects
    content = re.sub(
        r'"[./]*assets/' + re.escape(slug) + r'/photometrics/',
        f'"/products/{slug}/assets/photometrics/',
        content
    )
    return content

def fix_wedge_photometrics(content):
    """
    Remove the id="photometrics" div from Wedge (section omitted per K5).
    Keep the sticky-nav href="#photometrics" link.
    """
    # Remove the deferred photometrics div
    content = re.sub(
        r'<div id="photometrics"[^>]*>[\s\S]*?</div>\s*',
        '',
        content,
        count=1
    )
    return content

def apply_r5_motion_eyebrow(content):
    """R5: Change 'Engineering In Motion' → 'ENGINEERING IN MOTION' in motion eyebrow"""
    content = content.replace('Engineering In Motion', 'ENGINEERING IN MOTION')
    return content

def sync_pdp(mockup_filename, slug):
    mockup_path = os.path.join(MOCKUP_DIR, mockup_filename)
    astro_path = os.path.join(REPO, "src/pages/products", slug, "index.astro")
    
    if not os.path.exists(mockup_path):
        print(f"  [{slug}] ERROR: mockup not found: {mockup_path}")
        return False
    if not os.path.exists(astro_path):
        print(f"  [{slug}] ERROR: Astro wrapper not found: {astro_path}")
        return False
    
    with open(mockup_path, 'r', encoding='utf-8') as f:
        mockup_content = f.read()
    with open(astro_path, 'r', encoding='utf-8') as f:
        astro_content = f.read()
    
    try:
        # Extract parts
        astro_header = extract_astro_header(astro_content)
        astro_footer = extract_astro_footer(astro_content)
        mockup_style = extract_mockup_style(mockup_content)
        mockup_body = extract_mockup_body(mockup_content)
        
        # Fix asset paths in body
        mockup_body = fix_asset_paths(mockup_body, slug)
        mockup_body = fix_photometric_paths(mockup_body, slug)
        
        # Wedge-specific: remove photometrics section
        if slug == 'wedge':
            mockup_body = fix_wedge_photometrics(mockup_body)
            print(f"  [{slug}] Applied Wedge photometrics omission")
        
        # R5: motion eyebrow uppercase for illuminator and sentinel
        if slug in ('illuminator', 'sentinel'):
            mockup_body = apply_r5_motion_eyebrow(mockup_body)
            print(f"  [{slug}] Applied R5 motion eyebrow uppercase")
        
        # Assemble new Astro wrapper
        new_content = (
            astro_header +
            '<style is:global>\n' +
            mockup_style +
            '\n</style>\n' +
            mockup_body + '\n' +
            astro_footer + '\n'
        )
        
        with open(astro_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  [{slug}] ✅ Synced ({len(new_content)} chars)")
        return True
        
    except Exception as e:
        print(f"  [{slug}] ERROR: {e}")
        return False

# Run sync for all 16 PDPs
success = 0
fail = 0
for mockup_file, slug in MOCKUP_MAP.items():
    result = sync_pdp(mockup_file, slug)
    if result:
        success += 1
    else:
        fail += 1

print(f"\nDone: {success} synced, {fail} failed")
