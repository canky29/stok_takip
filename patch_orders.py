import re

with open('app_v4.js', 'r') as f:
    js = f.read()

# Replace manual requestOrder with auto logic + orders rendering
orders_code = """
window.autoRequestOrder = (product) => {
    let orders = JSON.parse(localStorage.getItem('orders') || '[]');
    if(!orders.some(o => o.productId === product.id)) {
        orders.push({
            id: Date.now(),
            productId: product.id,
            productName: product.name,
            time: new Date().toLocaleTimeString('tr-TR', {hour: '2-digit', minute:'2-digit'})
        });
        localStorage.setItem('orders', JSON.stringify(orders));
        if(window.renderOrders) renderOrders();
    }
};

window.requestOrder = (id) => {
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let p = prods.find(x => x.id === id);
    if(p) {
        autoRequestOrder(p);
        alert(p.name + ' için imalathaneye üretim isteği gönderildi!');
    }
};

window.completeOrder = (orderId) => {
    let orders = JSON.parse(localStorage.getItem('orders') || '[]');
    const ord = orders.find(x => x.id === orderId);
    if(ord) {
        let prods = JSON.parse(localStorage.getItem('products') || '[]');
        let p = prods.find(x => x.id === ord.productId);
        if(p) {
            p.stock = p.maxStock || p.stock; 
            localStorage.setItem('products', JSON.stringify(prods));
        }
        orders = orders.filter(x => x.id !== orderId);
        localStorage.setItem('orders', JSON.stringify(orders));
        renderOrders();
        renderProducts();
    }
};

window.cancelOrder = (orderId) => {
    if(confirm('Bu siparişi iptal etmek istediğinize emin misiniz?')) {
        let orders = JSON.parse(localStorage.getItem('orders') || '[]');
        orders = orders.filter(x => x.id !== orderId);
        localStorage.setItem('orders', JSON.stringify(orders));
        renderOrders();
    }
};

window.renderOrders = () => {
    const container = document.getElementById('kds-pending');
    if(!container) return;
    
    let orders = JSON.parse(localStorage.getItem('orders') || '[]');
    if(orders.length === 0) {
        container.innerHTML = `<div class="col-span-full text-center py-10 text-stone-500 font-bold"><i data-lucide="coffee" class="w-10 h-10 mx-auto mb-3 opacity-50"></i>Şu an bekleyen imalat siparişi yok.</div>`;
        if(typeof lucide !== 'undefined') lucide.createIcons();
        return;
    }
    
    let html = '';
    orders.forEach(o => {
        html += `
        <div class="bg-white rounded-2xl p-5 shadow-lg border-l-4 border-l-red-500 border border-stone-200 flex flex-col gap-4">
            <div>
                <div class="flex justify-between items-start mb-2">
                    <h3 class="text-xl font-black text-stone-800 uppercase tracking-tight">${o.productName}</h3>
                    <span class="bg-red-100 text-red-600 px-2 py-1 rounded-lg text-[10px] font-black uppercase tracking-wider flex items-center gap-1 shadow-sm"><i data-lucide="flame" class="w-3 h-3"></i> Acil</span>
                </div>
                <div class="text-xs text-stone-500 font-bold flex items-center gap-1"><i data-lucide="clock" class="w-3 h-3"></i> Sipariş Saati: ${o.time}</div>
            </div>
            <div class="flex flex-col gap-2 mt-auto pt-2">
                <button onclick="completeOrder(${o.id})" class="w-full bg-emerald-600 text-white font-black py-3 rounded-xl hover:bg-emerald-700 shadow flex items-center justify-center gap-2 transition active:scale-95">
                    <i data-lucide="check-circle" class="w-5 h-5"></i> Tamamlandı & Teslim Et
                </button>
                <button onclick="cancelOrder(${o.id})" class="w-full bg-stone-100 text-stone-500 font-black py-2.5 rounded-xl hover:bg-stone-200 hover:text-stone-700 transition text-xs flex items-center justify-center gap-1.5 active:scale-95 border border-stone-200">
                    <i data-lucide="x" class="w-3.5 h-3.5"></i> İptal Et
                </button>
            </div>
        </div>
        `;
    });
    container.innerHTML = html;
    if(typeof lucide !== 'undefined') lucide.createIcons();
};
"""

js = re.sub(r'window\.requestOrder = \(.*?\}\;', orders_code, js, flags=re.DOTALL)

# Add autoRequestOrder into updateProduct
update_prod_logic = """
        if(field === 'stock') {
            if(p.stock + delta >= 0 && p.stock + delta <= p.maxStock) p.stock += delta;
        } else if(field === 'sales') {
            if(delta > 0 && p.stock >= 1) { p.sales += 1; p.stock -= 1; }
            else if(delta < 0 && p.sales >= 1) { p.sales -= 1; p.stock += 1; }
        } else if(field === 'waste') {
            if(delta > 0 && p.stock >= 1) { p.waste += 1; p.stock -= 1; }
            else if(delta < 0 && p.waste >= 1) { p.waste -= 1; p.stock += 1; }
        }
        
        // Auto Order Check
        const pct = Math.min(100, Math.round((p.stock / (p.maxStock || 1)) * 100));
        if(pct <= 30) {
            autoRequestOrder(p);
        }
        
        localStorage.setItem('products', JSON.stringify(prods));
"""

js = re.sub(r'        if\(field === \'stock\'\).*?localStorage\.setItem\(\'products\', JSON\.stringify\(prods\)\);', update_prod_logic, js, flags=re.DOTALL)

# Add renderOrders to initialization
js = js.replace('renderProducts();\n});', 'renderProducts();\n    renderOrders();\n});')

# Also fix the requestOrder call inside renderProducts button to pass id instead of name
js = js.replace("requestOrder('${p.name}')", "requestOrder(${p.id})")

with open('app_v4.js', 'w') as f:
    f.write(js)
