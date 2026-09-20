with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

old_submit = """window.submitNewCategory = () => {
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
};"""

new_submit = """window.submitNewCategory = () => {
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
            closeNewCategoryModal();
        } else {
            showToast("Bu kategori zaten mevcut!", "error");
            // Do not close the modal, let them fix it
        }
    } else {
        showToast("Lütfen bir kategori adı girin.", "error");
    }
};"""

js = js.replace(old_submit, new_submit)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)

print("Submit logic updated with toasts.")
