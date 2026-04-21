#!/usr/bin/env python3
"""
Validate that SEO and performance improvements have been applied correctly.
"""
import os
import re
import sys

def check_file(filepath):
    """Check a single HTML file for improvements."""
    print(f"Checking: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        'custom.css': 'Has external CSS reference' in content,
        'unique_description': 'Productive Workspace Guides &amp; Reviews' not in content,
        'canonical': 'rel="canonical"' in content,
        'json_ld': 'application/ld+json' in content,
        'lazy_loading': 'loading="lazy"' in content or 'loading=\'lazy\'' in content,
    }
    
    # Check for meta description length
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    if desc_match:
        desc = desc_match.group(1)
        checks['desc_length'] = 50 <= len(desc) <= 160
        checks['desc_not_generic'] = desc != 'Productive Workspace Guides & Reviews'
    else:
        checks['desc_length'] = False
        checks['desc_not_generic'] = False
    
    results = []
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        results.append(f"{status} {check}")
    
    print("  " + " | ".join(results))
    return all(checks.values())

def main():
    print("Validating improvements across all HTML files...\n")
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk("."):
        # Skip some directories
        if '_site' in root or 'DEPLOY' in root or 'AFFILIATE_SETUP' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Found {len(html_files)} HTML files")
    
    passed_files = 0
    failed_files = 0
    
    for file in sorted(html_files):
        try:
            if check_file(file):
                passed_files += 1
            else:
                failed_files += 1
        except Exception as e:
            print(f"  Error checking {file}: {e}")
            failed_files += 1
        print()
    
    print(f"\nSummary:")
    print(f"  Passed: {passed_files}")
    print(f"  Failed: {failed_files}")
    print(f"  Total: {len(html_files)}")
    
    if failed_files > 0:
        print("\n⚠ Some files need attention.")
        return 1
    else:
        print("\n✅ All files pass validation!")
        return 0

if __name__ == '__main__':
    sys.exit(main())