window.openInventoryModal = (id = null) => {
    let inv = null;
    if(id) {
        const inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
        inv = inventory.find(x => x.id === id);
    }
    
    document.getElementById('inventory-id').value = inv ? inv.id : '';
    document.getElementById('inventory-name').value = inv ? inv.name : '';
    document.getElementById('inventory-amount').value = inv ? inv.amount : '';
    document.getElementById('inventory-unit').value = inv ? inv.unit : 'Adet';
    document.getElementById('inventory-notes').value = inv ? inv.notes : '';
    document.getElementById('inventory-modal-title').textContent = inv ? 'Envanter Ürünü Düzenle' : 'Yeni Ürün Ekle';
    
    document.getElementById('inventory-modal').classList.remove('hidden');
};

window.closeInventoryModal = () => {
    document.getElementById('inventory-modal').classList.add('hidden');
};

window.submitInventory = (e) => {
    e.preventDefault();
    const id = document.getElementById('inventory-id').value;
    const name = document.getElementById('inventory-name').value;
    const amount = document.getElementById('inventory-amount').value;
    const unit = document.getElementById('inventory-unit').value;
    const notes = document.getElementById('inventory-notes').value;
    
    let inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
    
    if(id) {
        const index = inventory.findIndex(x => x.id == id);
        if(index > -1) {
            inventory[index] = { ...inventory[index], name, amount, unit, notes, lastUpdated: new Date().toISOString() };
        }
    } else {
        inventory.push({
            id: Date.now(),
            name,
            amount,
            unit,
            notes,
            lastUpdated: new Date().toISOString()
        });
    }
    
    localStorage.setItem('inventory', JSON.stringify(inventory));
    window.closeInventoryModal();
    window.renderInventory();
};

window.deleteInventory = (id) => {
    window.openConfirmModal('Silme Onayı', 'Bu envanter kaydını silmek istediğinize emin misiniz? Bu işlem geri alınamaz.', 'Evet, Sil', () => {
        let inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
        inventory = inventory.filter(x => x.id !== id);
        localStorage.setItem('inventory', JSON.stringify(inventory));
        window.renderInventory();
        window.closeConfirmModal();
    });
};

window.renderInventory = () => {
    const container = document.getElementById('inventory-container');
    if(!container) return;
    
    let inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
    const search = (document.getElementById('inventory-search')?.value || '').toLowerCase();
    
    if(search) {
        inventory = inventory.filter(r => 
            (r.name || '').toLowerCase().includes(search) || 
            (r.notes || '').toLowerCase().includes(search)
        );
    }
    
    if(inventory.length === 0) {
        container.innerHTML = `<div class="col-span-full text-center py-12 text-stone-500 font-bold bg-white rounded-3xl border border-stone-200 shadow-sm flex flex-col items-center justify-center gap-2"><i data-lucide="package" class="w-10 h-10 text-stone-300"></i>Kayıt bulunamadı.</div>`;
        if(typeof lucide !== 'undefined') lucide.createIcons();
        return;
    }
    
    let html = '';
    inventory.sort((a,b) => b.id - a.id).forEach(r => {
        const dateStr = r.lastUpdated ? new Date(r.lastUpdated).toLocaleDateString('tr-TR', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : '';
        
        html += `
        <div class="bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] border border-stone-200/60 flex flex-col relative overflow-hidden transition duration-300 p-6 gap-5">
            <div class="flex items-start justify-between">
                <div>
                    <h3 class="text-xl font-black text-stone-800 tracking-tight leading-none mb-2">${r.name}</h3>
                    <div class="text-xs font-bold text-stone-400 flex items-center gap-1"><i data-lucide="clock" class="w-3.5 h-3.5"></i> Son G. ${dateStr}</div>
                </div>
                <div class="bg-amber-50 text-amber-600 px-3 py-1.5 rounded-xl border border-amber-200 text-lg font-black shadow-sm shrink-0 flex items-center gap-1">
                    ${r.amount} <span class="text-xs uppercase tracking-widest">${r.unit}</span>
                </div>
            </div>
            
            ${r.notes ? `
            <div class="text-sm font-medium text-stone-600 bg-stone-50 p-3.5 rounded-xl border border-stone-200 flex items-start gap-2.5">
                <i data-lucide="info" class="w-4 h-4 mt-0.5 text-stone-400 shrink-0"></i> 
                <span class="leading-relaxed italic">"${r.notes}"</span>
            </div>` : '<div class="flex-1"></div>'}
            
            <div class="mt-auto pt-4 border-t border-stone-100 flex gap-2">
                <button onclick="openInventoryModal(${r.id})" class="flex-1 bg-stone-50 hover:bg-stone-100 text-stone-600 font-black py-3 rounded-2xl transition active:scale-95 flex items-center justify-center gap-2 text-sm border border-stone-200 shadow-sm">
                    <i data-lucide="edit-2" class="w-4 h-4"></i> Düzenle
                </button>
                <button onclick="deleteInventory(${r.id})" class="bg-rose-50 hover:bg-rose-600 hover:text-white text-rose-600 p-3 rounded-2xl transition border border-rose-200 shadow-sm">
                    <i data-lucide="trash-2" class="w-5 h-5"></i>
                </button>
            </div>
        </div>
        `;
    });
    container.innerHTML = html;
    if(typeof lucide !== 'undefined') lucide.createIcons();
};
