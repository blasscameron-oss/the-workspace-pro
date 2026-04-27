#!/bin/bash
echo "Checking _site directory for Cloudflare deployment..."
echo "=================================================="

# Check key files exist
required_files=(
  "_site/index.html"
  "_site/sitemap.xml"
  "_site/robots.txt"
  "_site/_headers"
  "_site/_redirects"
  "_site/_routes.json"
  "_site/static/css/custom.css"
  "_site/package.json"
  "_site/CLOUDFLARE_DEPLOYMENT.md"
)

missing=0
for file in "${required_files[@]}"; do
  if [ -f "$file" ]; then
    echo "✓ $file"
  else
    echo "✗ $file (MISSING)"
    ((missing++))
  fi
done

echo ""
echo "Checking HTML file count..."
html_count=$(find _site -name "*.html" | wc -l)
echo "HTML files in _site: $html_count"

echo ""
echo "Checking for Cloudflare Pages configuration..."
if grep -q "Cloudflare" _site/CLOUDFLARE_DEPLOYMENT.md 2>/dev/null; then
  echo "✓ Cloudflare deployment guide present"
else
  echo "✗ Cloudflare guide missing or corrupted"
fi

if [ -f "_site/wrangler.toml" ]; then
  echo "✓ wrangler.toml present (optional)"
fi

echo ""
echo "Checking ZIP file..."
if [ -f "workspace-pro-deploy-2026-04-18.zip" ]; then
  zip_size=$(du -h workspace-pro-deploy-2026-04-18.zip | cut -f1)
  echo "✓ Deployment ZIP: workspace-pro-deploy-2026-04-18.zip ($zip_size)"
else
  echo "✗ ZIP file not found"
fi

echo ""
echo "=================================================="
if [ $missing -eq 0 ]; then
  echo "✅ _site directory is ready for Cloudflare Pages deployment!"
  echo ""
  echo "Next steps:"
  echo "1. Go to https://pages.cloudflare.com"
  echo "2. Click 'Create a project'"
  echo "3. Select 'Direct upload'"
  echo "4. Drag and drop the '_site' folder or ZIP file"
  echo "5. Follow instructions in CLOUDFLARE_DEPLOYMENT.md"
else
  echo "⚠ $missing required files are missing."
  echo "Run ./sync_site.sh to sync updates."
fi