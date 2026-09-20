import re

with open('app_v4.js', 'r') as f:
    content = f.read()

# Add edit/delete category functions
new_functions = """
window.editCategory = (oldName) => {
    const newName = prompt('Kategori için yeni bir isim girin:', oldName);
    if(newName && newName.trim() !== '' && newName !== oldName) {
        const name = newName.trim();
        // Update categories array
        let cats = JSON.parse(localStorage.getItem('categories') || '[]');
        const index = cats.indexOf(oldName);
        if(index > -1) {
            cats[index] = name;
        } else {
            cats.push(name);
        }
        localStorage.setItem('categories', JSON.stringify(cats));
        
        // Update products belonging to this category
        let prods = JSON.parse(localStorage.getItem('products') || '[]');
        let updated = false;
        prods.forEach(p => {
            if(p.category === oldName) {
                p.category = name;
                updated = true;
            }
        });
        if(updated) localStorage.setItem('products', JSON.stringify(prods));
        
        renderCategoriesSelect();
        renderProducts();
    }
};

window.deleteCategory = (catName) => {
    if(confirm(`"${catName}" kategorisini silmek istediğinize emin misiniz?\n\nNot: Bu kategorideki ürünler "Diğer" kategorisine taşınacaktır.`)) {
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
        
        // Ensure "Diğer" is in categories if we moved products
        if(updated && !cats.includes('Diğer')) {
            cats.push('Diğer');
            localStorage.setItem('categories', JSON.stringify(cats));
        }
        
        renderCategoriesSelect();
        renderProducts();
    }
};
"""

# Insert new_functions before window.renderProducts
content = content.replace("window.renderProducts =", new_functions + "\nwindow.renderProducts =")

# Update the HTML generation in renderProducts to include the edit/delete buttons
header_html = """
        let catHtml = `
            <div class="mb-8 relative group">
                <div class="flex items-center gap-3 mb-4 border-b-2 border-amber-600 pb-2 w-max">
                    <h2 class="text-xl font-black text-stone-800 uppercase tracking-wider">${cat}</h2>
                    <div class="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1">
                        <button onclick="editCategory('${cat}')" class="p-1.5 bg-stone-100 hover:bg-stone-200 text-stone-600 rounded-lg transition" title="Kategoriyi Düzenle">
                            <i data-lucide="pencil" class="w-4 h-4"></i>
                        </button>
                        <button onclick="deleteCategory('${cat}')" class="p-1.5 bg-rose-50 hover:bg-rose-100 text-rose-600 rounded-lg transition" title="Kategoriyi Sil">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        `;
"""
content = re.sub(r'let catHtml = `\s*<div class="mb-8">\s*<h2[^>]*>\$\{cat\}<\/h2>\s*<div[^>]*>\s*`;', header_html, content)

with open('app_v4.js', 'w') as f:
    f.write(content)
