#!/bin/bash
set -e

cd "$(dirname "$0")"
IMAGE_DIR="static/images"
PRODUCT_DIR="$IMAGE_DIR/products"

# Create directories if they don't exist
mkdir -p "$PRODUCT_DIR"

# Function to download image from picsum.photos
download_picsum() {
    local width="$1"
    local height="$2"
    local image_id="$3"  # optional ID for specific image
    local output="$4"
    
    if [ -z "$image_id" ]; then
        # Random image
        url="https://picsum.photos/${width}/${height}.jpg"
    else
        # Specific image by ID
        url="https://picsum.photos/id/${image_id}/${width}/${height}.jpg"
    fi
    
    if curl -s -L -o "$output" "$url"; then
        if [ -s "$output" ]; then
            echo "Downloaded: $output"
            return 0
        fi
    fi
    echo "Failed to download: $output"
    return 1
}

# Product images (800x600)
echo "Downloading product images..."
# Keyboard - using image ID 160 (keyboard)
download_picsum 800 600 160 "$PRODUCT_DIR/ergo-keyboard-2026.jpg"
# Monitor arm - using image ID 180 (tech)
download_picsum 800 600 180 "$PRODUCT_DIR/monitor-arm-2026.jpg"

# Guide images (1200x630)
echo "Downloading guide images..."
# Lighting guide - using image ID 96 (light)
download_picsum 1200 630 96 "$IMAGE_DIR/guide-lighting-2026.jpg"
# Cable management - using image ID 167 (cables)
download_picsum 1200 630 167 "$IMAGE_DIR/guide-cable-2026.jpg"
# Mindset - using image ID 175 (office)
download_picsum 1200 630 175 "$IMAGE_DIR/guide-mindset-2026.jpg"

# OG images (1200x630)
echo "Downloading Open Graph images..."
# Home OG - using image ID 96 (office with light)
download_picsum 1200 630 96 "$IMAGE_DIR/og-home-2026.jpg"
# Deals OG - using image ID 160 (keyboard) + 180 (tech) composite - just use 160
download_picsum 1200 630 160 "$IMAGE_DIR/og-deals-2026.jpg"

echo "Done!"