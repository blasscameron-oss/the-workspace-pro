#!/usr/bin/env python3
import os
import re
import sys

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Remove Twitter and Instagram list items
    # Pattern matches the entire <li> line with indentation
    # We'll replace with empty string (remove line)
    # Using regex with multiline flag
    # Note: This might leave empty lines; that's fine.
    content = re.sub(r'^\s*<li><a href="#" class="hover:text-white transition">Twitter</a></li>\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*<li><a href="#" class="hover:text-white transition">Instagram</a></li>\s*$', '', content, flags=re.MULTILINE)
    
    # Fix Privacy Policy link (href="#" to /privacy/)
    content = re.sub(r'<a href="#" class="text-accent hover:underline">Privacy Policy</a>', '<a href="/privacy/" class="text-accent hover:underline">Privacy Policy</a>', content)
    
    # Fix Terms link (href="#" to /terms/) and update text to "Terms of Service"
    content = re.sub(r'<a href="#" class="text-accent hover:underline">Terms</a>', '<a href="/terms/" class="text-accent hover:underline">Terms of Service</a>', content)
    
    # Also fix "Terms of Service" if already present but href="#"
    content = re.sub(r'<a href="#" class="text-accent hover:underline">Terms of Service</a>', '<a href="/terms/" class="text-accent hover:underline">Terms of Service</a>', content)
    
    if content != original:
        print(f'Updated {filepath}')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    # Find all HTML files excluding _site directory
    for root, dirs, files in os.walk('.'):
        if '_site' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                fix_file(filepath)

if __name__ == '__main__':
    main()