import re

# Patch index.html
with open('/Applications/patuli_Stok_Takip/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

old_html = """                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                            <i data-lucide="image" class="w-4 h-4 text-stone-400"></i>
                        </div>
                        <input type="file" id="inventory-img-file" accept="image/*" onchange="previewInventoryImageFile(this)" class="w-full text-xs text-stone-500 border border-stone-300 rounded-xl bg-white p-2 pl-9 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-amber-100 file:text-amber-800 hover:file:bg-amber-200 cursor-pointer">
                    </div>"""

new_html = """                    <div class="flex flex-col gap-2">
                        <div class="relative">
                            <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                                <i data-lucide="link" class="w-4 h-4 text-stone-400"></i>
                            </div>
                            <input type="text" id="inventory-img-url-input" onchange="previewInventoryImageUrlInput(this.value)" class="w-full bg-stone-50 border border-stone-200 rounded-xl px-4 py-2.5 pl-9 text-sm font-medium text-stone-800 focus:outline-none focus:ring-2 focus:ring-amber-500" placeholder="Görsel URL'si yapıştırın (İsteğe bağlı)">
                        </div>
                        <div class="relative flex items-center justify-center">
                            <div class="border-t border-stone-200 flex-1"></div>
                            <span class="text-xs font-bold text-stone-400 px-3">VEYA</span>
                            <div class="border-t border-stone-200 flex-1"></div>
                        </div>
                        <div class="relative">
                            <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                                <i data-lucide="image" class="w-4 h-4 text-stone-400"></i>
                            </div>
                            <input type="file" id="inventory-img-file" accept="image/*" onchange="previewInventoryImageFile(this)" class="w-full text-xs text-stone-500 border border-stone-300 rounded-xl bg-white p-2 pl-9 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-amber-100 file:text-amber-800 hover:file:bg-amber-200 cursor-pointer">
                        </div>
                    </div>"""

html_content = html_content.replace(old_html, new_html)

with open('/Applications/patuli_Stok_Takip/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)


# Patch app_v4.js
with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Add previewInventoryImageUrlInput
new_js_funcs = """window.previewInventoryImageUrlInput = (val) => {
    document.getElementById('inventory-img-url').value = val;
    document.getElementById('inventory-img-file').value = '';
    window.previewInventoryImageUrl(val);
};

window.previewInventoryImageFile"""

js_content = js_content.replace("window.previewInventoryImageFile", new_js_funcs)

# Update previewInventoryImageFile to clear the URL input box
js_content = js_content.replace(
    "document.getElementById('inventory-img-url').value = e.target.result;",
    "document.getElementById('inventory-img-url').value = e.target.result;\n            document.getElementById('inventory-img-url-input').value = '';"
)

# Update removeInventoryImagePreview to clear the URL input box
js_content = js_content.replace(
    "document.getElementById('inventory-img-url').value = '';",
    "document.getElementById('inventory-img-url').value = '';\n    document.getElementById('inventory-img-url-input').value = '';"
)

# Update openInventoryModal to clear or set the URL input box correctly
# Right now it's: 
# document.getElementById('inventory-img-url').value = inv ? (inv.imgUrl || '') : '';
# window.previewInventoryImageUrl(inv ? (inv.imgUrl || '') : '');

old_open = """    document.getElementById('inventory-img-url').value = inv ? (inv.imgUrl || '') : '';
    window.previewInventoryImageUrl(inv ? (inv.imgUrl || '') : '');"""

new_open = """    const imgUrlStr = inv ? (inv.imgUrl || '') : '';
    document.getElementById('inventory-img-url').value = imgUrlStr;
    document.getElementById('inventory-img-url-input').value = imgUrlStr.startsWith('data:') ? '' : imgUrlStr;
    window.previewInventoryImageUrl(imgUrlStr);"""

js_content = js_content.replace(old_open, new_open)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
