#!/bin/bash
set -e

cd "$(dirname "$0")"

# Function to convert JPG to WebP
convert_to_webp() {
    local input="$1"
    local output="${input%.*}.webp"
    if [ -f "$input" ]; then
        convert "$input" -quality 85 -define webp:method=6 "$output"
        echo "Created: $output"
    fi
}

echo "Creating WebP versions..."
# Convert all 2026 JPG images
for img in static/images/products/*2026.jpg static/images/guide-*2026.jpg static/images/og-*2026.jpg; do
    if [ -f "$img" ]; then
        convert_to_webp "$img"
    fi
done

echo "Done!"