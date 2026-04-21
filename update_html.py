#!/usr/bin/env python3
"""
Batch update HTML files with SEO, performance, and accessibility improvements.
"""

import os
import re
import sys
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Page type to description mapping
DESCRIPTIONS = {
    'about': 'Learn about The Workspace Pro mission to help you build healthier, more productive home offices with expert-curated guides and ergonomic product recommendations.',
    'best-standing-desks-under-500': 'Discover the best standing desks under $500 for your home office. Compare features, prices, and ergonomic benefits of top budget-friendly standing desk options.',
    'cable-management-solutions': 'Effective cable management solutions for a clean, organized home office. Learn about cable trays, sleeves, clips, and routing techniques to eliminate desk clutter.',
    'contact': 'Contact The Workspace Pro team with questions, feedback, or partnership inquiries. We\'re here to help you build a better home office.',
    'dual-monitor-setup-productivity': 'Maximize productivity with a dual monitor setup. Learn optimal configuration, mounting options, and software tips for remote work efficiency.',
    'ergonomic-accessories-home-office': 'Essential ergonomic accessories for your home office: monitor arms, keyboard trays, footrests, and more to improve comfort and reduce strain.',
    'ergonomic-office-chair-buying-guide': 'Discover what to look for in an ergonomic office chair with our comprehensive buying guide. Features, top picks, and setup tips for a healthy home office.',
    'guides': 'Browse our complete collection of home office guides covering ergonomics, productivity, lighting, cable management, and workspace optimization.',
    'home': 'Expert-curated ergonomic home office guides, product recommendations, and daily tips to build a healthier, more productive workspace. Discover top picks for desks, chairs, monitors, and accessories.',
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

# JSON-LD templates
ARTICLE_SCHEMA_TEMPLATE = '''    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{title}",
      "description": "{description}",
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
        "@id": "https://www.theworkspacepro.com{path}"
      }}
    }}
    </script>'''

WEBSITE_SCHEMA_TEMPLATE = '''    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebSite",
      "name": "The Workspace Pro",
      "description": "Expert-curated ergonomic home office guides, product recommendations, and daily tips to build a healthier, more productive workspace.",
      "url": "https://www.theworkspacepro.com/",
      "potentialAction": {{
        "@type": "SearchAction",
        "target": "https://www.theworkspacepro.com/search?q={{search_term_string}}",
        "query-input": "required name=search_term_string"
      }}
    }}
    </script>'''

ORGANIZATION_SCHEMA_TEMPLATE = '''    <script type="application/ld+json">
    {{
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
    }}
    </script>'''

def get_page_key(path):
    """Extract page key from file path."""
    # Remove content/ prefix and /index.html suffix
    if 'content/' in path:
        path = path.split('content/')[1]
    if path.endswith('/index.html'):
        path = path[:-11]
    if path.endswith('.html'):
        path = path[:-5]
    return path

def update_file(filepath):
    """Update a single HTML file with improvements."""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get page key for descriptions
    rel_path = str(filepath.relative_to(BASE_DIR))
    page_key = get_page_key(rel_path)
    
    # 1. Replace style block with external CSS reference
    style_pattern = r'<style>\s*\.hero-bg[\s\S]*?</style>'
    css_link = '    <link rel="stylesheet" href="/static/css/custom.css">'
    
    if re.search(style_pattern, content):
        content = re.sub(style_pattern, css_link, content)
        print(f"  ✓ Replaced style block")
    else:
        print(f"  ⚠ Style block not found")
    
    # 2. Update meta description
    meta_desc_pattern = r'<meta name="description" content="[^"]*">'
    og_desc_pattern = r'<meta property="og:description" content="[^"]*">'
    twitter_desc_pattern = r'<meta name="twitter:description" content="[^"]*">'
    
    description = DESCRIPTIONS.get(page_key, 'Expert-curated ergonomic home office guides, product recommendations, and daily tips to build a healthier, more productive workspace.')
    
    new_meta_desc = f'<meta name="description" content="{description}">'
    new_og_desc = f'<meta property="og:description" content="{description}">'
    new_twitter_desc = f'<meta name="twitter:description" content="{description}">'
    
    content = re.sub(meta_desc_pattern, new_meta_desc, content)
    content = re.sub(og_desc_pattern, new_og_desc, content)
    content = re.sub(twitter_desc_pattern, new_twitter_desc, content)
    print(f"  ✓ Updated descriptions")
    
    # 3. Add canonical tag after twitter:image
    canonical_pattern = r'(<meta name="twitter:image"[^>]+>)'
    canonical_url = "https://www.theworkspacepro.com/"
    if page_key not in ['', 'index']:
        canonical_url += f"{'content/' if 'content/' in rel_path else ''}{page_key}/"
    
    canonical_tag = f'\n    <link rel="canonical" href="{canonical_url}">'
    content = re.sub(canonical_pattern, r'\1' + canonical_tag, content)
    print(f"  ✓ Added canonical: {canonical_url}")
    
    # 4. Add JSON-LD schema before </head>
    if page_key in ['', 'index']:
        # Home page gets Website + Organization
        schema = WEBSITE_SCHEMA_TEMPLATE + '\n' + ORGANIZATION_SCHEMA_TEMPLATE
    elif page_key in ['about', 'contact', 'privacy', 'terms', 'guides', 'tips', 'podcasts']:
        # Other pages get WebPage schema
        schema = f'''    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebPage",
      "name": "{page_key.title().replace('-', ' ')}",
      "description": "{description}",
      "url": "{canonical_url}"
    }}
    </script>'''
    else:
        # Guide/articles get Article schema
        # Extract title from HTML
        title_match = re.search(r'<title>([^<]+)</title>', content)
        title = title_match.group(1).replace(' | The Workspace Pro', '') if title_match else page_key.replace('-', ' ').title()
        schema = ARTICLE_SCHEMA_TEMPLATE.format(
            title=title,
            description=description,
            path=f"/{'content/' if 'content/' in rel_path else ''}{page_key}/"
        )
    
    content = content.replace('</head>', schema + '\n</head>')
    print(f"  ✓ Added JSON-LD schema")
    
    # 5. Add lazy loading to images (simple approach - add to img tags without loading attribute)
    # This is a bit more complex, we'll do a simple regex
    img_pattern = r'(<img[^>]+)(?<!loading="[^"]+")(?<!loading=\'[^\']+\')(/?>)'
    def add_lazy(match):
        tag = match.group(1)
        closing = match.group(2)
        if 'loading=' not in tag:
            tag += ' loading="lazy" decoding="async"'
        return tag + closing
    
    content = re.sub(img_pattern, add_lazy, content)
    print(f"  ✓ Added lazy loading to images")
    
    # 6. Add affiliate transparency near "Check Price" buttons
    check_price_pattern = r'(<a[^>]*Check Price[^<]*</a>)'
    transparency_text = '\n                    <p class="text-xs text-zinc-500 mt-2 text-center">We may earn a commission at no extra cost to you. Prices checked daily.</p>'
    
    def add_transparency(match):
        return match.group(1) + transparency_text
    
    content = re.sub(check_price_pattern, add_transparency, content, flags=re.IGNORECASE)
    
    # Also check for "See Current Deal"
    see_deal_pattern = r'(<a[^>]*See Current Deal[^<]*</a>)'
    def add_transparency_deal(match):
        return match.group(1) + '\n                <p class="text-xs text-gray-500 mt-2">We may earn a commission at no extra cost to you. Prices checked daily.</p>'
    
    content = re.sub(see_deal_pattern, add_transparency_deal, content, flags=re.IGNORECASE)
    print(f"  ✓ Added affiliate transparency text")
    
    # 7. Add form validation script for newsletter forms
    if 'newsletter' in content.lower():
        # Check if validation script already exists
        if 'newsletter-message' not in content:
            # Simple addition - would need more context-aware insertion
            print(f"  ⚠ Newsletter form found (manual check needed)")
    
    # Write updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ File updated successfully\n")

def main():
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(BASE_DIR):
        # Skip some directories
        if '_site' in root or 'DEPLOY' in root or 'README' in root or 'AFFILIATE_SETUP' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(Path(root) / file)
    
    print(f"Found {len(html_files)} HTML files")
    
    # Skip already updated files if needed
    files_to_process = [f for f in html_files]
    
    for filepath in files_to_process:
        try:
            update_file(filepath)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
    
    print("Done!")

if __name__ == '__main__':
    main()