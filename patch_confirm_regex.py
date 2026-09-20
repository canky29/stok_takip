import re

with open('app_v4.js', 'r') as f:
    js = f.read()

# Replace deleteCategory
js = re.sub(r'window\.deleteCategory = \(catName\) => \{.*?renderProducts\(\);\n    \}\n\};', """window.deleteCategory = (catName) => {
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
            
            if(updated && !cats.includes('Diğer')) {
                cats.push('Diğer');
                localStorage.setItem('categories', JSON.stringify(cats));
            }
            
            closeConfirmModal();
            renderProducts();
        }
    );
};""", js, flags=re.DOTALL)

with open('app_v4.js', 'w') as f:
    f.write(js)
