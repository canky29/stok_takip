import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    content = f.read()

new_render_finance = """window.renderFinance = () => {
    const tbody = document.getElementById('finance-tbody');
    if(!tbody) return;
    
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let html = '';
    
    if (prods.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="p-8 text-center text-stone-500 font-bold">Kayıtlı ürün bulunmamaktadır.</td></tr>`;
        return;
    }

    // Group products by category
    const grouped = {};
    prods.forEach(p => {
        const cat = p.category || 'Diğer';
        if (!grouped[cat]) grouped[cat] = [];
        grouped[cat].push(p);
    });

    Object.keys(grouped).sort().forEach(cat => {
        // Render Category Header Row
        html += `
        <tr class="bg-stone-100/80">
            <td colspan="7" class="p-3 pl-4 font-black text-stone-800 text-sm border-y border-stone-200">
                ${cat}
            </td>
        </tr>`;

        grouped[cat].sort((a, b) => b.id - a.id).forEach(p => {
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
                <td class="p-4 pl-6">
                    <div class="font-black text-stone-800">${p.name}</div>
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
    });
    
    tbody.innerHTML = html;
    if(typeof lucide !== 'undefined') lucide.createIcons();
};"""

# Replace the window.renderFinance definition
pattern = re.compile(r'window\.renderFinance\s*=\s*\(\)\s*=>\s*\{.*?(?=\n\n|\Z)', re.DOTALL)
new_content = pattern.sub(new_render_finance, content)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(new_content)

print("Patched renderFinance to group by category!")
