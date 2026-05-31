"""
v2.5 · Liberty CSS bundle recovery
Root cause: <style is:global> at line 37 contains raw text (comment notes + mockup HTML)
instead of CSS. The actual CSS (:root with --bg-darker) is inside a nested <style> tag
at line 190, which Astro's CSS pipeline ignores.

Fix: replace lines 37-3270 (the corrupted outer style block + nested inner style wrapper)
with a clean <style is:global> that starts directly with :root.

Touches: src/pages/products/liberty/index.astro ONLY.
"""
from pathlib import Path

p = Path('src/pages/products/liberty/index.astro')
lines = p.read_text().splitlines(keepends=True)

# Indices (0-based):
# 36  = line 37: <style is:global>  (corrupted outer style tag)
# 37-188 = lines 38-189: raw text garbage (comment notes + mockup HTML boilerplate)
# 189 = line 190: <style>  (inner style tag — NOT is:global)
# 190-3267 = lines 191-3268: actual CSS content (:root, all rules)
# 3268 = line 3269: blank line
# 3269 = line 3270: </style>  (closes inner style)

# Verify boundaries
assert lines[36].strip() == '<style is:global>', f"Expected <style is:global> at line 37, got: {lines[36].strip()!r}"
assert lines[189].strip() == '<style>', f"Expected <style> at line 190, got: {lines[189].strip()!r}"
assert lines[3269].strip() == '</style>', f"Expected </style> at line 3270, got: {lines[3269].strip()!r}"
assert ':root' in lines[190], f"Expected :root at line 191, got: {lines[190]!r}"

# Extract the actual CSS content (lines 191-3269, i.e., indices 190-3268)
css_content = lines[190:3269]  # includes the blank line before </style>

# Build the replacement: clean <style is:global> with the actual CSS
replacement = ['    <style is:global>\n'] + css_content + ['</style>\n']

# Reconstruct: keep everything before line 37 (index 36), insert replacement, keep everything after line 3270 (index 3269)
new_lines = lines[:36] + replacement + lines[3270:]

p.write_text(''.join(new_lines))

# Verify
result = p.read_text()
assert '--bg-darker: #14171b' in result, "FAIL: --bg-darker not found after fix"
assert result.count('<style is:global>') == 1, f"FAIL: expected 1 <style is:global>, got {result.count('<style is:global>')}"
# The nested <style> (line 190) should be gone
lines_after = result.splitlines()
style_global_idx = next(i for i, l in enumerate(lines_after) if '<style is:global>' in l)
print(f"<style is:global> now at line {style_global_idx + 1}")
print(f"Line {style_global_idx + 2}: {lines_after[style_global_idx + 1][:60]!r}")
print(f"--bg-darker present: {'--bg-darker: #14171b' in result}")
print(f"Total <style is:global> tags: {result.count('<style is:global>')}")
print(f"Total lines: {len(lines_after)}")
print("PASS: Liberty style block fixed.")
