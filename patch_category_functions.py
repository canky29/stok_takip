import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

# 1. Update renderInventory header
old_header = r'<h2 class="text-xl font-black text-stone-800 mb-4 border-b border-stone-200 pb-2 uppercase tracking-widest">\$\{c\}</h2>'
new_header = """<div class="flex items-center justify-between mb-4 border-b border-stone-200 pb-2">
                    <h2 class="text-xl font-black text-stone-800 uppercase tracking-widest">${c}</h2>
                    <div class="flex gap-2">
                        <button onclick="editInvCategory('${c.replace("'", "\\'")}')" class="text-stone-400 hover:text-stone-700 transition px-2" title="Kategoriyi Düzenle"><i data-lucide="edit-2" class="w-4 h-4"></i></button>
                        <button onclick="deleteInvCategory('${c.replace("'", "\\'")}')" class="text-rose-400 hover:text-rose-600 transition px-2" title="Kategoriyi Sil"><i data-lucide="trash-2" class="w-4 h-4"></i></button>
                    </div>
                </div>"""

js = re.sub(old_header, new_header, js)

# 2. Update category modal functions
old_funcs = """window.addNewInvCategory = () => {
    document.getElementById('new-category-input').value = '';
    const el = document.getElementById('new-category-modal');
    if(el) {
        el.classList.remove('hidden');
        setTimeout(() => {
            document.getElementById('new-category-input').focus();
        }, 100);
    }
};

window.closeNewCategoryModal = () => {
    const el = document.getElementById('new-category-modal');
    if(el) el.classList.add('hidden');
};

window.submitNewInvCategory = () => {
    let newCat = document.getElementById('new-category-input').value;
    if(newCat && newCat.trim() !== '') {
        newCat = newCat.trim();
        let cats = getInvCategories();
        
        // Case-insensitive check
        const exists = cats.find(c => c.toLowerCase() === newCat.toLowerCase());
        
        if(!exists) {
            cats.push(newCat);
            localStorage.setItem('invCategories', JSON.stringify(cats));
            showToast("Yeni kategori başarıyla eklendi!", "success");
            
            // Re-populate the select
            const sel = document.getElementById('inventory-category');
            if(sel) {
                let opts = '';
                cats.forEach(c => opts += `<option value="${c}">${c}</option>`);
                sel.innerHTML = opts;
                sel.value = newCat; // Select the newly added one
            }
            closeNewCategoryModal(); renderInventory();
        } else {
            showToast("Bu kategori zaten mevcut!", "error");
            // Do not close the modal, let them fix it
        }
    } else {
        showToast("Lütfen bir kategori adı girin.", "error");
    }
};"""

new_funcs = """window.editingInvCategory = null;

window.addNewInvCategory = () => {
    window.editingInvCategory = null;
    const title = document.getElementById('new-category-modal-title');
    const btn = document.getElementById('new-category-submit-btn');
    if(title) title.textContent = 'Yeni Kategori Ekle';
    if(btn) btn.textContent = 'Ekle';
    
    document.getElementById('new-category-input').value = '';
    const el = document.getElementById('new-category-modal');
    if(el) {
        el.classList.remove('hidden');
        setTimeout(() => {
            document.getElementById('new-category-input').focus();
        }, 100);
    }
};

window.editInvCategory = (oldCat) => {
    window.editingInvCategory = oldCat;
    const title = document.getElementById('new-category-modal-title');
    const btn = document.getElementById('new-category-submit-btn');
    if(title) title.textContent = 'Kategoriyi Düzenle';
    if(btn) btn.textContent = 'Güncelle';
    
    document.getElementById('new-category-input').value = oldCat;
    const el = document.getElementById('new-category-modal');
    if(el) {
        el.classList.remove('hidden');
        setTimeout(() => {
            document.getElementById('new-category-input').focus();
        }, 100);
    }
};

window.deleteInvCategory = (cat) => {
    window.openConfirmModal('Kategoriyi Sil', `"${cat}" kategorisini silmek istediğinize emin misiniz? (Bu kategorideki ürünler "Kategorisiz" olarak işaretlenecektir.)`, 'Evet, Sil', () => {
        let cats = getInvCategories();
        cats = cats.filter(c => c !== cat);
        localStorage.setItem('invCategories', JSON.stringify(cats));
        
        let inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
        let updated = false;
        inventory.forEach(r => {
            if(r.category === cat) {
                r.category = ""; // make it uncategorized
                updated = true;
            }
        });
        if(updated) {
            localStorage.setItem('inventory', JSON.stringify(inventory));
        }
        
        populateInvCategoryDropdown();
        window.closeConfirmModal();
        renderInventory();
        showToast("Kategori silindi.", "success");
    });
};

window.closeNewCategoryModal = () => {
    const el = document.getElementById('new-category-modal');
    if(el) el.classList.add('hidden');
    window.editingInvCategory = null;
};

window.submitNewInvCategory = () => {
    let newCat = document.getElementById('new-category-input').value;
    if(newCat && newCat.trim() !== '') {
        newCat = newCat.trim();
        let cats = getInvCategories();
        
        // Case-insensitive check
        const exists = cats.find(c => c.toLowerCase() === newCat.toLowerCase());
        
        if(!exists || exists === window.editingInvCategory) {
            if(window.editingInvCategory) {
                // UPDATE MODE
                const idx = cats.indexOf(window.editingInvCategory);
                if(idx > -1) cats[idx] = newCat;
                localStorage.setItem('invCategories', JSON.stringify(cats));
                
                // Update products in inventory
                let inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
                let updated = false;
                inventory.forEach(r => {
                    if(r.category === window.editingInvCategory) {
                        r.category = newCat;
                        updated = true;
                    }
                });
                if(updated) {
                    localStorage.setItem('inventory', JSON.stringify(inventory));
                }
                
                showToast("Kategori güncellendi!", "success");
            } else {
                // CREATE MODE
                cats.push(newCat);
                localStorage.setItem('invCategories', JSON.stringify(cats));
                showToast("Yeni kategori başarıyla eklendi!", "success");
            }
            
            populateInvCategoryDropdown();
            closeNewCategoryModal(); 
            renderInventory();
        } else {
            showToast("Bu kategori zaten mevcut!", "error");
        }
    } else {
        showToast("Lütfen bir kategori adı girin.", "error");
    }
};"""

js = js.replace(old_funcs, new_funcs)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)
    
print("Category edit/delete logic implemented.")
