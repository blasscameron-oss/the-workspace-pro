#!/bin/bash
TAG="workspacepro-20"
# Update index.html
sed -i 's|href="https://example\.com/desk"|href="https://www.amazon.com/s?k=standing+desk\&tag='"$TAG"'"|g' index.html
sed -i 's|href="https://example\.com/chair"|href="https://www.amazon.com/s?k=ergonomic+office+chair\&tag='"$TAG"'"|g' index.html
sed -i 's|href="https://example\.com/monitor"|href="https://www.amazon.com/s?k=32+inch+4k+monitor\&tag='"$TAG"'"|g' index.html
sed -i 's|href="https://example\.com/arm"|href="https://www.amazon.com/s?k=monitor+arm+gas+spring\&tag='"$TAG"'"|g' index.html
sed -i 's|href="https://example\.com/keyboard"|href="https://www.amazon.com/s?k=ergonomic+split+keyboard\&tag='"$TAG"'"|g' index.html
# Update deals.html (no keyboard)
sed -i 's|href="https://example\.com/desk"|href="https://www.amazon.com/s?k=standing+desk\&tag='"$TAG"'"|g' deals.html
sed -i 's|href="https://example\.com/chair"|href="https://www.amazon.com/s?k=ergonomic+office+chair\&tag='"$TAG"'"|g' deals.html
sed -i 's|href="https://example\.com/monitor"|href="https://www.amazon.com/s?k=32+inch+4k+monitor\&tag='"$TAG"'"|g' deals.html
sed -i 's|href="https://example\.com/arm"|href="https://www.amazon.com/s?k=monitor+arm+gas+spring\&tag='"$TAG"'"|g' deals.html
