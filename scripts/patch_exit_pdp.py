#!/usr/bin/env python3
"""
Apply §C fixes to src/pages/collections/constant/exit.astro:
  C.1 - Remove the black eyebrow strip from the React bundle
  C.2 - Insert canonical 5-segment breadcrumb in the Astro wrapper
  C.3 - Add Lato !important CSS pin in the Astro wrapper
"""
import re, json, gzip, base64

path = 'src/pages/collections/constant/exit.astro'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

orig = content

# ── C.1: Remove eyebrow strip from the React bundle ──────────────────────────
# The eyebrow strip is in the React component (UUID 1349abce-6c96-444f-bdbd-32a86bca19b4)
# It renders as a <div className="eyebrow-bar"> or similar containing CONSTⒶNT — LIFE SAFETY etc.
# We need to decompress, patch, recompress, and re-encode

scripts = re.findall(r'(<script[^>]*>)(.*?)(</script>)', content, re.DOTALL)
print(f"Found {len(scripts)} script blocks")

# Find the bundle data script (the large JSON one)
bundle_script_idx = None
bundle_data = None
for i, (open_tag, body, close_tag) in enumerate(scripts):
    if len(body) > 100000:
        try:
            bundle_data = json.loads(body)
            bundle_script_idx = i
            print(f"Bundle data script found at index {i}, {len(bundle_data)} UUIDs")
            break
        except:
            pass

if bundle_data is None:
    print("ERROR: Could not find bundle data script")
    exit(1)

# Patch the React component UUID
react_uuid = '1349abce-6c96-444f-bdbd-32a86bca19b4'
react_data = bundle_data[react_uuid]
raw = gzip.decompress(base64.b64decode(react_data['data']))
text = raw.decode('utf-8')

print(f"React component size: {len(text)} chars")

# Find and remove the eyebrow bar div
# The eyebrow bar contains "USA designed · Montclair CA" and REP LOCATOR links
# Pattern: find the opening <div className="eyebrow-bar"> or similar and its closing </div>

# First, find the exact pattern
idx_912 = text.find('912-3220')
if idx_912 == -1:
    print("ERROR: Could not find eyebrow content")
    exit(1)

# Find the start of the eyebrow bar div by looking backwards from 912-3220
# The eyebrow bar starts with something like <div className="eyebrow-bar">
# Look backwards for the opening div
search_start = max(0, idx_912 - 2000)
chunk = text[search_start:idx_912+500]

# Find the eyebrow bar opening tag
# Look for className="eyebrow-bar" or similar
eyebrow_patterns = [
    r'<div\s+className="eyebrow-bar"',
    r'<div\s+className=\{[^}]*eyebrow[^}]*\}',
    r'<div\s+style=\{[^}]*background[^}]*\}\s+className="[^"]*eyebrow[^"]*"',
]

eyebrow_start = None
for pat in eyebrow_patterns:
    m = re.search(pat, chunk)
    if m:
        eyebrow_start = search_start + m.start()
        print(f"Found eyebrow bar at {eyebrow_start} with pattern: {pat}")
        break

if eyebrow_start is None:
    # Try to find by looking at the context around 912-3220
    # The structure is: <div className="...">...<span>USA designed · Montclair CA</span>...</div>
    # Find the parent div
    print(f"Context around 912-3220: {text[max(0,idx_912-500):idx_912+200]!r}")
    
    # Try finding the div that contains this content
    # Look for <div className= before the 912-3220 text
    search_zone = text[max(0, idx_912-1500):idx_912]
    # Find the last <div className= in this zone
    div_matches = list(re.finditer(r'<div\s+className=', search_zone))
    if div_matches:
        last_div = div_matches[-1]
        eyebrow_start = max(0, idx_912-1500) + last_div.start()
        print(f"Found parent div at {eyebrow_start}: {text[eyebrow_start:eyebrow_start+100]!r}")

if eyebrow_start is None:
    print("ERROR: Could not find eyebrow bar start")
    exit(1)

# Now find the end of the eyebrow bar div by counting braces
# Find the matching </div> for the eyebrow bar
depth = 0
i = eyebrow_start
while i < len(text):
    if text[i:i+4] == '<div':
        depth += 1
    elif text[i:i+6] == '</div>':
        depth -= 1
        if depth == 0:
            eyebrow_end = i + 6
            break
    i += 1

print(f"Eyebrow bar: [{eyebrow_start}:{eyebrow_end}]")
print(f"Content: {text[eyebrow_start:eyebrow_start+200]!r}")
print(f"End: {text[eyebrow_end-100:eyebrow_end]!r}")

