import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

old_reset_logic = """window.resetData = () => {
    if(confirm('Sistemi en son kaydettiğiniz duruma döndürmek istediğinize emin misiniz?')) {
        const keys = ['products', 'categories', 'orders', 'customerOrders', 'receivables', 'inventory'];
        const backups = {};
        keys.forEach(k => {
            backups[k] = localStorage.getItem(k + '_backup');
        });
        
        localStorage.clear();
        
        keys.forEach(k => {
            if (backups[k]) {
                localStorage.setItem(k, backups[k]);
                localStorage.setItem(k + '_backup', backups[k]);
            }
        });
        
        // Ensure default categories/products exist if no backup
        if(!localStorage.getItem('products')) localStorage.setItem('products', JSON.stringify([]));
        if(!localStorage.getItem('categories')) localStorage.setItem('categories', JSON.stringify(['Ekmek Çeşitleri', 'Pastalar']));
        
        location.reload();
    }
};

window.saveAllSettings = () => {
    const keys = ['products', 'categories', 'orders', 'customerOrders', 'receivables', 'inventory'];
    keys.forEach(k => {
        const val = localStorage.getItem(k);
        if (val) {
            localStorage.setItem(k + '_backup', val);
        }
    });
    showToast('Tüm verileriniz ve ayarlarınız başarıyla kaydedildi! Ayarları sıfırladığınızda bu duruma dönülecektir.');
};"""

new_reset_logic = """window.resetData = () => {
    window.openConfirmModal('Ayarları Sıfırla', 'Sistemi en son kaydettiğiniz duruma döndürmek istediğinize emin misiniz? Kaydetmediğiniz tüm veriler silinecektir.', 'Evet, Geri Dön', () => {
        const keys = ['products', 'categories', 'orders', 'customerOrders', 'receivables', 'inventory', 'invCategories', 'adminPassword'];
        const backups = {};
        keys.forEach(k => {
            backups[k] = localStorage.getItem(k + '_backup');
        });
        
        localStorage.clear();
        
        keys.forEach(k => {
            if (backups[k]) {
                localStorage.setItem(k, backups[k]);
                localStorage.setItem(k + '_backup', backups[k]); // keep the backup alive
            }
        });
        
        // Ensure defaults if no backup was found
        if(!localStorage.getItem('products')) localStorage.setItem('products', JSON.stringify([]));
        if(!localStorage.getItem('categories')) localStorage.setItem('categories', JSON.stringify(['Ekmek Çeşitleri', 'Pastalar']));
        if(!localStorage.getItem('invCategories')) localStorage.setItem('invCategories', JSON.stringify(['Un', 'İmalathane', 'Meşrubat', 'Kutu']));
        
        window.closeConfirmModal();
        location.reload();
    });
};

window.saveAllSettings = () => {
    const keys = ['products', 'categories', 'orders', 'customerOrders', 'receivables', 'inventory', 'invCategories', 'adminPassword'];
    keys.forEach(k => {
        const val = localStorage.getItem(k);
        if (val) {
            localStorage.setItem(k + '_backup', val);
        }
    });
    showToast('Sistem Başarıyla Kaydedildi! Geri dönülebilecek bir yedek oluşturuldu.', 'success');
};"""

if old_reset_logic in js:
    js = js.replace(old_reset_logic, new_reset_logic)
else:
    # Use regex if exact match fails
    js = re.sub(r'window\.resetData = \(\) => \{.*?(?=// Rendering)', new_reset_logic + "\n", js, flags=re.DOTALL)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)
    
print("Backup logic patched.")
