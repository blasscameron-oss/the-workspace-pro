#!/bin/bash
# Sync updated HTML files and assets to _site directory

set -e

echo "Syncing updates to _site directory..."

# 1. Copy custom.css to _site
mkdir -p _site/static/css
cp static/css/custom.css _site/static/css/
echo "✓ Copied custom.css"

# 2. Copy all HTML files, preserving directory structure
find . -name "*.html" -not -path "./_site/*" -not -path "./AFFILIATE_SETUP/*" -not -path "./DEPLOY/*" -not -path "./README/*" -not -path "./quick_test/*" | while read file; do
    # Skip if file is in _site or other excluded directories
    if [[ "$file" == ./_site/* ]] || [[ "$file" == ./AFFILIATE_SETUP/* ]] || [[ "$file" == ./DEPLOY/* ]] || [[ "$file" == ./README/* ]] || [[ "$file" == ./quick_test/* ]]; then
        continue
    fi
    
    # Get relative path
    rel_path="${file#./}"
    
    # Determine destination in _site
    if [[ "$rel_path" == index.html ]]; then
        dest="_site/index.html"
    elif [[ "$rel_path" == deals.html ]]; then
        dest="_site/deals.html"
    elif [[ "$rel_path" == content/* ]]; then
        dest="_site/$rel_path"
    else
        # Skip other HTML files not in content/ or root
        continue
    fi
    
    # Create destination directory if needed
    mkdir -p "$(dirname "$dest")"
    
    # Copy the file
    cp "$file" "$dest"
    echo "  Copied: $rel_path → $dest"
done

echo "✓ All HTML files synced"

# 3. Copy other necessary assets
# sitemap.xml
cp sitemap.xml _site/ 2>/dev/null && echo "✓ Copied sitemap.xml" || echo "⚠ sitemap.xml not found"
# robots.txt  
cp robots.txt _site/ 2>/dev/null && echo "✓ Copied robots.txt" || echo "⚠ robots.txt not found"
# search.json (if exists)
cp search.json _site/ 2>/dev/null && echo "✓ Copied search.json" || echo "⚠ search.json not found"

# 4. Copy deployment config files
cp netlify.toml _headers _redirects _routes.json _site/ 2>/dev/null && echo "✓ Copied deployment configs" || echo "⚠ Some config files not found"

echo ""
echo "✅ _site directory updated with all improvements!"
echo "   Total HTML files: $(find _site -name "*.html" | wc -l)"
echo "   Ready for deployment."