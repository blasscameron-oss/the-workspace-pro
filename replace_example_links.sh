#!/bin/bash
set -e

echo "Replacing example.com placeholder links with Amazon affiliate links..."

# Function to replace in a file
replace_link() {
    local file="$1"
    local old="$2"
    local new="$3"
    if grep -q "$old" "$file"; then
        sed -i "s|$old|$new|g" "$file"
        echo "  Updated: $file"
    fi
}

# Chair guide
chair_file="content/ergonomic-office-chair-buying-guide/index.html"
if [ -f "$chair_file" ]; then
    replace_link "$chair_file" \
        'https://example.com/chairs' \
        'https://www.amazon.com/s?k=ergonomic+chair'
fi

# Organization guide
org_file="content/small-home-office-organization-hacks/index.html"
if [ -f "$org_file" ]; then
    replace_link "$org_file" \
        'https://example.com/organization' \
        'https://www.amazon.com/s?k=office+organization+tools'
fi

# Dual monitor guide
dual_file="content/dual-monitor-setup-productivity/index.html"
if [ -f "$dual_file" ]; then
    replace_link "$dual_file" \
        'https://example.com/dual-monitor' \
        'https://www.amazon.com/s?k=dual+monitor+stand'
fi

# Standing desk guide
desk_file="content/best-standing-desks-under-500/index.html"
if [ -f "$desk_file" ]; then
    replace_link "$desk_file" \
        'https://example.com/standing-desks' \
        'https://www.amazon.com/s?k=standing+desk'
fi

echo "✅ Example links replaced."