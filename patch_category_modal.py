import re

with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    html = f.read()

new_modal_html = """
    <!-- New Category Modal -->
    <div id="new-category-modal" class="fixed inset-0 bg-stone-900/60 backdrop-blur-sm hidden flex items-center justify-center z-[120]">
        <div class="bg-white p-8 rounded-3xl shadow-2xl w-[24rem] max-w-[95vw] transform scale-95 transition-transform border border-stone-200">
            <h3 class="text-xl font-black text-stone-800 mb-4">Yeni Kategori Ekle</h3>
            <div class="space-y-4">
                <div>
                    <label class="block text-xs font-black text-stone-500 uppercase tracking-widest mb-1.5">Kategori Adı</label>
                    <input type="text" id="new-category-input" class="w-full bg-stone-50 border border-stone-200 rounded-xl px-4 py-3 font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-amber-500" placeholder="Örn: Temizlik">
                </div>
                <div class="flex gap-3 pt-2">
                    <button type="button" onclick="closeNewCategoryModal()" class="flex-1 bg-stone-100 hover:bg-stone-200 text-stone-600 font-bold py-3 rounded-xl transition">İptal</button>
                    <button type="button" onclick="submitNewCategory()" class="flex-1 bg-amber-600 hover:bg-amber-700 text-white font-bold py-3 rounded-xl shadow-lg shadow-amber-600/20 transition">Kaydet</button>
                </div>
            </div>
        </div>
    </div>
"""

if 'id="new-category-modal"' not in html:
    html = html.replace('<!-- Modal for Adding New Product -->', new_modal_html + '\n    <!-- Modal for Adding New Product -->')
    with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
        f.write(html)
        print("Category modal HTML injected.")

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

old_add_cat = """window.addNewInvCategory = () => {
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
};"""

new_add_cat = """window.addNewInvCategory = () => {
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

window.submitNewCategory = () => {
    let newCat = document.getElementById('new-category-input').value;
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
    closeNewCategoryModal();
};
// Bind enter key on input
document.addEventListener('DOMContentLoaded', () => {
    const catInput = document.getElementById('new-category-input');
    if(catInput) {
        catInput.addEventListener('keypress', (e) => {
            if(e.key === 'Enter') {
                e.preventDefault();
                submitNewCategory();
            }
        });
    }
});"""

js = js.replace(old_add_cat, new_add_cat)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)

print("Category modal JS applied.")
