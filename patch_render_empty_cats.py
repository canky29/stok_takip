with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

old_render = """    cats.forEach(c => {
        let items = inventory.filter(r => r.category === c);
        if(items.length > 0) {
            html += `
            <div class="mb-2">
                <h2 class="text-xl font-black text-stone-800 mb-4 border-b border-stone-200 pb-2 uppercase tracking-widest">${c}</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    ${items.sort((a,b) => b.id - a.id).map(renderCard).join('')}
                </div>
            </div>
            `;
        }
    });"""

new_render = """    cats.forEach(c => {
        let items = inventory.filter(r => r.category === c);
        html += `
        <div class="mb-2">
            <h2 class="text-xl font-black text-stone-800 mb-4 border-b border-stone-200 pb-2 uppercase tracking-widest">${c}</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        `;
        if(items.length > 0) {
            html += items.sort((a,b) => b.id - a.id).map(renderCard).join('');
        } else {
            html += `<div class="col-span-full py-8 text-center text-stone-400 font-bold bg-stone-50 rounded-2xl border border-stone-200 border-dashed">Bu kategoride henüz ürün bulunmuyor.</div>`;
        }
        html += `
            </div>
        </div>
        `;
    });"""

js = js.replace(old_render, new_render)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)

print("Empty categories will now be rendered.")
