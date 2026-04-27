#!/bin/bash
set -e

echo "Fixing footer links..."

# Find HTML files, exclude _site directory
find . -name "*.html" -type f ! -path "./_site/*" | while read file; do
    echo "Processing $file"
    # Backup (optional)
    # cp "$file" "$file.bak"
    
    # Remove Twitter line
    sed -i '/Twitter<\/a>/d' "$file"
    # Remove Instagram line
    sed -i '/Instagram<\/a>/d' "$file"
    
    # Fix Privacy Policy link
    sed -i 's|<a href="#" class="text-accent hover:underline">Privacy Policy</a>|<a href="/privacy/" class="text-accent hover:underline">Privacy Policy</a>|g' "$file"
    
    # Fix Terms link (both 'Terms' and 'Terms of Service')
    sed -i 's|<a href="#" class="text-accent hover:underline">Terms</a>|<a href="/terms/" class="text-accent hover:underline">Terms of Service</a>|g' "$file"
    sed -i 's|<a href="#" class="text-accent hover:underline">Terms of Service</a>|<a href="/terms/" class="text-accent hover:underline">Terms of Service</a>|g' "$file"
done

echo "Done."