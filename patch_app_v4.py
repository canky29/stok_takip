import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Add critical field to openInventoryModal
content = content.replace(
    "document.getElementById('inventory-amount').value = inv ? inv.amount : '';",
    "document.getElementById('inventory-amount').value = inv ? inv.amount : '';\n    document.getElementById('inventory-critical').value = inv ? (inv.critical || '') : '';"
)

# Add critical field to submitInventory
content = content.replace(
    "const amount = document.getElementById('inventory-amount').value;",
    "const amount = document.getElementById('inventory-amount').value;\n    const critical = document.getElementById('inventory-critical').value;"
)

content = content.replace(
    "inventory[index] = { ...inventory[index], name, amount, unit, notes, lastUpdated: new Date().toISOString() };",
    "inventory[index] = { ...inventory[index], name, amount, unit, critical, notes, lastUpdated: new Date().toISOString() };"
)

content = content.replace(
    """            amount,
            unit,
            notes,""",
    """            amount,
            unit,
            critical,
            notes,"""
)

# Add updateInventoryAmount function
update_func = """
window.updateInventoryAmount = (id, delta) => {
    let inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
    const index = inventory.findIndex(x => x.id === id);
    if(index > -1) {
        let newAmount = parseFloat(inventory[index].amount) + delta;
        if (newAmount < 0) newAmount = 0;
        inventory[index].amount = newAmount;
        inventory[index].lastUpdated = new Date().toISOString();
        localStorage.setItem('inventory', JSON.stringify(inventory));
        window.renderInventory();
    }
};
"""
content = content.replace("window.deleteInventory = (id) => {", update_func + "\nwindow.deleteInventory = (id) => {")

# Update renderInventory html
old_html_block = """        html += `
        <div class="bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] border border-stone-200/60 flex flex-col relative overflow-hidden transition duration-300 p-6 gap-5">
            <div class="flex items-start justify-between">
                <div>
                    <h3 class="text-xl font-black text-stone-800 tracking-tight leading-none mb-2">${r.name}</h3>
                    <div class="text-xs font-bold text-stone-400 flex items-center gap-1"><i data-lucide="clock" class="w-3.5 h-3.5"></i> Son G. ${dateStr}</div>
                </div>
                <div class="bg-amber-50 text-amber-600 px-3 py-1.5 rounded-xl border border-amber-200 text-lg font-black shadow-sm shrink-0 flex items-center gap-1">
                    ${r.amount} <span class="text-xs uppercase tracking-widest">${r.unit}</span>
                </div>
            </div>"""

new_html_block = """        let isCritical = false;
        let criticalBadge = '';
        let cardBorderClass = 'border-stone-200/60';
        if (r.critical && parseFloat(r.amount) <= parseFloat(r.critical)) {
            isCritical = true;
            cardBorderClass = 'border-rose-500 shadow-[0_0_15px_rgba(244,63,94,0.1)]';
            criticalBadge = `<div class="absolute -top-3 -right-3 bg-rose-500 text-white text-[10px] font-black uppercase tracking-widest py-4 px-6 rounded-bl-3xl shadow-md transform rotate-12 flex items-center gap-1"><i data-lucide="alert-triangle" class="w-3 h-3"></i> Kritik</div>`;
        }

        html += `
        <div class="bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] border ${cardBorderClass} flex flex-col relative overflow-hidden transition duration-300 p-6 gap-5">
            ${criticalBadge}
            <div class="flex items-start justify-between relative z-10">
                <div class="pr-8">
                    <h3 class="text-xl font-black text-stone-800 tracking-tight leading-none mb-2">${r.name}</h3>
                    <div class="text-xs font-bold text-stone-400 flex items-center gap-1"><i data-lucide="clock" class="w-3.5 h-3.5"></i> Son G. ${dateStr}</div>
                </div>
                <div class="flex flex-col items-end gap-2">
                    <div class="${isCritical ? 'bg-rose-50 text-rose-600 border-rose-200' : 'bg-amber-50 text-amber-600 border-amber-200'} px-3 py-1.5 rounded-xl border text-lg font-black shadow-sm shrink-0 flex items-center gap-1">
                        ${r.amount} <span class="text-xs uppercase tracking-widest">${r.unit}</span>
                    </div>
                    <div class="flex items-center gap-1 bg-stone-100 rounded-lg p-1 border border-stone-200">
                        <button onclick="updateInventoryAmount(${r.id}, -1)" class="w-8 h-8 flex items-center justify-center bg-white hover:bg-stone-200 text-stone-700 rounded transition font-black shadow-sm border border-stone-200">-</button>
                        <button onclick="updateInventoryAmount(${r.id}, 1)" class="w-8 h-8 flex items-center justify-center bg-white hover:bg-stone-200 text-stone-700 rounded transition font-black shadow-sm border border-stone-200">+</button>
                    </div>
                </div>
            </div>"""

content = content.replace(old_html_block, new_html_block)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w', encoding='utf-8') as f:
    f.write(content)
