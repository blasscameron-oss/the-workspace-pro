#!/usr/bin/env python3
import os
import sys

# Simple string replacements that should work for all files

# Read the custom CSS to verify it exists
css_path = "/home/cameron/.openclaw/workspace/workspace-pro-minimal/static/css/custom.css"
if not os.path.exists(css_path):
    print("Error: CSS file not found at", css_path)
    sys.exit(1)

# Files to process (excluding already done: index.html, about/index.html, ergonomic-office-chair-buying-guide/index.html)
files = [
    "content/best-standing-desks-under-500/index.html",
    "content/cable-management-solutions/index.html", 
    "content/contact/index.html",
    "content/dual-monitor-setup-productivity/index.html",
    "content/ergonomic-accessories-home-office/index.html",
    "content/guides/index.html",
    "content/home-office-budget-setup-under-1000/index.html",
    "content/home-office-desk-guide-2026/index.html",
    "content/home-office-lighting-guide/index.html",
    "content/podcasts/index.html",
    "content/privacy/index.html",
    "content/productive-workspace-mindset/index.html",
    "content/small-home-office-organization-hacks/index.html",
    "content/terms/index.html",
    "content/tips/index.html",
]

# Page-specific descriptions
descriptions = {
    "best-standing-desks-under-500": "Discover the best standing desks under $500 for your home office. Compare features, prices, and ergonomic benefits of top budget-friendly standing desk options.",
    "cable-management-solutions": "Effective cable management solutions for a clean, organized home office. Learn about cable trays, sleeves, clips, and routing techniques to eliminate desk clutter.",
    "contact": "Contact The Workspace Pro team with questions, feedback, or partnership inquiries. We're here to help you build a better home office.",
    "dual-monitor-setup-productivity": "Maximize productivity with a dual monitor setup. Learn optimal configuration, mounting options, and software tips for remote work efficiency.",
    "ergonomic-accessories-home-office": "Essential ergonomic accessories for your home office: monitor arms, keyboard trays, footrests, and more to improve comfort and reduce strain.",
    "guides": "Browse our complete collection of home office guides covering ergonomics, productivity, lighting, cable management, and workspace optimization.",
    "home-office-budget-setup-under-1000": "Build a complete, ergonomic home office setup for under $1000. Budget-friendly desk, chair, monitor, and accessory recommendations for remote workers.",
    "home-office-desk-guide-2026": "Complete guide to choosing the perfect home office desk in 2026. Compare standing desks, traditional desks, materials, sizes, and features.",
    "home-office-lighting-guide": "Home office lighting guide: How to choose the best lights for productivity, reduce eye strain, and create an ideal work environment with natural and artificial lighting.",
    "podcasts": "Listen to top productivity and workspace podcasts curated by The Workspace Pro. Learn from experts about ergonomics, remote work, and home office optimization.",
    "privacy": "Privacy policy for The Workspace Pro. Learn how we collect, use, and protect your personal information when you visit our website.",
    "productive-workspace-mindset": "Develop a productive workspace mindset with tips for focus, time management, and creating an environment that supports deep work and creativity.",
    "small-home-office-organization-hacks": "Space-saving organization hacks for small home offices. Maximize productivity in limited spaces with clever storage and layout solutions.",
    "terms": "Terms of service for The Workspace Pro website. Please read these terms carefully before using our content, product recommendations, or newsletter.",
    "tips": "Daily workspace tips and productivity hacks to improve your home office setup, ergonomics, and work habits. New tip every day.",
}

for file in files:
    print(f"Processing {file}...")
    with open(file, 'r') as f:
        content = f.read()
    
    # Get page key
    page_key = file.split('/')[-2]
    
    # 1. Replace style block (simple approach - find and replace)
    # The style block starts with <style> and ends with </style>
    # We'll find the position and replace
    start = content.find('<style>')
    end = content.find('</style>')
    
    if start != -1 and end != -1:
        # Include the closing tag
        end += len('</style>')
        old_style = content[start:end]
        content = content[:start] + '    <link rel="stylesheet" href="/static/css/custom.css">' + content[end:]
        print(f"  ✓ Replaced style block")
    else:
        print(f"  ⚠ Style block not found")
    
    # 2. Update descriptions
    desc = descriptions.get(page_key, "Expert-curated ergonomic home office guides, product recommendations, and daily tips to build a healthier, more productive workspace.")
    
    # Replace meta description
    import re
    content = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', content)
    content = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">', content) 
    content = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{desc}">', content)
    print(f"  ✓ Updated descriptions")
    
    # 3. Add canonical tag after twitter:image
    canonical_url = f"https://www.theworkspacepro.com/{file.replace('index.html', '')}"
    # Find twitter:image line
    twit_img_pattern = r'<meta name="twitter:image"[^>]*>'
    match = re.search(twit_img_pattern, content)
    if match:
        replacement = match.group(0) + f'\n    <link rel="canonical" href="{canonical_url}">'
        content = re.sub(twit_img_pattern, replacement, content, count=1)
        print(f"  ✓ Added canonical tag")
    
    # 4. Add JSON-LD schema before </head>
    if page_key in ['about', 'contact', 'privacy', 'terms', 'guides', 'tips', 'podcasts']:
        schema = f'''    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "WebPage",
      "name": "{page_key.replace('-', ' ').title()}",
      "description": "{desc}",
      "url": "{canonical_url}"
    }}
    </script>'''
    else:
        # Article schema for guides
        # Extract title
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
    
    # 5. Simple image lazy loading - add to img tags
    # This regex looks for <img followed by attributes and >, without loading attribute
    def add_lazy(match):
        img_tag = match.group(0)
        if 'loading=' not in img_tag:
            # Insert before closing >
            if img_tag.endswith('/>'):
                img_tag = img_tag[:-2] + ' loading="lazy" decoding="async" />'
            else:
                img_tag = img_tag[:-1] + ' loading="lazy" decoding="async">'
        return img_tag
    
    content = re.sub(r'<img[^>]+(?:/>|>)', add_lazy, content)
    print(f"  ✓ Added lazy loading to images")
    
    # 6. Affiliate transparency
    # Check Price buttons
    content = re.sub(
        r'(<a[^>]*>Check Price</a>)',
        r'\1\n                    <p class="text-xs text-zinc-500 mt-2 text-center">We may earn a commission at no extra cost to you. Prices checked daily.</p>',
        content,
        flags=re.IGNORECASE
    )
    
    # See Current Deal buttons  
    content = re.sub(
        r'(<a[^>]*>See Current Deal</a>)',
        r'\1\n                <p class="text-xs text-gray-500 mt-2">We may earn a commission at no extra cost to you. Prices checked daily.</p>',
        content,
        flags=re.IGNORECASE
    )
    
    print(f"  ✓ Added affiliate transparency")
    
    # Write back
    with open(file, 'w') as f:
        f.write(content)
    
    print(f"  ✓ Completed {page_key}\n")

print("All files processed!")