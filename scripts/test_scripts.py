"""
Test each new script block in radiator to find which one causes the build error.
"""
import re, subprocess

with open('/tmp/radiator_old_full.astro', 'r') as f:
    old_content = f.read()

with open('/tmp/radiator_new_backup2.astro', 'r') as f:
    new_content = f.read()

# Get new HTML body
new_main_style_end = new_content.find('</style>') + len('</style>')
new_first_script_start = new_content.find('<script', new_main_style_end)
new_body = new_content[new_main_style_end:new_first_script_start]

# Get new scripts
new_scripts = list(re.finditer(r'<script(?! type="application/ld\+json")[^>]*>([\s\S]*?)</script>', new_content))

# Get old scripts
old_scripts = list(re.finditer(r'<script(?! type="application/ld\+json")[^>]*>([\s\S]*?)</script>', old_content))

# Get new CSS
new_style_start = new_content.find('<style is:global>') + len('<style is:global>')
new_style_end = new_content.find('</style>')
new_css = new_content[new_style_start:new_style_end]

# Build base: old frontmatter + old BaseLayout + NEW CSS + NEW body
test_base = old_content[:old_content.find('</style>') + len('</style>')]
style_start = test_base.find('<style is:global>') + len('<style is:global>')
style_end = test_base.find('</style>')
test_base = test_base[:style_start] + new_css + test_base[style_end:]
test_base = test_base + new_body

def test_build(content):
    with open('src/pages/products/radiator/index.astro', 'w') as f:
        f.write(content)
    result = subprocess.run(
        ['pnpm', 'build'],
        capture_output=True, text=True, cwd='/home/ubuntu/alg-website-src'
    )
    success = 'Syntax error' not in result.stdout and 'Syntax error' not in result.stderr
    return success

# Test: add one new script at a time
print("Testing scripts one by one...")
for i in range(len(new_scripts)):
    # Use old scripts for 0..i-1, new script for i, old scripts for i+1..
    scripts_text = ''
    for j in range(len(new_scripts)):
        if j == i:
            scripts_text += new_scripts[j].group(0) + '\n'
        elif j < len(old_scripts):
            scripts_text += old_scripts[j].group(0) + '\n'
    
    test_content = test_base + scripts_text + '\n</BaseLayout>\n'
    ok = test_build(test_content)
    print(f"  Script {i+1} (new): {'OK' if ok else 'FAIL'}")
    if not ok:
        print(f"    -> Script {i+1} is the problem!")
        # Save the failing script for analysis
        with open(f'/tmp/failing_script_{i+1}.js', 'w') as f:
            f.write(new_scripts[i].group(1))
        break

# Restore new file
with open('src/pages/products/radiator/index.astro', 'w') as f:
    f.write(new_content)
print("Restored new file")
