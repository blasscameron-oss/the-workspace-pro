#!/bin/bash

# Update all HTML files with improvements

set -e

BASE_DIR="/home/cameron/.openclaw/workspace/workspace-pro-minimal"

# Array of files to process (excluding already updated ones)
FILES=(
  "$BASE_DIR/content/best-standing-desks-under-500/index.html"
  "$BASE_DIR/content/cable-management-solutions/index.html"
  "$BASE_DIR/content/contact/index.html"
  "$BASE_DIR/content/dual-monitor-setup-productivity/index.html"
  "$BASE_DIR/content/ergonomic-accessories-home-office/index.html"
  "$BASE_DIR/content/guides/index.html"
  "$BASE_DIR/content/home-office-budget-setup-under-1000/index.html"
  "$BASE_DIR/content/home-office-desk-guide-2026/index.html"
  "$BASE_DIR/content/home-office-lighting-guide/index.html"
  "$BASE_DIR/content/podcasts/index.html"
  "$BASE_DIR/content/privacy/index.html"
  "$BASE_DIR/content/productive-workspace-mindset/index.html"
  "$BASE_DIR/content/small-home-office-organization-hacks/index.html"
  "$BASE_DIR/content/terms/index.html"
  "$BASE_DIR/content/tips/index.html"
)

# Descriptions for each page
declare -A DESCRIPTIONS
DESCRIPTIONS["best-standing-desks-under-500"]="Discover the best standing desks under $500 for your home office. Compare features, prices, and ergonomic benefits of top budget-friendly standing desk options."
DESCRIPTIONS["cable-management-solutions"]="Effective cable management solutions for a clean, organized home office. Learn about cable trays, sleeves, clips, and routing techniques to eliminate desk clutter."
DESCRIPTIONS["contact"]="Contact The Workspace Pro team with questions, feedback, or partnership inquiries. We're here to help you build a better home office."
DESCRIPTIONS["dual-monitor-setup-productivity"]="Maximize productivity with a dual monitor setup. Learn optimal configuration, mounting options, and software tips for remote work efficiency."
DESCRIPTIONS["ergonomic-accessories-home-office"]="Essential ergonomic accessories for your home office: monitor arms, keyboard trays, footrests, and more to improve comfort and reduce strain."
DESCRIPTIONS["guides"]="Browse our complete collection of home office guides covering ergonomics, productivity, lighting, cable management, and workspace optimization."
DESCRIPTIONS["home-office-budget-setup-under-1000"]="Build a complete, ergonomic home office setup for under $1000. Budget-friendly desk, chair, monitor, and accessory recommendations for remote workers."
DESCRIPTIONS["home-office-desk-guide-2026"]="Complete guide to choosing the perfect home office desk in 2026. Compare standing desks, traditional desks, materials, sizes, and features."
DESCRIPTIONS["home-office-lighting-guide"]="Home office lighting guide: How to choose the best lights for productivity, reduce eye strain, and create an ideal work environment with natural and artificial lighting."
DESCRIPTIONS["podcasts"]="Listen to top productivity and workspace podcasts curated by The Workspace Pro. Learn from experts about ergonomics, remote work, and home office optimization."
DESCRIPTIONS["privacy"]="Privacy policy for The Workspace Pro. Learn how we collect, use, and protect your personal information when you visit our website."
DESCRIPTIONS["productive-workspace-mindset"]="Develop a productive workspace mindset with tips for focus, time management, and creating an environment that supports deep work and creativity."
DESCRIPTIONS["small-home-office-organization-hacks"]="Space-saving organization hacks for small home offices. Maximize productivity in limited spaces with clever storage and layout solutions."
DESCRIPTIONS["terms"]="Terms of service for The Workspace Pro website. Please read these terms carefully before using our content, product recommendations, or newsletter."
DESCRIPTIONS["tips"]="Daily workspace tips and productivity hacks to improve your home office setup, ergonomics, and work habits. New tip every day."

echo "Processing ${#FILES[@]} HTML files..."

