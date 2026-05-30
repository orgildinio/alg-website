"""
Binary search to find the exact line in radiator/index.astro causing the build error.
Strategy: replace the second half of the new file with the old file's content,
then narrow down which section is causing the issue.
"""
import subprocess
import shutil

NEW_FILE = 'src/pages/products/radiator/index.astro'
OLD_FILE = '/tmp/radiator_old_full.astro'
BACKUP = '/tmp/radiator_binary_backup.astro'

with open(NEW_FILE, 'r') as f:
    new_content = f.read()

with open(OLD_FILE, 'r') as f:
    old_content = f.read()

# Save backup
with open(BACKUP, 'w') as f:
    f.write(new_content)

new_lines = new_content.split('\n')
old_lines = old_content.split('\n')

print(f"New file: {len(new_lines)} lines")
print(f"Old file: {len(old_lines)} lines")

def test_build(content):
    with open(NEW_FILE, 'w') as f:
        f.write(content)
    result = subprocess.run(
        ['pnpm', 'build'],
        capture_output=True, text=True, cwd='/home/ubuntu/alg-website-src'
    )
    success = 'Syntax error' not in result.stdout and 'Syntax error' not in result.stderr
    return success

# Binary search: find the smallest section of new_lines that causes the error
# Start with the first half of the new file + rest of old file
lo, hi = 0, len(new_lines)

print("\nBinary searching for the problematic line...")

while lo < hi - 1:
    mid = (lo + hi) // 2
    # Use first `mid` lines from new, rest from old
    test_content = '\n'.join(new_lines[:mid]) + '\n' + '\n'.join(old_lines[mid:])
    
    if test_build(test_content):
        print(f"  Lines 0-{mid}: OK (issue is in lines {mid}-{hi})")
        lo = mid
    else:
        print(f"  Lines 0-{mid}: FAIL (issue is in lines {lo}-{mid})")
        hi = mid

print(f"\nProblem is around line {lo}-{hi}")
print(f"New line {lo}: {repr(new_lines[lo-1] if lo > 0 else '')}")
print(f"New line {hi}: {repr(new_lines[hi-1] if hi <= len(new_lines) else '')}")

# Restore new file
with open(NEW_FILE, 'w') as f:
    f.write(new_content)
print("\nRestored new file")
