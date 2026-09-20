import re

with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    html = f.read()

# Replace header buttons
old_header_buttons = """                <div class="relative w-full md:w-96">
                    <i data-lucide="search" class="w-4 h-4 text-stone-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
                    <input type="text" id="inventory-search" oninput="renderInventory()" placeholder="Envanterde ürün ara..." class="w-full pl-10 pr-4 py-3 bg-stone-50 border border-stone-200 rounded-xl text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-amber-500">
                </div>
                <button onclick="openInventoryModal()" class="w-full md:w-auto bg-amber-600 hover:bg-amber-700 text-white font-black py-3 px-6 rounded-xl shadow-lg shadow-amber-600/20 transition active:scale-95 flex items-center justify-center gap-2">
                    <i data-lucide="plus" class="w-5 h-5"></i> Yeni Ürün Ekle
                </button>"""

new_header_buttons = """                <div class="relative w-full md:w-96">
                    <i data-lucide="search" class="w-4 h-4 text-stone-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
                    <input type="text" id="inventory-search" oninput="renderInventory()" placeholder="Envanterde ürün ara..." class="w-full pl-10 pr-4 py-3 bg-stone-50 border border-stone-200 rounded-xl text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-amber-500">
                </div>
                <div class="flex flex-col md:flex-row gap-3 w-full md:w-auto">
                    <button onclick="addNewInvCategory()" class="w-full md:w-auto bg-stone-100 hover:bg-stone-200 text-stone-700 font-black py-3 px-6 rounded-xl border border-stone-200 transition active:scale-95 flex items-center justify-center gap-2">
                        <i data-lucide="folder-plus" class="w-5 h-5"></i> Yeni Kategori
                    </button>
                    <button onclick="openInventoryModal()" class="w-full md:w-auto bg-amber-600 hover:bg-amber-700 text-white font-black py-3 px-6 rounded-xl shadow-lg shadow-amber-600/20 transition active:scale-95 flex items-center justify-center gap-2">
                        <i data-lucide="plus" class="w-5 h-5"></i> Yeni Ürün Ekle
                    </button>
                </div>"""

html = html.replace(old_header_buttons, new_header_buttons)

# Remove the small inline link
old_inline = """                <div>
                    <div class="flex justify-between items-center mb-1.5">
                        <label class="block text-xs font-black text-stone-500 uppercase tracking-widest">Kategori</label>
                        <button type="button" onclick="addNewInvCategory()" class="text-[10px] font-bold text-amber-600 hover:text-amber-700 uppercase tracking-widest">+ Yeni Ekle</button>
                    </div>"""

new_inline = """                <div>
                    <div class="flex justify-between items-center mb-1.5">
                        <label class="block text-xs font-black text-stone-500 uppercase tracking-widest">Kategori</label>
                    </div>"""

html = html.replace(old_inline, new_inline)

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(html)

print("Button moved to header.")
