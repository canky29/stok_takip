import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    content = f.read()

# We need to replace renderRecipeIngredients to make the price an input field
# and add a function updateRecipeItemCost(index, value)

new_render = """window.updateRecipeItemCost = (index, val) => {
    if(!currentRecipeProductId) return;
    let allRecipes = JSON.parse(localStorage.getItem('recipes') || '{}');
    if(allRecipes[currentRecipeProductId]) {
        let item = allRecipes[currentRecipeProductId][index];
        if(val === '' || isNaN(parseFloat(val))) {
            delete item.manualCost; // revert to auto calculation
        } else {
            item.manualCost = parseFloat(val);
        }
        localStorage.setItem('recipes', JSON.stringify(allRecipes));
        renderRecipeIngredients();
    }
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
                
                let basePricePerUnit = 0;
                
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
                     if (invItem.qty > 0) {
                         calculatedCost = (parseFloat(invItem.price) / parseFloat(invItem.qty)) * parseFloat(item.qty);
                     }
                }
            }
            
            // Override with manual cost if user provided one
            let finalCost = item.manualCost !== undefined ? parseFloat(item.manualCost) : calculatedCost;
            grandTotal += finalCost;
            
            let autoCalcHint = item.manualCost !== undefined ? 'title="Kendi girdiğiniz özel fiyat (Envanterden çekilmez)"' : 'title="Envanterden otomatik hesaplandı"';
            let iconColor = item.manualCost !== undefined ? 'text-amber-500' : 'text-indigo-600';
            
            html += `
            <tr class="hover:bg-stone-50 transition border-b border-stone-100 last:border-0 group">
                <td class="py-3 px-2">
                    <div class="font-bold text-stone-800">${invName}</div>
                </td>
                <td class="py-3 px-2 text-center font-bold text-stone-600">
                    ${item.qty} ${item.unit}
                </td>
                <td class="py-3 px-2 text-right">
                    <div class="flex justify-end items-center gap-2">
                        <i data-lucide="${item.manualCost !== undefined ? 'edit-3' : 'calculator'}" class="w-4 h-4 ${iconColor} opacity-50" ${autoCalcHint}></i>
                        <div class="relative w-24">
                            <div class="absolute inset-y-0 left-0 flex items-center pl-2 pointer-events-none text-stone-400 font-bold text-sm">₺</div>
                            <input type="number" step="0.01" min="0" onchange="updateRecipeItemCost(${index}, this.value)" value="${finalCost.toFixed(2)}" class="w-full bg-white border border-stone-200 hover:border-indigo-300 rounded-lg py-1.5 pl-6 pr-2 text-sm font-black text-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-right transition">
                        </div>
                    </div>
                </td>
                <td class="py-3 px-2 text-right">
                    <button onclick="removeRecipeIngredient(${index})" class="text-stone-300 hover:text-rose-500 transition" title="Kaldır">
                        <i data-lucide="trash-2" class="w-4 h-4"></i>
                    </button>
                </td>
            </tr>`;
        });
        totalPanel.classList.remove('hidden');
    }
    
    tbody.innerHTML = html;
    totalEl.textContent = grandTotal.toFixed(2) + " ₺";
    
    window.currentRecipeGrandTotal = grandTotal;
    
    if(typeof lucide !== 'undefined') lucide.createIcons();
};"""

# Replace window.renderRecipeIngredients with new code
content = re.sub(r'window\.renderRecipeIngredients\s*=\s*\(\)\s*=>\s*\{.*?(?=window\.openRecipeIngredientModal)', new_render, content, flags=re.DOTALL)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(content)

print("Updated recipe cost rendering!")
