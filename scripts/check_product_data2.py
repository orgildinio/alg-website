import re, json, gzip, base64

slug = 'em07-cmb150dc'
path = f'public/products/{slug}/index.html'

with open(path) as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', html)
print(f"Number of scripts: {len(scripts)}")

manifest = json.loads(scripts[1])
print(f"Manifest type: {type(manifest)}, len: {len(manifest)}")
print(f"First entry type: {type(manifest[0])}")

# Show first few entries
for i, entry in enumerate(manifest[:5]):
    if isinstance(entry, dict):
        print(f"Entry {i}: id={entry.get('id', 'no-id')}, keys={list(entry.keys())}")
    else:
        print(f"Entry {i}: type={type(entry)}, val={str(entry)[:100]}")

# Find entries with 'content'
for i, entry in enumerate(manifest):
    if isinstance(entry, dict) and 'content' in entry:
        try:
            decoded = gzip.decompress(base64.b64decode(entry['content'])).decode('utf-8')
            if 'PRODUCT' in decoded or 'downloads' in decoded:
                print(f"\nEntry {i} (id={entry.get('id', 'no-id')}) has PRODUCT/downloads")
                # Find downloads
                m = re.search(r'"downloads"\s*:\s*(\[.*?\])', decoded, re.DOTALL)
                if m:
                    print(f"  downloads: {m.group(1)[:200]}")
                else:
                    print(f"  No downloads array found")
                # Find PRODUCT
                m2 = re.search(r'window\.PRODUCT\s*=\s*(\{[^}]+\})', decoded)
                if m2:
                    print(f"  PRODUCT: {m2.group(1)[:300]}")
        except Exception as e:
            pass
