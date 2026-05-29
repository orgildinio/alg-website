#!/usr/bin/env python3
"""
Apply §C.1 fix to exit.astro: remove the utility div (eyebrow strip) from the TopBar React component.
The previous patch only removed the 'right' div; this removes the entire <div className="utility"> block.
"""
import re, json, gzip, base64

path = 'src/pages/collections/constant/exit.astro'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract bundle data
scripts = re.findall(r'(<script[^>]*>)(.*?)(</script>)', content, re.DOTALL)
bundle_script_idx = None
bundle_data = None
for i, (open_tag, body, close_tag) in enumerate(scripts):
    if len(body) > 100000:
        try:
            bundle_data = json.loads(body)
            bundle_script_idx = i
            break
        except:
            pass

react_uuid = '1349abce-6c96-444f-bdbd-32a86bca19b4'
raw = gzip.decompress(base64.b64decode(bundle_data[react_uuid]['data']))
text = raw.decode('utf-8')

# Find the utility div start
utility_pattern = '<div className="utility">'
idx_utility = text.find(utility_pattern)
if idx_utility == -1:
    print("ERROR: Could not find utility div")
    exit(1)

print(f"Found utility div at {idx_utility}")
print(f"Context: {text[idx_utility:idx_utility+300]!r}")

# Find the matching closing </div> for the utility div
depth = 0
i = idx_utility
while i < len(text):
    if text[i:i+4] == '<div':
        depth += 1
    elif text[i:i+6] == '</div>':
        depth -= 1
        if depth == 0:
            utility_end = i + 6
            break
    i += 1

print(f"Utility div ends at {utility_end}")
print(f"End context: {text[utility_end-50:utility_end+100]!r}")

# Remove the utility div (including any surrounding whitespace/newlines)
# Find the start of the line containing the utility div
line_start = text.rfind('\n', 0, idx_utility) + 1
# Find the end of the line containing the closing </div>
line_end = text.find('\n', utility_end)
if line_end == -1:
    line_end = len(text)
else:
    line_end += 1  # include the newline

text_patched = text[:line_start] + text[line_end:]
print(f"After removal: {len(text_patched)} chars (removed {len(text) - len(text_patched)} chars)")

# Verify
if 'LIFE SAFETY' in text_patched.upper() or 'ALWAYS ON' in text_patched.upper():
    print("WARNING: LIFE SAFETY / ALWAYS ON still present")
    idx = text_patched.upper().find('ALWAYS ON')
    print(f"  Context: {text_patched[max(0,idx-100):idx+200]!r}")
else:
    print("OK: Eyebrow content removed")

if 'utility' in text_patched:
    # Check if it's still in the CSS (that's OK)
    idx = text_patched.find('"utility"')
    if idx != -1:
        print(f"WARNING: 'utility' className still present at {idx}: {text_patched[max(0,idx-50):idx+100]!r}")
    else:
        print("OK: utility className gone from JSX")

# Recompress
patched_bytes = text_patched.encode('utf-8')
compressed = gzip.compress(patched_bytes)
encoded = base64.b64encode(compressed).decode('ascii')
bundle_data[react_uuid]['data'] = encoded

# Rebuild bundle JSON
new_bundle_json = json.dumps(bundle_data, ensure_ascii=False)
old_script_body = scripts[bundle_script_idx][1]
content = content.replace(old_script_body, new_bundle_json, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"OK: exit.astro updated")
