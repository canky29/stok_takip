import re

with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    content = f.read()

recipe_card = """
                <!-- Reçete & Maliyet Aracı Card -->
                <div onclick="setRole('RECIPE')" class="group bg-white p-7 rounded-3xl border border-stone-200/80 shadow-md hover:shadow-2xl hover:border-indigo-500/50 transition-all duration-300 cursor-pointer flex flex-col justify-between">
                    <div>
                        <div class="w-14 h-14 rounded-2xl bg-indigo-100 text-indigo-700 flex items-center justify-center font-black mb-5 group-hover:bg-indigo-600 group-hover:text-white transition duration-300 shadow-sm">
                            <i data-lucide="flask-conical" class="w-7 h-7"></i>
                        </div>
                        <h3 class="text-2xl font-black text-stone-900 mb-2 group-hover:text-indigo-600 transition">Reçete Hesaplama</h3>
                        <p class="text-stone-500 text-sm font-medium leading-relaxed">
                            Ürün reçetelerini hazırlayın, kullanılan hammaddelere göre toplam maliyeti kuruşu kuruşuna çıkarıp kaydedin.
                        </p>
                    </div>
                    <div class="mt-8 pt-5 border-t border-stone-100 flex items-center justify-between">
                        <span class="text-xs font-black bg-indigo-50 text-indigo-800 px-3 py-1.5 rounded-xl border border-indigo-200 flex items-center gap-1.5">
                            <i data-lucide="calculator" class="w-3.5 h-3.5 text-indigo-600"></i> Yeni Maliyet Çıkar
                        </span>
                        <span class="text-sm font-black text-indigo-600 flex items-center gap-1 group-hover:translate-x-1 transition">Aracı Aç <i data-lucide="arrow-right" class="w-4 h-4"></i></span>
                    </div>
                </div>
            </div>
"""

# The grid ends with "</div>\n\n            <!-- CATEGORY HIGHLIGHTS / GALLERY GRID -->"
# Wait, let's just find the exact </div> of the grid and replace it
pattern = re.compile(r'                </div>\n            </div>\n\n            <!-- CATEGORY HIGHLIGHTS', re.DOTALL)
content = pattern.sub(recipe_card + "\n\n            <!-- CATEGORY HIGHLIGHTS", content)

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(content)

print("Card added.")
