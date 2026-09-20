import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r', encoding='utf-8') as f:
    content = f.read()

reset_data_str = """window.resetData = () => {
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
};"""

save_all_settings_str = """window.saveAllSettings = () => {
    const keys = ['products', 'categories', 'orders', 'customerOrders', 'receivables', 'inventory'];
    keys.forEach(k => {
        const val = localStorage.getItem(k);
        if (val) {
            localStorage.setItem(k + '_backup', val);
        }
    });
    alert('Tüm verileriniz ve ayarlarınız başarıyla kaydedildi! Ayarları sıfırladığınızda bu duruma dönülecektir.');
};"""

# Use regex to replace the functions
content = re.sub(
    r"window\.resetData = \(\) => \{.*?\n\};",
    reset_data_str,
    content,
    flags=re.DOTALL
)

content = re.sub(
    r"window\.saveAllSettings = \(\) => \{.*?\n\};",
    save_all_settings_str,
    content,
    flags=re.DOTALL
)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w', encoding='utf-8') as f:
    f.write(content)
