#!/usr/bin/env python3
"""
Update a guide page with new design system (head, header, footer).
Usage: python3 update_guide.py <input_html> <output_html>
"""

import sys
import os
from bs4 import BeautifulSoup

def extract_guide_meta(soup):
    """Extract guide-specific meta tags from original soup."""
    meta = {}
    # Title
    title_tag = soup.find('title')
    meta['title'] = title_tag.string if title_tag else ''
    
    # Meta description
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    meta['description'] = desc_tag.get('content', '') if desc_tag else ''
    
    # Canonical
    canonical_tag = soup.find('link', rel='canonical')
    meta['canonical'] = canonical_tag.get('href', '') if canonical_tag else ''
    
    # OG tags
    og_title = soup.find('meta', property='og:title')
    meta['og_title'] = og_title.get('content', '') if og_title else ''
    og_desc = soup.find('meta', property='og:description')
    meta['og_desc'] = og_desc.get('content', '') if og_desc else ''
    og_image = soup.find('meta', property='og:image')
    meta['og_image'] = og_image.get('content', '') if og_image else ''
    og_url = soup.find('meta', property='og:url')
    meta['og_url'] = og_url.get('content', '') if og_url else ''
    
    # Twitter tags
    twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
    meta['twitter_title'] = twitter_title.get('content', '') if twitter_title else ''
    twitter_desc = soup.find('meta', attrs={'name': 'twitter:description'})
    meta['twitter_desc'] = twitter_desc.get('content', '') if twitter_desc else ''
    twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
    meta['twitter_image'] = twitter_image.get('content', '') if twitter_image else ''
    
    # JSON-LD schema (keep original)
    script_ld = soup.find('script', type='application/ld+json')
    meta['json_ld'] = script_ld.string if script_ld else ''
    
    return meta

def update_head(template_head_soup, guide_meta):
    """Update template head soup with guide-specific meta."""
    # Update title
    title_tag = template_head_soup.find('title')
    if title_tag and guide_meta['title']:
        title_tag.string = guide_meta['title']
    
    # Update meta description
    desc_tag = template_head_soup.find('meta', attrs={'name': 'description'})
    if desc_tag and guide_meta['description']:
        desc_tag['content'] = guide_meta['description']
    
    # Update canonical
    canonical_tag = template_head_soup.find('link', rel='canonical')
    if canonical_tag and guide_meta['canonical']:
        canonical_tag['href'] = guide_meta['canonical']
    
    # Update OG tags
    og_title = template_head_soup.find('meta', property='og:title')
    if og_title and guide_meta['og_title']:
        og_title['content'] = guide_meta['og_title']
    og_desc = template_head_soup.find('meta', property='og:description')
    if og_desc and guide_meta['og_desc']:
        og_desc['content'] = guide_meta['og_desc']
    og_image = template_head_soup.find('meta', property='og:image')
    if og_image and guide_meta['og_image']:
        og_image['content'] = guide_meta['og_image']
    og_url = template_head_soup.find('meta', property='og:url')
    if og_url and guide_meta['og_url']:
        og_url['content'] = guide_meta['og_url']
    
    # Update Twitter tags
    twitter_title = template_head_soup.find('meta', attrs={'name': 'twitter:title'})
    if twitter_title and guide_meta['twitter_title']:
        twitter_title['content'] = guide_meta['twitter_title']
    twitter_desc = template_head_soup.find('meta', attrs={'name': 'twitter:description'})
    if twitter_desc and guide_meta['twitter_desc']:
        twitter_desc['content'] = guide_meta['twitter_desc']
    twitter_image = template_head_soup.find('meta', attrs={'name': 'twitter:image'})
    if twitter_image and guide_meta['twitter_image']:
        twitter_image['content'] = guide_meta['twitter_image']
    
    # Replace JSON-LD schema
    script_ld = template_head_soup.find('script', type='application/ld+json')
    if script_ld and guide_meta['json_ld']:
        script_ld.string = guide_meta['json_ld']
    
    return template_head_soup

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 update_guide.py <input_html> <output_html>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Read template (index.html)
    with open('index.html', 'r', encoding='utf-8') as f:
        template_html = f.read()
    
    # Parse template
    template_soup = BeautifulSoup(template_html, 'html.parser')
    
    # Extract template header and footer
    template_header = template_soup.find('header', role='banner')
    template_footer = template_soup.find('footer', role='contentinfo')
    
    # Extract template head (everything up to </head>)
    template_head = template_soup.head
    
    # Read guide
    with open(input_file, 'r', encoding='utf-8') as f:
        guide_html = f.read()
    
    guide_soup = BeautifulSoup(guide_html, 'html.parser')
    
    # Extract guide meta
    guide_meta = extract_guide_meta(guide_soup)
    
    # Update template head with guide meta
    updated_head = update_head(template_head, guide_meta)
    
    # Find guide's main content (article)
    guide_article = guide_soup.find('article')
    if not guide_article:
        guide_article = guide_soup.find('main')
    if not guide_article:
        guide_article = guide_soup.find('body')
    
    # Create new soup
    new_soup = BeautifulSoup('<!DOCTYPE html>', 'html.parser')
    new_soup.append(new_soup.new_tag('html', lang='en', **{'class': 'scroll-smooth'}))
    
    # Add updated head
    new_soup.html.append(updated_head)
    
    # Create body
    body = new_soup.new_tag('body', **{
        'class': 'bg-surface text-neutral-900 dark:bg-neutral-900 dark:text-neutral-100 font-sans antialiased min-h-screen flex flex-col'
    })
    new_soup.html.append(body)
    
    # Add skip link (optional)
    skip = new_soup.new_tag('a', href='#main-content', **{
        'class': 'sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 bg-primary text-white px-6 py-3 rounded-xl z-[100] shadow-lg'
    })
    skip.string = 'Skip to main content'
    body.append(skip)
    
    # Add header
    if template_header:
        body.append(template_header)
    
    # Create main element
    main = new_soup.new_tag('main', id='main-content', **{
        'class': 'flex-grow max-w-7xl mx-auto px-6 py-12'
    })
    body.append(main)
    
    # Add guide article content
    if guide_article:
        main.append(guide_article)
    
    # Add footer
    if template_footer:
        body.append(template_footer)
    
    # Add search overlay (from template)
    search_overlay = template_soup.find('div', id='search-overlay')
    if search_overlay:
        body.append(search_overlay)
    
    # Add scripts (copy from template body)
    template_body_scripts = template_soup.body.find_all('script')
    for script in template_body_scripts:
        body.append(script)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        # Prettify with minimal formatting
        f.write('<!DOCTYPE html>\n')
        f.write(str(new_soup.html.prettify()))
    
    print(f"Updated guide saved to {output_file}")

if __name__ == '__main__':
    main()