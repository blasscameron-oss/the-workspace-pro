#!/bin/bash
set -e

cd "$(dirname "$0")"
IMAGE_DIR="static/images"
PRODUCT_DIR="$IMAGE_DIR/products"

# Create directories if they don't exist
mkdir -p "$PRODUCT_DIR"

# Function to download image with retry
download_image() {
    local url="$1"
    local output="$2"
    local max_retries=3
    local retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        if curl -s -L -o "$output" "$url"; then
            if [ -s "$output" ]; then
                echo "Downloaded: $output"
                return 0
            fi
        fi
        retry_count=$((retry_count + 1))
        echo "Retry $retry_count for $output"
        sleep 1
    done
    echo "Failed to download: $output"
    return 1
}

# Function to convert to WebP
convert_to_webp() {
    local input="$1"
    local output="${input%.*}.webp"
    if command -v cwebp &> /dev/null; then
        cwebp -q 80 "$input" -o "$output" && echo "Converted to WebP: $output"
    elif command -v convert &> /dev/null; then
        convert "$input" -quality 80 "$output" && echo "Converted to WebP: $output"
    else
        echo "No WebP converter found (cwebp or imagemagick)"
    fi
}

# Product images (800x600)
echo "Downloading product images..."
download_image "https://source.unsplash.com/featured/800x600?standing-desk,office" "$PRODUCT_DIR/standing-desk-2026.jpg"
download_image "https://source.unsplash.com/featured/800x600?ergonomic-chair,office" "$PRODUCT_DIR/ergo-chair-2026.jpg"
download_image "https://source.unsplash.com/featured/800x600?computer-monitor,4k" "$PRODUCT_DIR/4k-monitor-2026.jpg"
download_image "https://source.unsplash.com/featured/800x600?keyboard,mechanical" "$PRODUCT_DIR/ergo-keyboard-2026.jpg"
download_image "https://source.unsplash.com/featured/800x600?monitor-arm,desk" "$PRODUCT_DIR/monitor-arm-2026.jpg"

# Guide images (1200x630)
echo "Downloading guide images..."
download_image "https://source.unsplash.com/featured/1200x630?home-office-lighting" "$IMAGE_DIR/guide-lighting-2026.jpg"
download_image "https://source.unsplash.com/featured/1200x630?cable-management,desk" "$IMAGE_DIR/guide-cable-2026.jpg"
download_image "https://source.unsplash.com/featured/1200x630?productivity,mindset" "$IMAGE_DIR/guide-mindset-2026.jpg"

# OG images (1200x630)
echo "Downloading Open Graph images..."
download_image "https://source.unsplash.com/featured/1200x630?home-office,standing-desk,ergonomic" "$IMAGE_DIR/og-home-2026.jpg"
download_image "https://source.unsplash.com/featured/1200x630?desk,chair,monitor,accessories" "$IMAGE_DIR/og-deals-2026.jpg"

# Convert all downloaded images to WebP
echo "Converting images to WebP..."
for img in "$PRODUCT_DIR"/*.jpg "$IMAGE_DIR"/guide-*.jpg "$IMAGE_DIR"/og-*.jpg; do
    if [ -f "$img" ]; then
        convert_to_webp "$img"
    fi
done

echo "Done!"