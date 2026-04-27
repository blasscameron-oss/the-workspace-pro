#!/bin/bash

# Clean up duplicate canonical tags and JSON-LD blocks
set -e

echo "Cleaning up duplicates..."

files=(
    "content/best-standing-desks-under-500/index.html"
    "content/cable-management-solutions/index.html"
    "content/contact/index.html"
    "content/dual-monitor-setup-productivity/index.html"
    "content/ergonomic-accessories-home-office/index.html"
    "content/guides/index.html"
    "content/home-office-budget-setup-under-1000/index.html"
    "content/home-office-desk-guide-2026/index.html"
    "content/home-office-lighting-guide/index.html"
    "content/podcasts/index.html"
    "content/privacy/index.html"
    "content/productive-workspace-mindset/index.html"
    "content/small-home-office-organization-hacks/index.html"
    "content/terms/index.html"
    "content/tips/index.html"
)

for file in "${files[@]}"; do
    echo "Checking $file"
    
    if [ ! -f "$file" ]; then
        echo "  File not found"
        continue
    fi
    
    # Count canonical tags
    canonical_count=$(grep -c 'rel="canonical"' "$file")
    if [ "$canonical_count" -gt 1 ]; then
        echo "  Found $canonical_count canonical tags, removing duplicates"
        # Keep only the first one
        awk '
        /rel="canonical"/ && !found {
            print $0
            found = 1
            next
        }
        /rel="canonical"/ && found {
            next  # Skip duplicates
        }
        { print $0 }
        ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
    fi
    
    # Count JSON-LD blocks (simplified check)
    jsonld_count=$(grep -c 'application/ld+json' "$file")
    if [ "$jsonld_count" -gt 1 ]; then
        echo "  Found $jsonld_count JSON-LD blocks, removing duplicates"
        # Keep only content between first <script type="application/ld+json"> and </script>
        awk '
        BEGIN { in_jsonld = 0; jsonld_count = 0 }
        /<script type="application\/ld+json">/ {
            jsonld_count++
            if (jsonld_count == 1) {
                in_jsonld = 1
                print $0
                next
            } else {
                in_jsonld = 1
                next
            }
        }
        /<\/script>/ && in_jsonld {
            if (jsonld_count == 1) {
                print $0
            }
            in_jsonld = 0
            next
        }
        { 
            if (!in_jsonld || jsonld_count == 1) {
                print $0
            }
        }
        ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
    fi
    
    echo "  ✓ Cleaned up"
done

echo "Done!"