import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    content = f.read()

reset_function = """window.resetFinanceStats = () => {
    if(!confirm('Tüm ürünlerin satış, fire ve geçmiş analiz verileri sıfırlanacak! Sadece şu anki güncel stok miktarları kalacak. Devam etmek istiyor musunuz?')) return;
    
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    prods.forEach(p => {
        p.sales = 0;
        p.waste = 0;
        p.history = {};
        p.totalEntered = p.stock || 0; // The only "produced" amount is now whatever is currently in stock
    });
    
    localStorage.setItem('products', JSON.stringify(prods));
    if (window.renderFinance) window.renderFinance();
    if (window.renderProducts) window.renderProducts();
    if (window.updateGlobalStats) window.updateGlobalStats();
    alert('Test verileri başarıyla sıfırlandı. Tüm istatistikler ve kar/zarar durumları baştan başlayacak.');
};"""

# Append the function if not exists
if "window.resetFinanceStats" not in content:
    content += "\n" + reset_function

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(content)

with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    html_content = f.read()

# Add button to the finance header
old_html = """<button onclick="expandAllFinanceCategories()" class="px-4 py-2 bg-stone-100 text-stone-600 font-bold text-sm rounded-xl hover:bg-stone-200 transition">Tümünü Aç</button>"""
new_html = """<button onclick="resetFinanceStats()" class="px-4 py-2 bg-rose-100 text-rose-600 font-bold text-sm rounded-xl hover:bg-rose-200 transition border border-rose-200 mr-2">Verileri Sıfırla</button>
                    <button onclick="expandAllFinanceCategories()" class="px-4 py-2 bg-stone-100 text-stone-600 font-bold text-sm rounded-xl hover:bg-stone-200 transition">Tümünü Aç</button>"""

if "resetFinanceStats()" not in html_content:
    html_content = html_content.replace(old_html, new_html)

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(html_content)

print("Reset button added!")
