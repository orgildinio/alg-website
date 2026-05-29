import re, json, gzip, base64

slug = 'em07-cmb150dc'
path = f'public/products/{slug}/index.html'

with open(path) as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', html)
print(f"Number of scripts: {len(scripts)}")

manifest = json.loads(scripts[1])
print(f"Manifest type: {type(manifest)}, keys: {list(manifest.keys())[:10]}")

# The manifest is a dict with UUID keys
for uuid, entry in manifest.items():
    print(f"UUID: {uuid}, type: {type(entry)}")
    if isinstance(entry, dict):
        print(f"  keys: {list(entry.keys())[:10]}")
        if 'content' in entry:
            try:
                decoded = gzip.decompress(base64.b64decode(entry['content'])).decode('utf-8')
                if 'downloads' in decoded or 'PRODUCT' in decoded:
                    print(f"  ** HAS PRODUCT/downloads **")
                    m = re.search(r'"downloads"\s*:\s*(\[.*?\])', decoded, re.DOTALL)
                    if m:
                        print(f"  downloads: {m.group(1)[:200]}")
            except Exception as e:
                print(f"  decode error: {e}")
