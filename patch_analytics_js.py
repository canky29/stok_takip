import re

with open('app_v4.js', 'r') as f:
    js = f.read()

# 1. Update product to track history
old_update = """        if(field === 'stock') {
            if(p.stock + delta >= 0 && p.stock + delta <= p.maxStock) p.stock += delta;
        } else if(field === 'sales') {
            if(delta > 0 && p.stock >= 1) { p.sales += 1; p.stock -= 1; }
            else if(delta < 0 && p.sales >= 1) { p.sales -= 1; p.stock += 1; }
        } else if(field === 'waste') {
            if(delta > 0 && p.stock >= 1) { p.waste += 1; p.stock -= 1; }
            else if(delta < 0 && p.waste >= 1) { p.waste -= 1; p.stock += 1; }
        }"""

new_update = """        const today = new Date().toISOString().split('T')[0];
        if (!p.history) p.history = {};
        if (!p.history[today]) p.history[today] = { sales: 0, waste: 0 };
        
        if(field === 'stock') {
            if(p.stock + delta >= 0 && p.stock + delta <= p.maxStock) p.stock += delta;
        } else if(field === 'sales') {
            if(delta > 0 && p.stock >= 1) { p.sales += 1; p.stock -= 1; p.history[today].sales++; }
            else if(delta < 0 && p.sales >= 1) { p.sales -= 1; p.stock += 1; p.history[today].sales = Math.max(0, p.history[today].sales - 1); }
        } else if(field === 'waste') {
            if(delta > 0 && p.stock >= 1) { p.waste += 1; p.stock -= 1; p.history[today].waste++; }
            else if(delta < 0 && p.waste >= 1) { p.waste -= 1; p.stock += 1; p.history[today].waste = Math.max(0, p.history[today].waste - 1); }
        }"""

js = js.replace(old_update, new_update)


