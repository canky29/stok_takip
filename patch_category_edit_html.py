with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    html = f.read()

# Update the modal title and button to have IDs so we can change them
old_modal_title = '<h3 class="text-xl font-black text-stone-800 mb-4">Yeni Kategori Ekle</h3>'
new_modal_title = '<h3 id="new-category-modal-title" class="text-xl font-black text-stone-800 mb-4">Yeni Kategori Ekle</h3>'

old_kaydet_btn = '<button type="button" onclick="submitNewInvCategory()" class="flex-1 bg-amber-600 hover:bg-amber-700 text-white font-bold py-3 rounded-xl shadow-lg shadow-amber-600/20 transition">Kaydet</button>'
new_kaydet_btn = '<button type="button" id="new-category-submit-btn" onclick="submitNewInvCategory()" class="flex-1 bg-amber-600 hover:bg-amber-700 text-white font-bold py-3 rounded-xl shadow-lg shadow-amber-600/20 transition">Kaydet</button>'

html = html.replace(old_modal_title, new_modal_title)
html = html.replace(old_kaydet_btn, new_kaydet_btn)

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(html)
print("HTML patched for category editing.")
