"""
Fix curly brace expressions in HTML bodies of all PDP Astro files.
Astro treats {expr} in HTML as template expressions. Curly braces in HTML
(e.g., in <code> tags showing SKU patterns) must be escaped as &#123; and &#125;.
This script only fixes occurrences in actual HTML body (not in script/style/comment blocks).
"""
import re
import os

VALID_ASTRO_EXPRS = {'{true}', '{false}', '{undefined}', '{null}'}

def get_in_block_positions(content):
    """Return set of character positions that are inside script/style/comment blocks."""
    scripts = list(re.finditer(r'<script[^>]*>([\s\S]*?)</script>', content))
    styles = list(re.finditer(r'<style[^>]*>([\s\S]*?)</style>', content))
    comments = list(re.finditer(r'<!--[\s\S]*?-->', content))
    
    in_block = set()
    for m in scripts + styles + comments:
        for i in range(m.start(), m.end()):
            in_block.add(i)
    return in_block

def fix_html_curly_braces(content):
    """Replace {expr} in HTML body with &#123;expr&#125;."""
    in_block = get_in_block_positions(content)
    
    result = []
    i = 0
    while i < len(content):
        if content[i] == '{' and i not in in_block:
            # Find the closing brace
            j = content.find('}', i)
            if j == -1:
                result.append(content[i:])
                break
            expr = content[i:j+1]
            if expr in VALID_ASTRO_EXPRS:
                result.append(expr)
            else:
                # Escape the curly braces
                inner = content[i+1:j]
                result.append('&#123;' + inner + '&#125;')
            i = j + 1
        else:
            result.append(content[i])
            i += 1
    
    return ''.join(result)

def check_and_fix_file(fpath):
    with open(fpath, 'r') as f:
        content = f.read()
    
    in_block = get_in_block_positions(content)
    
    # Find problematic expressions
    issues = []
    for m in re.finditer(r'\{[^}]+\}', content):
        if m.start() not in in_block:
            expr = m.group()
            if expr not in VALID_ASTRO_EXPRS:
                line = content[:m.start()].count('\n') + 1
                issues.append((line, expr, m.start()))
    
    if not issues:
        return False
    
    print(f"\n{os.path.basename(os.path.dirname(fpath))}:")
    for line, expr, pos in issues:
        ctx = content[max(0,pos-30):pos+len(expr)+30]
        print(f"  Line {line}: {expr} -> escaping")
    
    # Fix: only escape the problematic occurrences
    new_content = ''
    pos = 0
    while pos < len(content):
        if content[pos] == '{' and pos not in in_block:
            j = content.find('}', pos)
            if j == -1:
                new_content += content[pos:]
                break
            expr = content[pos:j+1]
            if expr in VALID_ASTRO_EXPRS:
                new_content += expr
            else:
                inner = content[pos+1:j]
                new_content += '&#123;' + inner + '&#125;'
            pos = j + 1
        else:
            new_content += content[pos]
            pos += 1
    
    with open(fpath, 'w') as f:
        f.write(new_content)
    return True

pdp_dir = '/home/ubuntu/alg-website-src/src/pages/products'
fixed = []
for slug in sorted(os.listdir(pdp_dir)):
    fpath = os.path.join(pdp_dir, slug, 'index.astro')
    if not os.path.exists(fpath):
        continue
    if check_and_fix_file(fpath):
        fixed.append(slug)

print(f"\n\nFixed {len(fixed)} files: {', '.join(fixed)}")
