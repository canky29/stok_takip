import re

# 1. Update index.html
with open('index.html', 'r') as f:
    html = f.read()

confirm_modal_html = """
    <!-- Unified Confirm Modal -->
    <div id="confirm-modal" class="fixed inset-0 bg-stone-900/60 backdrop-blur-sm hidden flex items-center justify-center z-[90]">
        <div class="bg-stone-50 p-8 rounded-3xl shadow-2xl w-[24rem] max-w-[90vw] transform scale-95 transition-transform border border-stone-200" id="confirm-modal-content">
            <div class="flex items-center justify-center mb-4 text-rose-500">
                <i data-lucide="alert-circle" class="w-16 h-16"></i>
            </div>
            <h3 id="confirm-modal-title" class="text-xl font-black text-center text-stone-800 mb-2">Emin misiniz?</h3>
            <p id="confirm-modal-desc" class="text-sm text-center text-stone-500 mb-8 font-medium">Bu işlem geri alınamaz.</p>
            
            <div class="grid grid-cols-2 gap-4">
                <button onclick="closeConfirmModal()" class="py-3.5 bg-stone-200 text-stone-700 font-bold rounded-xl hover:bg-stone-300 transition active:scale-95">
                    Vazgeç
                </button>
                <button onclick="executeConfirmCallback()" id="confirm-modal-btn" class="py-3.5 bg-rose-600 text-white font-bold rounded-xl hover:bg-rose-700 shadow-md transition active:scale-95">
                    Evet, Sil
                </button>
            </div>
        </div>
    </div>
"""

if 'id="confirm-modal"' not in html:
    html = html.replace('</body>', confirm_modal_html + '\n</body>')
    with open('index.html', 'w') as f:
        f.write(html)

# 2. Update app_v4.js
with open('app_v4.js', 'r') as f:
    js = f.read()

modal_js = """
let confirmCallback = null;

window.openConfirmModal = (title, desc, confirmText, callback) => {
    document.getElementById('confirm-modal-title').textContent = title;
    document.getElementById('confirm-modal-desc').textContent = desc;
    document.getElementById('confirm-modal-btn').textContent = confirmText || 'Evet, Onaylıyorum';
    confirmCallback = callback;
    
    const modal = document.getElementById('confirm-modal');
    const content = document.getElementById('confirm-modal-content');
    modal.classList.remove('hidden');
    setTimeout(() => content.classList.replace('scale-95', 'scale-100'), 10);
    if(typeof lucide !== 'undefined') lucide.createIcons();
};

window.closeConfirmModal = () => {
    const modal = document.getElementById('confirm-modal');
    const content = document.getElementById('confirm-modal-content');
    content.classList.replace('scale-100', 'scale-95');
    setTimeout(() => modal.classList.add('hidden'), 200);
    confirmCallback = null;
};

window.executeConfirmCallback = () => {
    if(confirmCallback) confirmCallback();
};
"""

js = modal_js + "\n" + js

# Replace deleteCategory
old_del_cat = """window.deleteCategory = (catName) => {
    if(confirm(`"${catName}" kategorisini silmek istediğinize emin misiniz?

Not: Bu kategorideki ürünler "Diğer" kategorisine taşınacaktır.`)) {
        let cats = JSON.parse(localStorage.getItem('categories') || '[]');
        cats = cats.filter(c => c !== catName);
        localStorage.setItem('categories', JSON.stringify(cats));
        
        let prods = JSON.parse(localStorage.getItem('products') || '[]');
        let updated = false;
        prods.forEach(p => {
            if(p.category === catName) {
                p.category = 'Diğer';
                updated = true;
            }
        });
        if(updated) localStorage.setItem('products', JSON.stringify(prods));
        
        if(!cats.includes('Diğer')) {
            cats.push('Diğer');
            localStorage.setItem('categories', JSON.stringify(cats));
        }
        
        renderProducts();
    }
};"""

new_del_cat = """window.deleteCategory = (catName) => {
    openConfirmModal(
        'Kategoriyi Sil',
        `"${catName}" kategorisini silmek istediğinize emin misiniz? İçindeki ürünler "Diğer" kategorisine taşınacaktır.`,
        'Evet, Sil',
        () => {
            let cats = JSON.parse(localStorage.getItem('categories') || '[]');
            cats = cats.filter(c => c !== catName);
            localStorage.setItem('categories', JSON.stringify(cats));
            
            let prods = JSON.parse(localStorage.getItem('products') || '[]');
            let updated = false;
            prods.forEach(p => {
                if(p.category === catName) {
                    p.category = 'Diğer';
                    updated = true;
                }
            });
            if(updated) localStorage.setItem('products', JSON.stringify(prods));
            
            if(!cats.includes('Diğer')) {
                cats.push('Diğer');
                localStorage.setItem('categories', JSON.stringify(cats));
            }
            
            closeConfirmModal();
            renderProducts();
        }
    );
};"""

js = js.replace(old_del_cat, new_del_cat)

# Replace deleteProduct
old_del_prod = """window.deleteProduct = (id) => {
    if(confirm('Bu ürünü silmek istediğinize emin misiniz?')) {
        let prods = JSON.parse(localStorage.getItem('products') || '[]');
        prods = prods.filter(x => x.id !== id);
        localStorage.setItem('products', JSON.stringify(prods));
        renderProducts();
    }
};"""

new_del_prod = """window.deleteProduct = (id) => {
    openConfirmModal(
        'Ürünü Sil',
        'Bu ürünü kalıcı olarak silmek istediğinize emin misiniz?',
        'Evet, Sil',
        () => {
            let prods = JSON.parse(localStorage.getItem('products') || '[]');
            prods = prods.filter(x => x.id !== id);
            localStorage.setItem('products', JSON.stringify(prods));
            closeConfirmModal();
            renderProducts();
        }
    );
};"""

js = js.replace(old_del_prod, new_del_prod)

# Replace cancelOrder
old_cancel = """window.cancelOrder = (orderId) => {
    if(confirm('Bu siparişi iptal etmek istediğinize emin misiniz?')) {
        let orders = JSON.parse(localStorage.getItem('orders') || '[]');
        orders = orders.filter(x => x.id !== orderId);
        localStorage.setItem('orders', JSON.stringify(orders));
        renderOrders();
    }
};"""

new_cancel = """window.cancelOrder = (orderId) => {
    openConfirmModal(
        'Siparişi İptal Et',
        'Bu siparişi imalathane listesinden kaldırmak istediğinize emin misiniz?',
        'Evet, İptal Et',
        () => {
            let orders = JSON.parse(localStorage.getItem('orders') || '[]');
            orders = orders.filter(x => x.id !== orderId);
            localStorage.setItem('orders', JSON.stringify(orders));
            closeConfirmModal();
            renderOrders();
        }
    );
};"""

js = js.replace(old_cancel, new_cancel)


with open('app_v4.js', 'w') as f:
    f.write(js)
