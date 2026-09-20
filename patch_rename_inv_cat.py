with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

# Replace the specific definition at the top (which is for Inventory)
old_func_def = "window.submitNewCategory = () => {"
new_func_def = "window.submitNewInvCategory = () => {"

# Only replace the FIRST occurrence!
js = js.replace(old_func_def, new_func_def, 1)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)

with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    html = f.read()

html = html.replace('onclick="submitNewCategory()" class="flex-1 bg-amber-600', 'onclick="submitNewInvCategory()" class="flex-1 bg-amber-600')

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(html)

print("Renamed submitNewCategory to submitNewInvCategory for inventory.")
