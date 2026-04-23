# Affiliate Link Setup

Your site now uses Amazon search links with a placeholder affiliate tag (`workspacepro-20`).

## What Was Changed

- **Homepage product cards** (5 items) now link to Amazon search results.
- **Deals page product cards** (4 items) now link to Amazon search results.
- All links include the `rel="sponsored noopener noreferrer"` attribute for SEO compliance.

## Next Steps

### 1. Get Your Amazon Associates Tag
- Sign up at [Amazon Associates](https://affiliate-program.amazon.com) if you haven't already.
- Once approved, your affiliate tag will look like `yourname-20` (e.g., `workspacepro-20`).

### 2. Replace the Placeholder Tag
Edit the file `affiliate-tag.txt` and replace `workspacepro-20` with your actual Amazon Associates tag.

### 3. Update All Links
Run the update script:

```bash
./update-affiliate-links.sh
```

This will regenerate all Amazon links with your tag.

### 4. Optional: Replace Search Queries with Specific Product Links
For higher conversion, replace the Amazon search links with direct product links.

Example:
- Instead of `https://www.amazon.com/s?k=standing+desk&tag=yourtag`
- Use `https://www.amazon.com/dp/B0XXXXXXX?tag=yourtag`

Update the `PRODUCT_MAPPING` in `update-affiliate-links.py` or edit the HTML files directly.

### 5. Deploy Changes
Commit and push:

```bash
git add .
git commit -m "Update affiliate tag"
git push origin main
```

## Legal Compliance

- The site already includes FTC disclosures in the footer.
- Amazon requires you to disclose that you earn from qualifying purchases.
- Ensure your Amazon Associates account is in good standing.

## Additional Affiliate Programs

Consider joining other retailer programs:
- **Staples** – Office furniture
- **Dell** – Monitors & computers
- **Logitech** – Keyboards, mice, webcams
- **IKEA** – Direct product links (no affiliate program)

Update guide pages with specific affiliate links as needed.

## Verification

After deployment, visit:
- https://www.theworkspacepro.com
- https://www.theworkspacepro.com/deals/

Click the "Check Price" buttons to confirm they lead to Amazon with your tag.

---

**Note**: The placeholder tag (`workspacepro-20`) will not earn commissions. Replace it with your own tag to start earning.