import re

with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    html = f.read()

# Add category to the inventory form
old_critical = """                <div>
                    <label class="block text-xs font-black text-stone-500 uppercase tracking-widest mb-1.5">Kritik Stok Uyarı Limiti</label>
                    <input type="number" step="0.01" id="inventory-critical" class="w-full bg-stone-50 border border-stone-200 rounded-xl px-4 py-3 font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-rose-500" placeholder="Örn: 5 (Bu değere düşünce kırmızı uyarır)">
                </div>"""

new_critical = """                <div>
                    <label class="block text-xs font-black text-stone-500 uppercase tracking-widest mb-1.5">Kritik Stok Uyarı Limiti</label>
                    <input type="number" step="0.01" id="inventory-critical" class="w-full bg-stone-50 border border-stone-200 rounded-xl px-4 py-3 font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-rose-500" placeholder="Örn: 5 (Bu değere düşünce kırmızı uyarır)">
                </div>
                
                <div>
                    <div class="flex justify-between items-center mb-1.5">
                        <label class="block text-xs font-black text-stone-500 uppercase tracking-widest">Kategori</label>
                        <button type="button" onclick="addNewInvCategory()" class="text-[10px] font-bold text-amber-600 hover:text-amber-700 uppercase tracking-widest">+ Yeni Ekle</button>
                    </div>
                    <select id="inventory-category" required class="w-full bg-stone-50 border border-stone-200 rounded-xl px-4 py-3 font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-amber-500">
                    </select>
                </div>"""

html = html.replace(old_critical, new_critical)

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(html)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

# Make sure invCategories is initialized in app_v4.js
init_code = """
window.getInvCategories = () => {
    let cats = localStorage.getItem('invCategories');
    if(!cats) {
        cats = ['Un', 'İmalathane', 'Meşrubat', 'Kutu'];
        localStorage.setItem('invCategories', JSON.stringify(cats));
    } else {
        cats = JSON.parse(cats);
    }
    return cats;
};

window.addNewInvCategory = () => {
    let newCat = prompt("Yeni kategori adını girin:");
    if(newCat && newCat.trim() !== '') {
        newCat = newCat.trim();
        let cats = getInvCategories();
        if(!cats.includes(newCat)) {
            cats.push(newCat);
            localStorage.setItem('invCategories', JSON.stringify(cats));
            showToast("Yeni kategori eklendi!", "success");
            
            // Re-populate the select
            const sel = document.getElementById('inventory-category');
            if(sel) {
                let opts = '';
                cats.forEach(c => opts += `<option value="${c}">${c}</option>`);
                sel.innerHTML = opts;
                sel.value = newCat; // Select the newly added one
            }
        }
    }
};

window.populateInvCategoryDropdown = (selectedValue = '') => {
    const sel = document.getElementById('inventory-category');
    if(!sel) return;
    let cats = getInvCategories();
    let opts = '';
    cats.forEach(c => opts += `<option value="${c}">${c}</option>`);
    sel.innerHTML = opts;
    if(selectedValue && cats.includes(selectedValue)) {
        sel.value = selectedValue;
    }
};
"""

js = js.replace("let pendingRole = null;", "let pendingRole = null;\n" + init_code)


# Modify openInventoryModal to populate the dropdown
old_open_inv = """window.openInventoryModal = (id = null) => {
    document.getElementById('inventory-img-url').value = '';
    document.getElementById('inventory-img-url-input').value = '';
    document.getElementById('inventory-img-file-input').value = '';
    document.getElementById('inventory-img-preview-box').classList.add('hidden');
    document.getElementById('inventory-img-preview').src = '';"""

new_open_inv = """window.openInventoryModal = (id = null) => {
    document.getElementById('inventory-img-url').value = '';
    document.getElementById('inventory-img-url-input').value = '';
    document.getElementById('inventory-img-file-input').value = '';
    document.getElementById('inventory-img-preview-box').classList.add('hidden');
    document.getElementById('inventory-img-preview').src = '';
    
    let invCat = '';
"""

js = js.replace(old_open_inv, new_open_inv)


old_open_inv_2 = """        document.getElementById('inventory-name').value = item.name;
        document.getElementById('inventory-amount').value = item.amount;
        document.getElementById('inventory-unit').value = item.unit;
        document.getElementById('inventory-critical').value = item.critical || '';"""

new_open_inv_2 = """        document.getElementById('inventory-name').value = item.name;
        document.getElementById('inventory-amount').value = item.amount;
        document.getElementById('inventory-unit').value = item.unit;
        document.getElementById('inventory-critical').value = item.critical || '';
        invCat = item.category || '';"""

js = js.replace(old_open_inv_2, new_open_inv_2)


old_open_inv_3 = """        document.getElementById('inventory-modal-title').textContent = 'Yeni Envanter';
    }
    openModal('inventory-modal');
};"""

new_open_inv_3 = """        document.getElementById('inventory-modal-title').textContent = 'Yeni Envanter';
    }
    populateInvCategoryDropdown(invCat);
    openModal('inventory-modal');
};"""

js = js.replace(old_open_inv_3, new_open_inv_3)


# Modify submitInventory to save the category
old_sub_inv = """    const newItem = {
        id: id || Date.now(),
        name: document.getElementById('inventory-name').value,
        amount: parseFloat(document.getElementById('inventory-amount').value),
        unit: document.getElementById('inventory-unit').value,
        critical: document.getElementById('inventory-critical').value ? parseFloat(document.getElementById('inventory-critical').value) : null,
        imgUrl: document.getElementById('inventory-img-url').value,
        lastUpdated: new Date().toISOString()
    };"""

new_sub_inv = """    const newItem = {
        id: id || Date.now(),
        name: document.getElementById('inventory-name').value,
        category: document.getElementById('inventory-category').value,
        amount: parseFloat(document.getElementById('inventory-amount').value),
        unit: document.getElementById('inventory-unit').value,
        critical: document.getElementById('inventory-critical').value ? parseFloat(document.getElementById('inventory-critical').value) : null,
        imgUrl: document.getElementById('inventory-img-url').value,
        lastUpdated: new Date().toISOString()
    };"""

js = js.replace(old_sub_inv, new_sub_inv)


with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)

print("Modal updated for inventory categories.")
