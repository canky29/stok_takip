import re

with open('app_v4.js', 'r') as f:
    content = f.read()

new_render = """
window.renderProducts = () => {
    const container = document.getElementById('products-container');
    if(!container) return;
    
    const prods = JSON.parse(localStorage.getItem('products') || '[]');
    const allCats = JSON.parse(localStorage.getItem('categories') || '[]');
    container.innerHTML = '';
    
    // Group by category, but include all categories even if empty
    const grouped = {};
    allCats.forEach(c => grouped[c] = []);
    prods.forEach(p => {
        if(!grouped[p.category]) grouped[p.category] = [];
        grouped[p.category].push(p);
    });
    
    for(const [cat, items] of Object.entries(grouped)) {
        let catHtml = `
            <div class="mb-8">
                <h2 class="text-xl font-black text-stone-800 mb-4 pb-2 border-b-2 border-amber-600 inline-block uppercase tracking-wider">${cat}</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        `;
        
        if (items.length === 0) {
            catHtml += `<div class="col-span-full text-stone-500 font-bold bg-stone-100 p-4 rounded-xl border border-stone-200">Bu kategoride henüz ürün bulunmuyor.</div>`;
        } else {
            items.forEach(p => {
                const pct = Math.round((p.stock / (p.maxStock || 1)) * 100);
                const isZero = p.stock === 0;
                const isLow = p.stock < (p.maxStock * 0.2);
                
                catHtml += `
                <div class="bg-white rounded-3xl overflow-hidden shadow-lg border border-stone-200/60 hover:shadow-xl transition flex flex-col">
                    <div class="relative h-48 w-full group">
                        <img src="${p.image}" class="w-full h-full object-cover" />
                        <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
                        <div class="absolute top-3 left-3 right-3 flex justify-between">
                            ${isZero ? `<span class="bg-white text-rose-600 px-2 py-0.5 rounded text-[10px] font-black tracking-wider shadow">TÜKENDİ (%0)</span>` : '<div></div>'}
                            ${isLow && !isZero ? `<span class="bg-orange-500 text-white px-2 py-0.5 rounded text-[10px] font-black tracking-wider shadow flex items-center gap-1"><i data-lucide="flame" class="w-3 h-3"></i> Acil İmalatta</span>` : ''}
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
                            <div class="w-10 h-10 rounded-full border-4 ${isZero ? 'border-rose-100 text-rose-600' : (isLow ? 'border-orange-100 text-orange-500' : 'border-emerald-100 text-emerald-500')} flex items-center justify-center font-black text-[10px]">
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
        }
        
        catHtml += `</div></div>`;
        container.innerHTML += catHtml;
    }
    if(typeof lucide !== 'undefined') lucide.createIcons();
};
"""

content = re.sub(r'window\.renderProducts = \(\) => \{.*?(?=\nwindow\.setRole =)', new_render, content, flags=re.DOTALL)
with open('app_v4.js', 'w') as f:
    f.write(content)
