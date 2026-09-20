import re

with open('app_v4.js', 'r') as f:
    js = f.read()

# 1. Dashboard function and filters
dash_code = """
window.updateDashboard = () => {
    const prods = JSON.parse(localStorage.getItem('products') || '[]');
    const cats = JSON.parse(localStorage.getItem('categories') || '[]');
    const orders = JSON.parse(localStorage.getItem('orders') || '[]');
    
    let criticalCount = 0;
    prods.forEach(p => {
        const pct = Math.min(100, Math.round((p.stock / (p.maxStock || 1)) * 100));
        if(pct <= 20) criticalCount++;
    });
    
    const e1 = document.getElementById('stat-total-products'); if(e1) e1.textContent = prods.length;
    const e2 = document.getElementById('stat-total-categories'); if(e2) e2.textContent = cats.length;
    const e3 = document.getElementById('stat-critical-products'); if(e3) e3.textContent = criticalCount;
    const e4 = document.getElementById('stat-urgent-requests'); if(e4) e4.textContent = orders.length;
};

let currentFilter = 'ALL';
window.setStockFilter = (filter) => {
    currentFilter = filter;
    renderProducts();
};

window.toggleCategory = (id) => {
    const el = document.getElementById(id);
    const icon = document.getElementById(id + '-icon');
    if(el) {
        el.classList.toggle('hidden');
        if(icon) icon.classList.toggle('-rotate-90');
    }
};

window.expandAllCategories = () => {
    document.querySelectorAll('.category-grid-container').forEach(el => el.classList.remove('hidden'));
    document.querySelectorAll('.category-toggle-icon').forEach(icon => icon.classList.remove('-rotate-90'));
};

window.collapseAllCategories = () => {
    document.querySelectorAll('.category-grid-container').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.category-toggle-icon').forEach(icon => icon.classList.add('-rotate-90'));
};

"""
js = dash_code + js

# 2. Modify renderProducts to use currentFilter and add Collapsible UI
new_renderProducts = """
window.renderProducts = () => {
    const container = document.getElementById('products-container');
    if(!container) return;
    
    let allProds = JSON.parse(localStorage.getItem('products') || '[]');
    const allCats = JSON.parse(localStorage.getItem('categories') || '[]');
    
    // Filter logic
    let prods = allProds;
    if(currentFilter === 'CRITICAL') {
        prods = allProds.filter(p => {
            const pct = Math.min(100, Math.round((p.stock / (p.maxStock || 1)) * 100));
            return pct <= 20;
        });
    } else if(currentFilter === 'EMPTY') {
        prods = allProds.filter(p => p.stock <= 0);
    } else if(currentFilter === 'NORMAL') {
        prods = allProds.filter(p => {
            const pct = Math.min(100, Math.round((p.stock / (p.maxStock || 1)) * 100));
            return pct > 20;
        });
    }

    container.innerHTML = '';
    
    // Group by category, but include all categories even if empty
    const grouped = {};
    allCats.forEach(c => grouped[c] = []);
    prods.forEach(p => {
        if(!grouped[p.category]) grouped[p.category] = [];
        grouped[p.category].push(p);
    });
    
    for(const [cat, items] of Object.entries(grouped)) {
        let catId = 'cat-grid-' + cat.replace(/[^a-zA-Z0-9]/g, '-').toLowerCase();
        let catHtml = `
            <div class="mb-8 relative group">
                <div class="flex items-center gap-3 mb-4 border-b-2 border-amber-600 pb-2 w-max">
                    <button onclick="toggleCategory('${catId}')" class="p-1 hover:bg-stone-200 rounded-lg transition text-stone-500">
                        <i data-lucide="chevron-down" id="${catId}-icon" class="w-5 h-5 transition-transform duration-300 category-toggle-icon"></i>
                    </button>
                    <h2 class="text-xl font-black text-stone-800 uppercase tracking-wider cursor-pointer" onclick="toggleCategory('${catId}')">${cat}</h2>
                    <div class="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1 ml-2">
                        <button onclick="editCategory('${cat}')" class="p-1.5 bg-stone-100 hover:bg-stone-200 text-stone-600 rounded-lg transition" title="Kategoriyi Düzenle">
                            <i data-lucide="pencil" class="w-4 h-4"></i>
                        </button>
                        <button onclick="deleteCategory('${cat}')" class="p-1.5 bg-rose-50 hover:bg-rose-100 text-rose-600 rounded-lg transition" title="Kategoriyi Sil">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                </div>
                <div id="${catId}" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 category-grid-container">
        `;
        
        if (items.length === 0) {
            catHtml += `<div class="col-span-full text-stone-500 font-bold bg-stone-100 p-4 rounded-xl border border-stone-200">Bu kategoride kritere uygun ürün bulunmuyor.</div>`;
        } else {
            items.forEach(p => {
                const pct = Math.min(100, Math.round((p.stock / (p.maxStock || 1)) * 100));
                const isZero = p.stock <= 0;
                const isLow = p.stock < (p.maxStock * 0.2);
                
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
                        
                        <div class="absolute top-3 left-3 right-3 flex justify-between pointer-events-none">
                            ${isZero ? `<span class="bg-white text-rose-600 px-2 py-0.5 rounded text-[10px] font-black tracking-wider shadow">TÜKENDİ (%0)</span>` : '<div></div>'}
                            ${isLow && !isZero ? `<span class="bg-orange-500 text-white px-2 py-0.5 rounded text-[10px] font-black tracking-wider shadow flex items-center gap-1"><i data-lucide="flame" class="w-3 h-3"></i> Acil İmalatta</span>` : ''}
                        </div>
                        
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
                            <button onclick="requestOrder(${p.id})" class="bg-amber-50 text-amber-700 border border-amber-200 py-2.5 rounded-xl text-[11px] font-black flex items-center justify-center gap-1.5 hover:bg-amber-100 active:scale-95 transition">
                                <i data-lucide="bell-ring" class="w-3.5 h-3.5"></i> İste
                            </button>
                        </div>
                    </div>
                </div>
                `;
            });
        }
        
        catHtml += `</div></div>`;
        container.innerHTML += catHtml;
    }
    updateDashboard();
    if(typeof lucide !== 'undefined') lucide.createIcons();
};
"""

js = re.sub(r'window\.renderProducts = \(\) => \{.*?updateDashboard\(\);\n    if\(typeof lucide !== \'undefined\'\) lucide\.createIcons\(\);\n\};\n?', new_renderProducts, js, flags=re.DOTALL)
if 'window.renderProducts = () =>' not in js:
    # If the first replace failed, try simpler replacement
    js = re.sub(r'window\.renderProducts = \(\) => \{.*?(?=\nwindow\.setRole =)', new_renderProducts, js, flags=re.DOTALL)

# Let's ensure updateDashboard is called in renderOrders too
js = js.replace('renderOrders = () => {', 'renderOrders = () => {\n    updateDashboard();')

with open('app_v4.js', 'w') as f:
    f.write(js)
