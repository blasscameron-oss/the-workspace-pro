#!/usr/bin/env python3
import re
import sys
import os

# Mapping of example.com paths to Amazon search URLs
MAPPINGS = {
    'chairs': 'https://www.amazon.com/s?k=ergonomic+chair',
    'organization': 'https://www.amazon.com/s?k=office+organization+tools',
    'dual-monitor': 'https://www.amazon.com/s?k=dual+monitor+stand',
    'standing-desks': 'https://www.amazon.com/s?k=standing+desk',
}

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find all anchor tags with example.com
    # Pattern: <a [^>]*href="https://example.com/([^"]+)"[^>]*>
    pattern = r'(<a\s[^>]*href=")https://example\.com/([^"]+)("[^>]*>)'
    
    def replace(match):
        prefix = match.group(1)
        path = match.group(2)
        suffix = match.group(3)
        
        if path not in MAPPINGS:
            print(f"  Warning: unknown example.com path '{path}' in {filepath}")
            return match.group(0)
        
        new_url = MAPPINGS[path]
        
        # Check if target="_blank" already present
        tag = match.group(0)
        if 'target="_blank"' not in tag:
            # Add target="_blank" before closing >
            if suffix.endswith('>'):
                suffix = ' target="_blank"' + suffix
            else:
                # suffix is something like "> with other attributes"
                pass
        
        # Check if rel="sponsored noopener noreferrer" already present
        if 'rel=' not in tag:
            # Add rel attribute
            if suffix.endswith('>'):
                suffix = ' rel="sponsored noopener noreferrer"' + suffix
            else:
                # suffix already has other attributes, insert before >
                pass
        
        # Simple approach: just replace URL and ensure target and rel
        # Let's reconstruct the tag with both attributes
        # We'll just replace URL and add target and rel if missing
        # For simplicity, we'll replace the whole tag with a standard one
        # But we need to preserve any existing classes, id, etc.
        # Let's do a more robust approach: parse attributes
        # But for now, just replace URL and add attributes if missing
        
        # Extract the rest of the tag after href
        # Actually, we'll just replace the href and ensure target and rel
        # We'll use regex to add attributes
        
        # Simple: replace URL and add target and rel
        new_tag = f'{prefix}{new_url}" target="_blank" rel="sponsored noopener noreferrer"{suffix}'
        return new_tag
    
    new_content = re.sub(pattern, replace, content)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        return True
    return False

def main():
    files = [
        'content/ergonomic-office-chair-buying-guide/index.html',
        'content/small-home-office-organization-hacks/index.html',
        'content/dual-monitor-setup-productivity/index.html',
        'content/best-standing-desks-under-500/index.html',
    ]
    
    updated = 0
    for f in files:
        if os.path.exists(f):
            if process_file(f):
                print(f"  Updated: {f}")
                updated += 1
        else:
            print(f"  Warning: {f} not found")
    
    print(f"✅ Updated {updated} files.")

if __name__ == '__main__':
    main()