# 2. Add analytics logic at the bottom
analytics_logic = """

let analyticsTimeFilter = 'ALL';
let chartInstance = null;

window.setAnalyticsTimeFilter = (filter) => {
    analyticsTimeFilter = filter;
    ['7D', '30D', 'ALL'].forEach(f => {
        const btn = document.getElementById('btn-time-' + f);
        if(!btn) return;
        if(f === filter) {
            btn.className = 'px-4 py-2 text-xs font-black rounded-lg transition bg-amber-600 text-white shadow-sm ring-2 ring-offset-2 ring-amber-500';
        } else {
            btn.className = 'px-4 py-2 text-xs font-black rounded-lg transition bg-stone-100 text-stone-600 hover:bg-stone-200';
        }
    });
    renderAnalyticsFloor();
};

window.renderAnalyticsFloor = () => {
    const container = document.getElementById('analytics-categories-container');
    if(!container) return;
    
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let cats = JSON.parse(localStorage.getItem('categories') || '[]');
    
    // Calculate sums based on time filter
    const now = new Date();
    prods.forEach(p => {
        if(analyticsTimeFilter === 'ALL') {
            p._calcSales = p.sales || 0;
            p._calcWaste = p.waste || 0;
        } else {
            p._calcSales = 0;
            p._calcWaste = 0;
            let daysLimit = analyticsTimeFilter === '7D' ? 7 : 30;
            if(p.history) {
                for (const [dateStr, data] of Object.entries(p.history)) {
                    let d = new Date(dateStr);
                    let diffTime = Math.abs(now - d);
                    let diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
                    if(diffDays <= daysLimit) {
                        p._calcSales += data.sales || 0;
                        p._calcWaste += data.waste || 0;
                    }
                }
            }
        }
    });
    
    // Calculate KPIs
    let totalStock = prods.reduce((sum, p) => sum + (p.stock || 0), 0);
    let totalSales = prods.reduce((sum, p) => sum + p._calcSales, 0);
    let totalWaste = prods.reduce((sum, p) => sum + p._calcWaste, 0);
    let avgWasteRate = totalSales + totalWaste > 0 ? Math.round((totalWaste / (totalSales + totalWaste)) * 100) : 0;
    
    const kpi1 = document.getElementById('kpi-total-stock'); if(kpi1) kpi1.textContent = totalStock;
    const kpi2 = document.getElementById('kpi-total-sales'); if(kpi2) kpi2.textContent = totalSales;
    const kpi3 = document.getElementById('kpi-total-waste'); if(kpi3) kpi3.textContent = totalWaste;
    
    // The UI doesn't have an ID for avgWasteRate, so we must add it or find it. Wait, the HTML has %0.
    // I'll search and replace in HTML if needed, but let's try to find element.
    // The HTML has `<div class="text-3xl font-black text-amber-600">%0</div>` under ORTALAMA FİRE ORANI. We will patch that in python too.

    // Group for chart
    let catLabels = [];
    let catSalesData = [];
    let catWasteData = [];
    
    cats.forEach(c => {
        let catProds = prods.filter(p => p.category === c);
        let s = catProds.reduce((sum, p) => sum + p._calcSales, 0);
        let w = catProds.reduce((sum, p) => sum + p._calcWaste, 0);
        catLabels.push(c);
        catSalesData.push(s);
        catWasteData.push(w);
    });
    
    // Draw Chart
    const ctx = document.getElementById('chart-category-perf');
    const msg = document.getElementById('chart-no-waste-msg');
    if(ctx) {
        if(totalSales === 0 && totalWaste === 0) {
            ctx.style.display = 'none';
            if(msg) msg.classList.remove('hidden');
        } else {
            ctx.style.display = 'block';
            if(msg) msg.classList.add('hidden');
            
            if(chartInstance) chartInstance.destroy();
            chartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: catLabels,
                    datasets: [
                        {
                            label: 'Satış',
                            data: catSalesData,
                            backgroundColor: '#10b981',
                            borderRadius: 6
                        },
                        {
                            label: 'Fire',
                            data: catWasteData,
                            backgroundColor: '#f43f5e',
                            borderRadius: 6
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, grid: { color: '#f5f5f4' } },
                        x: { grid: { display: false } }
                    }
                }
            });
        }
    }
    
    // Render Table
    let html = '';
    const searchVal = (document.getElementById('analytics-table-search')?.value || '').toLowerCase();
    
    cats.forEach(c => {
        let catProds = prods.filter(p => p.category === c && p.name.toLowerCase().includes(searchVal));
        if(catProds.length === 0) return;
        
        html += `
        <div class="border border-stone-200 rounded-xl overflow-hidden mb-4">
            <div class="bg-stone-50 px-4 py-3 border-b border-stone-200 flex justify-between items-center cursor-pointer hover:bg-stone-100 transition" onclick="document.getElementById('tbl-cat-${c.replace(/\s+/g, '-')}').classList.toggle('hidden')">
                <h4 class="font-black text-stone-800 uppercase tracking-wider">${c}</h4>
                <i data-lucide="chevron-down" class="w-4 h-4 text-stone-500"></i>
            </div>
            <div id="tbl-cat-${c.replace(/\s+/g, '-')}" class="overflow-x-auto">
                <table class="w-full text-left text-sm">
                    <thead class="bg-white text-stone-500 font-bold border-b border-stone-100 uppercase text-[10px] tracking-wider">
                        <tr>
                            <th class="px-4 py-3">Ürün Adı</th>
                            <th class="px-4 py-3">Kapasite</th>
                            <th class="px-4 py-3">Mevcut Stok</th>
                            <th class="px-4 py-3 text-emerald-600">Satış</th>
                            <th class="px-4 py-3 text-rose-600">Fire</th>
                            <th class="px-4 py-3">Fire Oranı</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-stone-100">
        `;
        
        catProds.forEach(p => {
            let total = p._calcSales + p._calcWaste;
            let rate = total > 0 ? Math.round((p._calcWaste / total) * 100) : 0;
            let rateColor = rate > 20 ? 'text-rose-600 font-black' : (rate > 10 ? 'text-amber-600 font-black' : 'text-emerald-600 font-black');
            html += `
                        <tr class="hover:bg-stone-50 transition">
                            <td class="px-4 py-3 font-black text-stone-800 flex items-center gap-3">
                                <img src="${p.image}" class="w-8 h-8 rounded-lg object-cover shadow-sm">
                                ${p.name}
                            </td>
                            <td class="px-4 py-3 font-medium text-stone-600">${p.maxStock} ${p.unit}</td>
                            <td class="px-4 py-3 font-black text-stone-800">${p.stock} ${p.unit}</td>
                            <td class="px-4 py-3 font-black text-emerald-600">${p._calcSales}</td>
                            <td class="px-4 py-3 font-black text-rose-600">${p._calcWaste}</td>
                            <td class="px-4 py-3 ${rateColor}">%${rate}</td>
                        </tr>
            `;
        });
        
        html += `</tbody></table></div></div>`;
    });
    
    if(html === '') {
        html = `<div class="text-center py-10 text-stone-500 font-bold bg-stone-50 rounded-xl border border-stone-200">Hiç kayıt bulunamadı.</div>`;
    }
    container.innerHTML = html;
    if(typeof lucide !== 'undefined') lucide.createIcons();
};

"""
js = js + analytics_logic

with open('app_v4.js', 'w') as f:
    f.write(js)
