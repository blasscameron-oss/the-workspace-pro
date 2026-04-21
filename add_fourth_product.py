#!/usr/bin/env python3
import sys

with open('index.html', 'r') as f:
    content = f.read()

# Find the grid section
grid_start = content.find('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">')
if grid_start == -1:
    sys.exit("Grid not found")

# Find the closing div of the grid (8 spaces)
import re
# Find next occurrence of "\n        </div>" after grid_start
match = re.search(r'\n        </div>', content[grid_start:])
if not match:
    sys.exit("Grid closing div not found")
grid_end = grid_start + match.start()  # position of newline before closing div

# Find the last product card closing div before grid_end
# Look for "            </div>" (12 spaces) that appears before grid_end
last_product_close = content.rfind('            </div>', grid_start, grid_end)
if last_product_close == -1:
    sys.exit("Last product close not found")

# Insert after that closing div (position after the closing tag)
insert_pos = last_product_close + len('            </div>')

# New product card HTML (indented with 12 spaces)
new_product = '''
            <div class="product-card bg-white dark:bg-zinc-900 rounded-3xl overflow-hidden border border-zinc-200 dark:border-zinc-800">
                <div class="h-64 bg-zinc-100 dark:bg-zinc-800 flex items-center justify-center p-8">
                    <picture>
                        <source type="image/webp" srcset="/static/images/products/ergonomic-chair-400.webp 400w, /static/images/products/ergonomic-chair-800.webp 800w, /static/images/products/ergonomic-chair-1600.webp 1600w" sizes="(max-width: 768px) 400px, 800px">
                        <source type="image/jpeg" srcset="/static/images/products/ergonomic-chair-400.jpg 400w, /static/images/products/ergonomic-chair-800.jpg 800w, /static/images/products/ergonomic-chair-1600.jpg 1600w" sizes="(max-width: 768px) 400px, 800px">
                        <img src="/static/images/products/ergonomic-chair-800.jpg" alt="Branch Ergonomic Chair Pro with 4D armrests, adjustable lumbar, and breathable mesh back" loading="lazy" decoding="async" class="max-h-full object-contain">
                    </picture>
                </div>
                <div class="p-8">
                    <div class="flex justify-between items-start mb-4">
                        <div>
                            <h3 class="font-semibold text-xl">Branch Ergonomic Chair Pro</h3>
                            <p class="text-emerald-600 font-medium">$699.99 USD</p>
                            <p class="text-xs text-zinc-500">Price as of Apr 21, 2026</p>
                        </div>
                        <span class="text-xs bg-zinc-100 dark:bg-zinc-800 px-3 py-1 rounded-full">Branch</span>
                    </div>
                    <p class="text-sm text-zinc-600 dark:text-zinc-400 mb-6">Premium ergonomic chair with 4D armrests, adjustable lumbar, and breathable mesh.</p>
                    <ul class="space-y-2 text-sm mb-8">


                        <li class="flex items-center gap-2"><i class="fa-solid fa-check text-emerald-500"></i> 4D armrests</li>



                        <li class="flex items-center gap-2"><i class="fa-solid fa-check text-emerald-500"></i> Adjustable lumbar</li>



                        <li class="flex items-center gap-2"><i class="fa-solid fa-check text-emerald-500"></i> Breathable mesh</li>




                    </ul>
                    <a href="https://www.branchfurniture.com/products/ergonomic-chair" target="_blank" rel="sponsored noopener noreferrer" class="block w-full text-center bg-zinc-900 dark:bg-white text-white dark:text-zinc-900 py-4 rounded-2xl font-semibold hover:bg-emerald-600 hover:text-white transition">
                        Check Price
                    </a>
                    <p class="text-xs text-zinc-500 mt-2 text-center">We may earn a commission at no extra cost to you. Prices checked daily.</p>
                </div>
            </div>
'''

# Insert with blank lines before and after to match spacing
new_content = content[:insert_pos] + "\n\n" + new_product + "\n\n" + content[insert_pos:]

# Now update schema.org JSON-LD
# Find the schema script and add fourth product
schema_start = new_content.find('"@graph": [')
if schema_start == -1:
    sys.exit("Schema graph not found")

# Find the closing bracket of the @graph array
bracket_start = new_content.find('[', schema_start)
bracket_end = new_content.find(']', bracket_start)
if bracket_start == -1 or bracket_end == -1:
    sys.exit("Schema array not found")

# Find the Dell monitor product by its URL
dell_url = 'https://www.amazon.com/s?k=Dell+S2421HN+monitor'
dell_idx = new_content.find(dell_url, schema_start)
if dell_idx == -1:
    sys.exit("Dell URL in schema not found")

# Find the closing brace after this URL
brace_close = new_content.find('}', dell_idx)
if brace_close == -1:
    sys.exit("Closing brace not found")

# Insert new product after this brace, with a comma
new_product_schema = ''',
    {
      "@type": "Product",
      "name": "Branch Ergonomic Chair Pro",
      "description": "Premium ergonomic chair with 4D armrests, adjustable lumbar, and breathable mesh.",
      "image": "/static/images/products/ergonomic-chair-800.jpg",
      "offers": {
        "@type": "Offer",
        "price": "699.99",
        "priceCurrency": "USD",
        "availability": "https://schema.org/InStock",
        "url": "https://www.branchfurniture.com/products/ergonomic-chair"
      }
    }'''

new_content = new_content[:brace_close+1] + new_product_schema + new_content[brace_close+1:]

# Write back
with open('index.html', 'w') as f:
    f.write(new_content)

print("Added fourth product card and updated schema.org")
print("Total product cards in grid:", new_content.count('class="product-card"'))
print("Schema products:", new_content.count('"@type": "Product"'))