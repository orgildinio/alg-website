import re, json, gzip, base64

slug = 'em07-cmb150dc'
path = f'public/products/{slug}/index.html'

with open(path) as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', html)
manifest = json.loads(scripts[1])

# The manifest uses 'data' not 'content'
# Check the 7cc67c4d UUID (PRODUCT data)
TARGET = '7cc67c4d-5c92-43dc-80d0-aac167d1c37c'
entry = manifest[TARGET]
print(f"Entry keys: {list(entry.keys())}")
print(f"mime: {entry.get('mime')}")
print(f"compressed: {entry.get('compressed')}")

data = entry['data']
if entry.get('compressed'):
    decoded = gzip.decompress(base64.b64decode(data)).decode('utf-8')
else:
    decoded = base64.b64decode(data).decode('utf-8')

print(f"\nDecoded length: {len(decoded)}")
print(f"\nFirst 500 chars:")
print(decoded[:500])

# Check for downloads
if 'downloads' in decoded:
    print("\n** HAS downloads **")
    m = re.search(r'"downloads"\s*:\s*(\[.*?\])', decoded, re.DOTALL)
    if m:
        print(f"downloads: {m.group(1)[:300]}")
else:
    print("\nNo 'downloads' key found")

# Check for any PDF or WD URLs
pdf_urls = re.findall(r'https?://[^\s"\'<>]*(?:pdf|workdrive|zoho)[^\s"\'<>]*', decoded, re.I)
print(f"\nPDF/WD URLs: {pdf_urls}")
