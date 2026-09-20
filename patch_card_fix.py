with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    content = f.read()

bad_html = '''                        <span class="text-sm font-black text-emerald-600 flex items-center gap-1 group-hover:translate-x-1 transition">Tabloyu Aç <i data-lucide="arrow-right" class="w-4 h-4"></i></span>
                    </div>

                <!-- Reçete & Maliyet Aracı Card -->'''

good_html = '''                        <span class="text-sm font-black text-emerald-600 flex items-center gap-1 group-hover:translate-x-1 transition">Tabloyu Aç <i data-lucide="arrow-right" class="w-4 h-4"></i></span>
                    </div>
                </div>

                <!-- Reçete & Maliyet Aracı Card -->'''

content = content.replace(bad_html, good_html)

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(content)

print("Card nesting fixed.")