# Remove the eyebrow bar
text_patched = text[:eyebrow_start] + text[eyebrow_end:]
print(f"After removal: {len(text_patched)} chars (removed {len(text) - len(text_patched)} chars)")

# Verify removal
if '912-3220' in text_patched:
    print("WARNING: 912-3220 still present after removal — checking context")
    idx = text_patched.find('912-3220')
    print(f"  Context: {text_patched[max(0,idx-100):idx+200]!r}")
else:
    print("OK: Eyebrow content removed successfully")

# Recompress
patched_bytes = text_patched.encode('utf-8')
compressed = gzip.compress(patched_bytes)
encoded = base64.b64encode(compressed).decode('ascii')
bundle_data[react_uuid]['data'] = encoded
print(f"Recompressed: {len(encoded)} chars (was {len(react_data['data'])} chars)")

# Rebuild the bundle JSON
new_bundle_json = json.dumps(bundle_data, ensure_ascii=False)

# Replace the bundle script in the content
# Find the exact script block to replace
old_script_body = scripts[bundle_script_idx][1]
content = content.replace(old_script_body, new_bundle_json, 1)
print(f"Bundle script replaced in content: {old_script_body[:50]!r} -> {new_bundle_json[:50]!r}")

# ── C.2: Insert canonical 5-segment breadcrumb ───────────────────────────────
# Insert between <BaseLayout> and <div class="constant-exit-pdp">
breadcrumb_html = '''  <nav class="alg-breadcrumb" aria-label="Breadcrumb" style="padding:10px 24px;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#6B7280;border-bottom:1px solid #E5E7EB;background:#fff;">
    <a href="/" style="color:#6B7280;text-decoration:none;">HOME</a>
    <span style="margin:0 6px;">›</span>
    <a href="/collections/" style="color:#6B7280;text-decoration:none;">PRODUCTS</a>
    <span style="margin:0 6px;">›</span>
    <a href="/collections/safety-controls/" style="color:#6B7280;text-decoration:none;">SAFETY &amp; CONTROLS</a>
    <span style="margin:0 6px;">›</span>
    <a href="/collections/constant/" style="color:#6B7280;text-decoration:none;">CONST<span style="color:#F32740;">Ⓐ</span>NT</a>
    <span style="margin:0 6px;">›</span>
    <span style="color:#111827;">EXIT</span>
  </nav>'''

# Insert after <BaseLayout ...> opening tag and before <div class="constant-exit-pdp">
old_host = '<BaseLayout title={title} description={description}>\n  <div class="constant-exit-pdp">'
new_host = f'<BaseLayout title={{title}} description={{description}}>\n{breadcrumb_html}\n  <div class="constant-exit-pdp">'
if old_host in content:
    content = content.replace(old_host, new_host, 1)
    print("OK: Breadcrumb inserted")
else:
    print(f"WARNING: Could not find insertion point for breadcrumb")
    print(f"Looking for: {old_host!r}")

# ── C.3: Add Lato !important CSS pin ─────────────────────────────────────────
# Insert a <style> block before </BaseLayout> or after the breadcrumb
lato_css = '''  <style>
    /* §C.3 · Lato pin — defeat Shopify/Cormorant cascade */
    .constant-exit-pdp h1,
    .constant-exit-pdp h2,
    .constant-exit-pdp h3,
    .constant-exit-pdp h4,
    .constant-exit-pdp p,
    .constant-exit-pdp a,
    .constant-exit-pdp li,
    .constant-exit-pdp button {
      font-family: 'Lato', system-ui, -apple-system, sans-serif !important;
    }
    .constant-exit-pdp .eyebrow,
    .constant-exit-pdp .alg-eyebrow,
    .constant-exit-pdp .mono,
    .constant-exit-pdp .spec-row,
    .constant-exit-pdp .spec-row .k,
    .constant-exit-pdp .spec-row .v,
    .constant-exit-pdp [class*="font-mono"] {
      font-family: 'JetBrains Mono', ui-monospace, "SF Mono", Menlo, monospace !important;
    }
  </style>'''

# Insert before </BaseLayout>
if '</BaseLayout>' in content:
    content = content.replace('</BaseLayout>', f'{lato_css}\n</BaseLayout>', 1)
    print("OK: Lato CSS pin inserted")
else:
    print("WARNING: Could not find </BaseLayout>")

# ── Write out ─────────────────────────────────────────────────────────────────
if content == orig:
    print("ERROR: No changes made!")
else:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"OK: exit.astro updated ({len(content)} chars, was {len(orig)} chars)")
