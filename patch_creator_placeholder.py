with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    html = f.read()

old_input = '<input type="text" id="cust-creator" required class="w-full border border-stone-300 rounded-xl bg-white p-3 text-sm font-bold text-stone-800 focus:border-amber-600 focus:outline-none" placeholder="Örn: Ayşe">'
new_input = '<input type="text" id="cust-creator" required class="w-full border border-stone-300 rounded-xl bg-white p-3 text-sm font-bold text-stone-800 focus:border-amber-600 focus:outline-none" placeholder="Örn: Hamide">'

html = html.replace(old_input, new_input)

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(html)
    
print("Updated placeholder to Hamide.")
