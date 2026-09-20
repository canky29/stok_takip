import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

# Replace the whole block of renderInventory starting from displayList logic
old_logic_start = """    let displayList = inventory;
    if(search) {
        displayList = inventory.filter(r => 
            r.name.toLowerCase().includes(search) || 
            (r.notes || '').toLowerCase().includes(search)
        );
    }
    
    if(inventory.length === 0) {
        container.innerHTML = `<div class="col-span-full text-center py-12 text-stone-500 font-bold bg-white rounded-3xl border border-stone-200 shadow-sm flex flex-col items-center justify-center gap-2"><i data-lucide="package" class="w-10 h-10 text-stone-300"></i>Kayıt bulunamadı.</div>`;
        if(typeof lucide !== 'undefined') lucide.createIcons();
        return;
    }
    
    let html = '';
    
    let cats = getInvCategories();
    // Default category for items created before categories existed
    let uncatItems = inventory.filter(r => !r.category);"""

new_logic_start = """    let displayList = inventory;
    if(search) {
        displayList = inventory.filter(r => 
            r.name.toLowerCase().includes(search) || 
            (r.notes || '').toLowerCase().includes(search)
        );
    }
    
    let html = '';
    
    let cats = getInvCategories();
    // Use displayList instead of inventory so search works!
    let uncatItems = displayList.filter(r => !r.category);"""

js = js.replace(old_logic_start, new_logic_start)

# Replace the inner loop referencing `inventory` with `displayList`
old_loop = """    cats.forEach(c => {
        let items = inventory.filter(r => r.category === c);"""

new_loop = """    cats.forEach(c => {
        let items = displayList.filter(r => r.category === c);"""

js = js.replace(old_loop, new_loop)

# Also handle if EVERYTHING is empty after search, but wait, categories will render as empty
# So we don't need a global empty state, the empty categories look nice.
# But what if search is active and NO items match? 
# Maybe we shouldn't render empty categories IF search is active?
# Let's conditionally hide empty categories if search is active.
old_render = """        if(items.length > 0) {
            html += items.sort((a,b) => b.id - a.id).map(renderCard).join('');
        } else {
            html += `<div class="col-span-full py-8 text-center text-stone-400 font-bold bg-stone-50 rounded-2xl border border-stone-200 border-dashed">Bu kategoride henüz ürün bulunmuyor.</div>`;
        }
        html += `
            </div>
        </div>
        `;"""

new_render = """        if(items.length > 0) {
            html += items.sort((a,b) => b.id - a.id).map(renderCard).join('');
        } else if (!search) {
            html += `<div class="col-span-full py-8 text-center text-stone-400 font-bold bg-stone-50 rounded-2xl border border-stone-200 border-dashed">Bu kategoride henüz ürün bulunmuyor.</div>`;
        }
        
        // Hide entire category block if searching and it's empty
        if(items.length === 0 && search) {
            // we remove the block we just opened by undoing the string addition
            // this is a bit hacky in JS, let's just reconstruct the string
        }"""

# Actually, it's easier to just build the html inside the loop correctly.
