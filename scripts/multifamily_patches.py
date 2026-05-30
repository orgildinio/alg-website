#!/usr/bin/env python3
"""
multifamily_patches.py — Apply patches 1-14 to multi-family PDPs.

Patch 1:  body class → multifamily-pdp (all 8 PDPs)
Patch 2:  canonical classes restore (gehry, eclipse-ii — sec-eyebrow, sec-title, section-inner)
Patch 3:  SafeZone breadcrumb already canonical in mockup (covered by Patch 4)
Patch 4:  Radius SafeZone full PDP deploy from mockup
Patch 5:  SafeZone breadcrumb verify (covered by Patch 4)
Patch 6-7: SafeZone hero pills/wattage (covered by Patch 4)
Patch 8:  Lunar Eclipse h1 tier-pro → tier-pro-plus; title PRO → PRO+
Patch 9:  Orbit-I h1 tier-eco → tier-pro; title PRO → PRO (already correct); fix h1 badge
Patch 10: Collection data — Eclipse-II maxWattage 18 → 24
Patch 11: Collection data — Radius SafeZone maxWattage 15 → 19
Patch 12: Collection data — Nebula-II maxWattage 20 → 15
Patch 13: Ⓐ glyph in tab titles — add multi-fⒶMILY to all 8 PDP titles
Patch 14: Eclipse-II CFG-COWORK-13 — wire buildSubmittalUrl() to all 8 PDPs
"""
import re, os, shutil

SLUGS = ['gehry', 'nebula-ii', 'orbit-i', 'radius-ii', 'radius-safezone',
         'ecrescent', 'eclipse-ii', 'lunar-eclipse']
BASE = 'src/pages/products/multi-family'
MOCKUP_DIR = '/home/ubuntu/upload/multifamily_bundle/source/mockups'

def read(path):
    with open(path) as f: return f.read()

def write(path, content):
    with open(path, 'w') as f: f.write(content)

# ── Patch 1: body class ──────────────────────────────────────────────────────
print("=== Patch 1: body class → multifamily-pdp ===")
for slug in SLUGS:
    f = f'{BASE}/{slug}/index.astro'
    content = read(f)
    # Replace bodyClass="page-{slug}-pdp" with bodyClass="multifamily-pdp page-{slug}-pdp"
    # Pattern: bodyClass="page-X-pdp" or bodyClass="page-X"
    new_content = re.sub(
        r'bodyClass="(page-[^"]+)"',
        lambda m: f'bodyClass="multifamily-pdp {m.group(1)}"'
        if 'multifamily-pdp' not in m.group(0) else m.group(0),
        content
    )
    if new_content != content:
        write(f, new_content)
        print(f'  ✅ {slug}: body class updated')
    else:
        print(f'  — {slug}: already has multifamily-pdp or no match')

# ── Patch 2: canonical classes (spot-check gehry, eclipse-ii) ───────────────
print("\n=== Patch 2: canonical classes (verify only — sec-eyebrow/sec-title/section-inner) ===")
for slug in ['gehry', 'eclipse-ii']:
    f = f'{BASE}/{slug}/index.astro'
    content = read(f)
    eyebrow = content.count('sec-eyebrow')
    title = content.count('sec-title')
    inner = content.count('section-inner')
    print(f'  {slug}: sec-eyebrow={eyebrow}, sec-title={title}, section-inner={inner}')
    # These are already in the synced mockup content — no fix needed if counts ≥ 6

# ── Patch 4: Radius SafeZone full PDP deploy ────────────────────────────────
print("\n=== Patch 4: Radius SafeZone full PDP deploy ===")
mockup_path = f'{MOCKUP_DIR}/mockup_radius-safezone_pdp_v1.html'
safezone_astro = f'{BASE}/radius-safezone/index.astro'

# Read the mockup HTML
mockup = read(mockup_path)

# Extract body content (between <body> and </body>)
body_match = re.search(r'<body[^>]*>(.*)</body>', mockup, re.DOTALL)
if not body_match:
    print('  ❌ Could not extract body from mockup')
