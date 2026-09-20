import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    content = f.read()

# Replace window.renderFinance to support sorting
new_render_finance = """window.financeSortMode = window.financeSortMode || 'CATEGORY';

window.setFinanceSortMode = (mode) => {
    window.financeSortMode = mode;
    window.renderFinance();
};

window.renderFinance = () => {
    const tbody = document.getElementById('finance-tbody');
    if(!tbody) return;
    
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let cats = JSON.parse(localStorage.getItem('categories') || '[]');
    let html = '';
    
    // Calculate net profit for each product beforehand for sorting
    prods.forEach(p => {
        const produced = parseFloat(p._calcEntered) || 0;
        const waste = parseFloat(p.waste) || 0;
        const remaining = parseFloat(p.amount) || 0;
        let sold = produced - remaining - waste;
        if (sold < 0) sold = 0;
        
        const costPrice = parseFloat(p.costPrice) || 0;
        const sellPrice = parseFloat(p.sellPrice) || 0;
        
        p._revenue = sold * sellPrice;
        p._costOfSold = sold * costPrice;
        p._wasteLoss = waste * costPrice;
        p._netProfit = p._revenue - p._costOfSold - p._wasteLoss;
        p._produced = produced;
        p._waste = waste;
        p._sold = sold;
    });
    
    const renderProductRow = (p, catIndex = '') => {
        const isLoss = p._netProfit < 0;
        const profitColor = isLoss ? 'text-rose-600' : 'text-emerald-600';
        const profitSign = isLoss ? '-' : '+';
        const profitIcon = isLoss ? 'trending-down' : 'trending-up';
        
        const rowClass = catIndex !== '' ? `finance-row-${catIndex}` : '';
        const paddingClass = catIndex !== '' ? 'pl-8' : '';
        const catBadge = catIndex === '' ? `<div class="text-xs font-bold text-stone-400 mt-0.5">${p.category || 'Diğer'}</div>` : '';

        return `
        <tr class="hover:bg-stone-50/50 transition ${rowClass}">
            <td class="p-4 ${paddingClass}">
                <div class="font-black text-stone-800">${p.name}</div>
                ${catBadge}
            </td>
            <td class="p-4 text-center">
                <div class="flex items-center justify-center gap-3 text-sm font-bold">
                    <span class="text-blue-600 bg-blue-50 px-2 py-0.5 rounded" title="Üretilen (Vitrine Çıkan)">${p._produced}</span>
                    <span class="text-stone-300">/</span>
                    <span class="text-rose-600 bg-rose-50 px-2 py-0.5 rounded" title="Fire">${p._waste}</span>
                    <span class="text-stone-300">/</span>
                    <span class="text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded" title="Satılan">${p._sold}</span>
                </div>
            </td>
            <td class="p-4">
                <div class="relative">
                    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-stone-400 font-bold text-sm">₺</div>
                    <input type="number" step="0.01" min="0" onchange="updateFinancePrice(${p.id}, 'cost', this.value)" value="${p.costPrice || ''}" placeholder="0.00" class="w-full bg-white border border-stone-200 rounded-lg py-1.5 pl-7 pr-2 text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-amber-500">
                </div>
            </td>
            <td class="p-4">
                <div class="relative">
                    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-stone-400 font-bold text-sm">₺</div>
                    <input type="number" step="0.01" min="0" onchange="updateFinancePrice(${p.id}, 'sell', this.value)" value="${p.sellPrice || ''}" placeholder="0.00" class="w-full bg-white border border-stone-200 rounded-lg py-1.5 pl-7 pr-2 text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-amber-500">
                </div>
            </td>
            <td class="p-4 text-right font-bold text-emerald-600">
                ₺${p._revenue.toFixed(2)}
            </td>
            <td class="p-4 text-right font-bold text-rose-600">
                ₺${p._wasteLoss.toFixed(2)}
            </td>
            <td class="p-4 text-right">
                <div class="flex items-center justify-end gap-1 font-black ${profitColor}">
                    <i data-lucide="${profitIcon}" class="w-4 h-4"></i>
                    ${profitSign}₺${Math.abs(p._netProfit).toFixed(2)}
                </div>
            </td>
        </tr>`;
    };

    if (window.financeSortMode === 'CATEGORY') {
        const grouped = {};
        cats.forEach(c => grouped[c] = []);
        prods.forEach(p => {
            const cat = p.category || 'Diğer';
            if (!grouped[cat]) grouped[cat] = [];
            grouped[cat].push(p);
        });

        let catIndex = 0;
        Object.keys(grouped).sort().forEach(cat => {
            catIndex++;
            html += `
            <tr class="bg-stone-100/80 cursor-pointer hover:bg-stone-200/60 transition" onclick="toggleFinanceCategory(${catIndex})">
                <td colspan="7" class="p-3 pl-4 font-black text-stone-800 text-sm border-y border-stone-200">
                    <div class="flex items-center gap-2">
                        <i id="finance-icon-${catIndex}" data-lucide="chevron-down" class="w-4 h-4 text-stone-500 transition-transform duration-200"></i>
                        ${cat}
                    </div>
                </td>
            </tr>`;
            grouped[cat].sort((a, b) => b.id - a.id).forEach(p => {
                html += renderProductRow(p, catIndex);
            });
        });
        
        if (prods.length === 0 && cats.length === 0) {
            html = `<tr><td colspan="7" class="p-8 text-center text-stone-500 font-bold">Kayıtlı ürün veya kategori bulunmamaktadır.</td></tr>`;
        }
    } else {
        // Flat list sorting
        if (window.financeSortMode === 'PROFIT_DESC') {
            prods.sort((a, b) => b._netProfit - a._netProfit);
        } else if (window.financeSortMode === 'PROFIT_ASC') {
            prods.sort((a, b) => a._netProfit - b._netProfit);
        }
        
        if (prods.length === 0) {
            html = `<tr><td colspan="7" class="p-8 text-center text-stone-500 font-bold">Kayıtlı ürün bulunmamaktadır.</td></tr>`;
        } else {
            prods.forEach(p => {
                html += renderProductRow(p, '');
            });
        }
    }
    
    tbody.innerHTML = html;
    if(typeof lucide !== 'undefined') lucide.createIcons();
    
    // Update active state of sort buttons if they exist
    const btns = document.querySelectorAll('.finance-sort-btn');
    btns.forEach(btn => {
        if(btn.dataset.sort === window.financeSortMode) {
            btn.classList.add('bg-stone-800', 'text-white');
            btn.classList.remove('bg-stone-100', 'text-stone-600', 'hover:bg-stone-200');
        } else {
            btn.classList.remove('bg-stone-800', 'text-white');
            btn.classList.add('bg-stone-100', 'text-stone-600', 'hover:bg-stone-200');
        }
    });
};"""

pattern = re.compile(r'window\.renderFinance\s*=\s*\(\)\s*=>\s*\{.*?(?=\nwindow\.expandAllFinanceCategories)', re.DOTALL)
content = pattern.sub(new_render_finance, content)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(content)

print("Patched app_v4.js for Finance Sorting!")
