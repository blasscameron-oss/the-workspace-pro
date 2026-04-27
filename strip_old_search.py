#!/usr/bin/env python3
"""Remove leftover old search overlays from 15 guide-style pages."""

import re, glob

for f in ['index.html', 'deals.html'] + sorted(glob.glob('content/*/index.html')):
    with open(f) as fp:
        content = fp.read()
    
    # Count how many times search-overlay appears
    count = len(re.findall(r'id="search-overlay"', content))
    if count <= 1:
        continue
    
    # Remove OLD search overlay divs (those with z-50 instead of z-[60],
    # or with aria-hidden="true")
    original = content
    content = re.sub(
        r'<div[^>]*aria-hidden="true"[^>]*id="search-overlay"[^>]*>.*?</div>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Also catch the guide-style search overlay pattern specifically
    # (starts after footer, ends before next section)
    content = re.sub(
        r'<div[^>]*id="search-overlay"[^>]*class="[^"]*z-50[^"]*"[^>]*>.*?</div>',
        '',
        content,
        flags=re.DOTALL
    )
    
    if content != original:
        with open(f, 'w') as fp:
            fp.write(content)
        print(f"  ✅ Fixed {f} ({'before' if count>1 else 'already clean'})")
    else:
        print(f"  ⚠️  Not cleaned: {f} ({count} matches)")
