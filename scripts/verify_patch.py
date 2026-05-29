import re, json, gzip, base64

slug = 'em07-cmb150dc'
path = f'public/products/{slug}/index.html'

with open(path) as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', html)
manifest = json.loads(scripts[1])

TARGET = '018e416e-13bd-453c-9f45-73e593db329c'
entry = manifest[TARGET]
data = entry['data']
compressed = entry.get('compressed', False)
print(f"compressed: {compressed}")

if compressed:
    decoded = gzip.decompress(base64.b64decode(data)).decode('utf-8')
else:
    decoded = base64.b64decode(data).decode('utf-8')

print(f"Decoded length: {len(decoded)}")

# Search for Download Specs
matches = list(re.finditer(r'Download.Specs', decoded, re.I))
print(f"Matches for 'Download Specs': {len(matches)}")

for m in matches:
    start = max(0, m.start() - 150)
    end = min(len(decoded), m.end() + 150)
    print(f"\nContext:")
    print(decoded[start:end])

# Also search for the PDF path
pdf_path = f'/products/{slug}/assets/datasheets/{slug}.pdf'
if pdf_path in decoded:
    print(f"\nPDF path found: {pdf_path}")
else:
    print(f"\nPDF path NOT found: {pdf_path}")
    # Search for any /products/ path
    paths = re.findall(r'/products/[^\s"\']+', decoded)
    print(f"Other /products/ paths: {paths[:5]}")
