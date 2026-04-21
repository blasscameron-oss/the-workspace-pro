#!/usr/bin/awk -f
# Awk script to update HTML files
BEGIN {
    # Page descriptions - would need to be passed as variables
    # For now, just a placeholder
    description = "PLACEHOLDER"
    page_key = "PLACEHOLDER"
}

# Track if we're in style block
/<style>/ { in_style = 1; next }
in_style && /<\/style>/ { 
    in_style = 0; 
    print "    <link rel=\"stylesheet\" href=\"/static/css/custom.css\">";
    next 
}
in_style { next } # Skip style block content

# Update meta description
/<meta name="description" content="[^"]*">/ && !desc_done {
    sub(/content="[^"]*"/, "content=\"" description "\"")
    desc_done = 1
}

# Update og:description
/<meta property="og:description" content="[^"]*">/ && !og_done {
    sub(/content="[^"]*"/, "content=\"" description "\"")
    og_done = 1
}

# Update twitter:description
/<meta name="twitter:description" content="[^"]*">/ && !twitter_done {
    sub(/content="[^"]*"/, "content=\"" description "\"")
    twitter_done = 1
}

# Add canonical after twitter:image
/<meta name="twitter:image"[^>]*>/ && !canonical_done {
    print $0
    print "    <link rel=\"canonical\" href=\"https://www.theworkspacepro.com/content/" page_key "/\">"
    canonical_done = 1
    next
}

# Add JSON-LD before </head>
/<\/head>/ && !head_closed {
    # Print schema first
    print_schema()
    head_closed = 1
}

# Default action: print line
{ 
    if (!((/<meta name="twitter:image"[^>]*>/ && canonical_done) || /<\/head>/)) {
        print $0
    }
}

function print_schema() {
    # Simplified schema - would need more logic for different page types
    print "    <script type=\"application/ld+json\">"
    print "    {"
    print "      \"@context\": \"https://schema.org\","
    print "      \"@type\": \"Article\","
    print "      \"headline\": \"PLACEHOLDER TITLE\","
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
    print "</head>"
}