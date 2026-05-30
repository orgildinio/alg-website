#!/usr/bin/env python3
"""
cross_collection_sweep_v2.1 — Patches F through J
"""
import re
from pathlib import Path

ROOT = Path('/home/ubuntu/alg-website-src')

def read(p): return p.read_text(encoding='utf-8')
def write(p, t): p.write_text(t, encoding='utf-8')

changes = []

# ─── PATCH F: Restore Ⓐ glyph in multi-fAMILY tab titles ──────────────────
print("=== Patch F: Restore Ⓐ glyph in multi-fAMILY tab titles ===")

# Multi-family PDPs are Astro wrappers
MF_SLUGS = ['gehry', 'nebula-ii', 'orbit-i', 'radius-ii', 'radius-safezone',
            'ecrescent', 'eclipse-ii', 'lunar-eclipse']

for slug in MF_SLUGS:
    astro_file = ROOT / f'src/pages/products/multi-family/{slug}/index.astro'
    if not astro_file.exists():
        print(f"  SKIP {slug}: file not found")
        continue
    content = read(astro_file)
    # Find the title prop in frontmatter
    # Pattern: title="multi-fAMILY · ProductName Series | Archipelago Lighting"
    # The Ⓐ should be in "multi-fⒶMILY" not "multi-fAMILY"
    
    # Check if title already has Ⓐ glyph
    if 'multi-f\u24b6MILY' in content or 'multi-fⒶMILY' in content:
        print(f"  OK {slug}: already has Ⓐ glyph")
        continue
    
    # Replace "multi-fAMILY" with "multi-fⒶMILY" in title prop only
    # The title prop is in the frontmatter: title="..."
    new_content = content.replace('multi-fAMILY', 'multi-f\u24b6MILY')
    if new_content != content:
        write(astro_file, new_content)
        count = content.count('multi-fAMILY')
        print(f"  Fixed {slug}: {count} occurrences")
        changes.append(f"Patch F: {slug}")
    else:
        print(f"  WARN {slug}: 'multi-fAMILY' not found in title")
        # Check what the title looks like
        m = re.search(r'title="([^"]*)"', content)
        if m:
            print(f"    Current title: {m.group(1)[:80]}")

# Also fix the multi-family collection page
mf_collection = ROOT / 'src/pages/collections/multi-family.astro'
if mf_collection.exists():
    content = read(mf_collection)
    if 'multi-fAMILY' in content and 'multi-f\u24b6MILY' not in content:
        new_content = content.replace('multi-fAMILY', 'multi-f\u24b6MILY')
        write(mf_collection, new_content)
        print(f"  Fixed collection page: multi-fAMILY → multi-fⒶMILY")
        changes.append("Patch F: collection page")
    else:
        print(f"  Collection page: {'OK' if 'multi-f' + chr(0x24b6) + 'MILY' in content else 'no multi-fAMILY found'}")

# ─── PATCH G: CFG-CHROME-4 mega-menu scroll-hide ────────────────────────────
print("\n=== Patch G: CFG-CHROME-4 mega-menu scroll-hide ===")

# Find the outermost shared layout
base_layout = ROOT / 'src/layouts/BaseLayout.astro'
site_layout = ROOT / 'src/layouts/SiteLayout.astro'

layout_file = None
for f in [base_layout, site_layout]:
    if f.exists():
        layout_file = f
        break

if not layout_file:
    # Search for any layout file
    for f in (ROOT / 'src/layouts').glob('*.astro'):
        layout_file = f
        break

