import re

with open('/Applications/patuli_Stok_Takip/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Add navigation button
old_nav = """                        <button id="btn-role-inventory" onclick="setRole('INVENTORY')" class="px-5 py-3 rounded-2xl font-black text-sm flex items-center gap-2.5 transition">
                            <i data-lucide="package-search" class="w-5 h-5"></i> Envanter Takibi
                        </button>"""

new_nav = old_nav + """
                        <button id="btn-role-finance" onclick="setRole('FINANCE')" class="px-5 py-3 rounded-2xl font-black text-sm flex items-center gap-2.5 transition">
                            <i data-lucide="calculator" class="w-5 h-5"></i> Maliyet & Kar
                        </button>"""

html_content = html_content.replace(old_nav, new_nav)

# Add view-finance container
old_view = """                <!-- Inventory List -->
                <div id="inventory-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 pb-24">
                    <!-- Cards injected by JS -->
                </div>
            </div>"""

new_view = old_view + """

            <!-- Maliyet ve Kar Görünümü -->
            <div id="view-finance" class="hidden animate-fade-in space-y-6">
                <!-- Header -->
                <div class="flex items-center gap-4 bg-white p-6 rounded-3xl shadow-sm border border-stone-200">
                    <div class="w-14 h-14 rounded-2xl bg-emerald-100 text-emerald-600 flex items-center justify-center shrink-0">
                        <i data-lucide="badge-dollar-sign" class="w-7 h-7"></i>
                    </div>
                    <div>
                        <h2 class="text-2xl font-black text-stone-800 tracking-tight">Maliyet & Kar Analizi</h2>
                        <p class="text-sm font-bold text-stone-400 mt-1">Ürünlerin maliyet ve satış fiyatlarını belirleyin, net kar/zarar durumunu anlık takip edin.</p>
                    </div>
                </div>

                <div class="bg-white rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-stone-200/60 overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="w-full text-left border-collapse min-w-[1000px]">
                            <thead>
                                <tr class="bg-stone-50 border-b border-stone-200/80">
                                    <th class="p-4 text-xs font-black text-stone-500 uppercase tracking-widest">Ürün</th>
                                    <th class="p-4 text-xs font-black text-stone-500 uppercase tracking-widest text-center">Üretim / Fire / Satış</th>
                                    <th class="p-4 text-xs font-black text-stone-500 uppercase tracking-widest w-32">Maliyet (₺)</th>
                                    <th class="p-4 text-xs font-black text-stone-500 uppercase tracking-widest w-32">Satış Fiyatı (₺)</th>
                                    <th class="p-4 text-xs font-black text-stone-500 uppercase tracking-widest text-right">Gelir</th>
                                    <th class="p-4 text-xs font-black text-stone-500 uppercase tracking-widest text-right">Fire Zararı</th>
                                    <th class="p-4 text-xs font-black text-stone-500 uppercase tracking-widest text-right">Net Kar / Zarar</th>
                                </tr>
                            </thead>
                            <tbody id="finance-tbody" class="divide-y divide-stone-100">
                                <!-- JS injecected -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>"""

html_content = html_content.replace(old_view, new_view)

with open('/Applications/patuli_Stok_Takip/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
