import re

with open('index.html', 'r') as f:
    content = f.read()

# Add fourth product card after the third product card
# Find the closing div of the third product card and the grid closing div
# Pattern: product card ends with "            </div>" then blank lines then "        </div>" (grid close)
# We'll insert before the grid closing div

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

# Find position to insert: after the third product card's closing div, before grid closing div
# Look for pattern: product card closing div (12 spaces), then maybe blank lines, then grid closing div (8 spaces)
# We'll use a more specific marker: find the monitor product card by its unique URL
monitor_url = 'https://www.amazon.com/s?k=Dell+S2421HN+monitor'
idx = content.find(monitor_url)
if idx == -1:
    print("Monitor URL not found")
    exit(1)

# Find the closing div of that product card: search forward for "            </div>" after the monitor card
# Actually find the closing </div> of the product-card div (the one after the commission paragraph)
# Let's find the commission paragraph first
commission_text = 'We may earn a commission at no extra cost to you. Prices checked daily.'
idx_commission = content.find(commission_text, idx)
if idx_commission == -1:
    print("Commission text not found")
    exit(1)

# Find the next "            </div>" after this commission text (closes the inner div)
# Then find the next "            </div>" after that (closes product-card)
# Then insert before "        </div>" (grid close)
# Let's do a simpler approach: find the grid closing div after the monitor card
# Look for "        </div>" that appears after monitor card and before schema script
# Use regex: find "        </div>" preceded by product card content
# We'll just find the index of "        </div>" that follows the monitor card pattern

# Actually, let's find the section containing all product cards
# Look for '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">'
grid_start = content.find('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">')
if grid_start == -1:
    # fallback to old class
    grid_start = content.find('<div class="grid md:grid-cols-3 gap-8">')
    if grid_start == -1:
        print("Grid not found")
        exit(1)

# Find the closing div of this grid: look for "        </div>" at same indent level after grid_start
# Count nested divs? Simpler: find the next "        </div>" after grid_start that is at indent 8 spaces
# Let's get substring from grid_start
sub = content[grid_start:]
# Find first occurrence of "\n        </div>" (8 spaces)
import re
match = re.search(r'\n        </div>', sub)
if not match:
    print("Grid closing div not found")
    exit(1)
    
grid_end = grid_start + match.start()  # position of newline before closing div

# Now we need to insert before this closing div, but after the last product card
# Find the last product card closing div before grid_end
# Look for "            </div>" that appears before grid_end and after grid_start
# We'll insert after the last occurrence of "            </div>" before grid_end
last_product_close = content.rfind('            </div>', grid_start, grid_end)
if last_product_close == -1:
    print("Last product close not found")
    exit(1)

# Insert after that closing div (position after the closing tag)
insert_pos = last_product_close + len('            </div>')

# Insert new product card with proper spacing (blank line before)
# Ensure there's already blank lines after the previous product card
# We'll insert "\n\n" + new_product + "\n\n"
new_content = content[:insert_pos] + "\n\n" + new_product + "\n\n" + content[insert_pos:]

# Update schema.org JSON-LD
# Find the schema script and add fourth product
schema_start = new_content.find('"@graph": [')
if schema_start == -1:
    print("Schema graph not found")
    exit(1)

# Find the array of products: from '[' to ']' within the script
# We'll insert a new product object before the closing bracket of the array
# Find the closing bracket of the @graph array
bracket_start = new_content.find('[', schema_start)
bracket_end = new_content.find(']', bracket_start)
if bracket_start == -1 or bracket_end == -1:
    print("Schema array not found")
    exit(1)

# Get the array content
array_content = new_content[bracket_start:bracket_end+1]
# Find the last product object (ends with "}" before the closing "]")
# Insert a new product object before the closing bracket
# We'll add a comma after the third product, then new product
# Actually, we need to insert before the closing bracket, after the last product's closing brace
# Look for the third product's closing brace (after Dell monitor)
# We'll find the Dell monitor product by its URL
dell_url = 'https://www.amazon.com/s?k=Dell+S2421HN+monitor'
dell_idx = new_content.find(dell_url, schema_start)
if dell_idx == -1:
    print("Dell URL in schema not found")
    exit(1)

# Find the closing brace after this URL
brace_close = new_content.find('}', dell_idx)
if brace_close == -1:
    print("Closing brace not found")
    exit(1)

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
