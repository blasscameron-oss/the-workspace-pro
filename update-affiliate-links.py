#!/usr/bin/env python3
"""
Replace placeholder affiliate links with Amazon search links containing your affiliate tag.
"""

import os
import re
import json
from pathlib import Path

# Configuration
AFFILIATE_TAG_FILE = "affiliate-tag.txt"
HTML_FILES = ["index.html", "deals.html"]

# Product mapping: placeholder path -> Amazon search query
PRODUCT_MAPPING = {
    "desk": "standing+desk",
    "chair": "ergonomic+office+chair",
    "monitor": "32+inch+4k+monitor",
    "arm": "monitor+arm+gas+spring",
    "keyboard": "ergonomic+split+keyboard",
}

def read_affiliate_tag():
    """Read affiliate tag from file, fallback to placeholder."""
    if os.path.exists(AFFILIATE_TAG_FILE):
        with open(AFFILIATE_TAG_FILE, "r") as f:
            tag = f.read().strip()
            if tag:
                return tag
    return "workspacepro-20"  # fallback

def generate_amazon_url(query, tag):
    """Generate Amazon search URL with affiliate tag."""
    return f"https://www.amazon.com/s?k={query}&tag={tag}"

def update_file(filepath, tag):
    """Replace example.com links in HTML file."""
    with open(filepath, "r") as f:
        content = f.read()
    
    # Find all example.com links
    pattern = r'href="https://example\.com/([^"]+)"'
    
    def replace_link(match):
        path = match.group(1)
        if path in PRODUCT_MAPPING:
            query = PRODUCT_MAPPING[path]
            new_url = generate_amazon_url(query, tag)
            return f'href="{new_url}"'
        else:
            # Default fallback
            new_url = generate_amazon_url(path, tag)
            return f'href="{new_url}"'
    
    new_content = re.sub(pattern, replace_link, content)
    
    if new_content != content:
        with open(filepath, "w") as f:
            f.write(new_content)
        print(f"Updated {filepath}")
        return True
    else:
        print(f"No changes in {filepath}")
        return False

def main():
    print("Updating affiliate links...")
    tag = read_affiliate_tag()
    print(f"Using affiliate tag: {tag}")
    
    updated = False
    for filename in HTML_FILES:
        if os.path.exists(filename):
            if update_file(filename, tag):
                updated = True
        else:
            print(f"Warning: {filename} not found")
    
    if updated:
        print("\nAffiliate links updated successfully.")
        print("Next steps:")
        print("1. Replace the placeholder tag in 'affiliate-tag.txt' with your actual Amazon Associates tag.")
        print("2. Review the updated HTML files to ensure links are correct.")
        print("3. Deploy the changes (git commit && git push).")
    else:
        print("No files needed updating.")

if __name__ == "__main__":
    main()