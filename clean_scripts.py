#!/usr/bin/env python3
"""
Fix interfering old inline scripts on all pages.

Two patterns to replace with clean dark mode persistence:

Pattern A (homepage-style): <script> ... SITE-WIDE DARK MODE & MOBILE MENU ... </script>
Pattern B (guide-style):    <script> ... Dark mode toggle functions ... toggleMobileMenu ... toggleSearch ... </script>

Also surgically removes:
- Old search overlay IIFE (quiz page)
- Old toggleMobileMenu + toggleSearch functions
- touchstart + click-outside handlers
- mobileMenuButton references (wrong ID)
"""

import re, glob, os

DARK = """        // Dark mode persistence
        var stored = localStorage.getItem('darkMode');
        if (stored === 'true') document.documentElement.classList.add('dark');
        else if (stored === 'false') document.documentElement.classList.remove('dark');
        function toggleDarkMode() {
            var isDark = document.documentElement.classList.contains('dark');
            if (isDark) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('darkMode', 'false');
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('darkMode', 'true');
            }
            if (window.updateDarkModeIcon) updateDarkModeIcon();
        }
        window.toggleDarkMode = toggleDarkMode;"""


def fix_file(fp):
    with open(fp) as f:
        c = f.read()
    orig = c
    actions = []
    prev = c

    # 1. Homepage-style full block
    c = re.sub(
        r'<script>\s*\n\s*// =+\s*\n\s*// SITE-WIDE DARK MODE & MOBILE MENU\s*\n\s*// =+\s*[\s\S]*?</script>',
        '<script>\n' + DARK + '\n    </script>',
        c, count=1
    )
    if c != prev: actions.append("homepage-block"); prev = c

    # 2. Guide-style full block
    c = re.sub(
        r'<script>\s*\n\s*// Dark mode toggle functions[\s\S]*?</script>',
        '<script>\n' + DARK + '\n    </script>',
        c, count=1
    )
    if c != prev: actions.append("guide-block"); prev = c

    # 3. Search overlay IIFE (quiz page)
    c = re.sub(
        r'\s*// =+\s*\n\s*// SEARCH OVERLAY\s*\n\s*// =+\s*\n\s*' +
        r'\(function\(\)\s*\{[\s\S]*?searchOverlay[\s\S]*?\}\s*\)\(\)\s*;?',
        '', c, count=1
    )
    if c != prev: actions.append("search-iife"); prev = c

    # 4. Standalone toggleMobileMenu
    c = re.sub(
        r'\n\s*// Mobile menu toggle\s*\n\s*' +
        r'function\s+toggleMobileMenu\s*\(\s*\)\s*\{[\s\S]*?\}',
        '', c
    )
    if c != prev: actions.append("toggleMobileMenu"); prev = c

    # 5. mmBtn handlers
    c = re.sub(
        r'\s*var\s+mmBtn\s*=\s*document\.getElementById\([\'"]mobileMenu(?:Toggle|Button)[\'"]\)[\s\S]*?' +
        r'mmBtn\.addEventListener\([\'"]touchstart[\'"],[\s\S]*?\}\s*\)\s*;?',
        '', c
    )
    if c != prev: actions.append("mmBtn"); prev = c

    # 6. click-outside handler
    c = re.sub(
        r'\s*document\.addEventListener\([\'"]click[\'"],\s*function\s*\(e\)\s*\{[\s\S]*?' +
        r'mobileMenu[\s\S]*?menu\.classList\.add\([\'"]hidden[\'"]\)[\s\S]*?\}\s*\)\s*;',
        '', c
    )
    if c != prev: actions.append("click-outside"); prev = c

    # 7. Standalone toggleSearch
    c = re.sub(
        r'\n\s*// Search toggle\s*\n\s*' +
        r'function\s+toggleSearch\s*\(\s*\)\s*\{[\s\S]*?\}',
        '', c
    )
    if c != prev: actions.append("toggleSearch"); prev = c

    # 8. Clean up orphan updateDarkModeIcon calls (now in nav.js)
    c = re.sub(r'\n\s*// Initialize dark mode icon\s*\n\s*updateDarkModeIcon\(\);', '', c)
    if c != prev: actions.append("orphan-icon")

    c = re.sub(r'\n{4,}', '\n\n\n', c)

    if actions:
        with open(fp, 'w') as f:
            f.write(c)
    return actions


def main():
    files = ['index.html', 'deals.html'] + sorted(glob.glob('content/*/index.html'))
    total = 0
    for fp in [f for f in files if os.path.isfile(f)]:
        name = os.path.relpath(fp)
        acts = fix_file(fp)
        if acts:
            print(f"  ✅ {name:50s} {', '.join(acts)}")
            total += 1
        else:
            print(f"  --- {name:50s} (clean)")
    print(f"\n✅ Fixed {total} pages")

if __name__ == '__main__':
    main()
