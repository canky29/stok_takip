import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    content = f.read()

# 1. Update setRole to support RECIPE
def repl_setrole(match):
    original = match.group(0)
    if "'view-recipe'" not in original:
        original = original.replace("['view-home'", "['view-home', 'view-recipe'")
    return original

content = re.sub(r'const views = \[.*?\];', repl_setrole, content)

# 2. Add recipe logic functions
recipe_js = """
// --- RECIPE CALCULATOR MODULE ---
let currentRecipeProductId = null;

window.renderRecipeView = () => {
    // Populate Product Dropdown
    const select = document.getElementById('recipe-product-select');
    if(!select) return;
    
    const prods = JSON.parse(localStorage.getItem('products') || '[]');
    let currentVal = select.value;
    
    let html = '<option value="">-- Lütfen Ürün Seçin --</option>';
    
    // Group options by category
    const grouped = {};
    prods.forEach(p => {
        const cat = p.category || 'Diğer';
        if(!grouped[cat]) grouped[cat] = [];
        grouped[cat].push(p);
    });
    
    Object.keys(grouped).sort().forEach(cat => {
        html += `<optgroup label="${cat}">`;
        grouped[cat].sort((a,b) => a.name.localeCompare(b.name)).forEach(p => {
            html += `<option value="${p.id}">${p.name}</option>`;
        });
        html += `</optgroup>`;
    });
    
    select.innerHTML = html;
    if(currentVal && prods.find(p => String(p.id) === currentVal)) {
        select.value = currentVal;
    }
    
    loadRecipeForSelectedProduct(); // re-render ingredients
};

window.loadRecipeForSelectedProduct = () => {
    const select = document.getElementById('recipe-product-select');
    const panel = document.getElementById('recipe-info-panel');
    const totalPanel = document.getElementById('recipe-total-panel');
    const btnAdd = document.getElementById('btn-add-ingredient');
    
    const val = select.value;
    currentRecipeProductId = val;
    
    if(!val) {
        panel.classList.add('hidden');
        totalPanel.classList.add('hidden');
        btnAdd.disabled = true;
        document.getElementById('recipe-ingredients-tbody').innerHTML = `<tr><td colspan="4" class="p-8 text-center text-stone-400 font-bold">Önce sol taraftan bir ürün seçin.</td></tr>`;
        return;
    }
    
    btnAdd.disabled = false;
    panel.classList.remove('hidden');
    
    const prods = JSON.parse(localStorage.getItem('products') || '[]');
    const p = prods.find(x => String(x.id) === val);
    if(p) {
        document.getElementById('recipe-product-name').textContent = p.name;
        document.getElementById('recipe-product-old-cost').textContent = (parseFloat(p.costPrice) || 0).toFixed(2) + " ₺";
        document.getElementById('recipe-product-img').src = p.image || '';
    }
    
    renderRecipeIngredients();
};

window.renderRecipeIngredients = () => {
    if(!currentRecipeProductId) return;
    
    const tbody = document.getElementById('recipe-ingredients-tbody');
    const totalEl = document.getElementById('recipe-total-cost');
    const totalPanel = document.getElementById('recipe-total-panel');
    
    let allRecipes = JSON.parse(localStorage.getItem('recipes') || '{}');
    let productRecipe = allRecipes[currentRecipeProductId] || [];
    
    let inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
    
    let html = '';
    let grandTotal = 0;
    
    if(productRecipe.length === 0) {
        html = `<tr><td colspan="4" class="p-8 text-center text-stone-400 font-bold">Bu ürün için henüz reçete kalemi eklenmemiş.</td></tr>`;
        totalPanel.classList.add('hidden');
    } else {
        productRecipe.forEach((item, index) => {
            const invItem = inventory.find(inv => String(inv.id) === String(item.invId));
            
            let invName = 'Bilinmeyen Hammadde';
            let calculatedCost = 0;
            
            if(invItem) {
                invName = invItem.name;
                // Calculate unit cost
                // Assuming invItem has: price (Total price), qty (Total qty), unit (Total unit)
                // We need to convert both to a standard base (e.g., grams) if possible, or assume same unit family
                
                let basePricePerUnit = 0; // price per 1 smallest unit (e.g. 1 gram, 1 ml)
                
                const normalizeQty = (q, u) => {
                    q = parseFloat(q);
                    if(u === 'kg') return { val: q * 1000, base: 'g' };
                    if(u === 'L') return { val: q * 1000, base: 'ml' };
                    return { val: q, base: u };
                };
                
                const invNorm = normalizeQty(invItem.qty, invItem.unit);
                const recNorm = normalizeQty(item.qty, item.unit);
                
                if (invNorm.base === recNorm.base && invNorm.val > 0) {
                    basePricePerUnit = parseFloat(invItem.price) / invNorm.val;
                    calculatedCost = basePricePerUnit * recNorm.val;
                } else if (invNorm.base === 'adet' || recNorm.base === 'adet') {
                    // fallback if units don't strictly match but we can just divide
                     if (invItem.qty > 0) {
                         calculatedCost = (parseFloat(invItem.price) / parseFloat(invItem.qty)) * parseFloat(item.qty);
                     }
                }
            }
            
            grandTotal += calculatedCost;
            
            html += `
            <tr class="hover:bg-stone-50 transition border-b border-stone-100 last:border-0">
                <td class="py-3 px-2">
                    <div class="font-bold text-stone-800">${invName}</div>
                </td>
                <td class="py-3 px-2 text-center font-bold text-stone-600">
                    ${item.qty} ${item.unit}
                </td>
                <td class="py-3 px-2 text-right font-black text-indigo-600">
                    ₺${calculatedCost.toFixed(2)}
                </td>
                <td class="py-3 px-2 text-right">
                    <button onclick="removeRecipeIngredient(${index})" class="text-stone-400 hover:text-rose-500 transition" title="Kaldır">
                        <i data-lucide="trash-2" class="w-4 h-4"></i>
                    </button>
                </td>
            </tr>`;
        });
        totalPanel.classList.remove('hidden');
    }
    
    tbody.innerHTML = html;
    totalEl.textContent = grandTotal.toFixed(2) + " ₺";
    
    // store the running total globally so save button can use it
    window.currentRecipeGrandTotal = grandTotal;
    
    if(typeof lucide !== 'undefined') lucide.createIcons();
};

window.openRecipeIngredientModal = () => {
    const select = document.getElementById('recipe-inv-select');
    let inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
    
    let html = '<option value="">Seçim Yapın...</option>';
    inventory.sort((a,b) => a.name.localeCompare(b.name)).forEach(inv => {
        html += `<option value="${inv.id}">${inv.name} (${inv.qty} ${inv.unit} - ${inv.price} ₺)</option>`;
    });
    select.innerHTML = html;
    
    document.getElementById('recipe-ing-qty').value = '';
    document.getElementById('recipe-inv-hint').textContent = 'Malzeme seçtiğinizde envanterdeki birim fiyatı burada görünecektir.';
    
    openModal('add-ingredient-modal');
};

window.updateRecipeUnitLabels = () => {
    const select = document.getElementById('recipe-inv-select');
    const hint = document.getElementById('recipe-inv-hint');
    const unitSelect = document.getElementById('recipe-ing-unit');
    
    if(!select.value) {
        hint.textContent = 'Malzeme seçtiğinizde envanterdeki birim fiyatı burada görünecektir.';
        return;
    }
    
    let inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
    const inv = inventory.find(x => String(x.id) === select.value);
    
    if(inv) {
        const u = inv.unit.toLowerCase();
        let defaultU = 'g';
        if(u === 'kg' || u === 'g') defaultU = 'g';
        else if(u === 'l' || u === 'ml') defaultU = 'ml';
        else defaultU = 'adet';
        
        unitSelect.value = defaultU;
        
        let p = parseFloat(inv.price) || 0;
        let q = parseFloat(inv.qty) || 1;
        hint.innerHTML = `Bu hammaddenin envanter kayıt fiyatı: <b>${p} ₺ / ${q} ${inv.unit}</b>`;
    }
};

window.submitRecipeIngredient = (e) => {
    e.preventDefault();
    if(!currentRecipeProductId) return;
    
    const invId = document.getElementById('recipe-inv-select').value;
    const qty = document.getElementById('recipe-ing-qty').value;
    const unit = document.getElementById('recipe-ing-unit').value;
    
    if(!invId || !qty) return;
    
    let allRecipes = JSON.parse(localStorage.getItem('recipes') || '{}');
    if(!allRecipes[currentRecipeProductId]) allRecipes[currentRecipeProductId] = [];
    
    allRecipes[currentRecipeProductId].push({
        invId,
        qty: parseFloat(qty),
        unit
    });
    
    localStorage.setItem('recipes', JSON.stringify(allRecipes));
    closeModal('add-ingredient-modal');
    renderRecipeIngredients();
};

window.removeRecipeIngredient = (index) => {
    if(!currentRecipeProductId) return;
    let allRecipes = JSON.parse(localStorage.getItem('recipes') || '{}');
    if(allRecipes[currentRecipeProductId]) {
        allRecipes[currentRecipeProductId].splice(index, 1);
        localStorage.setItem('recipes', JSON.stringify(allRecipes));
        renderRecipeIngredients();
    }
};

window.saveRecipeCostToProduct = () => {
    if(!currentRecipeProductId) return;
    
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let p = prods.find(x => String(x.id) === currentRecipeProductId);
    if(p) {
        p.costPrice = window.currentRecipeGrandTotal;
        localStorage.setItem('products', JSON.stringify(prods));
        document.getElementById('recipe-product-old-cost').textContent = p.costPrice.toFixed(2) + " ₺";
        
        // Also re-render finance if it's there
        if(window.renderFinance) window.renderFinance();
        
        alert(`${p.name} için güncel maliyet ${p.costPrice.toFixed(2)} ₺ olarak başarıyla kaydedildi!`);
    }
};

"""
content += "\n" + recipe_js

# Ensure setRole calls renderRecipeView()
setrole_hook = """    if(role === 'HOME') renderHome();
    if(role === 'INVENTORY') renderInventory();
    if(role === 'RECIPE') renderRecipeView();"""

content = re.sub(r'if\(role === \'HOME\'\) renderHome\(\);\n\s*if\(role === \'INVENTORY\'\) renderInventory\(\);', setrole_hook, content)


with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(content)

print("JS logic injected.")
