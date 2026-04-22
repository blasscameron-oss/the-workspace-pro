#!/bin/bash
set -e

cd "$(dirname "$0")"

# List of content directories to skip (non‑guide pages)
skip_dirs=("about" "contact" "privacy" "terms" "podcasts" "guides" "home" "tips")

for dir in content/*/; do
    dir_name=$(basename "$dir")
    if [[ ! -f "$dir/index.html" ]]; then
        continue
    fi
    # Skip if in skip list
    if printf '%s\n' "${skip_dirs[@]}" | grep -qx "$dir_name"; then
        echo "Skipping $dir_name (non‑guide)"
        continue
    fi
    echo "Updating $dir_name..."
    ./update_guide.py "$dir/index.html" "$dir/index-new.html"
    mv "$dir/index-new.html" "$dir/index.html"
done

echo "All guides updated."