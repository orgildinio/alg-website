#!/usr/bin/env python3
"""
§C.1 + §C.2 + §C.4 fix for exit.astro:
1. Remove header.hdr (brand logo + secondary nav + CTAs) from TopBar React bundle
2. Remove crumbs div (CATALOG breadcrumb + metadata strip) from TopBar React bundle
3. Fix breadcrumb tail in Astro wrapper: EXIT → EXIT & EMERGENCY
4. Strip · 2026 from sub-footer marker band in React bundle
"""
import re, json, gzip, base64

path = 'src/pages/collections/constant/exit.astro'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ── Step 1: Fix breadcrumb tail in Astro wrapper ──────────────────────────────
# Current: <span class="bc-current">EXIT</span>
# Target:  <span class="bc-current">EXIT &amp; EMERGENCY</span>
old_bc = '<span class="bc-current">EXIT</span>'
new_bc = '<span class="bc-current">EXIT &amp; EMERGENCY</span>'
if old_bc in content:
    content = content.replace(old_bc, new_bc, 1)
    print('OK: Breadcrumb tail fixed to EXIT & EMERGENCY')
else:
    print('WARN: Breadcrumb tail pattern not found — checking current state')
    m = re.search(r'bc-current[^>]*>([^<]+)<', content)
    if m:
        print(f'  Current bc-current: {repr(m.group(1))}')

# ── Step 2: Patch the React bundle ───────────────────────────────────────────
# Find the bundle manifest script
bundle_m = re.search(r'(<script type="__bundler/manifest">)([\s\S]*?)(</script>)', content)
if not bundle_m:
    print('ERROR: Could not find bundle manifest script')
    exit(1)

manifest = json.loads(bundle_m.group(2))
react_uuid = '1349abce-6c96-444f-bdbd-32a86bca19b4'

if react_uuid not in manifest:
    print(f'ERROR: React UUID {react_uuid} not in manifest')
    exit(1)

entry = manifest[react_uuid]
raw = gzip.decompress(base64.b64decode(entry['data']))
text = raw.decode('utf-8')

print(f'React bundle size: {len(text)} chars')

# ── Step 2a: Remove <header className="hdr"> block ───────────────────────────
header_pattern = '<header className="hdr">'
idx_header = text.find(header_pattern)
if idx_header == -1:
    print('INFO: header.hdr already removed or not found')
else:
    print(f'Found header.hdr at {idx_header}')
    # Find the matching </header>
    depth = 0
    i = idx_header
    header_end = -1
    while i < len(text):
        if text[i:i+8] == '<header ':
            depth += 1
        elif text[i:i+9] == '</header>':
            depth -= 1
            if depth == 0:
                header_end = i + 9
                break
        i += 1
    
    if header_end == -1:
        print('ERROR: Could not find end of header.hdr')
        exit(1)
    
    print(f'header.hdr ends at {header_end}')
    print(f'  Before: {repr(text[max(0,header_end-50):header_end+50])}')
    
    # Remove the header block and surrounding whitespace
    line_start = text.rfind('\n', 0, idx_header) + 1
    line_end = text.find('\n', header_end)
    if line_end == -1:
        line_end = len(text)
    else:
        line_end += 1
    
    text = text[:line_start] + text[line_end:]
    print(f'OK: header.hdr removed ({header_end - idx_header} chars)')

# ── Step 2b: Remove <div className="crumbs"> block ───────────────────────────
crumbs_pattern = '<div className="crumbs">'
idx_crumbs = text.find(crumbs_pattern)
if idx_crumbs == -1:
    print('INFO: crumbs div already removed or not found')
else:
    print(f'Found crumbs div at {idx_crumbs}')
    # Find the matching </div>
    depth = 0
    i = idx_crumbs
    crumbs_end = -1
    while i < len(text):
        if text[i:i+4] == '<div':
            depth += 1
        elif text[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                crumbs_end = i + 6
                break
        i += 1
    
    if crumbs_end == -1:
        print('ERROR: Could not find end of crumbs div')
        exit(1)
    
    print(f'crumbs div ends at {crumbs_end}')
    
    # Remove the crumbs block and surrounding whitespace
    line_start = text.rfind('\n', 0, idx_crumbs) + 1
    line_end = text.find('\n', crumbs_end)
    if line_end == -1:
        line_end = len(text)
    else:
        line_end += 1
    
    text = text[:line_start] + text[line_end:]
    print(f'OK: crumbs div removed ({crumbs_end - idx_crumbs} chars)')

# ── Step 2c: Strip · 2026 from sub-footer marker band ────────────────────────
# Look for "· 2026" or "LIFE-SAFETY PLATFORM · 2026" pattern
year_patterns = [
    ('· 2026', ''),
    (' · 2026', ''),
    ('· 2025', ''),
    (' · 2025', ''),
]
for old, new in year_patterns:
    if old in text:
        count = text.count(old)
        text = text.replace(old, new)
        print(f'OK: Replaced {count}x "{old}" with "{new}"')

# ── Step 2d: Verify chrome elements are gone ─────────────────────────────────
checks = [
    ('header.hdr', '<header className="hdr">'),
    ('crumbs div', '<div className="crumbs">'),
    ('LIFE SAFETY', 'LIFE SAFETY'),
    ('ALWAYS ON', 'ALWAYS ON'),
    ('REP LOCATOR', 'REP LOCATOR'),
    ('utility div', '<div className="utility">'),
]
print('\nPost-patch verification:')
for name, pattern in checks:
    found = pattern in text
    status = 'STILL PRESENT ⚠️' if found else 'absent ✓'
    print(f'  {name}: {status}')

# ── Recompress and update manifest ───────────────────────────────────────────
patched_bytes = text.encode('utf-8')
compressed = gzip.compress(patched_bytes)
encoded = base64.b64encode(compressed).decode('ascii')
manifest[react_uuid]['data'] = encoded

# Rebuild the manifest JSON
new_manifest_json = json.dumps(manifest, ensure_ascii=False)

# Replace in content
old_manifest_body = bundle_m.group(2)
content = content.replace(
    bundle_m.group(1) + old_manifest_body + bundle_m.group(3),
    bundle_m.group(1) + new_manifest_json + bundle_m.group(3),
    1
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nOK: exit.astro updated ({len(content)} chars)')
