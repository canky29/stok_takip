with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    html = f.read()

old_container = '<div id="inventory-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-2">'
new_container = '<div id="inventory-container" class="flex flex-col gap-8 mt-2">'

html = html.replace(old_container, new_container)

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(html)

print("HTML fixed.")
