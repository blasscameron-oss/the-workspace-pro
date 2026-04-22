#!/usr/bin/env python3
import sys
import os
import re

def replace_img_with_picture(html_content):
    """Replace img tags with picture elements for WebP fallback."""
    # Pattern to match img tags with src containing .jpg
    pattern = r'<img\s+([^>]*?)src="([^"]+\.jpg)"([^>]*?)>'
    
    def replace_match(match):
        attrs_before = match.group(1)
        src = match.group(2)
        attrs_after = match.group(3)
        
        # Get alt text from attributes
        alt_match = re.search(r'alt="([^"]*)"', attrs_before + attrs_after)
        alt = alt_match.group(1) if alt_match else ''
        
        # Get class attribute
        class_match = re.search(r'class="([^"]*)"', attrs_before + attrs_after)
        class_attr = class_match.group(1) if class_match else ''
        
        # Get loading/decoding attributes
        loading_match = re.search(r'loading="([^"]*)"', attrs_before + attrs_after)
        loading = loading_match.group(1) if loading_match else 'lazy'
        
        decoding_match = re.search(r'decoding="([^"]*)"', attrs_before + attrs_after)
        decoding = decoding_match.group(1) if decoding_match else 'async'
        
        # Create WebP src
        webp_src = src.replace('.jpg', '.webp')
        
        # Build picture element
        picture = f'''<picture>
  <source srcset="{webp_src}" type="image/webp">
  <source srcset="{src}" type="image/jpeg">
  <img src="{src}" alt="{alt}" loading="{loading}" decoding="{decoding}" class="{class_attr}">
</picture>'''
        
        return picture
    
    # Replace all matches
    return re.sub(pattern, replace_match, html_content)

def process_file(filename):
    """Process a single HTML file."""
    print(f"Processing {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = replace_img_with_picture(content)
    
    # Write back
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated {filename}")

def main():
    files = ['index.html', 'deals.html']
    
    for file in files:
        if os.path.exists(file):
            process_file(file)
        else:
            print(f"File {file} not found")
    
    # Also update guide images in content directory if needed
    # (optional)

if __name__ == '__main__':
    main()