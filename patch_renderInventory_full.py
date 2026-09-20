import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

# We want to replace the whole body of window.renderInventory
# from `const container = document.getElementById('inventory-container');` 
# up to `container.innerHTML = html;`

old_body_regex = r"const container = document\.getElementById\('inventory-container'\);\n\s*if\(!container\) return;\n\s*let search = document\.getElementById\('inventory-search'\)\?.value\.toLowerCase\(\) \|\| '';.*?container\.innerHTML = html;"

new_body = """const container = document.getElementById('inventory-container');
    if(!container) return;
    
    let search = document.getElementById('inventory-search')?.value.toLowerCase() || '';
    let displayList = inventory;
    
    if(search) {
        displayList = inventory.filter(r => 
            r.name.toLowerCase().includes(search) || 
            (r.notes || '').toLowerCase().includes(search)
        );
    }
    
    let html = '';
    
    let cats = getInvCategories();
    let uncatItems = displayList.filter(r => !r.category);
    
    const renderCard = (r) => {
        const dateStr = r.lastUpdated ? new Date(r.lastUpdated).toLocaleDateString('tr-TR', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : '';
        let isCritical = false;
        let criticalBadge = '';
        let cardBorderClass = 'border-stone-200/60';
        if (r.critical && parseFloat(r.amount) <= parseFloat(r.critical)) {
            isCritical = true;
            cardBorderClass = 'border-rose-500 shadow-[0_0_15px_rgba(244,63,94,0.1)]';
            criticalBadge = `<div class="absolute top-0 right-0 z-20 bg-rose-500 text-white text-[10px] font-black uppercase tracking-widest py-2 px-4 rounded-bl-3xl shadow-md flex items-center gap-1"><i data-lucide="alert-triangle" class="w-3 h-3"></i> Kritik</div>`;
        }

        let imgHtml = '';
        if (r.imgUrl) {
            imgHtml = `<div class="-mx-6 -mt-6 mb-4 h-48 bg-stone-100 overflow-hidden relative border-b border-stone-200">
                <img src="${r.imgUrl}" class="w-full h-full object-cover" alt="${r.name}">
            </div>`;
        }

        return `
        <div class="bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] border ${cardBorderClass} flex flex-col relative overflow-hidden transition duration-300 p-6 gap-5">
            ${criticalBadge}
            ${imgHtml}
            <div class="flex items-start justify-between relative z-10">
                <div class="pr-4">
                    <h3 class="text-xl font-black text-stone-800 tracking-tight leading-none mb-2">${r.name}</h3>
                    <div class="text-xs font-bold text-stone-400 flex items-center gap-1"><i data-lucide="clock" class="w-3.5 h-3.5"></i> Son G. ${dateStr}</div>
                </div>
                <div class="text-right shrink-0">
                    <div class="inline-flex items-baseline gap-1 bg-amber-50 text-amber-600 px-3 py-1.5 rounded-xl border border-amber-200">
                        <span class="text-xl font-black leading-none">${r.amount}</span>
                        <span class="text-[10px] font-black uppercase tracking-widest">${r.unit}</span>
                    </div>
                </div>
            </div>

            <div class="flex items-center gap-2 mt-auto pt-2 border-t border-stone-100 relative z-10">
                <button onclick="updateInventoryAmount(${r.id}, -1)" class="w-10 h-10 rounded-xl bg-stone-50 border border-stone-200 text-stone-600 font-bold text-lg hover:bg-stone-100 transition flex items-center justify-center shrink-0">-</button>
                <button onclick="updateInventoryAmount(${r.id}, 1)" class="w-10 h-10 rounded-xl bg-stone-50 border border-stone-200 text-stone-600 font-bold text-lg hover:bg-stone-100 transition flex items-center justify-center shrink-0">+</button>
                <div class="flex-1"></div>
                
                <button onclick="openInventoryModal(${r.id})" class="h-10 px-4 rounded-xl text-stone-500 hover:text-stone-800 hover:bg-stone-100 transition flex items-center gap-2 font-bold text-sm shrink-0">
                    <i data-lucide="edit-2" class="w-4 h-4"></i> Düzenle
                </button>
                
                <button onclick="deleteInventory(${r.id})" class="w-10 h-10 rounded-xl text-rose-400 hover:text-rose-600 hover:bg-rose-50 transition flex items-center justify-center shrink-0">
                    <i data-lucide="trash-2" class="w-4 h-4"></i>
                </button>
            </div>
        </div>
        `;
    };

    let hasAnyRendered = false;

    cats.forEach(c => {
        let items = displayList.filter(r => r.category === c);
        
        if (items.length > 0 || !search) {
            hasAnyRendered = true;
            html += `
            <div class="mb-2">
                <h2 class="text-xl font-black text-stone-800 mb-4 border-b border-stone-200 pb-2 uppercase tracking-widest">${c}</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            `;
            
            if(items.length > 0) {
                html += items.sort((a,b) => b.id - a.id).map(renderCard).join('');
            } else {
                html += `<div class="col-span-full py-8 text-center text-stone-400 font-bold bg-stone-50 rounded-2xl border border-stone-200 border-dashed">Bu kategoride henüz ürün bulunmuyor.</div>`;
            }
            
            html += `
                </div>
            </div>
            `;
        }
    });
    
    if(uncatItems.length > 0) {
        hasAnyRendered = true;
        html += `
        <div class="mb-2">
            <h2 class="text-xl font-black text-stone-800 mb-4 border-b border-stone-200 pb-2 uppercase tracking-widest">Kategorisiz</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                ${uncatItems.sort((a,b) => b.id - a.id).map(renderCard).join('')}
            </div>
        </div>
        `;
    }

    if (!hasAnyRendered) {
        html = `<div class="col-span-full text-center py-12 text-stone-500 font-bold bg-white rounded-3xl border border-stone-200 shadow-sm flex flex-col items-center justify-center gap-2"><i data-lucide="package" class="w-10 h-10 text-stone-300"></i>Kayıt bulunamadı.</div>`;
    }

    container.innerHTML = html;"""

js_new = re.sub(old_body_regex, new_body, js, flags=re.DOTALL)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js_new)

print("Full replacement complete.")
