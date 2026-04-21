#!/usr/bin/env python3
import os
import re
import sys

# Descriptions for each page
DESCRIPTIONS = {
    'best-standing-desks-under-500': 'Discover the best standing desks under $500 for your home office. Compare features, prices, and ergonomic benefits of top budget-friendly standing desk options.',
    'cable-management-solutions': 'Effective cable management solutions for a clean, organized home office. Learn about cable trays, sleeves, clips, and routing techniques to eliminate desk clutter.',
    'contact': 'Contact The Workspace Pro team with questions, feedback, or partnership inquiries. We\'re here to help you build a better home office.',
    'dual-monitor-setup-productivity': 'Maximize productivity with a dual monitor setup. Learn optimal configuration, mounting options, and software tips for remote work efficiency.',
    'ergonomic-accessories-home-office': 'Essential ergonomic accessories for your home office: monitor arms, keyboard trays, footrests, and more to improve comfort and reduce strain.',
    'guides': 'Browse our complete collection of home office guides covering ergonomics, productivity, lighting, cable management, and workspace optimization.',
    'home-office-budget-setup-under-1000': 'Build a complete, ergonomic home office setup for under $1000. Budget-friendly desk, chair, monitor, and accessory recommendations for remote workers.',
    'home-office-desk-guide-2026': 'Complete guide to choosing the perfect home office desk in 2026. Compare standing desks, traditional desks, materials, sizes, and features.',
    'home-office-lighting-guide': 'Home office lighting guide: How to choose the best lights for productivity, reduce eye strain, and create an ideal work environment with natural and artificial lighting.',
    'podcasts': 'Listen to top productivity and workspace podcasts curated by The Workspace Pro. Learn from experts about ergonomics, remote work, and home office optimization.',
    'privacy': 'Privacy policy for The Workspace Pro. Learn how we collect, use, and protect your personal information when you visit our website.',
    'productive-workspace-mindset': 'Develop a productive workspace mindset with tips for focus, time management, and creating an environment that supports deep work and creativity.',
    'small-home-office-organization-hacks': 'Space-saving organization hacks for small home offices. Maximize productivity in limited spaces with clever storage and layout solutions.',
    'terms': 'Terms of service for The Workspace Pro website. Please read these terms carefully before using our content, product recommendations, or newsletter.',
    'tips': 'Daily workspace tips and productivity hacks to improve your home office setup, ergonomics, and work habits. New tip every day.',
}

