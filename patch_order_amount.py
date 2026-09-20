import re

with open('app_v4.js', 'r') as f:
    js = f.read()

orders_code = """
window.autoRequestOrder = (product) => {
    let orders = JSON.parse(localStorage.getItem('orders') || '[]');
    if(!orders.some(o => o.productId === product.id)) {
        let amt = (product.maxStock || 10) - (product.stock || 0);
        if(amt <= 0) amt = 10;
        
        orders.push({
            id: Date.now(),
            productId: product.id,
            productName: product.name,
            productImage: product.image || 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500&auto=format&fit=crop&q=60',
            unit: product.unit || 'Adet',
            amount: amt,
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

window.updateOrderAmount = (orderId, delta) => {
    let orders = JSON.parse(localStorage.getItem('orders') || '[]');
    let o = orders.find(x => x.id === orderId);
    if(o) {
        if(o.amount + delta > 0) {
            o.amount += delta;
            localStorage.setItem('orders', JSON.stringify(orders));
            renderOrders();
        }
    }
};

window.completeOrder = (orderId) => {
    let orders = JSON.parse(localStorage.getItem('orders') || '[]');
    const ord = orders.find(x => x.id === orderId);
    if(ord) {
        let prods = JSON.parse(localStorage.getItem('products') || '[]');
        let p = prods.find(x => x.id === ord.productId);
        if(p) {
            p.stock += ord.amount; 
            if(p.stock > p.maxStock) p.stock = p.maxStock; // limit to max capacity just in case
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
            <div class="flex gap-4 items-center">
                <img src="${o.productImage}" class="w-16 h-16 object-cover rounded-xl shadow-sm border border-stone-200">
                <div class="flex-1">
                    <div class="flex justify-between items-start mb-1">
                        <h3 class="text-xl font-black text-stone-800 uppercase tracking-tight">${o.productName}</h3>
                        <span class="bg-red-100 text-red-600 px-2 py-1 rounded-lg text-[10px] font-black uppercase tracking-wider flex items-center gap-1 shadow-sm"><i data-lucide="flame" class="w-3 h-3"></i> Acil</span>
                    </div>
                    <div class="text-xs text-stone-500 font-bold flex items-center gap-1"><i data-lucide="clock" class="w-3 h-3"></i> Sipariş Saati: ${o.time}</div>
                </div>
            </div>
            
            <div class="bg-stone-50 p-3 rounded-xl border border-stone-200 flex justify-between items-center mt-1">
                <span class="text-xs font-bold text-stone-600 uppercase">Üretilecek Miktar:</span>
                <div class="flex items-center gap-2 bg-white border border-stone-300 rounded-lg p-1">
                    <button onclick="updateOrderAmount(${o.id}, -1)" class="w-8 h-8 rounded hover:bg-stone-100 font-bold text-stone-600 flex items-center justify-center">-</button>
                    <span class="text-sm font-black text-stone-800 min-w-[3rem] text-center">${o.amount} ${o.unit}</span>
                    <button onclick="updateOrderAmount(${o.id}, 1)" class="w-8 h-8 rounded hover:bg-stone-100 font-bold text-stone-600 flex items-center justify-center">+</button>
                </div>
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

js = re.sub(r'window\.autoRequestOrder = \(product\) => \{.*?\}\;\n};', orders_code, js, flags=re.DOTALL)

with open('app_v4.js', 'w') as f:
    f.write(js)
