import re

with open('app_v4.js', 'r') as f:
    js = f.read()

# Fix deleteProduct
old_del_prod = """window.deleteProduct = (id) => {
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

new_del_prod = """window.deleteProduct = (id) => {
    openConfirmModal(
        'Ürünü Sil',
        'Bu ürünü kalıcı olarak silmek istediğinize emin misiniz?',
        'Evet, Sil',
        () => {
            let prods = JSON.parse(localStorage.getItem('products') || '[]');
            prods = prods.filter(x => String(x.id) !== String(id));
            localStorage.setItem('products', JSON.stringify(prods));
            
            let orders = JSON.parse(localStorage.getItem('orders') || '[]');
            orders = orders.filter(x => String(x.productId) !== String(id));
            localStorage.setItem('orders', JSON.stringify(orders));
            
            closeConfirmModal();
            renderProducts();
            if(window.renderOrders) renderOrders();
        }
    );
};"""

js = js.replace(old_del_prod, new_del_prod)

# Fix cancelOrder
old_cancel = """window.cancelOrder = (orderId) => {
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

new_cancel = """window.cancelOrder = (orderId) => {
    openConfirmModal(
        'Siparişi İptal Et',
        'Bu siparişi imalathane listesinden kaldırmak istediğinize emin misiniz?',
        'Evet, İptal Et',
        () => {
            let orders = JSON.parse(localStorage.getItem('orders') || '[]');
            orders = orders.filter(x => String(x.id) !== String(orderId));
            localStorage.setItem('orders', JSON.stringify(orders));
            closeConfirmModal();
            renderOrders();
        }
    );
};"""

js = js.replace(old_cancel, new_cancel)

with open('app_v4.js', 'w') as f:
    f.write(js)
