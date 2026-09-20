import re

with open('index.html', 'r') as f:
    html_content = f.read()

modal_html = """
    <!-- Custom Modal for Editing Category -->
    <div id="edit-category-modal" class="fixed inset-0 bg-stone-900/60 backdrop-blur-sm hidden flex items-center justify-center z-50">
        <div class="bg-stone-50 p-8 rounded shadow-2xl w-[28rem] max-w-[90vw] transform scale-95 transition-transform border border-stone-200">
            <div class="flex justify-between items-center mb-6 border-b border-stone-200 pb-4">
                <h3 class="text-2xl font-black text-stone-800">Kategori Düzenle</h3>
                <button onclick="closeEditCategoryModal()" class="text-stone-400 hover:text-stone-700"><i data-lucide="x" class="w-6 h-6"></i></button>
            </div>
            
            <form onsubmit="submitEditCategory(event)" class="flex flex-col gap-4">
                <input type="hidden" id="edit-category-old-name">
                <div>
                    <label class="block text-sm font-bold text-stone-700 mb-1">Yeni Kategori Adı</label>
                    <input type="text" id="edit-category-new-name" required class="w-full border border-stone-300 rounded bg-white p-3 font-medium focus:border-amber-600 focus:outline-none" placeholder="Örn: Yeni İsim...">
                </div>
                
                <button type="submit" class="w-full py-4 mt-2 bg-amber-600 text-white font-black rounded hover:bg-amber-700 shadow transition">
                    Kaydet
                </button>
            </form>
        </div>
    </div>
"""

# Insert the modal before the script tag at the end of the body
html_content = html_content.replace('    <script src="app_v4.js', modal_html + '\n    <script src="app_v4.js')

with open('index.html', 'w') as f:
    f.write(html_content)


with open('app_v4.js', 'r') as f:
    js_content = f.read()

new_js = """
window.closeEditCategoryModal = () => {
    const el = document.getElementById('edit-category-modal');
    if(el) el.classList.add('hidden');
};

window.editCategory = (oldName) => {
    document.getElementById('edit-category-old-name').value = oldName;
    document.getElementById('edit-category-new-name').value = oldName;
    const el = document.getElementById('edit-category-modal');
    if(el) el.classList.remove('hidden');
};

window.submitEditCategory = (e) => {
    e.preventDefault();
    const oldName = document.getElementById('edit-category-old-name').value;
    const newName = document.getElementById('edit-category-new-name').value;
    
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
    closeEditCategoryModal();
};
"""

# Replace the prompt-based editCategory with the custom modal-based one
js_content = re.sub(r'window\.editCategory = \(oldName\) => \{.*?(?=window\.deleteCategory =)', new_js, js_content, flags=re.DOTALL)

with open('app_v4.js', 'w') as f:
    f.write(js_content)

