with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    html = f.read()

old_button = """            <button onclick="resetData()" class="shrink-0 px-3.5 py-2 text-xs font-black rounded-xl transition bg-stone-800 text-stone-300 hover:bg-red-900/60 hover:text-white border border-stone-700/60 flex items-center gap-1.5 shadow-sm" title="Tüm Ayarları Sıfırla ve Varsayılan Menüyü Yükle">
                <i data-lucide="rotate-ccw" class="w-4 h-4 text-amber-500"></i> Ayarları Sıfırla
            </button>"""

new_buttons = """            <button onclick="saveAllSettings()" class="shrink-0 px-3.5 py-2 text-xs font-black rounded-xl transition bg-stone-800 text-emerald-400 hover:bg-emerald-900/60 hover:text-emerald-300 border border-stone-700/60 flex items-center gap-1.5 shadow-sm" title="Tüm Sistemi Kaydet / Yedekle">
                <i data-lucide="save" class="w-4 h-4"></i> Sistemi Kaydet
            </button>
            <button onclick="resetData()" class="shrink-0 px-3.5 py-2 text-xs font-black rounded-xl transition bg-stone-800 text-stone-300 hover:bg-red-900/60 hover:text-white border border-stone-700/60 flex items-center gap-1.5 shadow-sm" title="En Son Kaydedilen Duruma Geri Dön">
                <i data-lucide="rotate-ccw" class="w-4 h-4 text-amber-500"></i> Ayarları Sıfırla
            </button>"""

html = html.replace(old_button, new_buttons)

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(html)
    
print("Added save button to HTML.")
