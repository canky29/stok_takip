import re

# 1. Update index.html to add URL input in Edit Product Modal
with open('index.html', 'r') as f:
    html = f.read()

url_input = """
                <div>
                    <label class="block text-sm font-bold text-stone-700 mb-1">Görsel Bağlantısı (URL)</label>
                    <input type="url" id="edit-prod-url" class="w-full border border-stone-300 rounded bg-white p-3 font-medium focus:border-amber-600 focus:outline-none" placeholder="Örn: https://example.com/image.jpg">
                </div>
"""

# Find where edit-prod-file is and insert after it
if 'id="edit-prod-url"' not in html:
    html = html.replace('<p class="text-[11px] text-stone-500 mt-1">Dosya seçmezseniz eski görsel kalır.</p>', '<p class="text-[11px] text-stone-500 mt-1">Dosya seçmezseniz eski görsel kalır.</p>\n</div>' + url_input)

with open('index.html', 'w') as f:
    f.write(html)

# 2. Update app_v4.js
with open('app_v4.js', 'r') as f:
    js = f.read()

# Add edit product functions
edit_funcs = """
window.openEditProductModal = (id) => {
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let p = prods.find(x => x.id === id);
    if(!p) return;
    
    document.getElementById('edit-prod-id').value = p.id;
    document.getElementById('edit-prod-existing-image').value = p.image || '';
    document.getElementById('edit-prod-name').value = p.name;
    document.getElementById('edit-prod-max').value = p.maxStock;
    document.getElementById('edit-prod-stock').value = p.stock;
    
    if(document.getElementById('edit-prod-url')) {
        document.getElementById('edit-prod-url').value = p.image && p.image.startsWith('http') ? p.image : '';
    }

    const catSelect = document.getElementById('edit-prod-category');
    if(catSelect) {
        catSelect.innerHTML = '';
        let cats = JSON.parse(localStorage.getItem('categories') || '[]');
        if(!cats.includes(p.category)) cats.push(p.category);
        cats.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            opt.textContent = c;
            if(c === p.category) opt.selected = true;
            catSelect.appendChild(opt);
        });
    }

    const unitSelect = document.getElementById('edit-prod-unit');
    if(unitSelect) unitSelect.value = p.unit;
    
    const el = document.getElementById('edit-product-modal');
    if(el) el.classList.remove('hidden');
};

window.closeEditModal = () => {
    const el = document.getElementById('edit-product-modal');
    if(el) el.classList.add('hidden');
};

window.submitEditProduct = (e) => {
    e.preventDefault();
    const id = parseInt(document.getElementById('edit-prod-id').value);
    const name = document.getElementById('edit-prod-name').value;
    const cat = document.getElementById('edit-prod-category').value;
    const unit = document.getElementById('edit-prod-unit').value;
    const max = parseInt(document.getElementById('edit-prod-max').value || 100);
    const stock = parseFloat(document.getElementById('edit-prod-stock').value || 0);
    const url = document.getElementById('edit-prod-url') ? document.getElementById('edit-prod-url').value : '';
    const existingImg = document.getElementById('edit-prod-existing-image').value;
    
    const finalImage = url || existingImg || 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500&auto=format&fit=crop&q=60';

    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let pIndex = prods.findIndex(x => x.id === id);
    if(pIndex > -1) {
        prods[pIndex].name = name;
        prods[pIndex].category = cat;
        prods[pIndex].unit = unit;
        prods[pIndex].maxStock = max;
        prods[pIndex].stock = stock;
        prods[pIndex].image = finalImage;
        localStorage.setItem('products', JSON.stringify(prods));
    }
    
    closeEditModal();
    renderProducts();
};

window.deleteProduct = (id) => {
    if(confirm('Bu ürünü silmek istediğinize emin misiniz?')) {
        let prods = JSON.parse(localStorage.getItem('products') || '[]');
        prods = prods.filter(x => x.id !== id);
        localStorage.setItem('products', JSON.stringify(prods));
        renderProducts();
    }
};

"""

js = js.replace('window.renderProducts = () => {', edit_funcs + '\nwindow.renderProducts = () => {')