else:
    body_html = body_match.group(1).strip()
    
    # Read current astro file to preserve frontmatter
    current = read(safezone_astro)
    
    # Extract frontmatter (--- ... ---)
    fm_match = re.match(r'^(---.*?---\n)', current, re.DOTALL)
    if not fm_match:
        print('  ❌ Could not find frontmatter')
    else:
        frontmatter = fm_match.group(1)
        
        # Extract BaseLayout opening tag with props
        bl_match = re.search(r'(<BaseLayout\s[^>]*>)', current, re.DOTALL)
        head_match = re.search(r'(<Fragment slot="head">.*?</Fragment>)', current, re.DOTALL)
        
        if bl_match and head_match:
            baselayout_open = bl_match.group(1)
            head_fragment = head_match.group(1)
            
            # Build the new Astro file
            new_astro = f'''{frontmatter}{baselayout_open}
  {head_fragment}
  {body_html}
</BaseLayout>
'''
            write(safezone_astro, new_astro)
            section_count = new_astro.count('<section')
            print(f'  ✅ radius-safezone: deployed from mockup ({len(new_astro):,} chars, {section_count} sections)')
        else:
            print(f'  ❌ Could not find BaseLayout or Fragment in current file')

# ── Patch 8: Lunar Eclipse tier reconcile ───────────────────────────────────
print("\n=== Patch 8: Lunar Eclipse tier-pro → tier-pro-plus ===")
f = f'{BASE}/lunar-eclipse/index.astro'
content = read(f)
# Fix h1 badge: tier-pro → tier-pro-plus, PRO → PRO+
new_content = content.replace(
    '<span class="tier-badge tier-pro">PRO</span>',
    '<span class="tier-badge tier-pro-plus">PRO+</span>'
)
# Fix title: PRO → PRO+ (only in the title= attribute)
new_content = re.sub(
    r'(title="[^"]*LDLL PRO[^+][^"]*")',
    lambda m: m.group(0).replace('LDLL PRO', 'LDLL PRO+'),
    new_content
)
if new_content != content:
    write(f, new_content)
    print(f'  ✅ lunar-eclipse: tier-pro-plus + title PRO+')
else:
    print(f'  — lunar-eclipse: no change needed')

# ── Patch 9: Orbit-I tier reconcile ─────────────────────────────────────────
print("\n=== Patch 9: Orbit-I h1 tier-eco → tier-pro ===")
f = f'{BASE}/orbit-i/index.astro'
content = read(f)
# Fix h1 badge: tier-eco ECO → tier-pro PRO
new_content = content.replace(
    '<span class="tier-badge tier-eco">ECO</span>',
    '<span class="tier-badge tier-pro">PRO</span>'
)
# Title already says PRO — verify
title_match = re.search(r'title="[^"]*LDGR PRO[^"]*"', new_content)
if new_content != content:
    write(f, new_content)
    print(f'  ✅ orbit-i: tier-pro badge | title PRO: {"✅" if title_match else "⚠️ check"}')
else:
    print(f'  — orbit-i: no change needed')

# ── Patches 10-12: Collection data wattage ───────────────────────────────────
print("\n=== Patches 10-12: Collection data wattage ===")
data_file = 'src/data/collections/multifamily.ts'
content = read(data_file)

# P10: Eclipse-II maxWattage 18 → 24
new_content = content
# Find Eclipse-II block and fix maxWattage
# The pattern is: family: 'Eclipse-II', ... maxWattage: 18,
new_content = re.sub(
    r"(family:\s*'Eclipse-II'[^}]*?)maxWattage:\s*18",
    r'\1maxWattage: 24',
    new_content,
    flags=re.DOTALL
)
# P11: Radius SafeZone maxWattage 15 → 19
new_content = re.sub(
    r"(family:\s*'Radius SafeZone'[^}]*?)maxWattage:\s*15",
    r'\1maxWattage: 19',
    new_content,
    flags=re.DOTALL
)
# P12: Nebula-II maxWattage 20 → 15
new_content = re.sub(
    r"(family:\s*'Nebula-II'[^}]*?)maxWattage:\s*20",
    r'\1maxWattage: 15',
    new_content,
    flags=re.DOTALL
)

