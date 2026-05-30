#!/usr/bin/env python3
"""
Fix relative src="assets/..." and src = 'assets/...' paths to absolute
/products/{slug}/assets/... in all 9 planoARCH submittal HTML files.
"""
import re, os

SLUGS = [
    'astra', 'solstice', 'solstice-safezone', 'spectra',
    'luxmark', 'lara', 'luna', 'waymark', 'retroarch-p1'
]

total_html = total_js = 0

for slug in SLUGS:
    f = f'public/products/{slug}/submittal/index.html'
    if not os.path.exists(f):
        print(f'  SKIP (missing): {f}')
        continue

    with open(f) as fh:
        content = fh.read()

    original = content
    prefix = f'/products/{slug}/'

    # Fix HTML src attributes: src="assets/...
    def fix_html_src(m):
        return f'src="{prefix}{m.group(1)}"'
    content, n1 = re.subn(r'src="(assets/[^"]+)"', fix_html_src, content)

    # Fix JS src assignments: src = 'assets/... or img.src = 'assets/...
    def fix_js_src(m):
        return f"{m.group(1)}'{prefix}{m.group(2)}'"
    content, n2 = re.subn(r"((?:img\.src|src)\s*=\s*)'(assets/[^']+)'", fix_js_src, content)

    # Fix JS template literals and string concatenations: 'assets/' + ...
    def fix_js_concat(m):
        return f"'{prefix}{m.group(1)}' + "
    content, n3 = re.subn(r"'(assets/[^']+)'\s*\+\s*", fix_js_concat, content)

    # Fix JS svgPath = 'assets/photometrics/...' + beam + '.svg' pattern
    def fix_js_svgpath(m):
        return f"var svgPath = '{prefix}{m.group(1)}' + "
    content, n4 = re.subn(r"var svgPath = '(assets/photometrics/[^']+)'\s*\+\s*", fix_js_svgpath, content)

    if content != original:
        with open(f, 'w') as fh:
            fh.write(content)
        remaining_html = len(re.findall(r'src="assets/', content))
        remaining_js = len(re.findall(r"src\s*=\s*'assets/", content))
        print(f'  ✅ {slug}: {n1} HTML + {n2} JS src + {n3} concat + {n4} svgPath fixed | remaining: {remaining_html} HTML, {remaining_js} JS')
        total_html += n1
        total_js += n2 + n3 + n4
    else:
        print(f'  — {slug}: no changes')

print(f'\nTotals: {total_html} HTML attrs, {total_js} JS refs fixed')
