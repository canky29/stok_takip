import re

with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    html = f.read()

old_panel = """                    <!-- Toplam Maliyet & Kayıt -->
                    <div id="recipe-total-panel" class="hidden mt-4 pt-6 border-t border-stone-100 flex flex-col md:flex-row items-center justify-between gap-4">
                        <div>
                            <div class="text-sm font-bold text-stone-500">1 Birim (Adet/Porsiyon) İçin</div>
                            <div class="text-3xl font-black text-emerald-600">Toplam: <span id="recipe-total-cost">0.00 ₺</span></div>
                        </div>
                        <button onclick="saveRecipeCostToProduct()" class="bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-4 rounded-xl font-black shadow-lg shadow-emerald-500/30 transition active:scale-95 flex items-center gap-2">
                            <i data-lucide="save" class="w-5 h-5"></i> Yeni Maliyet Olarak Kaydet
                        </button>
                    </div>"""

new_panel = """                    <!-- Toplam Maliyet & Kayıt -->
                    <div id="recipe-total-panel" class="hidden mt-6 pt-6 border-t border-stone-200 flex flex-col md:flex-row items-center justify-between gap-6">
                        
                        <div class="flex items-center gap-6 w-full md:w-auto overflow-x-auto pb-2 md:pb-0">
                            <!-- Maliyet -->
                            <div>
                                <div class="text-xs font-black text-rose-400 uppercase tracking-wider mb-1">Birim Maliyeti</div>
                                <div class="text-3xl font-black text-rose-500 flex items-baseline gap-1"><span id="recipe-total-cost">0.00</span><span class="text-lg">₺</span></div>
                            </div>
                            
                            <div class="h-10 w-px bg-stone-200"></div>
                            
                            <!-- Satış Fiyatı -->
                            <div>
                                <div class="text-xs font-black text-emerald-500 uppercase tracking-wider mb-1">Satış Fiyatı</div>
                                <div class="relative">
                                    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-emerald-600/50 font-bold text-lg">₺</div>
                                    <input type="number" id="recipe-sell-price" step="0.5" min="0" oninput="calculateRecipeProfit()" class="w-32 bg-emerald-50/50 border border-emerald-200 hover:border-emerald-400 rounded-xl py-1.5 pl-8 pr-3 text-2xl font-black text-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition shadow-sm">
                                </div>
                            </div>

                            <div class="h-10 w-px bg-stone-200"></div>

                            <!-- Kar Marjı -->
                            <div>
                                <div class="text-xs font-black text-indigo-400 uppercase tracking-wider mb-1">Birim Başı Kar</div>
                                <div class="text-2xl font-black text-indigo-600 flex items-baseline gap-1"><span id="recipe-profit-amount">0.00</span><span class="text-sm">₺</span></div>
                                <div id="recipe-profit-percent" class="text-[10px] font-bold text-indigo-400 bg-indigo-50 px-1.5 py-0.5 rounded inline-block mt-0.5">%0 Kar Marjı</div>
                            </div>
                        </div>

                        <button onclick="saveRecipeCostToProduct()" class="w-full md:w-auto bg-stone-900 hover:bg-black text-white px-8 py-4 rounded-xl font-black shadow-lg shadow-black/20 transition active:scale-95 flex items-center justify-center gap-2 shrink-0">
                            <i data-lucide="save" class="w-5 h-5"></i> Fiyatları Kaydet
                        </button>
                    </div>"""

html = html.replace(old_panel, new_panel)

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(html)


with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

# Modify loadRecipeForSelectedProduct to populate the selling price input
old_load = """    const p = prods.find(x => String(x.id) === val);
    if(p) {
        document.getElementById('recipe-product-name').textContent = p.name;
        document.getElementById('recipe-product-old-cost').textContent = (parseFloat(p.costPrice) || 0).toFixed(2) + " ₺";
        document.getElementById('recipe-product-img').src = p.image || '';
    }"""

new_load = """    const p = prods.find(x => String(x.id) === val);
    if(p) {
        document.getElementById('recipe-product-name').textContent = p.name;
        document.getElementById('recipe-product-old-cost').textContent = (parseFloat(p.costPrice) || 0).toFixed(2) + " ₺";
        document.getElementById('recipe-product-img').src = p.image || '';
        document.getElementById('recipe-sell-price').value = p.sellPrice || '';
    }"""

js = js.replace(old_load, new_load)

# Modify renderRecipeIngredients to call calculateRecipeProfit
old_render_end = """    window.currentRecipeGrandTotal = grandTotal;
    
    if(typeof lucide !== 'undefined') lucide.createIcons();"""

new_render_end = """    window.currentRecipeGrandTotal = grandTotal;
    if(window.calculateRecipeProfit) window.calculateRecipeProfit();
    
    if(typeof lucide !== 'undefined') lucide.createIcons();"""

js = js.replace(old_render_end, new_render_end)

# Add calculateRecipeProfit and update saveRecipeCostToProduct
new_funcs = """window.calculateRecipeProfit = () => {
    const cost = window.currentRecipeGrandTotal || 0;
    const sellInput = document.getElementById('recipe-sell-price');
    const profitEl = document.getElementById('recipe-profit-amount');
    const percentEl = document.getElementById('recipe-profit-percent');
    
    let sell = parseFloat(sellInput.value);
    if(isNaN(sell)) sell = 0;
    
    let profit = sell - cost;
    profitEl.textContent = profit.toFixed(2);
    
    if(profit > 0) {
        profitEl.className = 'text-2xl font-black text-emerald-600 flex items-baseline gap-1';
        percentEl.className = 'text-[10px] font-bold text-emerald-600 bg-emerald-50 px-1.5 py-0.5 rounded inline-block mt-0.5';
    } else if(profit < 0) {
        profitEl.className = 'text-2xl font-black text-rose-600 flex items-baseline gap-1';
        percentEl.className = 'text-[10px] font-bold text-rose-600 bg-rose-50 px-1.5 py-0.5 rounded inline-block mt-0.5';
    } else {
        profitEl.className = 'text-2xl font-black text-stone-400 flex items-baseline gap-1';
        percentEl.className = 'text-[10px] font-bold text-stone-400 bg-stone-100 px-1.5 py-0.5 rounded inline-block mt-0.5';
    }
    
    if(cost > 0 && sell > 0) {
        let margin = (profit / sell) * 100;
        percentEl.textContent = `%${margin.toFixed(0)} Kar Marjı`;
    } else {
        percentEl.textContent = `%0 Kar Marjı`;
    }
};

window.saveRecipeCostToProduct = () => {
    if(!currentRecipeProductId) return;
    
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let p = prods.find(x => String(x.id) === currentRecipeProductId);
    if(p) {
        p.costPrice = window.currentRecipeGrandTotal;
        
        let sell = parseFloat(document.getElementById('recipe-sell-price').value);
        if(!isNaN(sell)) p.sellPrice = sell;
        
        localStorage.setItem('products', JSON.stringify(prods));
        document.getElementById('recipe-product-old-cost').textContent = p.costPrice.toFixed(2) + " ₺";
        
        if(window.renderFinance) window.renderFinance();
        
        alert(`${p.name} fiyatları başarıyla güncellendi!\\nMaliyet: ${p.costPrice.toFixed(2)} ₺ \\nSatış: ${p.sellPrice.toFixed(2)} ₺`);
    }
};
"""

js = re.sub(r'window\.saveRecipeCostToProduct\s*=\s*\(\)\s*=>\s*\{.*?\};\n', new_funcs, js, flags=re.DOTALL)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)

print("Selling price input added to Recipe calculator!")
