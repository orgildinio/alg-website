"""
Validate all PDP Astro wrapper <script> blocks with node --check.
Fix any JS syntax errors found (primarily unescaped apostrophes in string literals).
"""
import re
import os
import subprocess
import tempfile

pdp_dir = 'src/pages/products'
total_errors = 0
total_fixes = 0

for slug in sorted(os.listdir(pdp_dir)):
    path = f'{pdp_dir}/{slug}/index.astro'
    if not os.path.exists(path):
        continue
    with open(path, 'r') as f:
        content = f.read()

    scripts_iter = list(re.finditer(
        r'<script((?! type="application/ld\+json")[^>]*)>([\s\S]*?)</script>',
        content
    ))
    new_content = content
    file_errors = 0

    for i, m in enumerate(scripts_iter):
        script_inner = m.group(2)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(script_inner)
            fname = f.name

        result = subprocess.run(['node', '--check', fname], capture_output=True, text=True)
        os.unlink(fname)

        if result.returncode != 0:
            file_errors += 1
            total_errors += 1
            print(f'  [{slug}] Script {i+1} FAILED: {result.stderr.split(chr(10))[1][:100]}')

            # Fix: escape unescaped apostrophes in single-quoted strings
            fixed = re.sub(
                r"'([^']*?)(\w)'s([^']*?)'",
                lambda m2: f"'{m2.group(1)}{m2.group(2)}\\'s{m2.group(3)}'",
                script_inner
            )
            if fixed != script_inner:
                new_content = new_content.replace(
                    m.group(0),
                    f'<script{m.group(1)}>{fixed}</script>',
                    1
                )
                total_fixes += 1
                print(f'    -> Fixed apostrophe escape')

    if file_errors > 0 and new_content != content:
        with open(path, 'w') as f:
            f.write(new_content)

print(f'\nTotal errors found: {total_errors}, fixes applied: {total_fixes}')