def update_file(filepath):
    """Update a single HTML file."""
    print(f"Updating {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract page key from path
    match = re.search(r'/content/([^/]+)/index\.html$', filepath)
    if match:
        page_key = match.group(1)
    else:
        # Check if it's root index.html
        if filepath.endswith('/index.html'):
            page_key = 'index'
        else:
            print(f"  ⚠ Could not extract page key from {filepath}")
            return
    
    desc = DESCRIPTIONS.get(page_key, 'Expert-curated ergonomic home office guides, product recommendations, and daily tips to build a healthier, more productive workspace.')
    
    # 1. Replace style block
    style_pattern = r'<style>\s*\.hero-bg[\s\S]*?</style>'
    if re.search(style_pattern, content):
        content = re.sub(style_pattern, '    <link rel="stylesheet" href="/static/css/custom.css">', content)
        print(f"  ✓ Replaced style block")
    else:
        print(f"  ⚠ Style block not found")
    
    # 2. Update meta descriptions
    meta_pattern = r'<meta name="description" content="[^"]*">'
    og_pattern = r'<meta property="og:description" content="[^"]*">'
    twitter_pattern = r'<meta name="twitter:description" content="[^"]*">'
    
    content = re.sub(meta_pattern, f'<meta name="description" content="{desc}">', content)
    content = re.sub(og_pattern, f'<meta property="og:description" content="{desc}">', content)
    content = re.sub(twitter_pattern, f'<meta name="twitter:description" content="{desc}">', content)
    print(f"  ✓ Updated descriptions")
    
    # 3. Add canonical tag after twitter:image
    canonical_url = f"https://www.theworkspacepro.com/content/{page_key}/"
    if page_key == 'index':
        canonical_url = "https://www.theworkspacepro.com/"
    
    twitter_image_pattern = r'<meta name="twitter:image"[^>]*>'
    match = re.search(twitter_image_pattern, content)
    if match:
        replacement = match.group(0) + f'\n    <link rel="canonical" href="{canonical_url}">'
        content = re.sub(twitter_image_pattern, replacement, content, count=1)
        print(f"  ✓ Added canonical tag: {canonical_url}")
    
    # 4. Add JSON-LD schema
    if page_key == 'index':
        # Home page - Website + Organization
        schema = '''    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "The Workspace Pro",
      "description": "Expert-curated ergonomic home office guides, product recommendations, and daily tips to build a healthier, more productive workspace.",
      "url": "https://www.theworkspacepro.com/",
      "potentialAction": {
        "@type": "SearchAction",
        "target": "https://www.theworkspacepro.com/search?q={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    }
    </script>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "The Workspace Pro",
      "url": "https://www.theworkspacepro.com/",
      "logo": "https://www.theworkspacepro.com/static/images/logo.png",
      "sameAs": [
        "https://twitter.com/workspacepro",
        "https://www.facebook.com/workspacepro",
        "https://www.instagram.com/workspacepro"
      ]
    }
    </script>'''
    elif page_key in ['about', 'contact', 'privacy', 'terms', 'guides', 'tips', 'podcasts']:
        # WebPage schema
        title = page_key.replace('-', ' ').title()
        schema = f'''    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebPage",
      "name": "{title}",
      "description": "{desc}",
      "url": "{canonical_url}"
    }}
    </script>'''
    else:
        # Article schema for guides
        # Extract title from HTML
        title_match = re.search(r'<title>([^<]+)</title>', content)
        if title_match:
            title = title_match.group(1).replace(' | The Workspace Pro', '')
        else:
            title = page_key.replace('-', ' ').title()
        
        schema = f'''    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{title}",
      "description": "{desc}",
      "image": "https://www.theworkspacepro.com/static/images/og-default.png",
      "author": {{
        "@type": "Organization",
        "name": "The Workspace Pro Team"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "The Workspace Pro",
        "logo": {{
          "@type": "ImageObject",
          "url": "https://www.theworkspacepro.com/static/images/logo.png"
        }}
      }},
      "datePublished": "2026-04-01",
      "dateModified": "2026-04-01",
      "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "{canonical_url}"
      }}
    }}
    </script>'''
    
    # Insert before </head>
    content = content.replace('</head>', schema + '\n</head>')
    print(f"  ✓ Added JSON-LD schema")
    
    # 5. Add lazy loading to images that don't have it
    def add_lazy(match):
        img_tag = match.group(0)
        if 'loading=' not in img_tag.lower():
            if '/>' in img_tag:
                img_tag = img_tag.replace('/>', ' loading="lazy" decoding="async" />')
            else:
                img_tag = img_tag.replace('>', ' loading="lazy" decoding="async">')
        return img_tag
    
    content = re.sub(r'<img[^>]+(?:/>|>)', add_lazy, content)
    print(f"  ✓ Added lazy loading to images")
    
    # 6. Add affiliate transparency
    # Check Price buttons
    check_price_pattern = r'(<a[^>]*>Check Price</a>)'
    transparency_html = '\n                    <p class="text-xs text-zinc-500 mt-2 text-center">We may earn a commission at no extra cost to you. Prices checked daily.</p>'
    content = re.sub(check_price_pattern, r'\1' + transparency_html, content, flags=re.IGNORECASE)
    
    # See Current Deal buttons
    see_deal_pattern = r'(<a[^>]*>See Current Deal</a>)'
    deal_transparency = '\n                <p class="text-xs text-gray-500 mt-2">We may earn a commission at no extra cost to you. Prices checked daily.</p>'
    content = re.sub(see_deal_pattern, r'\1' + deal_transparency, content, flags=re.IGNORECASE)
    
    print(f"  ✓ Added affiliate transparency")
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ Completed {page_key}\n")

def main():
    # Files to update (excluding already updated ones)
    files = [
        'content/best-standing-desks-under-500/index.html',
        'content/cable-management-solutions/index.html',
        'content/contact/index.html',
        'content/dual-monitor-setup-productivity/index.html',
        'content/ergonomic-accessories-home-office/index.html',
        'content/guides/index.html',
        'content/home-office-budget-setup-under-1000/index.html',
        'content/home-office-desk-guide-2026/index.html',
        'content/home-office-lighting-guide/index.html',
        'content/podcasts/index.html',
        'content/privacy/index.html',
        'content/productive-workspace-mindset/index.html',
        'content/small-home-office-organization-hacks/index.html',
        'content/terms/index.html',
        'content/tips/index.html',
    ]
    
    # Check which files exist
    existing_files = []
    for f in files:
        if os.path.exists(f):
            existing_files.append(f)
        else:
            print(f"Warning: File not found: {f}")
    
    print(f"Found {len(existing_files)} files to update")
    
    for f in existing_files:
        try:
            update_file(f)
        except Exception as e:
            print(f"Error updating {f}: {e}")
            import traceback
            traceback.print_exc()
    
    print("Done!")

if __name__ == '__main__':
    main()