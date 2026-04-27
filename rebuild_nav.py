#!/usr/bin/env python3
"""
Unified navigation rebuild — replaces ALL nav variants with the new
Top Persistent Navigation Bar across every page.
"""

import os, re, glob, shutil, subprocess as sp

NEW_NAV = """    <!-- Top Persistent Navigation Bar -->
    <header class="fixed top-0 left-0 right-0 z-50 bg-card/95 dark:bg-neutral-900/95 backdrop-blur-md border-b border-border dark:border-neutral-800 shadow-sm" role="banner">
        <div class="max-w-7xl mx-auto px-4 sm:px-6">
            <div class="flex items-center justify-between h-14 md:h-16">
                
                <!-- Logo -->
                <a href="/" class="flex items-center gap-2 shrink-0" aria-label="The Workspace Pro \u2013 Home">
                    <div class="w-9 h-9 md:w-10 md:h-10 rounded-lg bg-primary flex items-center justify-center shadow-sm">
                        <i class="fas fa-desktop text-white text-base md:text-lg"></i>
                    </div>
                    <div class="hidden sm:block">
                        <span class="text-lg md:text-xl font-bold text-primary font-serif whitespace-nowrap">The Workspace Pro</span>
                    </div>
                </a>
                
                <!-- Desktop Navigation -->
                <nav class="hidden md:flex items-center space-x-1">
                    <a href="/" class="px-3 py-2 text-sm font-medium hover:text-primary transition-colors rounded-lg hover:bg-surface">Home</a>
                    <a href="/content/guides/" class="px-3 py-2 text-sm font-medium hover:text-primary transition-colors rounded-lg hover:bg-surface">Guides</a>
                    <a href="/deals/" class="px-3 py-2 text-sm font-medium hover:text-primary transition-colors rounded-lg hover:bg-surface">Deals</a>
                    <a href="/content/quiz/" class="px-3 py-2 text-sm font-bold text-primary bg-primary/10 rounded-lg border border-primary/20 hover:bg-primary/15 transition-colors flex items-center gap-1"><i class="fas fa-star text-xs"></i> Quiz</a>
                    <a href="/content/community-setups/" class="px-3 py-2 text-sm font-medium hover:text-primary transition-colors rounded-lg hover:bg-surface">Community</a>
                </nav>
                
                <!-- Right side controls -->
                <div class="flex items-center gap-1 md:gap-1.5">
                    <button id="searchToggle" onclick="toggleSearch()" class="p-2 rounded-full hover:bg-surface dark:hover:bg-neutral-800 transition-colors" aria-label="Open search">
                        <i class="fas fa-search text-text-light dark:text-neutral-400 text-lg"></i>
                    </button>
                    <button id="navDarkToggle" onclick="toggleDarkMode()" class="p-2 rounded-full hover:bg-surface dark:hover:bg-neutral-800 transition-colors" aria-label="Toggle dark mode">
                        <i class="fas fa-moon text-primary text-lg" id="navDarkIcon"></i>
                        <i class="fas fa-sun text-primary text-lg hidden" id="navLightIcon"></i>
                    </button>
                    <button id="mobileMenuToggle" onclick="toggleMobileMenu()" class="md:hidden p-2 rounded-lg hover:bg-surface dark:hover:bg-neutral-800 transition-colors" aria-label="Open menu">
                        <i class="fas fa-bars text-xl text-text dark:text-neutral-200"></i>
                    </button>
                </div>
            </div>
        </div>
        
    </header>
        
        <!-- Mobile menu backdrop -->
        <div id="mobileMenuOverlay" class="hidden fixed inset-0 z-40 bg-black/40" onclick="closeMobileMenu()"></div>
        
        <!-- Mobile slide-in panel -->
        <div id="mobileMenu" class="hidden fixed top-0 right-0 h-screen w-72 max-w-[85vw] z-50 bg-card dark:bg-neutral-900 shadow-2xl overflow-y-auto">
            <div class="flex flex-col h-full">
                <div class="flex items-center justify-between p-4 border-b border-border dark:border-neutral-800">
                    <span class="font-bold text-primary"><i class="fas fa-desktop mr-2"></i>Menu</span>
                    <button onclick="closeMobileMenu()" class="p-2 rounded-full hover:bg-surface dark:hover:bg-neutral-800 transition-colors" aria-label="Close menu">
                        <i class="fas fa-times text-xl"></i>
                    </button>
                </div>
                <div class="flex-1 p-4 space-y-1">
                    <a href="/" class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-surface dark:hover:bg-neutral-800 font-medium transition-colors" onclick="closeMobileMenu()"><i class="fas fa-home w-5 text-primary"></i> Home</a>
                    <a href="/content/guides/" class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-surface dark:hover:bg-neutral-800 font-medium transition-colors" onclick="closeMobileMenu()"><i class="fas fa-compass w-5 text-primary"></i> Guides</a>
                    <a href="/deals/" class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-surface dark:hover:bg-neutral-800 font-medium transition-colors" onclick="closeMobileMenu()"><i class="fas fa-tag w-5 text-primary"></i> Deals</a>
                    <a href="/content/quiz/" class="flex items-center gap-3 px-4 py-3 rounded-lg bg-primary/10 border border-primary/20 font-bold text-primary transition-colors" onclick="closeMobileMenu()"><i class="fas fa-star w-5 text-primary"></i> Quiz</a>
                    <a href="/content/community-setups/" class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-surface dark:hover:bg-neutral-800 font-medium transition-colors" onclick="closeMobileMenu()"><i class="fas fa-users w-5 text-primary"></i> Community</a>
                    <hr class="my-4 border-border dark:border-neutral-800">
                    <a href="/content/tips/" class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-surface dark:hover:bg-neutral-800 font-medium transition-colors" onclick="closeMobileMenu()"><i class="fas fa-lightbulb w-5 text-primary"></i> Tips</a>
                    <a href="/podcasts/" class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-surface dark:hover:bg-neutral-800 font-medium transition-colors" onclick="closeMobileMenu()"><i class="fas fa-podcast w-5 text-primary"></i> Podcasts</a>
                    <a href="/content/about/" class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-surface dark:hover:bg-neutral-800 font-medium transition-colors" onclick="closeMobileMenu()"><i class="fas fa-info-circle w-5 text-primary"></i> About</a>
                </div>
                <div class="p-4 border-t border-border dark:border-neutral-800">
                    <a href="#newsletter" class="block w-full text-center bg-primary hover:bg-primary-light text-white font-semibold py-3 px-4 rounded-lg transition-colors" onclick="closeMobileMenu()"><i class="fas fa-envelope mr-2"></i> Get the Newsletter</a>
                </div>
            </div>
        </div>
        
        <!-- Search overlay -->
        <div id="search-overlay" class="hidden fixed inset-0 bg-black/50 z-[60] flex items-start justify-center pt-16 md:pt-24">
            <div class="bg-card dark:bg-neutral-900 rounded-xl shadow-2xl w-full max-w-2xl mx-4 mt-8 animate-fade-in">
                <div class="p-4 md:p-6">
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-lg md:text-xl font-bold">Search The Workspace Pro</h2>
                        <button onclick="closeSearch()" class="p-2 hover:bg-surface dark:hover:bg-neutral-800 rounded-full transition-colors" aria-label="Close search">
                            <i class="fas fa-times text-xl"></i>
                        </button>
                    </div>
                    <div class="relative">
                        <input type="text" id="search-input" placeholder="Type to search guides, tips, products..." class="w-full p-3 md:p-4 pl-12 rounded-lg border border-border dark:border-neutral-700 bg-surface dark:bg-neutral-800 focus:outline-none focus:ring-2 focus:ring-primary text-text dark:text-neutral-100" autocomplete="off">
                        <i class="fas fa-search absolute left-4 top-1/2 transform -translate-y-1/2 text-text-light dark:text-neutral-500"></i>
                    </div>
                    <div id="search-results" class="mt-4 max-h-80 overflow-y-auto hidden">
                        <!-- Results populated by search.min.js -->
                    </div>
                </div>
            </div>
        </div>"""