if new_content != content:
    write(data_file, new_content)
    # Verify
    for fam, expected in [('Eclipse-II', 24), ('Radius SafeZone', 19), ('Nebula-II', 15)]:
        m = re.search(rf"family:\s*'{re.escape(fam)}'[^}}]*?maxWattage:\s*(\d+)", new_content, re.DOTALL)
        actual = int(m.group(1)) if m else None
        status = '✅' if actual == expected else f'❌ got {actual}'
        print(f'  {fam}: maxWattage={actual} {status}')
else:
    print('  — no changes needed')

# ── Patch 13: Ⓐ glyph in tab titles ────────────────────────────────────────
print("\n=== Patch 13: Ⓐ glyph in tab titles ===")
GLYPH = 'Ⓐ'
for slug in SLUGS:
    f = f'{BASE}/{slug}/index.astro'
    content = read(f)
    # Find title= attribute and add Ⓐ to multi-family references
    # Pattern: "... | Archipelago Lighting" — add "multi-fⒶMILY" to description if missing
    # The title should contain "multi-fⒶMILY" somewhere
    if GLYPH not in content:
        # Add Ⓐ to the title attribute — replace "multi-family" with "multi-fⒶMILY" in title only
        new_content = re.sub(
            r'(title="[^"]*?)multi-family([^"]*")',
            lambda m: m.group(0).replace('multi-family', f'multi-f{GLYPH}MILY', 1),
            content
        )
        if new_content != content:
            write(f, new_content)
            print(f'  ✅ {slug}: Ⓐ glyph added to title')
        else:
            # Try adding to description
            print(f'  ⚠️ {slug}: no multi-family in title — check manually')
    else:
        print(f'  — {slug}: already has Ⓐ glyph')

# ── Patch 14: CFG-COWORK-13 buildSubmittalUrl() ─────────────────────────────
print("\n=== Patch 14: CFG-COWORK-13 buildSubmittalUrl() ===")

BUILD_SUBMITTAL_JS = """
  // CFG-COWORK-13: wire Generate Submittal PDF CTA to configurator state
  (function() {
    function buildSubmittalUrl() {
      var sku = (document.querySelector('[data-sku-display]') || {}).textContent || '';
      var size = (document.querySelector('[data-field="size"].chip-on') || {}).dataset && document.querySelector('[data-field="size"].chip-on').dataset.val || '';
      var pack = (document.querySelector('[data-field="pack"].chip-on') || {}).dataset && document.querySelector('[data-field="pack"].chip-on').dataset.val || '';
      var cct = (document.querySelector('[data-field="cct"].chip-on') || {}).dataset && document.querySelector('[data-field="cct"].chip-on').dataset.val || '';
      var finish = (document.querySelector('[data-field="finish"].chip-on') || {}).dataset && document.querySelector('[data-field="finish"].chip-on').dataset.val || '';
      var params = new URLSearchParams({ sku: sku, size: size, pack: pack, cct: cct, finish: finish });
      return 'submittal/?' + params.toString();
    }
    function rebindCta() {
      var cta = document.getElementById('cfgCtaPdf');
      if (cta) cta.href = buildSubmittalUrl();
    }
    document.addEventListener('DOMContentLoaded', function() {
      rebindCta();
      document.querySelectorAll('.chip').forEach(function(chip) {
        chip.addEventListener('click', function() { setTimeout(rebindCta, 50); });
      });
    });
  })();
"""

for slug in SLUGS:
    f = f'{BASE}/{slug}/index.astro'
    content = read(f)
    
    # Check if already wired
    if 'buildSubmittalUrl' in content:
        print(f'  — {slug}: already has buildSubmittalUrl')
        continue
    
    # Find the last </script> before </BaseLayout> and inject after it
    # Or inject before </BaseLayout>
    if 'cfgCtaPdf' in content or 'cfg-cta-pdf' in content:
        # Has the CTA button — inject the JS
        inject = f'<script>{BUILD_SUBMITTAL_JS}</script>\n</BaseLayout>'
        new_content = content.replace('</BaseLayout>', inject, 1)
        if new_content != content:
            write(f, new_content)
            print(f'  ✅ {slug}: buildSubmittalUrl() injected')
        else:
            print(f'  ⚠️ {slug}: could not inject — check manually')
    else:
        print(f'  — {slug}: no cfgCtaPdf button found (skip)')

print("\n=== All patches complete ===")
