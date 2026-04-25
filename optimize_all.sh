#!/bin/bash
# Batch optimization script for all HTML files

FILES=$(grep -rl "cdn.tailwindcss.com" --include="*.html" . | grep -v node_modules | grep -v _site | grep -v cloudflare_ | grep -v deploy_root | grep -v quick_test | grep -v AFFILIATE | grep -v DEPLOY | grep -v README | sort)

echo "Files to process:"
echo "$FILES" | wc -l

for f in $FILES; do
  echo "Processing: $f"
  
  # 1. Replace the entire Tailwind CDN block with pre-built CSS link
  # This is tricky because the tailwind.config block varies. Let's do a range deletion.
  # The block starts with '<!-- Tailwind CSS via CDN -->' and ends with '</script>'
  # after the tailwind.config script.
  # We'll replace the multi-line block using python for reliability
  
  python3 -c "
import re

with open('$f', 'r') as fh:
    content = fh.read()

# Remove the Tailwind CDN block (from comment to end of config script)
cdn_pattern = r'<!-- Tailwind CSS via CDN -->.*?</script>\s*'
replacement = '<!-- Tailwind CSS (pre-built) -->\n    <link rel=\"stylesheet\" href=\"/static/css/tailwind.min.css\">\n    '
content = re.sub(cdn_pattern, replacement, content, flags=re.DOTALL)

# Add display=swap to Google Fonts if not already there
content = content.replace('&display=swap', '&display=swap')  # no-op if present
if 'display=swap' not in content:
    content = content.replace(
        'href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&amp;family=Playfair+Display:wght@400;500;600;700\"',
        'href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&amp;family=Playfair+Display:wght@400;500;600;700&amp;display=swap\"'
    )
    content = content.replace(
        'href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@400;500;600;700\"',
        'href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:wght@400;500;600;700&display=swap\"'
    )

# Change JS src to .min.js with defer
for js in ['main', 'quiz', 'search']:
    old_src = f'/static/js/{js}.js'
    new_src = f'/static/js/{js}.min.js'
    if old_src in content and new_src not in content:
        # Add defer attribute
        content = content.replace(f'src=\"{old_src}\"', f'src=\"{new_src}\" defer')
        # Also handle cases where defer already exists
        content = content.replace(f'defer src=\"{new_src}\" defer', f'src=\"{new_src}\" defer')

with open('$f', 'w') as fh:
    fh.write(content)

print('  Done')
"
done

echo ""
echo "=== Verify ==="
echo "Tailwind CDN references remaining:"
grep -rl "cdn.tailwindcss.com" --include="*.html" . | grep -v node_modules | grep -v _site | grep -v cloudflare_ | grep -v deploy_root | grep -v quick_test | grep -v AFFILIATE | grep -v DEPLOY | grep -v README | wc -l
echo "New built CSS references:"
grep -rl "tailwind.min.css" --include="*.html" . | grep -v node_modules | grep -v _site | grep -v cloudflare_ | grep -v deploy_root | grep -v quick_test | grep -v AFFILIATE | grep -v DEPLOY | grep -v README | wc -l
echo "Defer attributes:"
grep -rl "defer" --include="*.html" . | grep -v node_modules | grep -v _site | grep -v cloudflare_ | grep -v deploy_root | grep -v quick_test | grep -v AFFILIATE | grep -v DEPLOY | grep -v README | wc -l
echo "display=swap:"
grep -rl "display=swap" --include="*.html" . | grep -v node_modules | grep -v _site | grep -v cloudflare_ | grep -v deploy_root | grep -v quick_test | grep -v AFFILIATE | grep -v DEPLOY | grep -v README | wc -l
