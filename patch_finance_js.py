import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Update setRole
old_set_role = """    if (role === 'INVENTORY') {
        document.getElementById('view-inventory').classList.remove('hidden');
        document.getElementById('btn-role-inventory').classList.add('bg-stone-800', 'text-white', 'shadow-md');
        document.getElementById('btn-role-inventory').classList.remove('text-stone-500', 'hover:bg-stone-200');
        window.renderInventory();
    } else {
        document.getElementById('view-inventory').classList.add('hidden');
        document.getElementById('btn-role-inventory').classList.remove('bg-stone-800', 'text-white', 'shadow-md');
        document.getElementById('btn-role-inventory').classList.add('text-stone-500', 'hover:bg-stone-200');
    }"""

new_set_role = old_set_role + """
    
    if (role === 'FINANCE') {
        document.getElementById('view-finance').classList.remove('hidden');
        document.getElementById('btn-role-finance').classList.add('bg-stone-800', 'text-white', 'shadow-md');
        document.getElementById('btn-role-finance').classList.remove('text-stone-500', 'hover:bg-stone-200');
        window.renderFinance();
    } else {
        document.getElementById('view-finance').classList.add('hidden');
        document.getElementById('btn-role-finance').classList.remove('bg-stone-800', 'text-white', 'shadow-md');
        document.getElementById('btn-role-finance').classList.add('text-stone-500', 'hover:bg-stone-200');
    }"""

js_content = js_content.replace(old_set_role, new_set_role)

# Add renderFinance and updateFinancePrice functions
finance_js = """
window.updateFinancePrice = (id, type, value) => {
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    const index = prods.findIndex(p => p.id === id);
    if(index > -1) {
        if(type === 'cost') {
            prods[index].costPrice = parseFloat(value) || 0;
        } else if(type === 'sell') {
            prods[index].sellPrice = parseFloat(value) || 0;
        }
        localStorage.setItem('products', JSON.stringify(prods));
        window.renderFinance();
    }
};

window.renderFinance = () => {
    const tbody = document.getElementById('finance-tbody');
    if(!tbody) return;
    
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let html = '';
    
    prods.sort((a, b) => b.id - a.id).forEach(p => {
        // Calculate production, waste, sales
        const produced = parseFloat(p._calcEntered) || 0;
        const waste = parseFloat(p.waste) || 0;
        const remaining = parseFloat(p.amount) || 0;
        let sold = produced - remaining - waste;
        if (sold < 0) sold = 0; // fallback just in case of manual stock adjustments

        // Prices
        const costPrice = parseFloat(p.costPrice) || 0;
        const sellPrice = parseFloat(p.sellPrice) || 0;

        // Financials
        const revenue = sold * sellPrice;
        const costOfSold = sold * costPrice;
        const wasteLoss = waste * costPrice;
        const netProfit = revenue - costOfSold - wasteLoss;
        
        const isLoss = netProfit < 0;
        const profitColor = isLoss ? 'text-rose-600' : 'text-emerald-600';
        const profitSign = isLoss ? '-' : '+';
        const profitIcon = isLoss ? 'trending-down' : 'trending-up';

        html += `
        <tr class="hover:bg-stone-50/50 transition">
            <td class="p-4">
                <div class="font-black text-stone-800">${p.name}</div>
                <div class="text-xs font-bold text-stone-400">${p.category}</div>
            </td>
            <td class="p-4 text-center">
                <div class="flex items-center justify-center gap-3 text-sm font-bold">
                    <span class="text-blue-600 bg-blue-50 px-2 py-0.5 rounded" title="Üretilen (Vitrine Çıkan)">${produced}</span>
                    <span class="text-stone-300">/</span>
                    <span class="text-rose-600 bg-rose-50 px-2 py-0.5 rounded" title="Fire">${waste}</span>
                    <span class="text-stone-300">/</span>
                    <span class="text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded" title="Satılan">${sold}</span>
                </div>
            </td>
            <td class="p-4">
                <div class="relative">
                    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-stone-400 font-bold text-sm">₺</div>
                    <input type="number" step="0.01" min="0" onchange="updateFinancePrice(${p.id}, 'cost', this.value)" value="${costPrice || ''}" placeholder="0.00" class="w-full bg-white border border-stone-200 rounded-lg py-1.5 pl-7 pr-2 text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-amber-500">
                </div>
            </td>
            <td class="p-4">
                <div class="relative">
                    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-stone-400 font-bold text-sm">₺</div>
                    <input type="number" step="0.01" min="0" onchange="updateFinancePrice(${p.id}, 'sell', this.value)" value="${sellPrice || ''}" placeholder="0.00" class="w-full bg-white border border-stone-200 rounded-lg py-1.5 pl-7 pr-2 text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-amber-500">
                </div>
            </td>
            <td class="p-4 text-right font-bold text-emerald-600">
                ₺${revenue.toFixed(2)}
            </td>
            <td class="p-4 text-right font-bold text-rose-600">
                ₺${wasteLoss.toFixed(2)}
            </td>
            <td class="p-4 text-right">
                <div class="flex items-center justify-end gap-1 font-black ${profitColor}">
                    <i data-lucide="${profitIcon}" class="w-4 h-4"></i>
                    ${profitSign}₺${Math.abs(netProfit).toFixed(2)}
                </div>
            </td>
        </tr>`;
    });
    
    if (prods.length === 0) {
        html = `<tr><td colspan="7" class="p-8 text-center text-stone-500 font-bold">Kayıtlı ürün bulunmamaktadır.</td></tr>`;
    }
    
    tbody.innerHTML = html;
    if(typeof lucide !== 'undefined') lucide.createIcons();
};
"""

js_content += "\n" + finance_js

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w', encoding='utf-8') as f:
    f.write(js_content)