# Modify renderProducts item generation
new_item_gen = """
            items.forEach(p => {
                const pct = Math.round((p.stock / (p.maxStock || 1)) * 100);
                const isZero = p.stock <= 0;
                const isLow = p.stock < (p.maxStock * 0.2);
                
                // Dynamic colors for the circle based on percentage
                let circleColor = 'border-emerald-100 text-emerald-500';
                if(pct <= 0) circleColor = 'border-rose-100 text-rose-600';
                else if(pct <= 20) circleColor = 'border-rose-300 text-rose-600';
                else if(pct <= 50) circleColor = 'border-orange-200 text-orange-500';
                else if(pct <= 75) circleColor = 'border-amber-200 text-amber-500';
                else circleColor = 'border-emerald-100 text-emerald-500';
                
                catHtml += `
                <div class="bg-white rounded-3xl overflow-hidden shadow-lg border border-stone-200/60 hover:shadow-xl transition flex flex-col relative group/card">
                    <div class="relative h-48 w-full group">
                        <img src="${p.image}" class="w-full h-full object-cover" />
                        <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
                        
                        <!-- Badges -->
                        <div class="absolute top-3 left-3 right-3 flex justify-between pointer-events-none">
                            ${isZero ? `<span class="bg-white text-rose-600 px-2 py-0.5 rounded text-[10px] font-black tracking-wider shadow">TÜKENDİ (%0)</span>` : '<div></div>'}
                            ${isLow && !isZero ? `<span class="bg-orange-500 text-white px-2 py-0.5 rounded text-[10px] font-black tracking-wider shadow flex items-center gap-1"><i data-lucide="flame" class="w-3 h-3"></i> Acil İmalatta</span>` : ''}
                        </div>
                        
                        <!-- Product Edit/Delete Actions (shown on hover) -->
                        <div class="absolute top-2 right-2 flex gap-1 opacity-0 group-hover/card:opacity-100 transition-opacity">
                            <button onclick="openEditProductModal(${p.id})" class="p-2 bg-white/90 hover:bg-white text-stone-700 rounded-lg shadow transition" title="Ürünü Düzenle">
                                <i data-lucide="pencil" class="w-4 h-4"></i>
                            </button>
                            <button onclick="deleteProduct(${p.id})" class="p-2 bg-rose-500/90 hover:bg-rose-600 text-white rounded-lg shadow transition" title="Ürünü Sil">
                                <i data-lucide="trash-2" class="w-4 h-4"></i>
                            </button>
                        </div>
                        
                        <h3 class="absolute bottom-3 left-4 text-white font-black text-lg truncate pr-4">${p.name}</h3>
                    </div>
                    
                    <div class="p-4 flex flex-col gap-4">
                        <div class="flex justify-between items-center">
                            <div class="flex flex-col">
                                <span class="text-[10px] text-stone-400 font-extrabold uppercase mb-1">STOK (${p.unit.toUpperCase()})</span>
                                <div class="flex items-center gap-2 bg-stone-50 border border-stone-200 rounded-xl p-1 w-fit">
                                    <button onclick="updateProduct(${p.id}, 'stock', -1)" class="w-7 h-7 rounded-lg hover:bg-stone-200 font-bold text-stone-600 flex items-center justify-center">-</button>
                                    <span class="text-sm font-black text-stone-800 min-w-[3rem] text-center">${p.stock} ${p.unit}</span>
                                    <button onclick="updateProduct(${p.id}, 'stock', 1)" class="w-7 h-7 rounded-lg hover:bg-stone-200 font-bold text-stone-600 flex items-center justify-center">+</button>
                                </div>
                            </div>
                            <div class="w-10 h-10 rounded-full border-4 ${circleColor} flex items-center justify-center font-black text-[10px]">
                                %${pct}
                            </div>
                        </div>
                        <div class="flex gap-2">
                            <div class="flex-1 border border-stone-200 rounded-xl p-1.5 flex justify-between items-center bg-stone-50">
                                <span class="text-[10px] font-bold text-stone-500">Satış:</span>
                                <div class="flex items-center gap-1">
                                    <button onclick="updateProduct(${p.id}, 'sales', -1)" class="w-5 h-5 bg-stone-200 rounded text-[10px] font-bold hover:bg-stone-300">-</button>
                                    <span class="text-xs font-black min-w-[1rem] text-center text-emerald-700">${p.sales}</span>
                                    <button onclick="updateProduct(${p.id}, 'sales', 1)" class="w-5 h-5 bg-emerald-600 text-white rounded text-[10px] font-bold hover:bg-emerald-700">+</button>
                                </div>
                            </div>
                            <div class="flex-1 border border-stone-200 rounded-xl p-1.5 flex justify-between items-center bg-stone-50">
                                <span class="text-[10px] font-bold text-stone-500">Fire:</span>
                                <div class="flex items-center gap-1">
                                    <button onclick="updateProduct(${p.id}, 'waste', -1)" class="w-5 h-5 bg-stone-200 rounded text-[10px] font-bold hover:bg-stone-300">-</button>
                                    <span class="text-xs font-black min-w-[1rem] text-center text-rose-700">${p.waste}</span>
                                    <button onclick="updateProduct(${p.id}, 'waste', 1)" class="w-5 h-5 bg-rose-600 text-white rounded text-[10px] font-bold hover:bg-rose-700">+</button>
                                </div>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-2 mt-2">
                            <button onclick="quickSell(${p.id})" class="bg-stone-900 text-white py-2.5 rounded-xl text-[11px] font-black flex items-center justify-center gap-1.5 hover:bg-stone-800 active:scale-95 transition">
                                <i data-lucide="shopping-cart" class="w-3.5 h-3.5"></i> Satış (-1)
                            </button>
                            <button onclick="requestOrder('${p.name}')" class="bg-amber-50 text-amber-700 border border-amber-200 py-2.5 rounded-xl text-[11px] font-black flex items-center justify-center gap-1.5 hover:bg-amber-100 active:scale-95 transition">
                                <i data-lucide="bell-ring" class="w-3.5 h-3.5"></i> İste
                            </button>
                        </div>
                    </div>
                </div>
                `;
            });
"""

# Replace the inner forEach loop in app_v4.js
js = re.sub(r'items\.forEach\(p => \{.*?<\/div>\n                `;\n            \}\);', new_item_gen, js, flags=re.DOTALL)

with open('app_v4.js', 'w') as f:
    f.write(js)
