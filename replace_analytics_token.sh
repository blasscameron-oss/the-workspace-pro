#!/bin/bash
set -e

REAL_TOKEN="cfut_2FwhIfvNRxBkiErMVLR9rkEhxyGa6kC5Y7QRwlLq6bcee2de"

echo "Replacing Cloudflare Analytics token in HTML files..."

# Replace in root HTML files
find . -maxdepth 1 -name "*.html" -type f | while read file; do
    if grep -q "YOUR_CF_ANALYTICS_TOKEN_HERE" "$file"; then
        sed -i "s/YOUR_CF_ANALYTICS_TOKEN_HERE/$REAL_TOKEN/g" "$file"
        echo "  Updated: $file"
    fi
done

# Replace in content/ directory
find content -name "*.html" -type f | while read file; do
    if grep -q "YOUR_CF_ANALYTICS_TOKEN_HERE" "$file"; then
        sed -i "s/YOUR_CF_ANALYTICS_TOKEN_HERE/$REAL_TOKEN/g" "$file"
        echo "  Updated: $file"
    fi
done

# Also replace in admin/ (though may not be deployed)
find admin -name "*.html" -type f 2>/dev/null | while read file; do
    if grep -q "YOUR_CF_ANALYTICS_TOKEN_HERE" "$file"; then
        sed -i "s/YOUR_CF_ANALYTICS_TOKEN_HERE/$REAL_TOKEN/g" "$file"
        echo "  Updated: $file"
    fi
done

echo "✅ Token replacement complete."