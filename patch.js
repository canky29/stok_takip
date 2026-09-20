function openModal(id) {
    const m = document.getElementById(id);
    if(m) m.classList.remove('hidden');
}
function closeModal(id) {
    const m = document.getElementById(id);
    if(m) m.classList.add('hidden');
}
window.openAddCategoryModal = () => openModal('add-category-modal');
window.closeAddCategoryModal = () => closeModal('add-category-modal');
window.openAddProductModal = () => openModal('add-product-modal');
window.closeAddProductModal = () => closeModal('add-product-modal');

window.submitNewProduct = (e) => {
    e.preventDefault();
    const name = document.getElementById('new-prod-name').value;
    const cat = document.getElementById('new-prod-category').value;
    const max = document.getElementById('new-prod-max').value;
    const stock = document.getElementById('new-prod-stock').value;
    
    let products = JSON.parse(localStorage.getItem('products') || '[]');
    products.push({ id: Date.now(), name, category: cat, maxStock: parseInt(max), stock: parseInt(stock), sales: 0, waste: 0 });
    localStorage.setItem('products', JSON.stringify(products));
    
    alert('Ürün başarıyla eklendi!');
    closeModal('add-product-modal');
    if(typeof renderProducts === 'function') renderProducts();
};

window.submitNewCategory = (e) => {
    e.preventDefault();
    const name = document.getElementById('new-category-name').value;
    
    let categories = JSON.parse(localStorage.getItem('categories') || '[]');
    if(!categories.includes(name)) {
        categories.push(name);
        localStorage.setItem('categories', JSON.stringify(categories));
    }
    
    // update select
    const sel = document.getElementById('new-prod-category');
    if(sel) {
        const opt = document.createElement('option');
        opt.value = name;
        opt.textContent = name;
        sel.appendChild(opt);
    }
    
    alert('Kategori başarıyla eklendi!');
    closeModal('add-category-modal');
    if(typeof renderProducts === 'function') renderProducts();
};