NAV_JS_SCRIPT = '\n    <script src="/static/js/nav.js" defer></script>'


def replace_nav_in_file(filepath):
    """Replace the nav section in a single HTML file, with all cleanups done BEFORE injection."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # ==========================================================
    # Phase 1: Clean OLD patterns from the original file
    # (before injecting new nav — prevents double-matching)
    # ==========================================================
    
    # 1a. Remove old standalone search overlays (outside nav)
    content = re.sub(
        r'<!-- Search overlay.*?-->.*?<div[^>]*id="(?:searchOverlay|search-overlay)"[^>]*>.*?</div>',
        '',
        content,
        count=1,
        flags=re.DOTALL
    )
    
    # 1b. Remove old standalone mobile menu divs (outside nav)
    #    Only match those using 'absolute' or 'sticky' positioning (old style),
    #    NOT 'fixed' (new style).
    content = re.sub(
        r'<!-- Mobile.*?-->.*?<div[^>]*id="(?:mobileMenu|mobile-menu)"[^>]*class="[^"]*\b(?:absolute|sticky)\b[^"]*"[^>]*>.*?</div>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 1c. Remove old mobile menu toggle button blocks
    content = re.sub(
        r'\s*<!\s*-- Mobile menu button -->.*?<div class="md:hidden flex items-center gap-2">.*?</div>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # ==========================================================
    # Phase 2: Replace the nav section itself
    # ==========================================================
    
    nav_replaced = False
    header_patterns = [
        # With preceding comment
        (r'^\s*<!--\s*(?:Header|header).*?-->?\s*\n?\s*<header[^>]*>.*?</header>', re.DOTALL | re.MULTILINE),
        # Just header tag
        (r'^\s*<header[^>]*>.*?</header>', re.DOTALL | re.MULTILINE),
        # nav tag (contact page)
        (r'^\s*<nav[^>]*role="navigation"[^>]*>.*?</nav>', re.DOTALL | re.MULTILINE),
    ]
    
    for pattern, flags in header_patterns:
        new_content = re.sub(pattern, NEW_NAV, content, count=1, flags=flags)
        if new_content != content:
            content = new_content
            nav_replaced = True
            break
    
    if not nav_replaced:
        print(f"  ❌ Could not find nav in {filepath}")
        # Restore from git
        sp.run(['git', 'checkout', '--', filepath], capture_output=True)
        return False
    
    # ==========================================================
    # Phase 3: Post-injection adjustments
    # ==========================================================
    
    # 3a. Add pt-14 to main element if missing
    def add_main_padding(match):
        attrs = match.group(1) or ''
        if 'pt-14' in attrs or 'pt-16' in attrs:
            return match.group(0)
        if 'class="' in attrs:
            return match.group(0).replace('class="', 'class="pt-14 md:pt-16 ', 1)
        elif "class='" in attrs:
            return match.group(0).replace("class='", "class='pt-14 md:pt-16 ", 1)
        else:
            return '<main class="pt-14 md:pt-16">'
    content = re.sub(r'<main(\s[^>]*)?>', add_main_padding, content, count=1)
    
    # 3b. Add nav.js script reference before </body>
    if '/static/js/nav.js' not in content:
        content = content.replace('</body>', f'{NAV_JS_SCRIPT}\n</body>')
    
    # 3c. Clean up excess blank lines
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"  ✅ {filepath}")
    return True


def main():
    files = ['index.html', 'deals.html'] + sorted(glob.glob('content/*/index.html'))
    src_files = [f for f in files if os.path.isfile(f)]
    
    print("=" * 60)
    print("REBUILDING NAVIGATION ON ALL PAGES")
    print("=" * 60)
    
    success = 0
    for f in src_files:
        if replace_nav_in_file(f):
            success += 1
    
    print(f"\n✅ Nav replaced on {success}/{len(src_files)} pages")
    
    # --- REBUILD DEPLOY_ROOT ---
    print("\n" + "=" * 60)
    print("REBUILDING DEPLOY_ROOT")
    print("=" * 60)
    
    if os.path.exists('_site'):
        shutil.rmtree('_site')
    
    sp.run(['bash', 'sync_site.sh'], check=True, capture_output=True)
    
    DEPLOY = '_site/deploy_root'
    if os.path.exists(DEPLOY):
        shutil.rmtree(DEPLOY)
    os.makedirs(f"{DEPLOY}/static", exist_ok=True)
    
    for cmd in [
        'cp index.html {d}/', 'cp deals.html {d}/', 'cp -r content {d}/', 'cp -r static {d}/',
    ]:
        sp.run(cmd.format(d=DEPLOY), shell=True, check=True)
    
    for f in ['_headers', '_redirects', 'robots.txt', 'sitemap.xml',
              'sitemap_index.xml', 'search.json']:
        if os.path.isfile(f):
            sp.run(f'cp {f} {DEPLOY}/', shell=True)
    
    html_c = len(glob.glob(f'{DEPLOY}/**/*.html', recursive=True))
    css_c = len(glob.glob(f'{DEPLOY}/static/css/*'))
    js_c = len(glob.glob(f'{DEPLOY}/static/js/*'))
    img_c = len(glob.glob(f'{DEPLOY}/static/images/**/*', recursive=True))
    
    print(f"\n✅ Deploy root rebuilt: {DEPLOY}/")
    print(f"   HTML: {html_c} | CSS: {css_c} | JS: {js_c} | Images: {img_c}")


if __name__ == '__main__':
    main()
