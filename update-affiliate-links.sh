#!/bin/bash
# Update affiliate links in HTML files with Amazon search URLs

set -e

TAG_FILE="affiliate-tag.txt"
if [[ -f "$TAG_FILE" ]]; then
    TAG=$(cat "$TAG_FILE" | tr -d '[:space:]')
else
    TAG="workspacepro-20"
fi

echo "Using affiliate tag: $TAG"

# Product mapping
declare -A MAP
MAP[desk]="standing+desk"
MAP[chair]="ergonomic+office+chair"
MAP[monitor]="32+inch+4k+monitor"
MAP[arm]="monitor+arm+gas+spring"
MAP[keyboard]="ergonomic+split+keyboard"

update_file() {
    local file=$1
    local changed=0
    local temp=$(mktemp)
    
    # Process each line
    while IFS= read -r line; do
        if [[ "$line" =~ href=\"https://example\.com/([^\"]+)\" ]]; then
            path="${BASH_REMATCH[1]}"
            query="${MAP[$path]:-$path}"
            new_url="https://www.amazon.com/s?k=$query&tag=$TAG"
            new_line="${line//href=\"https:\/\/example.com\/$path\"/href=\"$new_url\"}"
            if [[ "$line" != "$new_line" ]]; then
                line="$new_line"
                changed=1
            fi
        fi
        echo "$line" >> "$temp"
    done < "$file"
    
    if [[ $changed -eq 1 ]]; then
        mv "$temp" "$file"
        echo "Updated $file"
    else
        rm "$temp"
        echo "No changes in $file"
    fi
}

# Process files
for f in index.html deals.html; do
    if [[ -f "$f" ]]; then
        update_file "$f"
    else
        echo "Warning: $f not found"
    fi
done

echo "Done."