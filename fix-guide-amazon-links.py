#!/usr/bin/env python3
"""Add affiliate tag to Amazon links in guide pages (excluding deals.html and index.html)."""

import os
import re

TAG = "workspacepro-20"
CONTENT_DIR = "content"

def fix_amazon_links_in_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Pattern: href="https://www.amazon.com/..." without existing tag=
    def add_tag(match):
        url = match.group(1)
        if 'tag=' in url:
            return f'href="{url}"'  # Already tagged
        if '?' in url:
            new_url = f'{url}&tag={TAG}'
        else:
            new_url = f'{url}?tag={TAG}'
        return f'href="{new_url}"'
    
    new_content = re.sub(
        r'href="(https?://(?:www\.)?amazon\.com[^"]*)"',
        add_tag,
        content,
        flags=re.IGNORECASE
    )
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        return True
    return False

fixed = []
for root, dirs, files in os.walk(CONTENT_DIR):
    for f in files:
        if f == 'index.html':
            path = os.path.join(root, f)
            if fix_amazon_links_in_file(path):
                name = os.path.basename(root)
                fixed.append(name)
                print(f'  ✓ {name}')

print(f'\nFixed {len(fixed)} guide pages with Amazon links.')
