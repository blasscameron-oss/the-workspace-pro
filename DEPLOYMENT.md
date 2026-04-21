# Deployment Instructions for The Workspace Pro

## Quick Deploy (Drag & Drop)

1. **Download** this ZIP file (`theworkspacepro-optimized.zip`)
2. Go to **https://app.netlify.com/drop**
3. Drag and drop the ZIP file onto the Netlify drop zone
4. Netlify will automatically deploy your site

## Custom Domain Setup

After deployment:

1. In Netlify dashboard, go to **Site settings** → **Domain management**
2. Click **Add custom domain**
3. Enter `theworkspacepro.com` and `www.theworkspacepro.com`
4. Follow Netlify's DNS instructions:
   - **Option A (Recommended)**: Use Netlify DNS
   - **Option B**: Update existing DNS at Namecheap:
     - Remove existing A records
     - Add A record for `@` → `75.2.60.5`
     - Add A record for `www` → `75.2.60.5`
     - Wait 24-48 hours for DNS propagation

## Optimization Features Included

This build includes the following performance optimizations:

### ✅ Image Optimization
- **WebP format** with JPEG/PNG fallbacks (picture element)
- **Lazy loading** for below‑the‑fold images
- **Async decoding** to prevent main‑thread blocking
- **Responsive sizes** via `sizes="100vw"`

### ✅ JavaScript Optimization
- **Dynamic loading** of search scripts (Lunr.js + search.js)
- **Only loads when needed** (when search overlay opens)
- **Preconnect hints** for CDN resources

### ✅ CSS Optimization
- **Tailwind CSS v4** with minimal production output
- **Critical font loading** with `preload` and `font‑display: swap`
- **Minified via cssnano** in production builds

### ✅ Caching & Delivery
- **Immutable caching** for static assets (1 year)
- **Netlify CDN** with edge delivery
- **Compression** (gzip/Brotli) enabled via Netlify

### ✅ User Experience
- **Stamatiou‑inspired design** (muted palette, clean typography)
- **Mobile‑first responsive** with tap‑target optimizations
- **Dark mode toggle** with localStorage persistence
- **Smooth scroll** for anchor links
- **Client‑side search** with Lunr.js
- **Affiliate‑ready product cards** with disclosures

## Post‑Deployment Checks

After deployment, verify:

1. **Images load correctly** (check WebP support in Chrome DevTools → Network)
2. **Search functionality** (click search icon, type a query)
3. **Mobile responsiveness** (test on phone or Chrome DevTools device mode)
4. **Dark mode toggle** (click theme toggle in header)
5. **Product cards** display with affiliate links

## Affiliate Setup

To monetize product recommendations:

1. Sign up for affiliate programs (Amazon Associates, etc.)
2. Update `affiliateUrl` fields in `_data/products.json`
3. Redeploy or use Netlify's Git‑based deployment for updates

## Support

For issues or questions, refer to the project documentation or contact the development team.

---

**Build Date**: April 16, 2026  
**Optimized By**: OpenClaw with Full‑Stack Dev Skill  
**Framework**: Eleventy (11ty) + Tailwind CSS v4  
**Deployment**: Netlify (static hosting)