for FILE in "${FILES[@]}"; do
    echo "Processing: $FILE"
    
    # Extract page key from path
    PAGE_KEY=$(echo "$FILE" | sed -n 's|.*/content/\([^/]*\)/index.html|\1|p')
    
    if [ -z "$PAGE_KEY" ]; then
        echo "  ⚠ Could not extract page key, skipping"
        continue
    fi
    
    DESCRIPTION="${DESCRIPTIONS[$PAGE_KEY]}"
    if [ -z "$DESCRIPTION" ]; then
        DESCRIPTION="Expert-curated ergonomic home office guides, product recommendations, and daily tips to build a healthier, more productive workspace."
    fi
    
    # Backup original
    cp "$FILE" "$FILE.backup"
    
    # 1. Replace style block with external CSS
    # Using sed with pattern space for multiline replacement
    sed -i '/<style>/,/<\/style>/c\    <link rel="stylesheet" href="/static/css/custom.css">' "$FILE"
    
    # 2. Update meta descriptions
    sed -i "s|<meta name=\"description\" content=\"[^\"]*\">|<meta name=\"description\" content=\"$DESCRIPTION\">|" "$FILE"
    sed -i "s|<meta property=\"og:description\" content=\"[^\"]*\">|<meta property=\"og:description\" content=\"$DESCRIPTION\">|" "$FILE"
    sed -i "s|<meta name=\"twitter:description\" content=\"[^\"]*\">|<meta name=\"twitter:description\" content=\"$DESCRIPTION\">|" "$FILE"
    
    # 3. Add canonical tag after twitter:image
    CANONICAL_URL="https://www.theworkspacepro.com/content/$PAGE_KEY/"
    sed -i "s|<meta name=\"twitter:image\"[^>]*>|&\n    <link rel=\"canonical\" href=\"$CANONICAL_URL\">|" "$FILE"
    
    # 4. Determine schema type and add JSON-LD
    if [[ "$PAGE_KEY" =~ ^(about|contact|privacy|terms|guides|tips|podcasts)$ ]]; then
        # WebPage schema
        SCHEMA="<script type=\"application/ld+json\">
    {
      \"@context\": \"https://schema.org\",
      \"@type\": \"WebPage\",
      \"name\": \"${PAGE_KEY^}\",
      \"description\": \"$DESCRIPTION\",
      \"url\": \"$CANONICAL_URL\"
    }
    </script>"
    else
        # Article schema (for guides)
        # Extract title from HTML
        TITLE=$(grep -o '<title>[^<]*</title>' "$FILE" | sed 's/<title>\(.*\) | The Workspace Pro<\/title>/\1/')
        if [ -z "$TITLE" ]; then
            TITLE="${PAGE_KEY//-/ }"
            TITLE=$(echo "$TITLE" | sed 's/\b\(.\)/\u\1/g')
        fi
        
        SCHEMA="<script type=\"application/ld+json\">
    {
      \"@context\": \"https://schema.org\",
      \"@type\": \"Article\",
      \"headline\": \"$TITLE\",
      \"description\": \"$DESCRIPTION\",
      \"image\": \"https://www.theworkspacepro.com/static/images/og-default.png\",
      \"author\": {
        \"@type\": \"Organization\",
        \"name\": \"The Workspace Pro Team\"
      },
      \"publisher\": {
        \"@type\": \"Organization\",
        \"name\": \"The Workspace Pro\",
        \"logo\": {
          \"@type\": \"ImageObject\",
          \"url\": \"https://www.theworkspacepro.com/static/images/logo.png\"
        }
      },
      \"datePublished\": \"2026-04-01\",
      \"dateModified\": \"2026-04-01\",
      \"mainEntityOfPage\": {
        \"@type\": \"WebPage\",
        \"@id\": \"$CANONICAL_URL\"
      }
    }
    </script>"
    fi
    
    # Insert schema before </head>
    sed -i "s|</head>|$SCHEMA\n</head>|" "$FILE"
    
    # 5. Add lazy loading to images (simple - add to img tags without loading attribute)
    sed -i 's/<img\([^>]*\)>/<img\1 loading="lazy" decoding="async">/g' "$FILE"
    
    # 6. Add affiliate transparency near "Check Price" buttons
    sed -i 's|\(<a[^>]*Check Price[^<]*</a>\)|\1\n                    <p class="text-xs text-zinc-500 mt-2 text-center">We may earn a commission at no extra cost to you. Prices checked daily.</p>|gi' "$FILE"
    
    # Also for "See Current Deal"
    sed -i 's|\(<a[^>]*See Current Deal[^<]*</a>\)|\1\n                <p class="text-xs text-gray-500 mt-2">We may earn a commission at no extra cost to you. Prices checked daily.</p>|gi' "$FILE"
    
    echo "  ✓ Updated $PAGE_KEY"
done

echo "Done!"