if layout_file:
    content = read(layout_file)
    if 'CFG-CHROME-4' in content:
        print(f"  OK: CFG-CHROME-4 already present in {layout_file.name}")
    else:
        scroll_script = '''
<script>
  // CFG-CHROME-4 · mega-menu hides on scroll-down, shows on scroll-up
  (function () {
    const header = document.getElementById('site-header');
    if (!header) return;
    header.style.transition = 'transform 0.25s ease-out';
    let lastY = window.scrollY;
    let hidden = false;
    window.addEventListener('scroll', () => {
      const y = window.scrollY;
      const delta = y - lastY;
      if (y <= 0) {
        header.style.transform = 'translateY(0)';
        hidden = false;
      } else if (delta > 5 && !hidden) {
        header.style.transform = 'translateY(-100%)';
        hidden = true;
      } else if (delta < -5 && hidden) {
        header.style.transform = 'translateY(0)';
        hidden = false;
      }
      lastY = y;
    }, { passive: true });
  })();
</script>
'''
        # Insert just before </body>
        if '</body>' in content:
            new_content = content.replace('</body>', scroll_script + '</body>')
            write(layout_file, new_content)
            print(f"  Added CFG-CHROME-4 script to {layout_file.name}")
            changes.append("Patch G: CFG-CHROME-4")
        else:
            print(f"  WARN: No </body> tag found in {layout_file.name}")
else:
    print("  WARN: No layout file found")

# ─── PATCH H: Nightwatch + Watchtower tier corrections ──────────────────────
print("\n=== Patch H: Tier corrections ===")

tier_fixes = {
    'nightwatch': {
        'class_from': 'tier-badge tier-pro-plus',
        'class_to': 'tier-badge tier-pro',
        'text_from': '>PRO+<',
        'text_to': '>PRO<',
        'eyebrow_from': '· PRO+',
        'eyebrow_to': '· PRO',
    },
    'watchtower': {
        'class_from': 'tier-badge tier-pro-plus',
        'class_to': 'tier-badge tier-eco',
        'text_from': '>PRO+<',
        'text_to': '>ECO<',
        'eyebrow_from': '· PRO+',
        'eyebrow_to': '· ECO',
    },
}

for slug, fix in tier_fixes.items():
    # Fix PDP source
    astro_file = ROOT / f'src/pages/products/{slug}/index.astro'
    if astro_file.exists():
        content = read(astro_file)
        new_content = content
        new_content = new_content.replace(fix['class_from'], fix['class_to'])
        new_content = new_content.replace(fix['text_from'], fix['text_to'])
        new_content = new_content.replace(fix['eyebrow_from'], fix['eyebrow_to'])
        if new_content != content:
            write(astro_file, new_content)
            print(f"  Fixed {slug} PDP: PRO+ → {fix['text_to'].strip('><')}")
            changes.append(f"Patch H: {slug} PDP")
        else:
            print(f"  OK {slug} PDP: no PRO+ found (checking...)")
            # Check what tier is there
            m = re.search(r'tier-badge[^"]*"', content)
            if m:
                print(f"    Current tier class: {m.group()}")
    
    # Fix submittal page
    submittal_file = ROOT / f'public/products/{slug}/submittal/index.html'
    if submittal_file.exists():
        content = read(submittal_file)
        new_content = content
        new_content = new_content.replace(fix['class_from'], fix['class_to'])
        new_content = new_content.replace(fix['text_from'], fix['text_to'])
        new_content = new_content.replace(fix['eyebrow_from'], fix['eyebrow_to'])
        if new_content != content:
            write(submittal_file, new_content)
            print(f"  Fixed {slug} submittal")
            changes.append(f"Patch H: {slug} submittal")
        else:
            print(f"  OK {slug} submittal: no changes needed")

# ─── PATCH I: Sitewide PDP font-family override ─────────────────────────────
print("\n=== Patch I: Sitewide PDP font-family override ===")

# Find the global CSS file
global_css_candidates = [
    ROOT / 'src/styles/global.css',
    ROOT / 'src/styles/main.css',
    ROOT / 'src/styles/base.css',
    ROOT / 'public/styles/global.css',
]

# Also check src/layouts for inline styles
css_file = None
for f in global_css_candidates:
    if f.exists():
        css_file = f
        break

if not css_file:
    # Search for CSS files
    for f in (ROOT / 'src').rglob('*.css'):
        if 'global' in f.name.lower() or 'main' in f.name.lower() or 'base' in f.name.lower():
            css_file = f
            break

