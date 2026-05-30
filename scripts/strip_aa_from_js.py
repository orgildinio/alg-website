"""
Strip the Ⓐ (U+24B6) character from <script> blocks in all PDP Astro wrappers.
The Ⓐ character is used in HTML markup and CSS (where it works fine), but
esbuild fails to parse it when it appears inside <script> blocks.
The character only appears in JS comments (not in functional code), so
replacing it with 'A' is safe.
"""
import re
import os

AA = '\u24b6'  # Ⓐ
pdp_dir = 'src/pages/products'
fixed = 0

for slug in sorted(os.listdir(pdp_dir)):
    path = f'{pdp_dir}/{slug}/index.astro'
    if not os.path.exists(path):
        continue
    with open(path, 'r') as f:
        content = f.read()

    # Find all <script> blocks (not JSON-LD) and replace Ⓐ with A inside them
    def fix_script(m):
        inner = m.group(1)
        if AA in inner:
            inner = inner.replace(AA, 'A')
        return f'<script{m.group(2)}>{inner}</script>'

    # Match <script ...>...</script> but not type="application/ld+json"
    new_content = re.sub(
        r'<script((?! type="application/ld\+json")[^>]*)>([\s\S]*?)</script>',
        lambda m: f'<script{m.group(1)}>{m.group(2).replace(AA, "A")}</script>',
        content
    )

    if new_content != content:
        with open(path, 'w') as f:
            f.write(new_content)
        count = content.count(AA) - new_content.count(AA)
        print(f'  [{slug}] Stripped {count} Ⓐ from JS scripts')
        fixed += 1

print(f'\nDone: {fixed} files fixed')
