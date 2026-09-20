import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

# Fix openInventoryModal
old_open = """    document.getElementById('inventory-img-url-input').value = imgUrlStr.startsWith('data:') ? '' : imgUrlStr;
    window.previewInventoryImageUrl(imgUrlStr);
    
    document.getElementById('inventory-modal').classList.remove('hidden');
};"""

new_open = """    document.getElementById('inventory-img-url-input').value = imgUrlStr.startsWith('data:') ? '' : imgUrlStr;
    window.previewInventoryImageUrl(imgUrlStr);
    
    populateInvCategoryDropdown(inv ? inv.category : '');
    
    document.getElementById('inventory-modal').classList.remove('hidden');
};"""

js = js.replace(old_open, new_open)

# Fix submitInventory
old_submit = """window.submitInventory = (e) => {
    e.preventDefault();
    const id = document.getElementById('inventory-id').value;
    const name = document.getElementById('inventory-name').value;
    const amount = document.getElementById('inventory-amount').value;
    const critical = document.getElementById('inventory-critical').value;
    const unit = document.getElementById('inventory-unit').value;
    const notes = document.getElementById('inventory-notes').value;
    const imgUrl = document.getElementById('inventory-img-url').value;
    
    let inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
    
    if(id) {
        const index = inventory.findIndex(x => x.id == id);
        if(index > -1) {
            inventory[index] = { ...inventory[index], name, amount, unit, critical, notes, imgUrl, lastUpdated: new Date().toISOString() };
        }
    } else {
        inventory.push({
            id: Date.now(),
            name,
            amount,
            unit,
            critical,
            notes,
            imgUrl,
            lastUpdated: new Date().toISOString()
        });
    }"""

new_submit = """window.submitInventory = (e) => {
    e.preventDefault();
    const id = document.getElementById('inventory-id').value;
    const name = document.getElementById('inventory-name').value;
    const amount = document.getElementById('inventory-amount').value;
    const critical = document.getElementById('inventory-critical').value;
    const unit = document.getElementById('inventory-unit').value;
    const notes = document.getElementById('inventory-notes').value;
    const imgUrl = document.getElementById('inventory-img-url').value;
    const category = document.getElementById('inventory-category').value;
    
    let inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
    
    if(id) {
        const index = inventory.findIndex(x => x.id == id);
        if(index > -1) {
            inventory[index] = { ...inventory[index], name, amount, unit, critical, notes, imgUrl, category, lastUpdated: new Date().toISOString() };
        }
    } else {
        inventory.push({
            id: Date.now(),
            name,
            amount,
            unit,
            critical,
            notes,
            imgUrl,
            category,
            lastUpdated: new Date().toISOString()
        });
    }"""

js = js.replace(old_submit, new_submit)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)
    
print("Fixed inventory modal to correctly populate and save categories.")