if css_file:
    content = read(css_file)
    if 'CFG-TYPE-1 v3' in content:
        print(f"  OK: CFG-TYPE-1 v3 already present in {css_file}")
    else:
        font_override = '''
/* CFG-TYPE-1 v3 · Sitewide PDP Lato override · 2026-05-30 */
/* Overrides Cormorant Garamond (luxoARCH/planoARCH default) and Sora (multi-fAMILY legacy) */
/* Specificity: body.{collection}-pdp h1 > body.page-{slug}-pdp h1 */
body.luxoarch-pdp h1,
body.luxoarch-pdp h2,
body.planoarch-pdp h1,
body.planoarch-pdp h2,
body.cityarch-pdp h1,
body.cityarch-pdp h2,
body.multifamily-pdp h1,
body.multifamily-pdp h2 {
  font-family: Lato, system-ui, sans-serif !important;
}
'''
        write(css_file, content + font_override)
        print(f"  Added CFG-TYPE-1 v3 to {css_file}")
        changes.append("Patch I: font override")
else:
    # Add to BaseLayout inline style
    if layout_file and layout_file.exists():
        content = read(layout_file)
        if 'CFG-TYPE-1 v3' not in content:
            font_override = '''<style>
/* CFG-TYPE-1 v3 · Sitewide PDP Lato override · 2026-05-30 */
body.luxoarch-pdp h1, body.luxoarch-pdp h2,
body.planoarch-pdp h1, body.planoarch-pdp h2,
body.cityarch-pdp h1, body.cityarch-pdp h2,
body.multifamily-pdp h1, body.multifamily-pdp h2 {
  font-family: Lato, system-ui, sans-serif !important;
}
</style>
'''
            # Insert before </head>
            if '</head>' in content:
                new_content = content.replace('</head>', font_override + '</head>')
                write(layout_file, new_content)
                print(f"  Added CFG-TYPE-1 v3 inline to {layout_file.name}")
                changes.append("Patch I: font override inline")
    else:
        print("  WARN: No CSS file or layout found for font override")

# ─── PATCH J.2: Gehry canonical classes ─────────────────────────────────────
print("\n=== Patch J.2: Gehry canonical classes ===")

gehry_file = ROOT / 'src/pages/products/multi-family/gehry/index.astro'
if gehry_file.exists():
    content = read(gehry_file)
    section_inner_count = content.count('class="section-inner"')
    print(f"  Gehry current section-inner count: {section_inner_count}")
    
    if section_inner_count >= 6:
        print(f"  OK: Gehry already has {section_inner_count} section-inner elements")
    else:
        # The add_canonical_classes.py script should handle this
        # Let me check what sections Gehry has
        sections = re.findall(r'<section[^>]*id="([^"]*)"', content)
        print(f"  Gehry sections: {sections}")
        
        # Apply canonical classes to each section
        # Pattern: <section id="..."> → add section-inner wrapper
        # Check if sections already have section-inner
        new_content = content
        applied = 0
        
        for section_id in sections:
            # Find the section and check if it has section-inner
            pattern = f'<section[^>]*id="{section_id}"[^>]*>(.*?)</section>'
            m = re.search(pattern, new_content, re.DOTALL)
            if m:
                section_body = m.group(1)
                if 'section-inner' not in section_body:
                    # Add section-inner wrapper
                    # Find the opening tag
                    open_tag_end = new_content.find('>', new_content.find(f'id="{section_id}"')) + 1
                    close_tag_start = new_content.rfind('</section>', 0, new_content.find(f'id="{section_id}"') + 10000)
                    if close_tag_start > open_tag_end:
                        inner = new_content[open_tag_end:close_tag_start]
                        wrapped = f'\n  <div class="section-inner">{inner}  </div>\n'
                        new_content = new_content[:open_tag_end] + wrapped + new_content[close_tag_start:]
                        applied += 1
        
        if applied > 0:
            write(gehry_file, new_content)
            print(f"  Applied section-inner wrapper to {applied} sections in Gehry")
            changes.append(f"Patch J.2: Gehry {applied} section-inner wrappers")
        else:
            print(f"  No sections needed wrapping in Gehry")
else:
    print(f"  WARN: Gehry file not found at {gehry_file}")

print(f"\n=== Patches F-J complete: {len(changes)} changes ===")
for c in changes:
    print(f"  {c}")
