import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Add image preview logic
img_preview_js = """
window.previewInventoryImageFile = (input) => {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('inventory-img-preview').src = e.target.result;
            document.getElementById('inventory-img-preview-box').classList.remove('hidden');
            document.getElementById('inventory-img-url').value = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
};

window.previewInventoryImageUrl = (val) => {
    if(val && val.trim() !== '') {
        document.getElementById('inventory-img-preview').src = val;
        document.getElementById('inventory-img-preview-box').classList.remove('hidden');
    } else {
        window.removeInventoryImagePreview();
    }
};

window.removeInventoryImagePreview = () => {
    document.getElementById('inventory-img-preview').src = '';
    document.getElementById('inventory-img-preview-box').classList.add('hidden');
    document.getElementById('inventory-img-file').value = '';
    document.getElementById('inventory-img-url').value = '';
};
"""

js_content = js_content.replace(
    "window.openInventoryModal = (id = null) => {",
    img_preview_js + "\nwindow.openInventoryModal = (id = null) => {"
)

# Open Modal: Populate image URL
js_content = js_content.replace(
    "document.getElementById('inventory-modal-title').textContent = inv ? 'Envanter Ürünü Düzenle' : 'Yeni Ürün Ekle';",
    "document.getElementById('inventory-modal-title').textContent = inv ? 'Envanter Ürünü Düzenle' : 'Yeni Ürün Ekle';\n    document.getElementById('inventory-img-url').value = inv ? (inv.imgUrl || '') : '';\n    window.previewInventoryImageUrl(inv ? (inv.imgUrl || '') : '');"
)

# Submit Modal: Get image URL
js_content = js_content.replace(
    "const notes = document.getElementById('inventory-notes').value;",
    "const notes = document.getElementById('inventory-notes').value;\n    const imgUrl = document.getElementById('inventory-img-url').value;"
)

# Save image URL
js_content = js_content.replace(
    "inventory[index] = { ...inventory[index], name, amount, unit, critical, notes, lastUpdated: new Date().toISOString() };",
    "inventory[index] = { ...inventory[index], name, amount, unit, critical, notes, imgUrl, lastUpdated: new Date().toISOString() };"
)

js_content = js_content.replace(
    """            critical,
            notes,""",
    """            critical,
            notes,
            imgUrl,"""
)

# Update renderInventory html
old_html_block = """        html += `
        <div class="bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] border ${cardBorderClass} flex flex-col relative overflow-hidden transition duration-300 p-6 gap-5">
            ${criticalBadge}
            <div class="flex items-start justify-between relative z-10">
                <div class="pr-8">
                    <h3 class="text-xl font-black text-stone-800 tracking-tight leading-none mb-2">${r.name}</h3>
                    <div class="text-xs font-bold text-stone-400 flex items-center gap-1"><i data-lucide="clock" class="w-3.5 h-3.5"></i> Son G. ${dateStr}</div>
                </div>"""

new_html_block = """        let imgHtml = '';
        if (r.imgUrl) {
            imgHtml = `<div class="-mx-6 -mt-6 mb-4 h-40 bg-stone-100 overflow-hidden relative">
                <img src="${r.imgUrl}" class="w-full h-full object-cover" alt="${r.name}">
                <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
            </div>`;
        }

        html += `
        <div class="bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] border ${cardBorderClass} flex flex-col relative overflow-hidden transition duration-300 p-6 gap-5">
            ${criticalBadge}
            ${imgHtml}
            <div class="flex items-start justify-between relative z-10 ${r.imgUrl ? '-mt-10 text-white' : ''}">
                <div class="pr-8 drop-shadow-md">
                    <h3 class="text-xl font-black ${r.imgUrl ? 'text-white' : 'text-stone-800'} tracking-tight leading-none mb-2">${r.name}</h3>
                    <div class="text-xs font-bold ${r.imgUrl ? 'text-stone-200' : 'text-stone-400'} flex items-center gap-1"><i data-lucide="clock" class="w-3.5 h-3.5"></i> Son G. ${dateStr}</div>
                </div>"""

js_content = js_content.replace(old_html_block, new_html_block)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
