import re, json, gzip, base64

slug = 'em07-cmb150dc'
path = f'public/products/{slug}/index.html'

with open(path) as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', html)
print(f"Number of scripts: {len(scripts)}")

# The 4th script tag (index 3) is the inner HTML
inner_html = json.loads(scripts[3])
print(f"Inner HTML length: {len(inner_html)}")

# Check for downloads section
m = re.search(r'(?:§11|downloads|DOWNLOADS).{0,500}', inner_html, re.I | re.DOTALL)
if m:
    print('Downloads section found:')
    print(m.group(0)[:500])
else:
    print('No downloads section in inner HTML')

# Check for any PDF links
pdf_links = re.findall(r'href="([^"]*\.pdf[^"]*)"', inner_html, re.I)
print(f'PDF links: {pdf_links}')

# Check for any https links
https_links = re.findall(r'href="(https://[^"]+)"', inner_html)
print(f'HTTPS links: {https_links[:10]}')
