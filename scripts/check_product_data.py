import re, json, gzip, base64

em_slugs = [
    'em07-cmb150dc', 'em07-cmb260dc', 'em08-amb48dc', 'em08-hmb170dc',
    'em08-mt150dc', 'em08-ytb60dc', 'em15-hmb170dc', 'em15-pmb120ac',
    'em20-cmb150dc', 'em20-cmb260dc', 'em20-hmb135ac', 'em25-hmb170dc',
    'em25-pmb120ac', 'em30-umb170dc', 'em40-rmb170dc', 'em60-gmb170dc',
    'em60-umb170dc', 'crc6-em24-jbs-b', 'crc6-em24-jbs-w', 'crcu-em24-jbm'
]

TARGET_UUID = '7cc67c4d'

for slug in em_slugs:
    path = f'public/products/{slug}/index.html'
    try:
        with open(path) as f:
            html = f.read()
        scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', html)
        manifest = json.loads(scripts[1])
        
        for entry in manifest:
            if isinstance(entry, dict) and entry.get('id', '').startswith(TARGET_UUID):
                decoded = gzip.decompress(base64.b64decode(entry['content'])).decode('utf-8')
                # Find PRODUCT object
                m = re.search(r'window\.PRODUCT\s*=\s*(\{.*?\});', decoded, re.DOTALL)
                if m:
                    try:
                        prod = json.loads(m.group(1))
                        downloads = prod.get('downloads', 'NOT FOUND')
                        sku = prod.get('sku', prod.get('id', 'unknown'))
                        print(f'{slug}: sku={sku}, downloads={downloads}')
                    except Exception as e:
                        print(f'{slug}: JSON parse error: {e}')
                break
    except FileNotFoundError:
        print(f'{slug}: FILE NOT FOUND')

print("Done")
