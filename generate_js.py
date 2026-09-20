import json

js_content = """
document.addEventListener('DOMContentLoaded', () => {
    if (typeof lucide !== 'undefined') lucide.createIcons();
    initData();
    renderCategoriesSelect();
    renderProducts();
});

// Modal Helpers
window.openModal = (id) => { const el = document.getElementById(id); if(el) el.classList.remove('hidden'); };
window.closeModal = (id) => { const el = document.getElementById(id); if(el) el.classList.add('hidden'); };

window.openAddCategoryModal = () => openModal('add-category-modal');
window.closeAddCategoryModal = () => closeModal('add-category-modal');
window.openAddProductModal = () => openModal('add-product-modal');
window.closeAddProductModal = () => closeModal('add-product-modal');

// Init Data
function initData() {
    if(!localStorage.getItem('products')) localStorage.setItem('products', JSON.stringify([]));
    if(!localStorage.getItem('categories')) localStorage.setItem('categories', JSON.stringify(['Ekmek Çeşitleri', 'Pastalar']));
}

function renderCategoriesSelect() {
    const cats = JSON.parse(localStorage.getItem('categories') || '[]');
    const select = document.getElementById('new-prod-category');
    if(select) {
        select.innerHTML = '';
        cats.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            opt.textContent = c;
            select.appendChild(opt);
        });
    }
}

// Submits
window.submitNewCategory = (e) => {
    e.preventDefault();
    const name = document.getElementById('new-category-name').value;
    let cats = JSON.parse(localStorage.getItem('categories') || '[]');
    if(!cats.includes(name)) {
        cats.push(name);
        localStorage.setItem('categories', JSON.stringify(cats));
    }
    renderCategoriesSelect();
    closeModal('add-category-modal');
    e.target.reset();
};

window.submitNewProduct = (e) => {
    e.preventDefault();
    const name = document.getElementById('new-prod-name').value;
    const cat = document.getElementById('new-prod-category').value;
    const unit = document.getElementById('new-prod-unit') ? document.getElementById('new-prod-unit').value : 'Adet';
    const max = parseInt(document.getElementById('new-prod-max').value || 100);
    const stock = parseInt(document.getElementById('new-prod-stock').value || 0);
    const url = document.getElementById('new-prod-url').value;
    
    // Simple placeholder if no image
    const image = url || 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500&auto=format&fit=crop&q=60';

    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    prods.push({
        id: Date.now(),
        name, category: cat, unit, maxStock: max, stock, sales: 0, waste: 0, image
    });
    localStorage.setItem('products', JSON.stringify(prods));
    
    closeModal('add-product-modal');
    e.target.reset();
    renderProducts();
};

// Update functions
window.updateProduct = (id, field, delta) => {
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let p = prods.find(x => x.id === id);
    if(p) {
        if(field === 'stock') {
            if(p.stock + delta >= 0) p.stock += delta;
        } else if(field === 'sales') {
            if(delta > 0 && p.stock >= 1) { p.sales += 1; p.stock -= 1; }
            else if(delta < 0 && p.sales >= 1) { p.sales -= 1; p.stock += 1; }
        } else if(field === 'waste') {
            if(delta > 0 && p.stock >= 1) { p.waste += 1; p.stock -= 1; }
            else if(delta < 0 && p.waste >= 1) { p.waste -= 1; p.stock += 1; }
        }
        localStorage.setItem('products', JSON.stringify(prods));
        renderProducts();
    }
};

window.quickSell = (id) => {
    updateProduct(id, 'sales', 1);
};

window.requestOrder = (name) => {
    alert(name + ' için imalathaneye üretim isteği gönderildi!');
};

window.resetAllSales = () => {
    if(confirm('Tüm satışları sıfırlamak istediğinize emin misiniz?')) {
        let prods = JSON.parse(localStorage.getItem('products') || '[]');
        prods.forEach(p => p.sales = 0);
        localStorage.setItem('products', JSON.stringify(prods));
        renderProducts();
    }
};

window.resetAllWaste = () => {
    if(confirm('Tüm fireleri sıfırlamak istediğinize emin misiniz?')) {
        let prods = JSON.parse(localStorage.getItem('products') || '[]');
        prods.forEach(p => p.waste = 0);
        localStorage.setItem('products', JSON.stringify(prods));
        renderProducts();
    }
};

window.resetData = () => {
    if(confirm('Ayarları sıfırlamak istediğinize emin misiniz?')) {
        localStorage.clear();
        location.reload();
    }
};

window.saveAllSettings = () => alert('Kaydedildi!');

// Rendering
window.renderProducts = () => {
    const container = document.getElementById('products-container');
    if(!container) return;
    
    const prods = JSON.parse(localStorage.getItem('products') || '[]');
    container.innerHTML = '';
    
    // Group by category
    const grouped = prods.reduce((acc, p) => {
        if(!acc[p.category]) acc[p.category] = [];
        acc[p.category].push(p);
        return acc;
    }, {});
    
    for(const [cat, items] of Object.entries(grouped)) {
        let catHtml = `
            <div class="mb-8">
                <h2 class="text-xl font-black text-stone-800 mb-4 pb-2 border-b-2 border-amber-600 inline-block uppercase tracking-wider">${cat}</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        `;
        
        items.forEach(p => {
            const pct = Math.round((p.stock / (p.maxStock || 1)) * 100);
            const isZero = p.stock === 0;
            const isLow = p.stock < (p.maxStock * 0.2);
            
            catHtml += `
            <div class="bg-white rounded-3xl overflow-hidden shadow-lg border border-stone-200/60 hover:shadow-xl transition flex flex-col">
                <!-- Image Header -->
                <div class="relative h-48 w-full group">
                    <img src="${p.image}" class="w-full h-full object-cover" />
                    <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
                    
                    <!-- Badges -->
                    <div class="absolute top-3 left-3 right-3 flex justify-between">
                        ${isZero ? `<span class="bg-white text-rose-600 px-2 py-0.5 rounded text-[10px] font-black tracking-wider shadow">TÜKENDİ (%0)</span>` : '<div></div>'}
                        ${isLow && !isZero ? `<span class="bg-orange-500 text-white px-2 py-0.5 rounded text-[10px] font-black tracking-wider shadow flex items-center gap-1"><i data-lucide="flame" class="w-3 h-3"></i> Acil İmalatta</span>` : ''}
                    </div>
                    
                    <h3 class="absolute bottom-3 left-4 text-white font-black text-lg truncate pr-4">${p.name}</h3>
                </div>
                
                <!-- Body -->
                <div class="p-4 flex flex-col gap-4">
                    <!-- Stock Controls -->
                    <div class="flex justify-between items-center">
                        <div class="flex flex-col">
                            <span class="text-[10px] text-stone-400 font-extrabold uppercase mb-1">STOK (${p.unit.toUpperCase()})</span>
                            <div class="flex items-center gap-2 bg-stone-50 border border-stone-200 rounded-xl p-1 w-fit">
                                <button onclick="updateProduct(${p.id}, 'stock', -1)" class="w-7 h-7 rounded-lg hover:bg-stone-200 font-bold text-stone-600 flex items-center justify-center">-</button>
                                <span class="text-sm font-black text-stone-800 min-w-[3rem] text-center">${p.stock} ${p.unit}</span>
                                <button onclick="updateProduct(${p.id}, 'stock', 1)" class="w-7 h-7 rounded-lg hover:bg-stone-200 font-bold text-stone-600 flex items-center justify-center">+</button>
                            </div>
                        </div>
                        
                        <!-- Circular % -->
                        <div class="w-10 h-10 rounded-full border-4 ${isZero ? 'border-rose-100 text-rose-600' : (isLow ? 'border-orange-100 text-orange-500' : 'border-emerald-100 text-emerald-500')} flex items-center justify-center font-black text-[10px]">
                            %${pct}
                        </div>
                    </div>
                    
                    <!-- Sales and Waste Mini Controls -->
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
                    
                    <!-- Bottom Buttons -->
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
        
        catHtml += `</div></div>`;
        container.innerHTML += catHtml;
    }
    
    if(typeof lucide !== 'undefined') lucide.createIcons();
};

window.setRole = (role) => {
    const roles = ['HOME', 'UPPER', 'LOWER', 'ORDERS', 'ANALYTICS'];
    roles.forEach(r => {
        const viewEl = document.getElementById('view-' + r.toLowerCase());
        const btnEl = document.getElementById('btn-role-' + r.toLowerCase());
        if(viewEl) viewEl.style.display = 'none';
        if(btnEl) {
            btnEl.classList.remove('bg-amber-600', 'text-white');
            if(r !== 'HOME') btnEl.classList.add('bg-transparent', 'text-stone-300');
            else btnEl.classList.add('bg-transparent', 'text-stone-300');
        }
    });
    const selectedView = document.getElementById('view-' + role.toLowerCase());
    if(selectedView) selectedView.style.display = 'flex';
    const selectedBtn = document.getElementById('btn-role-' + role.toLowerCase());
    if(selectedBtn) {
        selectedBtn.classList.remove('bg-transparent', 'text-stone-300');
        selectedBtn.classList.add('bg-amber-600', 'text-white');
    }
    if(typeof lucide !== 'undefined') lucide.createIcons();
};

let currentSlide = 0;
const totalSlides = 5;
window.goToHeroSlide = (index) => {
    currentSlide = index;
    for(let i=0; i<totalSlides; i++){
        const slide = document.getElementById('hero-slide-'+i);
        const dot = document.getElementById('hero-dot-'+i);
        if(slide) {
            if(i === index) { slide.classList.remove('opacity-0', 'scale-105'); slide.classList.add('opacity-100', 'scale-100'); }
            else { slide.classList.remove('opacity-100', 'scale-100'); slide.classList.add('opacity-0', 'scale-105'); }
        }
        if(dot) {
            if(i === index) { dot.classList.remove('bg-stone-500/70', 'w-2.5', 'h-2.5'); dot.classList.add('bg-amber-400', 'w-3.5', 'h-3.5', 'shadow-sm', 'shadow-amber-500'); }
            else { dot.classList.remove('bg-amber-400', 'w-3.5', 'h-3.5', 'shadow-sm', 'shadow-amber-500'); dot.classList.add('bg-stone-500/70', 'w-2.5', 'h-2.5'); }
        }
    }
};
setInterval(() => { window.goToHeroSlide((currentSlide+1)%totalSlides); }, 5000);
"""

with open('app_v4.js', 'w') as f:
    f.write(js_content)
