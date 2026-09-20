import re

with open('/Applications/patuli_Stok_Takip/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Add image upload to the inventory modal
image_upload_html = """
                <div>
                    <label class="block text-xs font-black text-stone-500 uppercase tracking-widest mb-1.5">Ürün Görseli</label>
                    <input type="hidden" id="inventory-img-url" value="">
                    
                    <div id="inventory-img-preview-box" class="hidden mb-3 relative rounded-xl overflow-hidden border border-stone-200">
                        <img id="inventory-img-preview" src="" alt="Önizleme" class="w-full h-40 object-cover">
                        <button type="button" onclick="removeInventoryImagePreview()" class="absolute top-2 right-2 bg-stone-900/60 hover:bg-rose-600 text-white p-1.5 rounded-lg transition backdrop-blur-sm">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                    
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                            <i data-lucide="image" class="w-4 h-4 text-stone-400"></i>
                        </div>
                        <input type="file" id="inventory-img-file" accept="image/*" onchange="previewInventoryImageFile(this)" class="w-full text-xs text-stone-500 border border-stone-300 rounded-xl bg-white p-2 pl-9 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-amber-100 file:text-amber-800 hover:file:bg-amber-200 cursor-pointer">
                    </div>
                </div>
"""

# Insert image_upload_html before the Notlar / Açıklama div
html_content = html_content.replace(
    """                <div>
                    <label class="block text-xs font-black text-stone-500 uppercase tracking-widest mb-1.5">Notlar / Açıklama</label>""",
    image_upload_html + "\n" + """                <div>
                    <label class="block text-xs font-black text-stone-500 uppercase tracking-widest mb-1.5">Notlar / Açıklama</label>"""
)

with open('/Applications/patuli_Stok_Takip/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
