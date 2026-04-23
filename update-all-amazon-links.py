#!/usr/bin/env python3
"""
Add affiliate tag to all Amazon links in HTML files.
"""

import os
import re
import sys

TAG_FILE = "affiliate-tag.txt"

def read_tag():
    if os.path.exists(TAG_FILE):
        with open(TAG_FILE, "r") as f:
            tag = f.read().strip()
            if tag:
                return tag
    print(f"Error: {TAG_FILE} not found or empty.")
    sys.exit(1)

def add_tag_to_url(url, tag):
    """Add affiliate tag to Amazon URL."""
    # Already has tag? Skip
    if re.search(r'[?&]tag=', url):
        return url
    # Determine separator
    if '?' in url:
        separator = '&'
    else:
        separator = '?'
    return f"{url}{separator}tag={tag}"

def process_file(filepath, tag):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Pattern for Amazon URLs
    # Match href="https://www.amazon.com/..."
    pattern = r'(href="https://www\.amazon\.com[^"]+)"'
    
    def replace(match):
        url = match.group(1)
        new_url = add_tag_to_url(url, tag)
        return f'{new_url}"'
    
    new_content = re.sub(pattern, replace, content)
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        return True
    return False

def main():
    tag = read_tag()
    print(f"Using affiliate tag: {tag}")
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk("."):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    
    updated = 0
    for filepath in html_files:
        if process_file(filepath, tag):
            print(f"Updated {filepath}")
            updated += 1
    
    print(f"\nUpdated {updated} files.")
    print("Don't forget to commit and deploy.")

if __name__ == "__main__":
    main()