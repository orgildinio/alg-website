#!/usr/bin/env python3
"""
Patch A · cross_collection_sweep_v2.3
Add cityarch-pdp (where missing) + page-{slug}-pdp to all 7 canonical cityARCH static HTML body tags.
"""
import re
from pathlib import Path

REPO = Path('/home/ubuntu/alg-website-src')

# slug → desired body classes
PATCHES = {
    'lptp-symmetry-post-top':    'symmetry-pdp cityarch-pdp page-lptp-symmetry-post-top-pdp',
    'lpar-traffic-par38':        'cityarch-pdp page-lpar-traffic-par38-pdp',
    'ly-t10-slimline-sign-lamp': 'cityarch-pdp page-ly-t10-slimline-sign-lamp-pdp',
    'lrdw-abbey-roadway':        'cityarch-pdp page-lrdw-abbey-roadway-pdp',
    'lhmf-omnimax-high-mast':    'cityarch-pdp page-lhmf-omnimax-high-mast-pdp',
    'lptp-unity-post-top':       'cityarch-pdp page-lptp-unity-post-top-pdp',
    'lbol-sentry-bollard':       'cityarch-pdp page-lbol-sentry-bollard-pdp',
}

results = []
for slug, classes in PATCHES.items():
    path = REPO / 'public' / 'products' / slug / 'index.html'
    if not path.exists():
        results.append(f'  ❌ MISSING: {slug}')
        continue

    content = path.read_text(encoding='utf-8')

    # Find the actual <body ...> tag (the rendered one, not in JS comments)
    # Match the standalone <body> or <body class="..."> tag on its own line
    # Use a pattern that matches the opening body tag
    old_body = re.search(r'^<body[^>]*>$', content, re.MULTILINE)
    if not old_body:
        results.append(f'  ❌ NO BODY TAG FOUND: {slug}')
        continue

    old_tag = old_body.group(0)
    new_tag = f'<body class="{classes}">'

    if old_tag == new_tag:
        results.append(f'  ✅ ALREADY CORRECT: {slug} → {old_tag}')
        continue

    new_content = content[:old_body.start()] + new_tag + content[old_body.end():]
    path.write_text(new_content, encoding='utf-8')
    results.append(f'  ✅ PATCHED: {slug}\n     {old_tag} → {new_tag}')

print('\n'.join(results))
print('\nDone.')
