#!/usr/bin/env python3
"""
planoARCH audit cleanup:
  Patch 1: Remove family/round-out cards with href=/products/controls/ or /products/hallmark/
  Patch 2: Strip 'dowpremium' text (replace with empty string or remove containing element)
  Patch 3: Scrub dev-artifact HTML comments matching 8 patterns
"""
import re, os

SLUGS = [
    'astra','solstice','solstice-safezone','spectra','luxmark','proarch-t',
    'trackstar','lara','luna','waymark','proarch','retroarch-p1','retroarch-t1'
]

DEV_PATTERNS = [
    'PDP_BUILD_PLAYBOOK',
    'WorkDrive URLs LIVE',
    '/PM/v2_mockups/',
    '/PM/playbooks/',
    'wired 2026',
    'captured 2026',
    'same canonical pattern as',
    'planoARCH',  # plain-A (not glyph)
]

def remove_card_by_href(content, href_pattern):
    """Remove entire <a class="family-card"> or <a class="round-out-card"> block containing href."""
    # Match any <a ...> block that contains the target href
    # The card can be family-card, round-out-card, or similar
    card_re = re.compile(
        r'<a\b[^>]*class="[^"]*(?:family-card|round-out-card|product-card)[^"]*"[^>]*>.*?</a>',
        re.DOTALL
    )
    
    removed = 0
    def replacer(m):
        nonlocal removed
        if href_pattern in m.group(0):
            removed += 1
            return ''
        return m.group(0)
    
    new_content = card_re.sub(replacer, content)
    return new_content, removed

def strip_dowpremium(content):
    """Remove 'dowpremium' text — it appears as a CSS class or text node."""
    # As a class in class attribute: class="... dowpremium ..."
    # As standalone text
    original = content
    
    # Remove as CSS class
    content = re.sub(r'\bdowpremium\b', '', content)
    
    # Clean up double spaces in class attrs
    content = re.sub(r'class="([^"]*?)\s{2,}([^"]*?)"', lambda m: f'class="{m.group(1).strip()} {m.group(2).strip()}"', content)
    content = re.sub(r'class="\s+"', 'class=""', content)
    
    count = original.count('dowpremium')
    return content, count

def scrub_dev_comments(content):
    """Remove entire <!-- ... --> blocks matching any dev-artifact pattern."""
    removed = 0
    
    def comment_replacer(m):
        nonlocal removed
        comment_body = m.group(0)
        if any(p in comment_body for p in DEV_PATTERNS):
            removed += 1
            return ''
        return comment_body
    
    new_content = re.sub(r'<!--.*?-->', comment_replacer, content, flags=re.DOTALL)
    return new_content, removed

total_p1 = total_p2 = total_p3 = 0

for slug in SLUGS:
    f = f'public/products/{slug}/index.html'
    if not os.path.exists(f):
        print(f'  SKIP (missing): {slug}')
        continue
    
    with open(f) as fh:
        content = fh.read()
    
    original = content
    p1_removed = p2_removed = p3_removed = 0
    
    # Patch 1: Remove broken href cards
    for bad_href in ['/products/controls/', '/products/hallmark/']:
        content, n = remove_card_by_href(content, bad_href)
        p1_removed += n
    
    # Patch 2: Strip dowpremium
    content, p2_removed = strip_dowpremium(content)
    
    # Patch 3: Scrub dev-artifact comments
    content, p3_removed = scrub_dev_comments(content)
    
    if content != original:
        with open(f, 'w') as fh:
            fh.write(content)
        print(f'  ✅ {slug}: P1={p1_removed} cards removed, P2={p2_removed} dowpremium, P3={p3_removed} comments')
        total_p1 += p1_removed
        total_p2 += p2_removed
        total_p3 += p3_removed
    else:
        print(f'  — {slug}: no changes')

print(f'\nTotals: P1={total_p1} cards, P2={total_p2} dowpremium, P3={total_p3} comments')
