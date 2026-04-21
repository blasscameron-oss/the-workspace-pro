#!/usr/bin/awk -f

# Awk script to update HTML files
# Usage: awk -f update.awk -v page_key=key -v description="desc" file.html > file.new.html

BEGIN {
    # State variables
    in_style = 0
    style_replaced = 0
    desc_replaced = 0
    og_desc_replaced = 0
    twitter_desc_replaced = 0
    canonical_added = 0
    twitter_image_found = 0
    head_closed = 0
}

# Replace style block
/<style>/ {
    in_style = 1
    print "    <link rel=\"stylesheet\" href=\"/static/css/custom.css\">"
    next
}

in_style && /<\/style>/ {
    in_style = 0
    style_replaced = 1
    next
}

in_style {
    # Skip lines inside style block
    next
}

# Update meta description
/<meta name="description" content="[^"]*">/ && !desc_replaced {
    sub(/content="[^"]*"/, "content=\"" description "\"")
    desc_replaced = 1
}

# Update og:description
/<meta property="og:description" content="[^"]*">/ && !og_desc_replaced {
    sub(/content="[^"]*"/, "content=\"" description "\"")
    og_desc_replaced = 1
}

# Update twitter:description  
/<meta name="twitter:description" content="[^"]*">/ && !twitter_desc_replaced {
    sub(/content="[^"]*"/, "content=\"" description "\"")
    twitter_desc_replaced = 1
}

# Add canonical after twitter:image
/<meta name="twitter:image"[^>]*>/ && !canonical_added {
    print $0
    print "    <link rel=\"canonical\" href=\"https://www.theworkspacepro.com/content/" page_key "/\">"
    canonical_added = 1
    next
}

# Add JSON-LD before </head>
/<\/head>/ && !head_closed {
    # Print schema first
    if (page_key ~ /^(about|contact|privacy|terms|guides|tips|podcasts)$/) {
        print "    <script type=\"application/ld+json\">"
        print "    {"
        print "      \"@context\": \"https://schema.org\","
        print "      \"@type\": \"WebPage\","
        printf "      \"name\": \""
        # Capitalize page key
        split(page_key, words, "-")
        for (i in words) {
            words[i] = toupper(substr(words[i],1,1)) substr(words[i],2)
        }
        name = words[1]
        for (i=2; i<=length(words); i++) {
            name = name " " words[i]
        }
        printf "%s\",\n", name
        print "      \"description\": \"" description "\","
        print "      \"url\": \"https://www.theworkspacepro.com/content/" page_key "/\""
        print "    }"
        print "    </script>"
    } else {
        # Article schema - would need title extraction
        print "    <script type=\"application/ld+json\">"
        print "    {"
        print "      \"@context\": \"https://schema.org\","
        print "      \"@type\": \"Article\","
        printf "      \"headline\": \""
        # Simple title from page_key
        split(page_key, words, "-")
        for (i in words) {
            words[i] = toupper(substr(words[i],1,1)) substr(words[i],2)
        }
        title = words[1]
        for (i=2; i<=length(words); i++) {
            title = title " " words[i]
        }
        printf "%s\",\n", title
        print "      \"description\": \"" description "\","
        print "      \"image\": \"https://www.theworkspacepro.com/static/images/og-default.png\","
        print "      \"author\": {"
        print "        \"@type\": \"Organization\","
        print "        \"name\": \"The Workspace Pro Team\""
        print "      },"
        print "      \"publisher\": {"
        print "        \"@type\": \"Organization\","
        print "        \"name\": \"The Workspace Pro\","
        print "        \"logo\": {"
        print "          \"@type\": \"ImageObject\","
        print "          \"url\": \"https://www.theworkspacepro.com/static/images/logo.png\""
        print "        }"
        print "      },"
        print "      \"datePublished\": \"2026-04-01\","
        print "      \"dateModified\": \"2026-04-01\","
        print "      \"mainEntityOfPage\": {"
        print "        \"@type\": \"WebPage\","
        print "        \"@id\": \"https://www.theworkspacepro.com/content/" page_key "/\""
        print "      }"
        print "    }"
        print "    </script>"
    }
    head_closed = 1
}

# Print all other lines
{
    if (!((/<meta name="twitter:image"[^>]*>/ && canonical_added) || /<\/head>/)) {
        print $0
    }
}

END {
    if (!style_replaced) {
        print "WARNING: Style block not found" > "/dev/stderr"
    }
}