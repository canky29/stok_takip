with open('index.html', 'r') as f:
    html = f.read()

bad_html = """                    <p class="text-[11px] text-stone-500 mt-1">Dosya seçmezseniz eski görsel kalır.</p>
</div>
                <div>
                    <label class="block text-sm font-bold text-stone-700 mb-1">Görsel Bağlantısı (URL)</label>"""

good_html = """                    <p class="text-[11px] text-stone-500 mt-1">Dosya seçmezseniz eski görsel kalır.</p>
                </div>
                <div>
                    <label class="block text-sm font-bold text-stone-700 mb-1">Görsel Bağlantısı (URL)</label>"""

if bad_html in html:
    html = html.replace(bad_html, good_html)

# Also check for double </div>
double_div = """                </div>

                </div>
                
                <div>
                    <label class="block text-sm font-bold text-stone-700 mb-1">Ürün Adı</label>"""

fixed_double_div = """                </div>
                
                <div>
                    <label class="block text-sm font-bold text-stone-700 mb-1">Ürün Adı</label>"""

if double_div in html:
    html = html.replace(double_div, fixed_double_div)

with open('index.html', 'w') as f:
    f.write(html)
