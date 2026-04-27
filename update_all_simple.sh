#!/bin/bash

# Simple script to update all HTML files
set -e

echo "Starting update of HTML files..."

# Array of files and their descriptions
declare -A desc
desc["best-standing-desks-under-500"]="Discover the best standing desks under \$500 for your home office. Compare features, prices, and ergonomic benefits of top budget-friendly standing desk options."
desc["cable-management-solutions"]="Effective cable management solutions for a clean, organized home office. Learn about cable trays, sleeves, clips, and routing techniques to eliminate desk clutter."
desc["contact"]="Contact The Workspace Pro team with questions, feedback, or partnership inquiries. We're here to help you build a better home office."
desc["dual-monitor-setup-productivity"]="Maximize productivity with a dual monitor setup. Learn optimal configuration, mounting options, and software tips for remote work efficiency."
desc["ergonomic-accessories-home-office"]="Essential ergonomic accessories for your home office: monitor arms, keyboard trays, footrests, and more to improve comfort and reduce strain."
desc["guides"]="Browse our complete collection of home office guides covering ergonomics, productivity, lighting, cable management, and workspace optimization."
desc["home-office-budget-setup-under-1000"]="Build a complete, ergonomic home office setup for under \$1000. Budget-friendly desk, chair, monitor, and accessory recommendations for remote workers."
desc["home-office-desk-guide-2026"]="Complete guide to choosing the perfect home office desk in 2026. Compare standing desks, traditional desks, materials, sizes, and features."
desc["home-office-lighting-guide"]="Home office lighting guide: How to choose the best lights for productivity, reduce eye strain, and create an ideal work environment with natural and artificial lighting."
desc["podcasts"]="Listen to top productivity and workspace podcasts curated by The Workspace Pro. Learn from experts about ergonomics, remote work, and home office optimization."
desc["privacy"]="Privacy policy for The Workspace Pro. Learn how we collect, use, and protect your personal information when you visit our website."
desc["productive-workspace-mindset"]="Develop a productive workspace mindset with tips for focus, time management, and creating an environment that supports deep work and creativity."
desc["small-home-office-organization-hacks"]="Space-saving organization hacks for small home offices. Maximize productivity in limited spaces with clever storage and layout solutions."
desc["terms"]="Terms of service for The Workspace Pro website. Please read these terms carefully before using our content, product recommendations, or newsletter."
desc["tips"]="Daily workspace tips and productivity hacks to improve your home office setup, ergonomics, and work habits. New tip every day."

# List of files to process
files=(
    "best-standing-desks-under-500"
    "cable-management-solutions"
    "contact"
    "dual-monitor-setup-productivity"
    "ergonomic-accessories-home-office"
    "guides"
    "home-office-budget-setup-under-1000"
    "home-office-desk-guide-2026"
    "home-office-lighting-guide"
    "podcasts"
    "privacy"
    "productive-workspace-mindset"
    "small-home-office-organization-hacks"
    "terms"
    "tips"
)

for page in "${files[@]}"; do
    file="content/$page/index.html"
    echo "Processing $file"
    
    if [ ! -f "$file" ]; then
        echo "  File not found, skipping"
        continue
    fi
    
    # Backup
    cp "$file" "$file.bak"
    
    # Get description (escape for sed)
    description="${desc[$page]}"
    # Escape for sed: replace & with \&, / with \/
    description_sed=$(echo "$description" | sed 's/[&/\]/\\&/g')
    
    # 1. Replace style block with external CSS
    sed -i '/<style>/,/<\/style>/c\    <link rel="stylesheet" href="/static/css/custom.css">' "$file"
    
    # 2. Update meta descriptions
    sed -i "s|<meta name=\"description\" content=\"[^\"]*\">|<meta name=\"description\" content=\"$description_sed\">|" "$file"
    sed -i "s|<meta property=\"og:description\" content=\"[^\"]*\">|<meta property=\"og:description\" content=\"$description_sed\">|" "$file"
    sed -i "s|<meta name=\"twitter:description\" content=\"[^\"]*\">|<meta name=\"twitter:description\" content=\"$description_sed\">|" "$file"
    
    # 3. Add canonical tag
    sed -i "s|<meta name=\"twitter:image\"[^>]*>|&\n    <link rel=\"canonical\" href=\"https://www.theworkspacepro.com/content/$page/\">|" "$file"
    
    # 4. Determine schema type and add JSON-LD before </head>
    if [[ "$page" =~ ^(about|contact|privacy|terms|guides|tips|podcasts)$ ]]; then
        # WebPage schema
        schema="<script type=\"application/ld+json\">
    {
      \"@context\": \"https://schema.org\",
      \"@type\": \"WebPage\",
      \"name\": \"${page^}\",
      \"description\": \"$description_sed\",
      \"url\": \"https://www.theworkspacepro.com/content/$page/\"
    }
    </script>"
    else
        # Article schema
        # Extract title from HTML (simplified)
        title=$(grep -o '<title>[^<]*</title>' "$file" | sed 's/<title>\(.*\) | The Workspace Pro<\/title>/\1/')
        if [ -z "$title" ]; then
            # Convert page key to title
            title=$(echo "$page" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)}1')
        fi
        # Escape title for sed
        title_sed=$(echo "$title" | sed 's/[&/\]/\\&/g')
        
        schema="<script type=\"application/ld+json\">
    {
      \"@context\": \"https://schema.org\",
      \"@type\": \"Article\",
      \"headline\": \"$title_sed\",
      \"description\": \"$description_sed\",
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
        \"@id\": \"https://www.theworkspacepro.com/content/$page/\"
      }
    }
    </script>"
    fi
    
    # Insert schema before </head>
    # Escape schema for sed
    schema_sed=$(echo "$schema" | sed ':a;N;$!ba;s/\n/\\n/g')
    sed -i "s|</head>|$schema_sed\\n</head>|" "$file"
    
    echo "  ✓ Updated $page"
done

echo "Done!"