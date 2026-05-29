import re, json, gzip, base64

slug = 'em07-cmb150dc'
path = f'public/products/{slug}/index.html'

with open(path) as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', html)
manifest = json.loads(scripts[1])

# Check the 018e416e UUID (React component with Download Specs CTA)
TARGET = '018e416e-13bd-453c-9f45-73e593db329c'
entry = manifest[TARGET]
data = entry['data']
if entry.get('compressed'):
    decoded = gzip.decompress(base64.b64decode(data)).decode('utf-8')
else:
    decoded = base64.b64decode(data).decode('utf-8')

# Find the Download Specs button
matches = list(re.finditer(r'DOWNLOAD.SPECS', decoded, re.I))
print(f"Found {len(matches)} matches for DOWNLOAD SPECS")

for m in matches:
    start = max(0, m.start() - 300)
    end = min(len(decoded), m.end() + 300)
    print(f"\n--- Match at pos {m.start()} ---")
    print(decoded[start:end])
    print("---")
