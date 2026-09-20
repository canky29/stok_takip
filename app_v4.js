
window.exportDatabase = () => {
    const backup = {};
    for(let i=0; i<localStorage.length; i++) {
        let key = localStorage.key(i);
        backup[key] = localStorage.getItem(key);
    }
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(backup));
    const dlAnchorElem = document.createElement('a');
    dlAnchorElem.setAttribute("href", dataStr);
    const date = new Date().toISOString().split('T')[0];
    dlAnchorElem.setAttribute("download", `patuli_yedek_${date}.json`);
    dlAnchorElem.click();
    window.showToast("Yedek dosyası bilgisayarınıza indirildi.", "success");
};

window.importDatabase = (input) => {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                const data = JSON.parse(e.target.result);
                window.openConfirmModal('Yedek Yükleme', 'Mevcut tüm sistem verileri silinecek ve seçtiğiniz dosyadaki veriler yüklenecek. Onaylıyor musunuz?', 'Evet, Yükle', () => {
                    localStorage.clear();
                    for(let key in data) {
                        localStorage.setItem(key, data[key]);
                    }
                    window.closeConfirmModal();
                    window.showToast("Yedek başarıyla yüklendi! Sayfa yenileniyor...", "success");
                    setTimeout(() => window.location.reload(), 1500);
                });
            } catch (err) {
                console.error(err);
                window.showToast("Dosya okunamadı veya geçersiz format.", "error");
            }
            input.value = '';
        };
        reader.readAsText(input.files[0]);
    }
};


// --- QUOTA FIX AGGRESSIVE ---
(function() {
    try {
        // Nuke all base64 images from inventory
        const inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
        let modified = false;
        inventory.forEach(item => {
            if (item.imgUrl && item.imgUrl.startsWith('data:image')) {
                item.imgUrl = '';
                modified = true;
            }
        });
        if (modified) {
            localStorage.setItem('inventory', JSON.stringify(inventory));
        }
        
        // Nuke all base64 images from products
        const prods = JSON.parse(localStorage.getItem('products') || '[]');
        let pmod = false;
        prods.forEach(item => {
            if (item.image && item.image.startsWith('data:image')) {
                item.image = ''; // Reset to default or empty
                pmod = true;
            }
        });
        if (pmod) {
            localStorage.setItem('products', JSON.stringify(prods));
        }
    } catch(e) {
        console.error("Aggressive quota fix failed", e);
    }
})();
// -----------------


// PERSONNEL & EXPENSES LOGIC
window.openPersonnelModal = () => {
    document.getElementById('personnel-modal').classList.remove('hidden');
    document.getElementById('personnel-name').value = '';
    document.getElementById('personnel-desc').value = '';
    document.getElementById('personnel-amount').value = '';
    document.querySelector('input[name="personnel_type"][value="AVANS"]').checked = true;
    window.togglePersonnelTypeUI();
};

window.togglePersonnelTypeUI = () => {
    const isAvans = document.querySelector('input[name="personnel_type"]:checked').value === 'AVANS';
    document.getElementById('lbl-personnel-name').innerText = isAvans ? 'Personel Adı' : 'Tedarikçi / Kurum Adı';
    document.getElementById('personnel-desc').placeholder = isAvans ? 'Örn: Maaş avansı vb.' : 'Örn: Baklava alımı, malzeme ödemesi vb.';
    
    if(isAvans) {
        document.getElementById('personnel-name').classList.remove('hidden');
        document.getElementById('supplier-select-wrapper').classList.add('hidden');
        document.getElementById('supplier-select').classList.remove('ring-orange-500');
        document.getElementById('personnel-name').classList.add('ring-cyan-500');
    } else {
        document.getElementById('personnel-name').classList.add('hidden');
        document.getElementById('supplier-select-wrapper').classList.remove('hidden');
        document.getElementById('personnel-name').classList.remove('ring-cyan-500');
        document.getElementById('supplier-select').classList.add('ring-orange-500');
        window.renderSupplierOptions();
    }
};

window.renderSupplierOptions = (selectVal = null) => {
    const select = document.getElementById('supplier-select');
    if(!select) return;
    const suppliers = JSON.parse(localStorage.getItem('suppliers') || '[]');
    let html = `<option value="">-- Tedarikçi Seçiniz --</option>`;
    suppliers.forEach(s => {
        html += `<option value="${s.id}">${s.name}</option>`;
    });
    select.innerHTML = html;
    if(selectVal) select.value = selectVal;
};

window.addNewSupplierPrompt = () => {
    document.getElementById('new-supplier-input').value = '';
    document.getElementById('new-supplier-modal').classList.remove('hidden');
    setTimeout(() => document.getElementById('new-supplier-input').focus(), 100);
};

window.submitNewSupplier = (e) => {
    e.preventDefault();
    const name = document.getElementById('new-supplier-input').value.trim();
    if(name.length > 0) {
        const suppliers = JSON.parse(localStorage.getItem('suppliers') || '[]');
        const newSupplier = { id: Date.now().toString(), name: name };
        suppliers.push(newSupplier);
        localStorage.setItem('suppliers', JSON.stringify(suppliers));
        window.showToast(name + " tedarikçilere eklendi.");
        window.renderSupplierOptions(newSupplier.id);
        if(window.closeModal) window.closeModal('new-supplier-modal');
        else document.getElementById('new-supplier-modal').classList.add('hidden');
    }
};

window.submitPersonnelRecord = (e) => {
    e.preventDefault();
    const type = document.querySelector('input[name="personnel_type"]:checked').value;
    let name = '';
    
    if(type === 'AVANS') {
        name = document.getElementById('personnel-name').value.trim();
    } else {
        const select = document.getElementById('supplier-select');
        if(select.value) {
            name = select.options[select.selectedIndex].text;
        }
    }
    
    const desc = document.getElementById('personnel-desc').value.trim();
    const amount = parseFloat(document.getElementById('personnel-amount').value);
    
    if(!name || isNaN(amount) || amount <= 0) {
        window.showToast("Lütfen tüm alanları doldurun.", "error");
        return;
    }
    
    let records = JSON.parse(localStorage.getItem('personnel_records') || '[]');
    records.push({
        id: Date.now().toString(),
        date: new Date().toISOString(),
        type: type,
        name: name,
        desc: desc,
        amount: amount
    });
    localStorage.setItem('personnel_records', JSON.stringify(records));
    
    window.closeModal('personnel-modal');
    window.showToast(type === 'AVANS' ? 'Personel avansı kaydedildi.' : 'Dış gider kaydedildi.');
    window.renderPersonnelRecords();
    window.renderB2BRecords();
};

let pendingDeleteId = null;

window.deletePersonnelRecord = (id) => {
    pendingDeleteId = id;
    window.deleteContext = 'PERSONNEL';
    document.getElementById('finance-password-verify-view').classList.remove('hidden');
    document.getElementById('finance-password-change-view').classList.add('hidden');
    document.getElementById('finance-password-input').value = '';
    document.getElementById('finance-password-modal').classList.remove('hidden');
    setTimeout(() => document.getElementById('finance-password-input').focus(), 100);
};

window.deleteContext = 'PERSONNEL'; // Default
window.submitFinancePassword = (e) => {
    e.preventDefault();
    const pwd = document.getElementById('finance-password-input').value;
    const correctPass = localStorage.getItem('financeDeletePassword') || '12345';
    
    if(pwd === correctPass) {
        window.closeModal('finance-password-modal');
        
        if(window.deleteContext === 'B2B' && pendingB2BDeleteId) {
            window.openConfirmModal(
                'Kaydı Sil', 
                'Bu cari işlemi kalıcı olarak silmek istediğinize emin misiniz?',
                'Evet, Sil',
                () => {
                    let records = JSON.parse(localStorage.getItem('b2b_records') || '[]');
                    records = records.filter(r => String(r.id) !== String(pendingB2BDeleteId));
                    localStorage.setItem('b2b_records', JSON.stringify(records));
                    
                    if(window.closeConfirmModal) window.closeConfirmModal();
                    window.showToast('Cari kayıt silindi.');
                    window.renderB2BRecords();
                    pendingB2BDeleteId = null;
                }
            );
        }
        else if(pendingDeleteId) {
            window.openConfirmModal(
                'Kaydı Sil', 
                'Bu avans / gider kaydını kalıcı olarak silmek istediğinize emin misiniz?',
                'Evet, Sil',
                () => {
                    let records = JSON.parse(localStorage.getItem('personnel_records') || '[]');
                    records = records.filter(r => String(r.id) !== String(pendingDeleteId));
                    localStorage.setItem('personnel_records', JSON.stringify(records));
                    
                    if(window.closeConfirmModal) window.closeConfirmModal();
                    window.showToast('Kayıt başarıyla silindi.');
                    window.renderPersonnelRecords();
    window.renderB2BRecords();
                    pendingDeleteId = null;
                }
            );
        }
    } else {
        window.showToast("Hatalı şifre! İşlem iptal edildi.", "error");
        document.getElementById('finance-password-input').value = '';
        document.getElementById('finance-password-input').focus();
    }
};

window.changeFinanceDeletePassword = () => {
    document.getElementById('finance-password-verify-view').classList.add('hidden');
    document.getElementById('finance-password-change-view').classList.remove('hidden');
    document.getElementById('change-finance-old').value = '';
    document.getElementById('change-finance-new').value = '';
    document.getElementById('finance-password-modal').classList.remove('hidden');
    setTimeout(() => document.getElementById('change-finance-old').focus(), 100);
};

window.submitChangeFinancePassword = (e) => {
    e.preventDefault();
    const oldP = document.getElementById('change-finance-old').value;
    const newP = document.getElementById('change-finance-new').value;
    const currentPass = localStorage.getItem('financeDeletePassword') || '12345';
    
    if(oldP !== currentPass) {
        window.showToast("Mevcut şifre hatalı!", "error");
        return;
    }
    
    if(newP.trim() === '') return;
    
    localStorage.setItem('financeDeletePassword', newP.trim());
    window.closeModal('finance-password-modal');
    window.showToast("Kayıt silme şifreniz güncellendi.");
};

window.renderPersonnelRecords = () => {
    const tbody = document.getElementById('personnel-records-tbody');
    const statPersonnel = document.getElementById('stat-personnel-advances');
    const statSupplier = document.getElementById('stat-supplier-expenses');
    const homeStat = document.getElementById('home-stat-personnel');
    const filterMonth = document.getElementById('personnel-filter-month');
    
    if(!tbody) return;
    
    let records = JSON.parse(localStorage.getItem('personnel_records') || '[]');
    
    // Sort descending by date
    records.sort((a,b) => new Date(b.date) - new Date(a.date));
    
    // Populate filter dropdown if empty
    if(filterMonth.options.length <= 1) {
        let months = new Set();
        records.forEach(r => {
            const d = new Date(r.date);
            months.add(`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}`);
        });
        const sortedMonths = Array.from(months).sort().reverse();
        sortedMonths.forEach(m => {
            const opt = document.createElement('option');
            opt.value = m;
            const [y, mo] = m.split('-');
            const monthNames = ['Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık'];
            opt.innerText = `${monthNames[parseInt(mo)-1]} ${y}`;
            filterMonth.appendChild(opt);
        });
    }
    
    const selectedMonth = filterMonth.value;
    if(selectedMonth !== 'all') {
        records = records.filter(r => {
            const d = new Date(r.date);
            const mStr = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}`;
            return mStr === selectedMonth;
        });
    }
    
    const searchInput = document.getElementById('personnel-search-input');
    if(searchInput && searchInput.value.trim() !== '') {
        const query = searchInput.value.trim().toLowerCase();
        records = records.filter(r => {
            return (r.name && r.name.toLowerCase().includes(query)) || 
                   (r.desc && r.desc.toLowerCase().includes(query));
        });
    }
    
    let totalAvans = 0;
    let totalGider = 0;
    
    let html = '';
    if(records.length === 0) {
        html = `<tr><td colspan="6" class="p-8 text-center text-stone-400 font-bold">Kayıt bulunamadı.</td></tr>`;
    } else {
        records.forEach(r => {
            if(r.type === 'AVANS') totalAvans += r.amount;
            else if(r.type === 'TEDARIKCI') totalGider += r.amount;
            
            const dateStr = new Date(r.date).toLocaleDateString('tr-TR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });
            
            html += `
                <tr class="hover:bg-stone-50/50 transition">
                    <td class="py-4 px-6 text-stone-600 font-bold whitespace-nowrap">${dateStr}</td>
                    <td class="py-4 px-6">
                        ${r.type === 'AVANS' 
                            ? `<span class="bg-cyan-50 text-cyan-700 px-2.5 py-1 rounded-lg text-xs font-black border border-cyan-100">Avans</span>`
                            : `<span class="bg-orange-50 text-orange-700 px-2.5 py-1 rounded-lg text-xs font-black border border-orange-100">Dış Gider</span>`
                        }
                    </td>
                    <td class="py-4 px-6 font-black text-stone-800">${r.name}</td>
                    <td class="py-4 px-6 text-stone-500">${r.desc || '-'}</td>
                    <td class="py-4 px-6 text-right font-black ${r.type === 'AVANS' ? 'text-cyan-600' : 'text-orange-600'}">${r.amount.toFixed(2)} ₺</td>
                    <td class="py-4 px-6 text-center">
                        <button onclick="window.deletePersonnelRecord('${r.id}')" class="w-8 h-8 rounded-lg bg-stone-100 hover:bg-red-100 text-stone-500 hover:text-red-600 flex items-center justify-center mx-auto transition">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
    }
    
    tbody.innerHTML = html;
    if(statPersonnel) statPersonnel.innerText = totalAvans.toFixed(2) + ' ₺';
    if(statSupplier) statSupplier.innerText = totalGider.toFixed(2) + ' ₺';
    
    const titleAvans = document.getElementById('title-personnel-advances');
    const titleSupplier = document.getElementById('title-supplier-expenses');
    if (searchInput && searchInput.value.trim() !== '') {
        if(titleAvans) titleAvans.innerText = 'Avans Toplamı (Arama)';
        if(titleSupplier) titleSupplier.innerText = 'Gider Toplamı (Arama)';
    } else {
        if(titleAvans) titleAvans.innerText = 'Toplam Personel Avansı';
        if(titleSupplier) titleSupplier.innerText = 'Toplam Dış Gider (Tedarikçi)';
    }
    
    // Update home stat (all time count)
    if(homeStat) {
        const allRecords = JSON.parse(localStorage.getItem('personnel_records') || '[]');
        homeStat.innerText = `${allRecords.length} Avans / Gider`;
    }
    
    if(typeof lucide !== 'undefined') lucide.createIcons();
};


let pendingRole = null;

window.getInvCategories = () => {
    let cats = localStorage.getItem('invCategories');
    if(!cats) {
        cats = ['Un', 'İmalathane', 'Meşrubat', 'Kutu'];
        localStorage.setItem('invCategories', JSON.stringify(cats));
    } else {
        cats = JSON.parse(cats);
    }
    return cats;
};

window.editingInvCategory = null;

window.addNewInvCategory = () => {
    window.editingInvCategory = null;
    const title = document.getElementById('new-category-modal-title');
    const btn = document.getElementById('new-category-submit-btn');
    if(title) title.textContent = 'Yeni Kategori Ekle';
    if(btn) btn.textContent = 'Ekle';
    
    document.getElementById('new-category-input').value = '';
    const el = document.getElementById('new-category-modal');
    if(el) {
        el.classList.remove('hidden');
        setTimeout(() => {
            document.getElementById('new-category-input').focus();
        }, 100);
    }
};

window.editInvCategory = (oldCat) => {
    window.editingInvCategory = oldCat;
    const title = document.getElementById('new-category-modal-title');
    const btn = document.getElementById('new-category-submit-btn');
    if(title) title.textContent = 'Kategoriyi Düzenle';
    if(btn) btn.textContent = 'Güncelle';
    
    document.getElementById('new-category-input').value = oldCat;
    const el = document.getElementById('new-category-modal');
    if(el) {
        el.classList.remove('hidden');
        setTimeout(() => {
            document.getElementById('new-category-input').focus();
        }, 100);
    }
};

window.deleteInvCategory = (cat) => {
    window.openConfirmModal('Kategoriyi Sil', `"${cat}" kategorisini silmek istediğinize emin misiniz? (Bu kategorideki ürünler "Kategorisiz" olarak işaretlenecektir.)`, 'Evet, Sil', () => {
        let cats = getInvCategories();
        cats = cats.filter(c => c !== cat);
        localStorage.setItem('invCategories', JSON.stringify(cats));
        
        let inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
        let updated = false;
        inventory.forEach(r => {
            if(r.category === cat) {
                r.category = ""; // make it uncategorized
                updated = true;
            }
        });
        if(updated) {
            localStorage.setItem('inventory', JSON.stringify(inventory));
        }
        
        populateInvCategoryDropdown();
        window.closeConfirmModal();
        renderInventory();
        showToast("Kategori silindi.", "success");
    });
};

window.closeNewCategoryModal = () => {
    const el = document.getElementById('new-category-modal');
    if(el) el.classList.add('hidden');
    window.editingInvCategory = null;
};

window.submitNewInvCategory = () => {
    let newCat = document.getElementById('new-category-input').value;
    if(newCat && newCat.trim() !== '') {
        newCat = newCat.trim();
        let cats = getInvCategories();
        
        // Case-insensitive check
        const exists = cats.find(c => c.toLowerCase() === newCat.toLowerCase());
        
        if(!exists || exists === window.editingInvCategory) {
            if(window.editingInvCategory) {
                // UPDATE MODE
                const idx = cats.indexOf(window.editingInvCategory);
                if(idx > -1) cats[idx] = newCat;
                localStorage.setItem('invCategories', JSON.stringify(cats));
                
                // Update products in inventory
                let inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
                let updated = false;
                inventory.forEach(r => {
                    if(r.category === window.editingInvCategory) {
                        r.category = newCat;
                        updated = true;
                    }
                });
                if(updated) {
                    localStorage.setItem('inventory', JSON.stringify(inventory));
                }
                
                showToast("Kategori güncellendi!", "success");
            } else {
                // CREATE MODE
                cats.push(newCat);
                localStorage.setItem('invCategories', JSON.stringify(cats));
                showToast("Yeni kategori başarıyla eklendi!", "success");
            }
            
            populateInvCategoryDropdown();
            closeNewCategoryModal(); 
            renderInventory();
        } else {
            showToast("Bu kategori zaten mevcut!", "error");
        }
    } else {
        showToast("Lütfen bir kategori adı girin.", "error");
    }
};
// Bind enter key on input
document.addEventListener('DOMContentLoaded', () => {
    const catInput = document.getElementById('new-category-input');
    if(catInput) {
        catInput.addEventListener('keypress', (e) => {
            if(e.key === 'Enter') {
                e.preventDefault();
                submitNewInvCategory();
            }
        });
    }
});

window.populateInvCategoryDropdown = (selectedValue = '') => {
    const sel = document.getElementById('inventory-category');
    if(!sel) return;
    let cats = getInvCategories();
    let opts = '';
    cats.forEach(c => opts += `<option value="${c}">${c}</option>`);
    sel.innerHTML = opts;
    if(selectedValue && cats.includes(selectedValue)) {
        sel.value = selectedValue;
    }
};


window.toggleAuthMode = (mode) => {
    if(mode === 'CHANGE') {
        document.getElementById('auth-login-view').classList.add('hidden');
        document.getElementById('auth-change-view').classList.remove('hidden');
        document.getElementById('change-old-password').value = '';
        document.getElementById('change-new-password').value = '';
        document.getElementById('change-new-password-confirm').value = '';
        document.getElementById('change-old-password').focus();
    } else {
        document.getElementById('auth-change-view').classList.add('hidden');
        document.getElementById('auth-login-view').classList.remove('hidden');
        document.getElementById('auth-password').value = '';
        document.getElementById('auth-password').focus();
    }
};

window.submitChangePassword = (e) => {
    e.preventDefault();
    const oldPass = document.getElementById('change-old-password').value;
    const newPass = document.getElementById('change-new-password').value;
    const confirmPass = document.getElementById('change-new-password-confirm').value;
    
    const correctPass = localStorage.getItem('adminPassword') || '1234';
    
    if(oldPass !== correctPass) {
        showToast('Eski şifrenizi yanlış girdiniz!', 'error');
        return;
    }
    
    if(newPass.length < 4) {
        showToast('Yeni şifre en az 4 karakter olmalıdır.', 'error');
        return;
    }
    
    if(newPass !== confirmPass) {
        showToast('Yeni şifreler birbiriyle eşleşmiyor!', 'error');
        return;
    }
    
    localStorage.setItem('adminPassword', newPass);
    showToast('Şifreniz başarıyla değiştirildi! Yeni şifreyle giriş yapabilirsiniz.', 'success');
    toggleAuthMode('LOGIN');
};


window.closeAuthModal = () => {
    const el = document.getElementById('auth-modal');
    if(el) el.classList.add('hidden');
    pendingRole = null;
};

window.submitAuth = (e) => {
    e.preventDefault();
    const pass = document.getElementById('auth-password').value;
    const correctPass = localStorage.getItem('adminPassword') || '1234';
    
    if(pass === correctPass) {
        const roleToLoad = pendingRole;
        closeAuthModal();
        showToast('Giriş başarılı, yetki onaylandı.', 'success');
        if(roleToLoad) {
            window.setRole(roleToLoad, true);
            
            const accessKeys = {
                'PERSONNEL': 'lastPersonnelAccess',
                'FINANCE': 'lastFinanceAccess',
                'RECIPE': 'lastRecipeAccess',
                'B2B': 'lastB2BAccess'
            };
            
            if(accessKeys[roleToLoad]) {
                const storageKey = accessKeys[roleToLoad];
                const lastAccess = localStorage.getItem(storageKey);
                const nowStr = new Date().toLocaleDateString('tr-TR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });
                
                if (lastAccess) {
                    let pageName = "";
                    if(roleToLoad === 'PERSONNEL') pageName = "Personel & Gider Takibi";
                    else if(roleToLoad === 'FINANCE') pageName = "Maliyet & Kar Analizi";
                    else if(roleToLoad === 'RECIPE') pageName = "Reçete Hesaplama";
                    else if(roleToLoad === 'B2B') pageName = "Müşteri Cari & Toptancı";
                    
                    document.getElementById('access-info-time').innerHTML = `<span class="block text-xs font-bold text-stone-400 mb-1">${pageName}</span>${lastAccess}`;
                    document.getElementById('access-info-modal').classList.remove('hidden');
                }
                
                localStorage.setItem(storageKey, nowStr);
            }
        }
    } else {
        showToast('Hatalı şifre!', 'error');
        document.getElementById('auth-password').value = '';
    }
};


// --- TOAST NOTIFICATIONS ---
window.showToast = (message, type = 'success') => {
    const container = document.getElementById('toast-container');
    if(!container) return;
    
    const toast = document.createElement('div');
    
    // Style variations based on type
    let bgClass = 'bg-stone-900 text-white';
    let icon = '<i data-lucide="check-circle-2" class="w-5 h-5 text-emerald-400"></i>';
    
    if (type === 'error') {
        bgClass = 'bg-rose-600 text-white';
        icon = '<i data-lucide="alert-circle" class="w-5 h-5 text-white"></i>';
    } else if (type === 'info') {
        bgClass = 'bg-indigo-600 text-white';
        icon = '<i data-lucide="info" class="w-5 h-5 text-white"></i>';
    }

    toast.className = `flex items-center gap-3 px-6 py-4 rounded-full shadow-2xl transform transition-all duration-500 translate-y-[-20px] opacity-0 ${bgClass}`;
    
    // Preserve line breaks for messages with 

    const formattedMessage = message.replace(/\n/g, '<br>');
    
    toast.innerHTML = `
        ${icon}
        <span class="font-bold text-sm leading-tight">${formattedMessage}</span>
    `;
    
    container.appendChild(toast);
    
    if(typeof lucide !== 'undefined') lucide.createIcons();
    
    // Animate in
    requestAnimationFrame(() => {
        toast.classList.remove('translate-y-[-20px]', 'opacity-0');
        toast.classList.add('translate-y-0', 'opacity-100');
    });
    
    // Animate out and remove
    setTimeout(() => {
        toast.classList.remove('translate-y-0', 'opacity-100');
        toast.classList.add('translate-y-[-20px]', 'opacity-0');
        setTimeout(() => toast.remove(), 500);
    }, 3500);
};


let confirmCallback = null;

window.openConfirmModal = (title, desc, confirmText, callback) => {
    document.getElementById('confirm-modal-title').textContent = title;
    document.getElementById('confirm-modal-desc').textContent = desc;
    document.getElementById('confirm-modal-btn').textContent = confirmText || 'Evet, Onaylıyorum';
    confirmCallback = callback;
    
    const modal = document.getElementById('confirm-modal');
    const content = document.getElementById('confirm-modal-content');
    modal.classList.remove('hidden');
    setTimeout(() => content.classList.replace('scale-95', 'scale-100'), 10);
    if(typeof lucide !== 'undefined') lucide.createIcons();
};

window.closeConfirmModal = () => {
    const modal = document.getElementById('confirm-modal');
    const content = document.getElementById('confirm-modal-content');
    content.classList.replace('scale-100', 'scale-95');
    setTimeout(() => modal.classList.add('hidden'), 200);
    confirmCallback = null;
};

window.executeConfirmCallback = () => {
    if(confirmCallback) confirmCallback();
};


window.updateDashboard = () => {
    const prods = JSON.parse(localStorage.getItem('products') || '[]');
    const cats = JSON.parse(localStorage.getItem('categories') || '[]');
    const orders = JSON.parse(localStorage.getItem('orders') || '[]');
    
    let criticalCount = 0;
    prods.forEach(p => {
        const pct = Math.min(100, Math.round((p.stock / (p.maxStock || 1)) * 100));
        if(pct <= 20) criticalCount++;
    });
    
    const e1 = document.getElementById('stat-total-products'); if(e1) e1.textContent = prods.length;
    const e2 = document.getElementById('stat-total-categories'); if(e2) e2.textContent = cats.length;
    const e3 = document.getElementById('stat-critical-products'); if(e3) e3.textContent = criticalCount;
    const e4 = document.getElementById('stat-urgent-requests'); if(e4) e4.textContent = orders.length;

    // Home view specific cards
    const h1 = document.getElementById('home-stat-products'); if(h1) h1.innerHTML = prods.length + ' Ürün';
    const h2 = document.getElementById('home-stat-critical'); if(h2) h2.innerHTML = criticalCount + ' Kritik';
    const h3 = document.getElementById('home-stat-orders'); if(h3) h3.innerHTML = '<span class="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span> ' + orders.length + ' Bekleyen Talep';
};


let currentFilter = 'ALL';
window.setStockFilter = (filter) => {
    currentFilter = filter;
    
    // Update button styles
    const filters = ['ALL', 'CRITICAL', 'EMPTY', 'NORMAL'];
    filters.forEach(f => {
        const btn = document.getElementById('filter-btn-' + f);
        if(!btn) return;
        if(f === filter) {
            btn.classList.remove('bg-stone-100', 'text-stone-600', 'hover:bg-stone-200');
            btn.classList.add('bg-amber-600', 'text-white', 'shadow-sm', 'ring-2', 'ring-offset-2', 'ring-amber-500');
        } else {
            btn.classList.add('bg-stone-100', 'text-stone-600', 'hover:bg-stone-200');
            btn.classList.remove('bg-amber-600', 'text-white', 'shadow-sm', 'ring-2', 'ring-offset-2', 'ring-amber-500');
        }
    });

    renderProducts();
    if (window.renderFinance) window.renderFinance();
};


window.toggleCategory = (id) => {
    const el = document.getElementById(id);
    const icon = document.getElementById(id + '-icon');
    if(el) {
        el.classList.toggle('hidden');
        if(icon) icon.classList.toggle('-rotate-90');
    }
};

window.expandAllCategories = () => {
    document.querySelectorAll('.category-grid-container').forEach(el => el.classList.remove('hidden'));
    document.querySelectorAll('.category-toggle-icon').forEach(icon => icon.classList.remove('-rotate-90'));
};

window.collapseAllCategories = () => {
    document.querySelectorAll('.category-grid-container').forEach(el => el.classList.add('hidden'));
    document.querySelectorAll('.category-toggle-icon').forEach(icon => icon.classList.add('-rotate-90'));
};


document.addEventListener('DOMContentLoaded', () => {
    if (typeof lucide !== 'undefined') lucide.createIcons();
    initData();
    renderCategoriesSelect();
    renderProducts();
    if (window.renderFinance) window.renderFinance();
    renderOrders();
    if(window.renderCustomerOrders) window.renderCustomerOrders();
    if(window.renderReceivables) window.renderReceivables();
    if(window.renderInventory) window.renderInventory();
    if(window.renderPersonnelRecords) window.renderPersonnelRecords();
    window.renderB2BRecords();
});

// Modal Helpers
window.openModal = (id) => { const el = document.getElementById(id); if(el) el.classList.remove('hidden'); };
window.closeModal = (id) => { const el = document.getElementById(id); if(el) el.classList.add('hidden'); };

window.openAddCategoryModal = () => openModal('add-category-modal');
window.closeAddCategoryModal = () => closeModal('add-category-modal');
window.openAddProductModal = () => openModal('add-product-modal');
window.closeAddProductModal = () => closeModal('add-product-modal');

// Init Data
function initData() {
    if(!localStorage.getItem('products')) localStorage.setItem('products', JSON.stringify([]));
    if(!localStorage.getItem('categories')) localStorage.setItem('categories', JSON.stringify(['Ekmek Çeşitleri', 'Pastalar']));
}

function renderCategoriesSelect() {
    const cats = JSON.parse(localStorage.getItem('categories') || '[]');
    const select = document.getElementById('new-prod-category');
    if(select) {
        select.innerHTML = '';
        cats.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            opt.textContent = c;
            select.appendChild(opt);
        });
    }
}

// Submits
window.submitNewCategory = (e) => {
    e.preventDefault();
    let name = document.getElementById('new-category-name').value;
    let cats = JSON.parse(localStorage.getItem('categories') || '[]');
    if(name && name.trim() !== "" && !cats.includes(name.trim())) { name = name.trim();
        cats.push(name);
        localStorage.setItem('categories', JSON.stringify(cats));
    }
    renderCategoriesSelect();
    closeModal('add-category-modal');
    e.target.reset(); renderProducts();
    if (window.renderFinance) window.renderFinance();
};

window.submitNewProduct = (e) => {
    e.preventDefault();
    const name = document.getElementById('new-prod-name').value;
    const cat = document.getElementById('new-prod-category').value;
    const unit = document.getElementById('new-prod-unit') ? document.getElementById('new-prod-unit').value : 'Adet';
    const max = parseInt(document.getElementById('new-prod-max').value || 100);
    const stock = parseInt(document.getElementById('new-prod-stock').value || 0);
    const url = document.getElementById('new-prod-url').value;
    
    // Simple placeholder if no image
    const image = url || 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500&auto=format&fit=crop&q=60';

    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    prods.push({
        id: Date.now(),
        name, category: cat, unit, maxStock: max, stock, sales: 0, waste: 0, image
    });
    
    try {
        localStorage.setItem('products', JSON.stringify(prods));
        closeModal('add-product-modal');
    } catch(err) {
        console.error(err);
        window.showToast('Depolama alanı dolu! Lütfen ürün görsellerini küçültün veya bazılarını silin.', 'error');
        return;
    }
    e.target.reset(); renderProducts();
    if (window.renderFinance) window.renderFinance();
    renderProducts();
    if (window.renderFinance) window.renderFinance();
};

// Update functions
window.updateProduct = (id, field, delta) => {
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let p = prods.find(x => String(x.id) === String(id));
    if(p) {

        const today = new Date().toISOString().split('T')[0];
        if (!p.history) p.history = {};
        if (!p.history[today]) p.history[today] = { sales: 0, waste: 0, criticalDrops: 0, restocks: 0, entered: 0 };
        
        // Initialize totalEntered if not present (assuming existing stock + sales + waste was entered)
        if (typeof p.totalEntered === 'undefined') {
            p.totalEntered = (p.stock || 0) + (p.sales || 0) + (p.waste || 0);
        }
        
        const prevStock = p.stock;
        
        if(field === 'stock') {
            if(p.stock + delta >= 0 && p.stock + delta <= p.maxStock) {
                p.stock += delta;
                if(delta > 0) {
                    p.totalEntered += delta;
                    p.history[today].entered = (p.history[today].entered || 0) + delta;
                }
            }
        } else if(field === 'sales') {
            if(delta > 0 && p.stock >= 1) { p.sales += 1; p.stock -= 1; p.history[today].sales++; }
            else if(delta < 0 && p.sales >= 1) { p.sales -= 1; p.stock += 1; p.history[today].sales = Math.max(0, p.history[today].sales - 1); }
        } else if(field === 'waste') {
            if(delta > 0 && p.stock >= 1) { p.waste += 1; p.stock -= 1; p.history[today].waste++; }
            else if(delta < 0 && p.waste >= 1) { p.waste -= 1; p.stock += 1; p.history[today].waste = Math.max(0, p.history[today].waste - 1); }
        }
        
        const prevPct = (prevStock / (p.maxStock || 1));
        const newPct = (p.stock / (p.maxStock || 1));
        if(prevPct >= 0.2 && newPct < 0.2) {
            p.history[today].criticalDrops = (p.history[today].criticalDrops || 0) + 1;
        }
        
        // Auto Order Check
        const pct = Math.min(100, Math.round((p.stock / (p.maxStock || 1)) * 100));
        if(pct <= 30) {
            autoRequestOrder(p);
        }
        
        localStorage.setItem('products', JSON.stringify(prods));

        renderProducts();
    if (window.renderFinance) window.renderFinance();
    }
};

window.quickSell = (id) => {
    updateProduct(id, 'sales', 1);
};


window.autoRequestOrder = (product) => {
    let orders = JSON.parse(localStorage.getItem('orders') || '[]');
    if(!orders.some(o => o.productId === product.id)) {
        orders.push({
            id: Date.now(),
            productId: product.id,
            productName: product.name,
            time: new Date().toLocaleTimeString('tr-TR', {hour: '2-digit', minute:'2-digit'})
        });
        localStorage.setItem('orders', JSON.stringify(orders));
        if(window.renderOrders) renderOrders();
    }
};

window.requestOrder = (id) => {
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let p = prods.find(x => String(x.id) === String(id));
    if(p) {
        autoRequestOrder(p);
        alert(p.name + ' için imalathaneye üretim isteği gönderildi!');
    }
};

window.closeCompleteOrderModal = () => {
    const el = document.getElementById('complete-order-modal');
    if(el) el.classList.add('hidden');
};

window.completeOrder = (orderId) => {
    let orders = JSON.parse(localStorage.getItem('orders') || '[]');
    const ord = orders.find(x => x.id === orderId);
    if(ord) {
        let prods = JSON.parse(localStorage.getItem('products') || '[]');
        let p = prods.find(x => x.id === ord.productId);
        
        document.getElementById('complete-order-id').value = orderId;
        
        if (p) {
            document.getElementById('complete-order-label').innerHTML = `<span class="text-amber-600">${p.name}</span> teslim alınıyor:`;
            document.getElementById('complete-order-unit').textContent = p.unit || 'ADET';
            let suggestedAmount = p.maxStock - p.stock > 0 ? parseFloat((p.maxStock - p.stock).toFixed(2)) : 10;
            document.getElementById('complete-order-amount').value = suggestedAmount;
        } else {
            document.getElementById('complete-order-label').textContent = `Üretim teslim alınıyor:`;
            document.getElementById('complete-order-unit').textContent = 'ADET';
            document.getElementById('complete-order-amount').value = 10;
        }
        
        const el = document.getElementById('complete-order-modal');
        if(el) el.classList.remove('hidden');
        
        setTimeout(() => document.getElementById('complete-order-amount').focus(), 100);
    }
};

window.submitCompleteOrder = (e) => {
    e.preventDefault();
    const orderId = parseInt(document.getElementById('complete-order-id').value, 10);
    const amount = parseFloat(document.getElementById('complete-order-amount').value);
    
    if(!isNaN(amount) && amount > 0) {
        let orders = JSON.parse(localStorage.getItem('orders') || '[]');
        const ord = orders.find(x => x.id === orderId);
        if(ord) {
            let prods = JSON.parse(localStorage.getItem('products') || '[]');
            let p = prods.find(x => x.id === ord.productId);
            if(p) {
                const today = new Date().toISOString().split('T')[0];
                if (!p.history) p.history = {};
                if (!p.history[today]) p.history[today] = { sales: 0, waste: 0, criticalDrops: 0, restocks: 0, entered: 0 };
                p.history[today].restocks = (p.history[today].restocks || 0) + 1;
                
                if (typeof p.totalEntered === 'undefined') {
                    p.totalEntered = (p.stock || 0) + (p.sales || 0) + (p.waste || 0);
                }
                
                p.stock += amount;
                p.totalEntered += amount;
                p.history[today].entered = (p.history[today].entered || 0) + amount;
                
                if(p.stock > p.maxStock) {
                    p.maxStock = p.stock;
                }
                localStorage.setItem('products', JSON.stringify(prods));
            }
            orders = orders.filter(x => x.id !== orderId);
            localStorage.setItem('orders', JSON.stringify(orders));
            renderOrders();
            renderProducts();
    if (window.renderFinance) window.renderFinance();
        }
    }
    closeCompleteOrderModal();
};

window.cancelOrder = (orderId) => {
    openConfirmModal(
        'Siparişi İptal Et',
        'Bu siparişi imalathane listesinden kaldırmak istediğinize emin misiniz?',
        'Evet, İptal Et',
        () => {
            let orders = JSON.parse(localStorage.getItem('orders') || '[]');
            orders = orders.filter(x => String(x.id) !== String(orderId));
            localStorage.setItem('orders', JSON.stringify(orders));
            closeConfirmModal();
            renderOrders();
        }
    );
};

window.renderOrders = () => {
    updateDashboard();
    if(window.renderAnalyticsFloor) renderAnalyticsFloor();
    const container = document.getElementById('kds-pending');
    if(!container) return;
    
    let orders = JSON.parse(localStorage.getItem('orders') || '[]');
    if(orders.length === 0) {
        container.innerHTML = `<div class="col-span-full text-center py-10 text-stone-500 font-bold"><i data-lucide="coffee" class="w-10 h-10 mx-auto mb-3 opacity-50"></i>Şu an bekleyen imalat siparişi yok.</div>`;
        if(typeof lucide !== 'undefined') lucide.createIcons();
        return;
    }
    
    let html = '';
    orders.forEach(o => {
        html += `
        <div class="bg-white rounded-2xl p-5 shadow-lg border-l-4 border-l-red-500 border border-stone-200 flex flex-col gap-4">
            <div>
                <div class="flex justify-between items-start mb-2">
                    <h3 class="text-xl font-black text-stone-800 uppercase tracking-tight">${o.productName}</h3>
                    <span class="bg-red-100 text-red-600 px-2 py-1 rounded-lg text-[10px] font-black uppercase tracking-wider flex items-center gap-1 shadow-sm"><i data-lucide="flame" class="w-3 h-3"></i> Acil</span>
                </div>
                <div class="text-xs text-stone-500 font-bold flex items-center gap-1"><i data-lucide="clock" class="w-3 h-3"></i> Sipariş Saati: ${o.time}</div>
            </div>
            <div class="flex flex-col gap-2 mt-auto pt-2">
                <button onclick="completeOrder(${o.id})" class="w-full bg-emerald-600 text-white font-black py-3 rounded-xl hover:bg-emerald-700 shadow flex items-center justify-center gap-2 transition active:scale-95">
                    <i data-lucide="check-circle" class="w-5 h-5"></i> Tamamlandı & Teslim Et
                </button>
                <button onclick="cancelOrder(${o.id})" class="w-full bg-stone-100 text-stone-500 font-black py-2.5 rounded-xl hover:bg-stone-200 hover:text-stone-700 transition text-xs flex items-center justify-center gap-1.5 active:scale-95 border border-stone-200">
                    <i data-lucide="x" class="w-3.5 h-3.5"></i> İptal Et
                </button>
            </div>
        </div>
        `;
    });
    container.innerHTML = html;
    if(typeof lucide !== 'undefined') lucide.createIcons();
};


window.resetAllSales = () => {
    if(confirm('Tüm satışları sıfırlamak istediğinize emin misiniz?')) {
        let prods = JSON.parse(localStorage.getItem('products') || '[]');
        prods.forEach(p => p.sales = 0);
        localStorage.setItem('products', JSON.stringify(prods));
        renderProducts();
    if (window.renderFinance) window.renderFinance();
    }
};

window.resetAllWaste = () => {
    if(confirm('Tüm fireleri sıfırlamak istediğinize emin misiniz?')) {
        let prods = JSON.parse(localStorage.getItem('products') || '[]');
        prods.forEach(p => p.waste = 0);
        localStorage.setItem('products', JSON.stringify(prods));
        renderProducts();
    if (window.renderFinance) window.renderFinance();
    }
};

window.resetData = () => {
    window.openConfirmModal('Ayarları Sıfırla', 'Sistemi en son kaydettiğiniz duruma döndürmek istediğinize emin misiniz? Kaydetmediğiniz tüm veriler silinecektir.', 'Evet, Geri Dön', () => {
        const keys = ['products', 'categories', 'orders', 'customerOrders', 'receivables', 'inventory', 'invCategories', 'adminPassword'];
        const backups = {};
        keys.forEach(k => {
            backups[k] = localStorage.getItem(k + '_backup');
        });
        
        localStorage.clear();
        
        keys.forEach(k => {
            if (backups[k]) {
                localStorage.setItem(k, backups[k]);
                localStorage.setItem(k + '_backup', backups[k]); // keep the backup alive
            }
        });
        
        // Ensure defaults if no backup was found
        if(!localStorage.getItem('products')) localStorage.setItem('products', JSON.stringify([]));
        if(!localStorage.getItem('categories')) localStorage.setItem('categories', JSON.stringify(['Ekmek Çeşitleri', 'Pastalar']));
        if(!localStorage.getItem('invCategories')) localStorage.setItem('invCategories', JSON.stringify(['Un', 'İmalathane', 'Meşrubat', 'Kutu']));
        
        window.closeConfirmModal();
        location.reload();
    });
};

window.saveAllSettings = () => {
    const keys = ['products', 'categories', 'orders', 'customerOrders', 'receivables', 'inventory', 'invCategories', 'adminPassword'];
    keys.forEach(k => {
        const val = localStorage.getItem(k);
        if (val) {
            localStorage.setItem(k + '_backup', val);
        }
    });
    showToast('Sistem Başarıyla Kaydedildi! Geri dönülebilecek bir yedek oluşturuldu.', 'success');
};
// Rendering



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
    if (window.renderFinance) window.renderFinance();
    }
    closeEditCategoryModal();
};
window.deleteCategory = (catName) => {
    openConfirmModal(
        'Kategoriyi Sil',
        `"${catName}" kategorisini ve içindeki tüm ürünleri silmek istediğinize emin misiniz? Bu işlem geri alınamaz.`,
        'Evet, Sil',
        () => {
            let cats = JSON.parse(localStorage.getItem('categories') || '[]');
            cats = cats.filter(c => c !== catName);
            localStorage.setItem('categories', JSON.stringify(cats));
            
            let prods = JSON.parse(localStorage.getItem('products') || '[]');
            const initialLength = prods.length;
            prods = prods.filter(p => p.category !== catName);
            if(prods.length !== initialLength) {
                localStorage.setItem('products', JSON.stringify(prods));
            }
            
            closeConfirmModal();
            renderProducts();
    if (window.renderFinance) window.renderFinance();
        }
    );
};


window.openEditProductModal = (id) => {
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let p = prods.find(x => String(x.id) === String(id));
    if(!p) return;
    
    document.getElementById('edit-prod-id').value = p.id;
    document.getElementById('edit-prod-existing-image').value = p.image || '';
    document.getElementById('edit-prod-name').value = p.name;
    document.getElementById('edit-prod-max').value = p.maxStock;
    document.getElementById('edit-prod-stock').value = p.stock;
    
    if(document.getElementById('edit-prod-url')) {
        document.getElementById('edit-prod-url').value = p.image && p.image.startsWith('http') ? p.image : '';
    }

    const catSelect = document.getElementById('edit-prod-category');
    if(catSelect) {
        catSelect.innerHTML = '';
        let cats = JSON.parse(localStorage.getItem('categories') || '[]');
        if(!cats.includes(p.category)) cats.push(p.category);
        cats.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            opt.textContent = c;
            if(c === p.category) opt.selected = true;
            catSelect.appendChild(opt);
        });
    }

    const unitSelect = document.getElementById('edit-prod-unit');
    if(unitSelect) unitSelect.value = p.unit;
    
    const el = document.getElementById('edit-product-modal');
    if(el) el.classList.remove('hidden');
};

window.closeEditModal = () => {
    const el = document.getElementById('edit-product-modal');
    if(el) el.classList.add('hidden');
};

window.submitEditProduct = (e) => {
    e.preventDefault();
    const id = parseInt(document.getElementById('edit-prod-id').value);
    const name = document.getElementById('edit-prod-name').value;
    const cat = document.getElementById('edit-prod-category').value;
    const unit = document.getElementById('edit-prod-unit').value;
    const max = parseInt(document.getElementById('edit-prod-max').value || 100);
    const stock = parseFloat(document.getElementById('edit-prod-stock').value || 0);
    const url = document.getElementById('edit-prod-url') ? document.getElementById('edit-prod-url').value : '';
    const existingImg = document.getElementById('edit-prod-existing-image').value;
    
    const finalImage = url || existingImg || 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500&auto=format&fit=crop&q=60';

    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let pIndex = prods.findIndex(x => x.id === id);
    if(pIndex > -1) {
        let p = prods[pIndex];
        
        if (typeof p.totalEntered === 'undefined') {
            p.totalEntered = (p.stock || 0) + (p.sales || 0) + (p.waste || 0);
        }
        
        const prevStock = p.stock || 0;
        if(stock > prevStock) {
            const diff = stock - prevStock;
            p.totalEntered += diff;
            const today = new Date().toISOString().split('T')[0];
            if (!p.history) p.history = {};
            if (!p.history[today]) p.history[today] = { sales: 0, waste: 0, criticalDrops: 0, restocks: 0, entered: 0 };
            p.history[today].entered = (p.history[today].entered || 0) + diff;
        }

        prods[pIndex].name = name;
        prods[pIndex].category = cat;
        prods[pIndex].unit = unit;
        prods[pIndex].maxStock = max;
        prods[pIndex].stock = stock;
        prods[pIndex].image = finalImage;
        localStorage.setItem('products', JSON.stringify(prods));
    }
    
    closeEditModal();
    renderProducts();
    if (window.renderFinance) window.renderFinance();
};

window.deleteProduct = (id) => {
    openConfirmModal(
        'Ürünü Sil',
        'Bu ürünü kalıcı olarak silmek istediğinize emin misiniz?',
        'Evet, Sil',
        () => {
            let prods = JSON.parse(localStorage.getItem('products') || '[]');
            prods = prods.filter(x => String(x.id) !== String(id));
            localStorage.setItem('products', JSON.stringify(prods));
            
            let orders = JSON.parse(localStorage.getItem('orders') || '[]');
            orders = orders.filter(x => String(x.productId) !== String(id));
            localStorage.setItem('orders', JSON.stringify(orders));
            
            closeConfirmModal();
            renderProducts();
    if (window.renderFinance) window.renderFinance();
            if(window.renderOrders) renderOrders();
        }
    );
};


window.renderProducts = () => {
    updateDashboard();
    const container = document.getElementById('products-container');
    if(!container) return;
    
    const openCategories = new Set();
    document.querySelectorAll('.category-grid-container').forEach(el => {
        if(!el.classList.contains('hidden')) {
            openCategories.add(el.id);
        }
    });
    
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    const allCats = JSON.parse(localStorage.getItem('categories') || '[]');
    container.innerHTML = '';
    
    // Apply stock filter
    if (currentFilter === 'CRITICAL') {
        prods = prods.filter(p => p.stock > 0 && p.stock < (p.maxStock * 0.2));
    } else if (currentFilter === 'EMPTY') {
        prods = prods.filter(p => p.stock <= 0);
    } else if (currentFilter === 'NORMAL') {
        prods = prods.filter(p => p.stock >= (p.maxStock * 0.2));
    }
    
    // Apply search filter
    const searchVal = (document.getElementById('search-input')?.value || '').toLowerCase();
    if (searchVal) {
        prods = prods.filter(p => 
            p.name.toLowerCase().includes(searchVal) || 
            p.category.toLowerCase().includes(searchVal)
        );
    }
    
    // Group by category, but include all categories even if empty
    const grouped = {};
    allCats.forEach(c => grouped[c] = []);
    prods.forEach(p => {
        if(!grouped[p.category]) grouped[p.category] = [];
        grouped[p.category].push(p);
    });
    
    for(const [cat, items] of Object.entries(grouped)) {
        
        // Hide empty categories when filtering or searching
        if ((currentFilter !== 'ALL' || searchVal) && items.length === 0) {
            continue;
        }
        
        let safeCatId = 'cat-grid-' + cat.replace(/\s+/g, '-');
        
        // Auto-expand if searching, otherwise use remembered state
        let isExpanded = searchVal ? true : openCategories.has(safeCatId);
        
        let isHidden = isExpanded ? '' : 'hidden';
        let isRotated = isExpanded ? '' : '-rotate-90';
        
        let catHtml = `
            <div class="mb-8 relative group">
                <div class="flex items-center gap-3 mb-4 border-b-2 border-amber-600 pb-2 w-max cursor-pointer select-none" onclick="toggleCategory('${safeCatId}')" title="Kategoriyi Aç/Kapat">
                    <h2 class="text-xl font-black text-stone-800 uppercase tracking-wider flex items-center gap-2">
                        <i id="${safeCatId}-icon" data-lucide="chevron-down" class="w-5 h-5 transition-transform category-toggle-icon ${isRotated}"></i>
                        ${cat}
                    </h2>
                    <div class="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1 ml-2" onclick="event.stopPropagation()">
                        <button onclick="editCategory('${cat}')" class="p-1.5 bg-stone-100 hover:bg-stone-200 text-stone-600 rounded-lg transition" title="Kategoriyi Düzenle">
                            <i data-lucide="pencil" class="w-4 h-4"></i>
                        </button>
                        <button onclick="deleteCategory('${cat}')" class="p-1.5 bg-rose-50 hover:bg-rose-100 text-rose-600 rounded-lg transition" title="Kategoriyi Sil">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                </div>
                <div id="${safeCatId}" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 category-grid-container ${isHidden}">
        `;

        
        if (items.length === 0) {
            catHtml += `<div class="col-span-full text-stone-500 font-bold bg-stone-100 p-4 rounded-xl border border-stone-200">Bu kategoride henüz ürün bulunmuyor.</div>`;
        } else {
            
            items.forEach(p => {
                const pct = Math.min(100, Math.round((p.stock / (p.maxStock || 1)) * 100));
                const isZero = p.stock <= 0;
                const isLow = p.stock < (p.maxStock * 0.2);
                
                // Dynamic colors for the circle based on percentage
                let circleColor = 'border-emerald-100 text-emerald-500';
                if(pct <= 0) circleColor = 'border-rose-100 text-rose-600';
                else if(pct <= 20) circleColor = 'border-rose-300 text-rose-600';
                else if(pct <= 50) circleColor = 'border-orange-200 text-orange-500';
                else if(pct <= 75) circleColor = 'border-amber-200 text-amber-500';
                else circleColor = 'border-emerald-100 text-emerald-500';
                
                catHtml += `
                <div class="bg-white rounded-3xl overflow-hidden shadow-lg border border-stone-200/60 hover:shadow-xl transition flex flex-col relative group/card">
                    <div class="relative h-48 w-full group">
                        <img src="${p.image}" class="w-full h-full object-cover" />
                        <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
                        
                        <!-- Badges -->
                        <div class="absolute top-3 left-3 right-3 flex justify-between pointer-events-none">
                            ${isZero ? `<span class="bg-white text-rose-600 px-2 py-0.5 rounded text-[10px] font-black tracking-wider shadow">TÜKENDİ (%0)</span>` : '<div></div>'}
                            ${isLow && !isZero ? `<span class="bg-orange-500 text-white px-2 py-0.5 rounded text-[10px] font-black tracking-wider shadow flex items-center gap-1"><i data-lucide="flame" class="w-3 h-3"></i> Acil İmalatta</span>` : ''}
                        </div>
                        
                        <!-- Product Edit/Delete Actions (shown on hover) -->
                        <div class="absolute top-2 right-2 flex gap-1 opacity-0 group-hover/card:opacity-100 transition-opacity">
                            <button onclick="openEditProductModal(${p.id})" class="p-2 bg-white/90 hover:bg-white text-stone-700 rounded-lg shadow transition" title="Ürünü Düzenle">
                                <i data-lucide="pencil" class="w-4 h-4"></i>
                            </button>
                            <button onclick="deleteProduct(${p.id})" class="p-2 bg-rose-500/90 hover:bg-rose-600 text-white rounded-lg shadow transition" title="Ürünü Sil">
                                <i data-lucide="trash-2" class="w-4 h-4"></i>
                            </button>
                        </div>
                        
                        <h3 class="absolute bottom-3 left-4 text-white font-black text-lg truncate pr-4">${p.name}</h3>
                    </div>
                    
                    <div class="p-4 flex flex-col gap-4">
                        <div class="flex justify-between items-center">
                            <div class="flex flex-col">
                                <span class="text-[10px] text-stone-400 font-extrabold uppercase mb-1">STOK (${p.unit.toUpperCase()})</span>
                                <div class="flex items-center gap-2 bg-stone-50 border border-stone-200 rounded-xl p-1 w-fit">
                                    <button onclick="updateProduct(${p.id}, 'stock', -1)" class="w-7 h-7 rounded-lg hover:bg-stone-200 font-bold text-stone-600 flex items-center justify-center">-</button>
                                    <span class="text-sm font-black text-stone-800 min-w-[3rem] text-center">${p.stock} ${p.unit}</span>
                                    <button onclick="updateProduct(${p.id}, 'stock', 1)" class="w-7 h-7 rounded-lg hover:bg-stone-200 font-bold text-stone-600 flex items-center justify-center">+</button>
                                </div>
                            </div>
                            <div class="w-10 h-10 rounded-full border-4 ${circleColor} flex items-center justify-center font-black text-[10px]">
                                %${pct}
                            </div>
                        </div>
                        <div class="flex gap-2">
                            <div class="flex-1 border border-stone-200 rounded-xl p-1.5 flex justify-between items-center bg-stone-50">
                                <span class="text-[10px] font-bold text-stone-500">Satış:</span>
                                <div class="flex items-center gap-1">
                                    <button onclick="updateProduct(${p.id}, 'sales', -1)" class="w-5 h-5 bg-stone-200 rounded text-[10px] font-bold hover:bg-stone-300">-</button>
                                    <span class="text-xs font-black min-w-[1rem] text-center text-emerald-700">${p.sales}</span>
                                    <button onclick="updateProduct(${p.id}, 'sales', 1)" class="w-5 h-5 bg-emerald-600 text-white rounded text-[10px] font-bold hover:bg-emerald-700">+</button>
                                </div>
                            </div>
                            <div class="flex-1 border border-stone-200 rounded-xl p-1.5 flex justify-between items-center bg-stone-50">
                                <span class="text-[10px] font-bold text-stone-500">Fire:</span>
                                <div class="flex items-center gap-1">
                                    <button onclick="updateProduct(${p.id}, 'waste', -1)" class="w-5 h-5 bg-stone-200 rounded text-[10px] font-bold hover:bg-stone-300">-</button>
                                    <span class="text-xs font-black min-w-[1rem] text-center text-rose-700">${p.waste}</span>
                                    <button onclick="updateProduct(${p.id}, 'waste', 1)" class="w-5 h-5 bg-rose-600 text-white rounded text-[10px] font-bold hover:bg-rose-700">+</button>
                                </div>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-2 mt-2">
                            <button onclick="quickSell(${p.id})" class="bg-stone-900 text-white py-2.5 rounded-xl text-[11px] font-black flex items-center justify-center gap-1.5 hover:bg-stone-800 active:scale-95 transition">
                                <i data-lucide="shopping-cart" class="w-3.5 h-3.5"></i> Satış (-1)
                            </button>
                            <button onclick="requestOrder(${p.id})" class="bg-amber-50 text-amber-700 border border-amber-200 py-2.5 rounded-xl text-[11px] font-black flex items-center justify-center gap-1.5 hover:bg-amber-100 active:scale-95 transition">
                                <i data-lucide="bell-ring" class="w-3.5 h-3.5"></i> İste
                            </button>
                        </div>
                    </div>
                </div>
                `;
            });

        }
        
        catHtml += `</div></div>`;
        container.innerHTML += catHtml;
    }
    if(typeof lucide !== 'undefined') lucide.createIcons();
};

window.setRole = (role, bypassAuth = false) => {
    if(!bypassAuth && (role === 'FINANCE' || role === 'RECIPE' || role === 'PERSONNEL' || role === 'B2B')) {
        pendingRole = role;
        document.getElementById('auth-password').value = '';
        document.getElementById('auth-modal').classList.remove('hidden');
        setTimeout(() => document.getElementById('auth-password').focus(), 100);
        return;
    }

    const roles = ['HOME', 'UPPER', 'LOWER', 'ORDERS', 'ANALYTICS', 'RECEIVABLES', 'INVENTORY', 'FINANCE', 'RECIPE', 'PERSONNEL', 'B2B'];
    roles.forEach(r => {
        const viewEl = document.getElementById('view-' + r.toLowerCase());
        const btnEl = document.getElementById('btn-role-' + r.toLowerCase());
        if(viewEl) {
            viewEl.style.display = ''; // Clear old inline styles
            viewEl.classList.add('hidden');
        }
        if(btnEl) {
            btnEl.classList.remove('bg-amber-600', 'text-white');
            btnEl.classList.add('bg-transparent', 'text-stone-300');
        }
    });
    const selectedView = document.getElementById('view-' + role.toLowerCase());
    if(selectedView) {
        selectedView.classList.remove('hidden');
        // Ensure flex is active if the container originally used it
        if(selectedView.classList.contains('flex-col') || selectedView.id !== 'view-finance') {
            selectedView.style.display = 'flex';
        } else {
            selectedView.style.display = 'block';
        }
    }
    const selectedBtn = document.getElementById('btn-role-' + role.toLowerCase());
    if(selectedBtn) {
        selectedBtn.classList.remove('bg-transparent', 'text-stone-300');
        selectedBtn.classList.add('bg-amber-600', 'text-white');
    }
    
    if(role === 'ORDERS' && window.renderCustomerOrders) {
        window.renderCustomerOrders();
    }
    if(role === 'ANALYTICS' && window.renderAnalyticsFloor) {
        window.renderAnalyticsFloor();
    }
    if(role === 'RECEIVABLES' && window.renderReceivables) {
        window.renderReceivables();
    }
    if(role === 'INVENTORY' && window.renderInventory) {
        window.renderInventory();
    }
    if(role === 'FINANCE' && window.renderFinance) {
        window.renderFinance();
    }
        if(role === 'PERSONNEL' && window.renderPersonnelRecords) {
        window.renderPersonnelRecords();
    window.renderB2BRecords();
    }
if(role === 'RECIPE') {
        window.renderRecipeView();
    }
    
    if(typeof lucide !== 'undefined') lucide.createIcons();
};

let currentSlide = 0;
const totalSlides = 5;
window.goToHeroSlide = (index) => {
    currentSlide = index;
    for(let i=0; i<totalSlides; i++){
        const slide = document.getElementById('hero-slide-'+i);
        const dot = document.getElementById('hero-dot-'+i);
        if(slide) {
            if(i === index) { slide.classList.remove('opacity-0', 'scale-105'); slide.classList.add('opacity-100', 'scale-100'); }
            else { slide.classList.remove('opacity-100', 'scale-100'); slide.classList.add('opacity-0', 'scale-105'); }
        }
        if(dot) {
            if(i === index) { dot.classList.remove('bg-stone-500/70', 'w-2.5', 'h-2.5'); dot.classList.add('bg-amber-400', 'w-3.5', 'h-3.5', 'shadow-sm', 'shadow-amber-500'); }
            else { dot.classList.remove('bg-amber-400', 'w-3.5', 'h-3.5', 'shadow-sm', 'shadow-amber-500'); dot.classList.add('bg-stone-500/70', 'w-2.5', 'h-2.5'); }
        }
    }
};
setInterval(() => { window.goToHeroSlide((currentSlide+1)%totalSlides); }, 5000);


let analyticsTimeFilter = '7';
let analyticsCategoryFilter = 'ALL';
let chartInstance = null;

window.setAnalyticsPeriod = (filter) => {
    analyticsTimeFilter = filter;
    ['7', '30'].forEach(f => {
        const btn = document.getElementById('analytics-period-' + f);
        if(!btn) return;
        if(f === filter) {
            btn.className = 'px-3.5 py-1.5 text-xs font-black rounded-lg transition bg-amber-600 text-white shadow-xs';
        } else {
            btn.className = 'px-3.5 py-1.5 text-xs font-black rounded-lg transition text-stone-600 hover:text-stone-900';
        }
    });
    renderAnalyticsFloor();
};

window.setAnalyticsCategory = (cat) => {
    analyticsCategoryFilter = cat;
    renderAnalyticsFloor();
};

window.renderAnalyticsFloor = () => {
    const container = document.getElementById('analytics-categories-container');
    if(!container) return;
    
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let cats = JSON.parse(localStorage.getItem('categories') || '[]');
    
    // Populate Category Dropdown (if not already hydrated)
    const catSelect = document.getElementById('analytics-category-filter');
    if(catSelect && catSelect.options.length <= 1) {
        let optionsHtml = '<option value="ALL">Tüm Kategoriler</option>';
        cats.forEach(c => {
            optionsHtml += `<option value="${c}">${c}</option>`;
        });
        catSelect.innerHTML = optionsHtml;
        catSelect.value = analyticsCategoryFilter;
    }
    
    // Calculate sums based on time filter
    const now = new Date();
    prods.forEach(p => {
        p._calcSales = 0;
        p._calcWaste = 0;
        p._calcLoss = 0;
        p._calcCriticalDrops = 0;
        p._calcRestocks = 0;
        p._calcEntered = 0;
        let daysLimit = (analyticsTimeFilter === '7' || analyticsTimeFilter === '7D') ? 7 : 30;
        if(p.history) {
            for (const [dateStr, data] of Object.entries(p.history)) {
                let d = new Date(dateStr);
                let diffTime = Math.abs(now - d);
                let diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
                if(diffDays <= daysLimit) {
                    p._calcSales += data.sales || 0;
                    p._calcWaste += data.waste || 0;
                    p._calcLoss += (data.waste || 0) * (parseFloat(p.costPrice) || 0);
                    p._calcCriticalDrops += data.criticalDrops || 0;
                    p._calcRestocks += data.restocks || 0;
                    p._calcEntered += data.entered || 0;
                }
            }
        }
    });
    
    // Apply Category Filter to products
    let filteredProds = prods;
    if(analyticsCategoryFilter !== 'ALL') {
        filteredProds = prods.filter(p => p.category === analyticsCategoryFilter);
    }
    
    // Calculate KPIs
    let totalStock = filteredProds.reduce((sum, p) => sum + (p.stock || 0), 0);
    let totalSales = filteredProds.reduce((sum, p) => sum + p._calcSales, 0);
    let totalWaste = filteredProds.reduce((sum, p) => sum + p._calcWaste, 0);
    
    let totalEntered = filteredProds.reduce((sum, p) => sum + p._calcEntered, 0);
    let avgWasteRate = totalEntered > 0 ? Math.round((totalWaste / totalEntered) * 100) : 0;
    

    const kpi4 = document.getElementById('kpi-avg-waste'); if(kpi4) kpi4.textContent = "%" + avgWasteRate;
    
    // Group for chart (Top 10 Wasted Products)
    let prodLabels = [];
    let prodWasteData = [];
    
    let metric = document.getElementById('analytics-waste-metric') ? document.getElementById('analytics-waste-metric').value : 'amount';
    let sortedProds = [];

    if (metric === 'loss') {
        sortedProds = [...filteredProds].filter(p => p._calcLoss > 0).sort((a,b) => b._calcLoss - a._calcLoss).slice(0, 10);
        sortedProds.forEach(p => {
            prodLabels.push(p.name);
            prodWasteData.push(p._calcLoss);
        });
    } else {
        sortedProds = [...filteredProds].filter(p => p._calcWaste > 0).sort((a,b) => b._calcWaste - a._calcWaste).slice(0, 10);
        sortedProds.forEach(p => {
            prodLabels.push(p.name);
            prodWasteData.push(p._calcWaste);
        });
    }
    
    // Draw Chart
    const ctx = document.getElementById('chart-category-perf');
    const msg = document.getElementById('chart-no-waste-msg');
    if(ctx) {
        if(sortedProds.length === 0) {
            ctx.style.display = 'none';
            if(msg) msg.classList.remove('hidden');
        } else {
            ctx.style.display = 'block';
            if(msg) msg.classList.add('hidden');
            
            if(chartInstance) chartInstance.destroy();
            chartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: prodLabels,
                    datasets: [
                        {
                            label: metric === 'loss' ? 'Zarar (TL)' : 'Fire Miktarı',
                            data: prodWasteData,
                            backgroundColor: '#f43f5e',
                            borderRadius: 6
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true, grid: { color: '#f5f5f4' } },
                        x: { grid: { display: false } }
                    }
                }
            });
        }
    }
    
    // Render Table
    let html = '';
    const searchVal = (document.getElementById('analytics-table-search')?.value || '').toLowerCase();
    
    let displayCats = cats;
    if(analyticsCategoryFilter !== 'ALL') {
        displayCats = cats.filter(c => c === analyticsCategoryFilter);
    }
    
    displayCats.forEach(c => {
        let catProds = prods.filter(p => p.category === c && p.name.toLowerCase().includes(searchVal));
        if(catProds.length === 0) return;
        
        html += `
        <div class="border border-stone-200 rounded-xl overflow-hidden mb-4">
            <div class="bg-stone-50 px-4 py-3 border-b border-stone-200 flex justify-between items-center cursor-pointer hover:bg-stone-100 transition" onclick="document.getElementById('tbl-cat-${c.replace(/\s+/g, '-')}').classList.toggle('hidden')">
                <h4 class="font-black text-stone-800 uppercase tracking-wider">${c}</h4>
                <i data-lucide="chevron-down" class="w-4 h-4 text-stone-500 transition-transform duration-200"></i>
            </div>
            <div id="tbl-cat-${c.replace(/\s+/g, '-')}" class="overflow-x-auto">
                <table class="w-full text-left text-sm">
                    <thead class="bg-white text-stone-500 font-bold border-b border-stone-100 uppercase text-[10px] tracking-wider">
                        <tr>
                            <th class="px-4 py-3">Ürün Adı</th>
                            <th class="px-4 py-3">Kapasite</th>
                            <th class="px-4 py-3 text-indigo-600">Stoğa Giren</th>
                            <th class="px-4 py-3 text-emerald-600">Satış</th>
                            <th class="px-4 py-3 text-rose-600">Fire</th>
                            <th class="px-4 py-3 text-rose-700">Zarar</th>
                            <th class="px-4 py-3 text-stone-800">Elde Kalan</th>
                            <th class="px-4 py-3 text-sky-600">Yenilenme</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-stone-100">
        `;
        
        catProds.forEach(p => {
            let totalEntered = p._calcEntered || 0;
            let rate = totalEntered > 0 ? Math.round((p._calcWaste / totalEntered) * 100) : 0;
            let rateColor = rate > 20 ? 'text-rose-600 font-black' : (rate > 10 ? 'text-amber-600 font-black' : 'text-emerald-600 font-black');
            html += `
                        <tr class="hover:bg-stone-50 transition">
                            <td class="px-4 py-3 font-black text-stone-800 flex items-center gap-3">
                                <img src="${p.image}" class="w-8 h-8 rounded-lg object-cover shadow-sm">
                                ${p.name}
                            </td>
                            <td class="px-4 py-3 font-medium text-stone-600">${p.maxStock} ${p.unit}</td>
                            <td class="px-4 py-3 font-black text-indigo-600">${totalEntered} <span class="text-[10px] font-bold text-indigo-400">${p.unit}</span></td>
                            <td class="px-4 py-3 font-black text-emerald-600">${p._calcSales} <span class="text-[10px] font-bold text-emerald-400">${p.unit}</span></td>
                            <td class="px-4 py-3 font-black text-rose-600">${p._calcWaste} <span class="text-[10px] font-bold text-rose-400">${p.unit}</span></td>
                            <td class="px-4 py-3 font-black text-rose-700">${(p._calcLoss || 0).toFixed(2)} ₺</td>
                            <td class="px-4 py-3 font-black text-stone-800">${p.stock} <span class="text-[10px] font-bold text-stone-400">${p.unit}</span></td>
                            <td class="px-4 py-3 font-black text-sky-600">${p._calcRestocks || 0}</td>
                        </tr>
            `;
        });
        
        html += `</tbody></table></div></div>`;
    });
    
    if(html === '') {
        html = `<div class="text-center py-10 text-stone-500 font-bold bg-stone-50 rounded-xl border border-stone-200">Hiç kayıt bulunamadı.</div>`;
    }
    container.innerHTML = html;
    if(typeof lucide !== 'undefined') lucide.createIcons();
};


// --- CUSTOMER ORDERS LOGIC ---

let customerOrdersTab = 'ACTIVE';

window.openCustomerOrderModal = (id = null) => {
    document.getElementById('customer-order-form').reset();
    document.getElementById('cust-order-id').value = id || '';
    document.getElementById('cust-img-preview-box').classList.add('hidden');
    document.getElementById('cust-img-preview').src = '';
    
    const select = document.getElementById('cust-prod-select');
    if(select) {
        select.innerHTML = '<option value="">-- Menüden Seçin (veya elle yazın) --</option>';
        let prods = JSON.parse(localStorage.getItem('products') || '[]');
        prods.forEach(p => {
            let opt = document.createElement('option');
            opt.value = p.name;
            opt.textContent = p.name;
            select.appendChild(opt);
        });
    }

    if(id) {
        document.getElementById('cust-modal-title').innerHTML = '<i data-lucide="edit" class="w-6 h-6 text-amber-600"></i> Siparişi Düzenle';
        let orders = JSON.parse(localStorage.getItem('customerOrders') || '[]');
        let ord = orders.find(x => x.id == id);
        if(ord) {
            document.getElementById('cust-name').value = ord.customerName || '';
            document.getElementById('cust-phone').value = ord.customerPhone || '';
            document.getElementById('cust-date').value = ord.date || '';
            document.getElementById('cust-time').value = ord.time || '';
            document.getElementById('cust-prod-name').value = ord.productName || '';
            document.getElementById('cust-qty').value = ord.qty || 1;
            document.getElementById('cust-unit').value = ord.unit || 'Adet';
            document.getElementById('cust-notes').value = ord.notes || '';
            document.getElementById('cust-img-url').value = ord.imgUrl || '';
            document.getElementById('cust-price').value = ord.price || '';
            
            // New fields
            if(document.getElementById('cust-advance')) document.getElementById('cust-advance').value = ord.deposit || '';
            if(document.getElementById('cust-deposit')) document.getElementById('cust-deposit').value = ord.deposit || '';
            
            if(document.getElementById('cust-creator')) document.getElementById('cust-creator').value = ord.creator || '';
            if(document.getElementById('cust-cake-content')) document.getElementById('cust-cake-content').value = ord.cakeContent || '';
            if(ord.imgUrl) window.previewCustImageUrl(ord.imgUrl);
        }
    } else {
        document.getElementById('cust-modal-title').innerHTML = '<i data-lucide="user-check" class="w-6 h-6 text-amber-600"></i> Yeni Müşteri Siparişi';
        let now = new Date();
        document.getElementById('cust-date').value = now.toISOString().split('T')[0];
        now.setHours(now.getHours() + 1);
        document.getElementById('cust-time').value = now.toTimeString().substring(0, 5);
    }
    
    window.openModal('customer-order-modal');
    if(typeof lucide !== 'undefined') lucide.createIcons();
};

window.closeCustomerOrderModal = () => {
    window.closeModal('customer-order-modal');
};

window.onCustomerProductSelect = () => {
    const val = document.getElementById('cust-prod-select').value;
    if(val) document.getElementById('cust-prod-name').value = val;
};

window.previewCustImageFile = (input) => {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var img = new Image();
            img.onload = function() {
                var canvas = document.createElement('canvas');
                var ctx = canvas.getContext('2d');
                var MAX_WIDTH = 500;
                var width = img.width;
                var height = img.height;
                if (width > MAX_WIDTH) { height *= MAX_WIDTH / width; width = MAX_WIDTH; }
                canvas.width = width; canvas.height = height;
                ctx.drawImage(img, 0, 0, width, height);
                var dataUrl = canvas.toDataURL('image/jpeg', 0.6);
                document.getElementById('cust-img-preview').src = dataUrl;
                document.getElementById('cust-img-preview-box').classList.remove('hidden');
                document.getElementById('cust-img-url').value = dataUrl;
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
};

window.previewCustImageUrl = (val) => {
    if(val && val.trim() !== '') {
        document.getElementById('cust-img-preview').src = val;
        document.getElementById('cust-img-preview-box').classList.remove('hidden');
    } else {
        window.removeCustImagePreview();
    }
};

window.removeCustImagePreview = () => {
    document.getElementById('cust-img-preview').src = '';
    document.getElementById('cust-img-preview-box').classList.add('hidden');
    document.getElementById('cust-img-file').value = '';
    document.getElementById('cust-img-url').value = '';
};

window.submitCustomerOrder = (e) => {
    e.preventDefault();
    const id = document.getElementById('cust-order-id').value;
    
    const ord = {
        id: id ? parseInt(id, 10) : Date.now(),
        customerName: document.getElementById('cust-name').value,
        customerPhone: document.getElementById('cust-phone').value,
        date: document.getElementById('cust-date').value,
        time: document.getElementById('cust-time').value,
        productName: document.getElementById('cust-prod-name').value,
        qty: parseFloat(document.getElementById('cust-qty').value),
        unit: document.getElementById('cust-unit').value,
        notes: document.getElementById('cust-notes').value,
        imgUrl: document.getElementById('cust-img-url').value,
        price: parseFloat(document.getElementById('cust-price').value || 0),
        deposit: parseFloat((document.getElementById('cust-advance') || document.getElementById('cust-deposit')).value || 0),
        creator: document.getElementById('cust-creator') ? document.getElementById('cust-creator').value : '',
        cakeContent: document.getElementById('cust-cake-content') ? document.getElementById('cust-cake-content').value : '',
        status: id ? undefined : 'ACTIVE', 
        createdAt: id ? undefined : Date.now()
    };

    let orders = JSON.parse(localStorage.getItem('customerOrders') || '[]');
    if(id) {
        const idx = orders.findIndex(x => x.id == id);
        if(idx > -1) {
            ord.status = orders[idx].status;
            ord.createdAt = orders[idx].createdAt;
            orders[idx] = ord;
        }
    } else {
        orders.push(ord);
    }
    
    localStorage.setItem('customerOrders', JSON.stringify(orders));
    window.closeCustomerOrderModal();
    window.renderCustomerOrders();
};

window.setCustomerOrderTab = (tab) => {
    customerOrdersTab = tab;
    
    const activeBtn = document.getElementById('cust-tab-ACTIVE');
    const delivBtn = document.getElementById('cust-tab-DELIVERED');
    
    if(tab === 'ACTIVE') {
        activeBtn.className = "px-4 py-2 text-xs font-black rounded-xl transition bg-amber-600 text-white shadow-sm flex items-center gap-2";
        activeBtn.innerHTML = `<span class="w-2 h-2 rounded-full bg-white animate-pulse"></span> Aktif Siparişler`;
        
        delivBtn.className = "px-4 py-2 text-xs font-black rounded-xl transition bg-stone-100 text-stone-600 hover:bg-stone-200 flex items-center gap-2";
        delivBtn.innerHTML = `<i data-lucide="check-circle-2" class="w-3.5 h-3.5 text-emerald-600"></i> Teslim Edilen Siparişler`;
    } else {
        delivBtn.className = "px-4 py-2 text-xs font-black rounded-xl transition bg-emerald-600 text-white shadow-sm flex items-center gap-2";
        delivBtn.innerHTML = `<i data-lucide="check-circle-2" class="w-3.5 h-3.5 text-white"></i> Teslim Edilen Siparişler`;
        
        activeBtn.className = "px-4 py-2 text-xs font-black rounded-xl transition bg-stone-100 text-stone-600 hover:bg-stone-200 flex items-center gap-2";
        activeBtn.innerHTML = `<span class="w-2 h-2 rounded-full bg-stone-400"></span> Aktif Siparişler`;
    }
    
    window.renderCustomerOrders();
};

window.completeCustomerOrder = (id) => {
    window.openConfirmModal('Siparişi Teslim Et', 'Bu siparişi müşteriye teslim edildi olarak işaretlemek istiyor musunuz?', 'Evet, Teslim Edildi', () => {
        let orders = JSON.parse(localStorage.getItem('customerOrders') || '[]');
        const idx = orders.findIndex(x => x.id == id);
        if(idx > -1) {
            orders[idx].status = 'DELIVERED';
            localStorage.setItem('customerOrders', JSON.stringify(orders));
            window.renderCustomerOrders();
        }
        window.closeConfirmModal();
    });
};

window.revertCustomerOrder = (id) => {
    let orders = JSON.parse(localStorage.getItem('customerOrders') || '[]');
    const idx = orders.findIndex(x => x.id == id);
    if(idx > -1) {
        orders[idx].status = 'ACTIVE';
        localStorage.setItem('customerOrders', JSON.stringify(orders));
        window.renderCustomerOrders();
    }
};

window.deleteCustomerOrder = (id) => {
    window.openConfirmModal('Siparişi Sil', 'Bu müşteri siparişini tamamen silmek istediğinize emin misiniz? Bu işlem geri alınamaz.', 'Evet, Sil', () => {
        let orders = JSON.parse(localStorage.getItem('customerOrders') || '[]');
        orders = orders.filter(x => x.id != id);
        localStorage.setItem('customerOrders', JSON.stringify(orders));
        window.renderCustomerOrders();
        window.closeConfirmModal();
    });
};


window.printKitchenOrder = (id) => {
    let orders = JSON.parse(localStorage.getItem('customerOrders') || '[]');
    let ord = orders.find(x => x.id == id);
    if(!ord) return;
    
    const printWindow = window.open('', '', 'width=600,height=800');
    const html = `
        <html>
        <head>
            <title>Mutfak Sipariş Fişi</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; color: #000; }
                h1 { text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px; text-transform: uppercase; letter-spacing: 2px; }
                .line { margin-bottom: 15px; font-size: 16px; border-bottom: 1px dashed #ccc; padding-bottom: 5px; }
                .label { font-weight: bold; width: 150px; display: inline-block; }
                .val { font-size: 18px; }
                .highlight { font-size: 22px; font-weight: bold; background: #eee; padding: 10px; border-radius: 5px; text-align: center; margin: 20px 0; border: 2px solid #000; }
                .notes { border: 1px solid #000; padding: 15px; border-radius: 5px; min-height: 80px; }
                .print-btn { display: block; width: 100%; padding: 15px; background: #000; color: #fff; text-align: center; font-size: 18px; cursor: pointer; border: none; margin-bottom: 20px; }
                @media print { .print-btn { display: none; } }
            </style>
        </head>
        <body>
            <button class="print-btn" onclick="window.print()">YAZDIR</button>
            <h1>Mutfak Sipariş Fişi</h1>
            <div class="line"><span class="label">Siparişi Düzenleyen:</span> <span class="val">${ord.creator || '-'}</span></div>
            <div class="line"><span class="label">Müşteri Adı:</span> <span class="val">${ord.customerName}</span></div>
            <div class="line"><span class="label">Teslimat Tarihi:</span> <span class="val">${ord.date} ${ord.time}</span></div>
            
            <div class="highlight">
                ${ord.productName} <br>
                <span style="font-size: 16px; font-weight: normal;">(${ord.qty} ${ord.unit})</span>
            </div>
            
            <div class="line"><span class="label">Pasta İçeriği:</span> <span class="val"><b>${ord.cakeContent || '-'}</b></span></div>
            
            <div style="margin-top:20px; font-weight:bold;">Müşteri Notu / Özel İstek:</div>
            <div class="notes">${ord.notes || 'Not yok.'}</div>
        </body>
        </html>
    `;
    printWindow.document.write(html);
    printWindow.document.close();
};

window.renderCustomerOrders = () => {
    const actContainer = document.getElementById('customer-orders-active');
    const delContainer = document.getElementById('customer-orders-delivered');
    if(!actContainer || !delContainer) return;
    
    let orders = JSON.parse(localStorage.getItem('customerOrders') || '[]');
    const search = (document.getElementById('cust-order-search')?.value || '').toLowerCase();
    
    if(search) {
        orders = orders.filter(o => 
            (o.customerName || '').toLowerCase().includes(search) || 
            (o.customerPhone || '').includes(search) ||
            (o.productName || '').toLowerCase().includes(search)
        );
    }
    
    const activeOrders = orders.filter(o => o.status === 'ACTIVE');
    const delivOrders = orders.filter(o => o.status === 'DELIVERED');
    
    // update stats
    document.getElementById('stat-active-customer-orders').textContent = activeOrders.length;
    document.getElementById('stat-delivered-customer-orders').textContent = delivOrders.length;
    document.getElementById('stat-total-customer-orders').textContent = orders.length;
    
    // update revenue
    const totalRevenue = delivOrders.reduce((sum, o) => sum + (parseFloat(o.price) || 0), 0);
    document.getElementById('stat-delivered-revenue').textContent = totalRevenue + ' ₺';
    
    if(customerOrdersTab === 'ACTIVE') {
        actContainer.classList.remove('hidden');
        delContainer.classList.add('hidden');
        _renderCustOrderGrid(actContainer, activeOrders, true);
    } else {
        actContainer.classList.add('hidden');
        delContainer.classList.remove('hidden');
        _renderCustOrderGrid(delContainer, delivOrders, false);
    }
    if(typeof lucide !== 'undefined') lucide.createIcons();
};

const _renderCustOrderGrid = (container, list, isActive) => {
    if(list.length === 0) {
        container.innerHTML = `<div class="col-span-full text-center py-12 text-stone-500 font-bold bg-white rounded-3xl border border-stone-200 shadow-sm flex flex-col items-center justify-center gap-2"><i data-lucide="inbox" class="w-10 h-10 text-stone-300"></i>Kayıt bulunamadı.</div>`;
        return;
    }
    
    let html = '';
    list.sort((a,b) => b.id - a.id).forEach(o => {
        const dateStr = o.date ? new Date(o.date).toLocaleDateString('tr-TR') : '';
        
        html += `
        <div class="bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] border border-stone-100 flex flex-col relative overflow-hidden transition duration-300">
            ${!isActive ? '<div class="absolute top-4 right-4 bg-emerald-500 text-white px-3 py-1.5 text-xs font-black tracking-wider rounded-xl shadow-lg z-10 flex items-center gap-1.5"><i data-lucide="check-circle-2" class="w-4 h-4"></i> TESLİM EDİLDİ</div>' : ''}
            
            <!-- Hero Image -->
            <div class="relative w-full h-48 bg-stone-50 shrink-0 group border-b border-stone-100">
                ${o.imgUrl ? 
                    `<img src="${o.imgUrl}" class="w-full h-full object-cover cursor-zoom-in" onclick="window.openLightboxModalForOrder(${o.id})">
                     <div class="absolute inset-0 bg-gradient-to-t from-stone-900/60 via-transparent to-transparent pointer-events-none"></div>` 
                    : 
                    `<div class="w-full h-full flex flex-col items-center justify-center text-stone-300 bg-stone-100/50">
                        <i data-lucide="image" class="w-12 h-12 mb-2 opacity-30"></i>
                        <span class="text-[10px] font-black uppercase tracking-widest opacity-40">Görsel Eklenmedi</span>
                    </div>`
                }
                
                <!-- Date/Time Badge overlay -->
                <div class="absolute bottom-4 left-4 bg-white/95 backdrop-blur px-3.5 py-2 rounded-2xl shadow-lg flex items-center gap-2.5 text-stone-800">
                    <div class="bg-amber-100 text-amber-600 p-1.5 rounded-xl">
                        <i data-lucide="calendar-clock" class="w-4 h-4"></i>
                    </div>
                    <div>
                        <div class="text-[9px] font-black text-stone-500 uppercase tracking-widest leading-none mb-1">Teslimat</div>
                        <div class="text-sm font-black leading-none">${dateStr} • ${o.time}</div>
                    </div>
                </div>
            </div>
            
            <!-- Content -->
            <div class="p-6 flex flex-col flex-1 gap-5">
                
                <!-- Customer Info -->
                <div class="flex flex-col">
                    <h3 class="text-2xl font-black text-stone-800 tracking-tight leading-none mb-2">${o.customerName}</h3>
                    <a href="tel:${o.customerPhone}" class="text-sm text-stone-500 font-bold flex items-center gap-1.5 hover:text-amber-600 transition w-max">
                        <i data-lucide="phone-call" class="w-4 h-4"></i> ${o.customerPhone}
                    </a>
                </div>
                
                <!-- Order Content & Pricing (Invoice Style) -->
                <div class="bg-stone-50 rounded-2xl p-5 border border-stone-200/60 shadow-inner mt-2">
                    <div class="flex items-start justify-between gap-4 mb-3">
                        <div>
                            <div class="text-[10px] font-black text-stone-400 uppercase tracking-widest mb-1">Sipariş Edilen</div>
                            <div class="text-lg font-black text-stone-800 leading-tight">${o.productName}</div>
                            ${o.cakeContent ? `<div class="text-[11px] font-bold text-amber-600 mt-1 uppercase tracking-wider">İçerik: ${o.cakeContent}</div>` : ''}
                            ${o.creator ? `<div class="text-[10px] font-bold text-stone-500 mt-1">Siparişi Alan: ${o.creator}</div>` : ''}
                        </div>
                        <div class="bg-white px-3 py-1.5 rounded-xl border border-stone-200 text-center shrink-0 shadow-sm flex flex-col items-center justify-center min-w-[4.5rem]">
                            <div class="text-[9px] font-black text-stone-400 uppercase tracking-widest mb-0.5">Miktar</div>
                            <div class="text-sm font-black text-amber-600 leading-none">${o.qty} <span class="text-xs text-stone-500 font-bold">${o.unit}</span></div>
                        </div>
                    </div>
                    
                    ${o.notes ? `
                    <div class="text-sm font-medium text-stone-600 bg-white p-3.5 rounded-xl border border-amber-200/60 flex items-start gap-2.5 mb-4 shadow-sm">
                        <i data-lucide="message-square" class="w-4 h-4 mt-0.5 text-amber-500 shrink-0"></i> 
                        <span class="leading-relaxed italic">"${o.notes}"</span>
                    </div>` : '<div class="mb-4"></div>'}
                    
                    <div class="border-t-2 border-dashed border-stone-200 pt-4 mt-2">
                        <div class="flex justify-between items-center mb-2">
                            <span class="text-sm text-stone-500 font-bold">Toplam Tutar</span>
                            <span class="text-sm font-black text-stone-700">${o.price} ₺</span>
                        </div>
                        <div class="flex justify-between items-center mb-2">
                            <span class="text-sm text-stone-500 font-bold">Alınan Kapora</span>
                            <span class="text-sm font-black text-emerald-600">${o.deposit > 0 ? '-' + o.deposit + ' ₺' : '0 ₺'}</span>
                        </div>
                        <div class="flex justify-between items-center mt-3 pt-3 border-t border-stone-200/80">
                            <span class="text-sm font-black text-stone-800">Kalan Ödeme</span>
                            ${o.price - o.deposit > 0 
                                ? `<div class="flex items-center gap-2">
                                     <span class="text-lg font-black text-rose-600">${o.price - o.deposit} ₺</span>
                                     <button onclick="payRemainingCustomerOrder(${o.id})" class="bg-emerald-50 hover:bg-emerald-600 hover:text-white text-emerald-600 border border-emerald-200 px-2.5 py-1.5 text-[10px] font-black rounded-lg transition uppercase tracking-wider flex items-center gap-1 shadow-sm shrink-0" title="Kalan ödemeyi tahsil et">
                                         <i data-lucide="banknote" class="w-3.5 h-3.5"></i> Tahsil Et
                                     </button>
                                   </div>` 
                                : `<span class="text-xs font-black text-emerald-700 bg-emerald-100 px-2.5 py-1 rounded-lg border border-emerald-200 uppercase tracking-wider shadow-sm flex items-center gap-1"><i data-lucide="check" class="w-3 h-3"></i> Ödendi</span>`
                            }
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Actions -->
            <div class="px-6 pb-6 pt-2 flex gap-2">
                ${isActive ? `
                <button onclick="completeCustomerOrder(${o.id})" class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-black py-3.5 rounded-2xl shadow-lg shadow-emerald-600/20 transition active:scale-95 flex items-center justify-center gap-2 text-sm">
                    <i data-lucide="check" class="w-5 h-5"></i> Teslim Et
                </button>
                <button onclick="openCustomerOrderModal(${o.id})" class="bg-amber-100 hover:bg-amber-200 text-amber-700 font-black p-3.5 rounded-2xl transition active:scale-95 border border-amber-200 shadow-sm" title="Düzenle"><i data-lucide="pencil" class="w-5 h-5"></i></button>
                <button onclick="printKitchenOrder(${o.id})" class="bg-stone-800 hover:bg-stone-900 text-white font-black p-3.5 rounded-2xl transition active:scale-95 shadow-sm" title="Mutfak Fişi Yazdır"><i data-lucide="printer" class="w-5 h-5"></i></button>
                ` : `
                <button onclick="revertCustomerOrder(${o.id})" class="flex-1 bg-stone-100 hover:bg-stone-200 text-stone-700 font-black py-3.5 rounded-2xl transition active:scale-95 flex items-center justify-center gap-2 text-sm border border-stone-200">
                    <i data-lucide="rotate-ccw" class="w-5 h-5"></i> Geri Al
                </button>
                `}
                <button onclick="deleteCustomerOrder(${o.id})" class="bg-rose-50 hover:bg-rose-100 text-rose-600 font-black p-3.5 rounded-2xl transition active:scale-95 border border-rose-100 shadow-sm" title="Sil"><i data-lucide="trash-2" class="w-5 h-5"></i></button>
            </div>
        </div>
        `;
    });
    container.innerHTML = html;
};

window.openLightboxModalForOrder = (orderId) => {
    const orders = JSON.parse(localStorage.getItem('customerOrders') || '[]');
    const order = orders.find(o => o.id === orderId);
    if(order && order.imgUrl) {
        document.getElementById('lightbox-img').src = order.imgUrl;
        document.getElementById('lightbox-modal').classList.remove('hidden');
    }
};

window.closeLightboxModal = () => {
    document.getElementById('lightbox-modal').classList.add('hidden');
    setTimeout(() => {
        document.getElementById('lightbox-img').src = '';
    }, 200);
};

window.payRemainingCustomerOrder = (id) => {
    window.openConfirmModal('Ödemeyi Tamamla', 'Kalan tutarı tahsil edildi olarak işaretlemek istiyor musunuz?', 'Evet, Tahsil Edildi', () => {
        let orders = JSON.parse(localStorage.getItem('customerOrders') || '[]');
        const idx = orders.findIndex(x => x.id == id);
        if(idx > -1) {
            orders[idx].deposit = orders[idx].price;
            localStorage.setItem('customerOrders', JSON.stringify(orders));
            window.renderCustomerOrders();
        }
        window.closeConfirmModal();
    });
};

let currentReceivableTab = 'ACTIVE';

window.setReceivableTab = (tab) => {
    currentReceivableTab = tab;
    const tabActive = document.getElementById('rec-tab-ACTIVE');
    const tabPaid = document.getElementById('rec-tab-PAID');
    
    if(tab === 'ACTIVE') {
        if(tabActive) tabActive.className = 'px-4 py-2 text-xs font-black rounded-xl transition bg-emerald-600 text-white shadow-sm flex items-center gap-2';
        if(tabActive) tabActive.innerHTML = '<span class="w-2 h-2 rounded-full bg-white animate-pulse"></span> Aktif Alacaklar';
        
        if(tabPaid) tabPaid.className = 'px-4 py-2 text-xs font-black rounded-xl transition bg-stone-100 text-stone-600 hover:bg-stone-200 flex items-center gap-2';
        if(tabPaid) tabPaid.innerHTML = '<i data-lucide="check-circle-2" class="w-3.5 h-3.5 text-emerald-600"></i> Tahsil Edilenler';
    } else {
        if(tabActive) tabActive.className = 'px-4 py-2 text-xs font-black rounded-xl transition bg-stone-100 text-stone-600 hover:bg-stone-200 flex items-center gap-2';
        if(tabActive) tabActive.innerHTML = '<span class="w-2 h-2 rounded-full bg-emerald-500"></span> Aktif Alacaklar';
        
        if(tabPaid) tabPaid.className = 'px-4 py-2 text-xs font-black rounded-xl transition bg-emerald-600 text-white shadow-sm flex items-center gap-2';
        if(tabPaid) tabPaid.innerHTML = '<i data-lucide="check-circle-2" class="w-3.5 h-3.5 text-white"></i> Tahsil Edilenler';
    }
    
    window.renderReceivables();
};

window.renderReceivables = () => {
    const container = document.getElementById('receivables-container');
    if(!container) return;
    
    let allReceivables = JSON.parse(localStorage.getItem('receivables') || '[]');
    const search = (document.getElementById('receivable-search')?.value || '').toLowerCase();
    
    // update stats
    const activeDebts = allReceivables.filter(r => !r.paid);
    const paidDebts = allReceivables.filter(r => r.paid);
    
    const totalActive = activeDebts.reduce((sum, r) => sum + (parseFloat(r.amount) || 0), 0);
    const totalPaid = paidDebts.reduce((sum, r) => sum + (parseFloat(r.amount) || 0), 0);
    
    const statTotal = document.getElementById('stat-total-receivables');
    if(statTotal) statTotal.textContent = totalActive + ' ₺';
    
    const statPaid = document.getElementById('stat-total-paid-receivables');
    if(statPaid) statPaid.textContent = totalPaid + ' ₺';
    
    const homeStat = document.getElementById('home-stat-receivables');
    if(homeStat) homeStat.innerHTML = `${activeDebts.length} Açık Kayıt`;
    
    let displayList = currentReceivableTab === 'ACTIVE' ? activeDebts : paidDebts;
    
    if(search) {
        displayList = displayList.filter(r => 
            (r.name || '').toLowerCase().includes(search) || 
            (r.phone || '').toLowerCase().includes(search) || 
            (r.notes || '').toLowerCase().includes(search)
        );
    }
    
    if(displayList.length === 0) {
        container.innerHTML = `<div class="col-span-full text-center py-12 text-stone-500 font-bold bg-white rounded-3xl border border-stone-200 shadow-sm flex flex-col items-center justify-center gap-2"><i data-lucide="wallet" class="w-10 h-10 text-stone-300"></i>Kayıt bulunamadı.</div>`;
        if(typeof lucide !== 'undefined') lucide.createIcons();
        return;
    }
    
    let html = '';
    displayList.sort((a,b) => b.id - a.id).forEach(r => {
        const dateStr = r.date ? new Date(r.date).toLocaleDateString('tr-TR', { day: '2-digit', month: 'short', year: 'numeric' }) : '';
        const paidDateStr = r.paidDate ? new Date(r.paidDate).toLocaleDateString('tr-TR', { day: '2-digit', month: 'short', year: 'numeric' }) : '';
        
        html += `
        <div class="bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] border border-stone-200/60 flex flex-col relative overflow-hidden transition duration-300 p-6 gap-5 opacity-100">
            <div class="flex items-start justify-between">
                <div>
                    <h3 class="text-xl font-black ${r.paid ? 'text-stone-500 line-through' : 'text-stone-800'} tracking-tight leading-none mb-1">${r.name}</h3>
                    ${r.phone ? `<div class="text-sm font-bold text-stone-500 mb-2 flex items-center gap-1.5"><i data-lucide="phone" class="w-4 h-4"></i> ${r.phone}</div>` : ''}
                    <div class="text-xs font-bold text-stone-400 flex items-center gap-1"><i data-lucide="calendar" class="w-3.5 h-3.5"></i> ${dateStr}</div>
                </div>
                <div class="${r.paid ? 'bg-stone-100 text-stone-500 border-stone-200' : 'bg-rose-50 text-rose-600 border-rose-200'} px-3 py-1.5 rounded-xl border text-lg font-black shadow-sm shrink-0">
                    ${r.amount} ₺
                </div>
            </div>
            
            ${r.notes ? `
            <div class="text-sm font-medium text-stone-600 bg-stone-50 p-3.5 rounded-xl border border-stone-200 flex items-start gap-2.5">
                <i data-lucide="message-square" class="w-4 h-4 mt-0.5 text-amber-500 shrink-0"></i> 
                <span class="leading-relaxed italic">"${r.notes}"</span>
            </div>` : '<div class="flex-1"></div>'}
            
            ${r.paid ? `
            <div class="mt-auto pt-4 border-t border-stone-100 flex gap-2">
                <div class="flex-1 bg-emerald-50 text-emerald-700 font-black py-3 rounded-2xl flex items-center justify-center gap-2 text-sm border border-emerald-200">
                    <i data-lucide="check-double" class="w-5 h-5"></i> ${paidDateStr} Tarihinde Tahsil Edildi
                </div>
                <button onclick="deleteReceivable(${r.id})" class="bg-rose-50 hover:bg-rose-600 hover:text-white text-rose-600 p-3 rounded-2xl transition border border-rose-200 shadow-sm">
                    <i data-lucide="trash-2" class="w-5 h-5"></i>
                </button>
            </div>
            ` : `
            <div class="mt-auto pt-4 border-t border-stone-100 flex gap-2">
                <button onclick="payReceivable(${r.id})" class="flex-1 bg-emerald-50 hover:bg-emerald-600 hover:text-white text-emerald-600 font-black py-3 rounded-2xl transition active:scale-95 flex items-center justify-center gap-2 text-sm border border-emerald-200 shadow-sm">
                    <i data-lucide="check-circle-2" class="w-5 h-5"></i> Tahsil Et
                </button>
                <button onclick="deleteReceivable(${r.id})" class="bg-rose-50 hover:bg-rose-600 hover:text-white text-rose-600 p-3 rounded-2xl transition border border-rose-200 shadow-sm">
                    <i data-lucide="trash-2" class="w-5 h-5"></i>
                </button>
            </div>
            `}
        </div>
        `;
    });
    container.innerHTML = html;
    if(typeof lucide !== 'undefined') lucide.createIcons();
};

window.openReceivableModal = () => {
    document.getElementById('receivable-id').value = '';
    document.getElementById('receivable-name').value = '';
    document.getElementById('receivable-phone').value = '';
    document.getElementById('receivable-amount').value = '';
    document.getElementById('receivable-notes').value = '';
    document.getElementById('receivable-modal').classList.remove('hidden');
};

window.closeReceivableModal = () => {
    document.getElementById('receivable-modal').classList.add('hidden');
};

window.submitReceivable = (e) => {
    e.preventDefault();
    const name = document.getElementById('receivable-name').value;
    const phone = document.getElementById('receivable-phone').value;
    const amount = document.getElementById('receivable-amount').value;
    const notes = document.getElementById('receivable-notes').value;
    
    let receivables = JSON.parse(localStorage.getItem('receivables') || '[]');
    
    receivables.push({
        id: Date.now(),
        name,
        phone,
        amount,
        notes,
        date: new Date().toISOString(),
        paid: false
    });
    
    localStorage.setItem('receivables', JSON.stringify(receivables));
    window.closeReceivableModal();
    window.renderReceivables();
};

window.payReceivable = (id) => {
    window.openConfirmModal('Tahsilat Onayı', 'Bu açık hesap tahsil edildi olarak işaretlenecek ve geçmişe taşınacak. Onaylıyor musunuz?', 'Evet, Tahsil Et', () => {
        let receivables = JSON.parse(localStorage.getItem('receivables') || '[]');
        const r = receivables.find(x => x.id === id);
        if(r) {
            r.paid = true;
            r.paidDate = new Date().toISOString();
        }
        localStorage.setItem('receivables', JSON.stringify(receivables));
        window.renderReceivables();
        window.closeConfirmModal();
    });
};

window.deleteReceivable = (id) => {
    window.openConfirmModal('Silme Onayı', 'Bu alacak kaydını silmek istediğinize emin misiniz? Bu işlem geri alınamaz.', 'Evet, Sil', () => {
        let receivables = JSON.parse(localStorage.getItem('receivables') || '[]');
        receivables = receivables.filter(x => x.id !== id);
        localStorage.setItem('receivables', JSON.stringify(receivables));
        window.renderReceivables();
        window.closeConfirmModal();
    });
};

window.previewInventoryImageUrlInput = (val) => {
    document.getElementById('inventory-img-url').value = val;
    document.getElementById('inventory-img-file').value = '';
    window.previewInventoryImageUrl(val);
};

window.previewInventoryImageFile = (input) => {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var img = new Image();
            img.onload = function() {
                var canvas = document.createElement('canvas');
                var ctx = canvas.getContext('2d');
                var MAX_WIDTH = 500;
                var width = img.width;
                var height = img.height;
                
                if (width > MAX_WIDTH) {
                    height *= MAX_WIDTH / width;
                    width = MAX_WIDTH;
                }
                
                canvas.width = width;
                canvas.height = height;
                ctx.drawImage(img, 0, 0, width, height);
                
                var dataUrl = canvas.toDataURL('image/jpeg', 0.6); // Compress to ~30-50kb
                
                document.getElementById('inventory-img-preview').src = dataUrl;
                document.getElementById('inventory-img-preview-box').classList.remove('hidden');
                document.getElementById('inventory-img-url').value = dataUrl;
                document.getElementById('inventory-img-url-input').value = '';
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
};

window.previewInventoryImageUrl = (val) => {
    if(val && val.trim() !== '') {
        document.getElementById('inventory-img-preview').src = val;
        document.getElementById('inventory-img-preview-box').classList.remove('hidden');
    } else {
        window.removeInventoryImagePreview();
    }
};

window.removeInventoryImagePreview = () => {
    document.getElementById('inventory-img-preview').src = '';
    document.getElementById('inventory-img-preview-box').classList.add('hidden');
    document.getElementById('inventory-img-file').value = '';
    document.getElementById('inventory-img-url').value = '';
    document.getElementById('inventory-img-url-input').value = '';
};

window.openInventoryModal = (id = null) => {
    let inv = null;
    if(id) {
        const inventory = JSON.parse(localStorage.getItem('inventory') || '[]');
        inv = inventory.find(x => x.id === id);
    }
    
    document.getElementById('inventory-id').value = inv ? inv.id : '';
    document.getElementById('inventory-name').value = inv ? inv.name : '';
    document.getElementById('inventory-amount').value = inv ? inv.amount : '';
    document.getElementById('inventory-critical').value = inv ? (inv.critical || '') : '';
    document.getElementById('inventory-unit').value = inv ? inv.unit : 'Adet';
    document.getElementById('inventory-notes').value = inv ? inv.notes : '';
    document.getElementById('inventory-modal-title').textContent = inv ? 'Envanter Ürünü Düzenle' : 'Yeni Ürün Ekle';
    const imgUrlStr = inv ? (inv.imgUrl || '') : '';
    document.getElementById('inventory-img-url').value = imgUrlStr;
    document.getElementById('inventory-img-url-input').value = imgUrlStr.startsWith('data:') ? '' : imgUrlStr;
    window.previewInventoryImageUrl(imgUrlStr);
    
    populateInvCategoryDropdown(inv ? inv.category : '');
    
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
    }
    
    try {
        localStorage.setItem('inventory', JSON.stringify(inventory));
        window.closeInventoryModal();
        window.renderInventory();
    } catch(err) {
        console.error(err);
        window.showToast('Depolama alanı dolu! Lütfen ürün görsellerini küçültün veya bazılarını silin.', 'error');
    }
};


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
    
    let displayList = inventory;
    if(search) {
        displayList = inventory.filter(r => 
            (r.name || '').toLowerCase().includes(search) || 
            (r.notes || '').toLowerCase().includes(search)
        );
    }
    
    let html = '';
    
    let cats = getInvCategories();
    let uncatItems = displayList.filter(r => !r.category);
    
    const renderCard = (r) => {
        const dateStr = r.lastUpdated ? new Date(r.lastUpdated).toLocaleDateString('tr-TR', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : '';
        let isCritical = false;
        let criticalBadge = '';
        let cardBorderClass = 'border-stone-200/60';
        if (r.critical && parseFloat(r.amount) <= parseFloat(r.critical)) {
            isCritical = true;
            cardBorderClass = 'border-rose-500 shadow-[0_0_15px_rgba(244,63,94,0.1)]';
            criticalBadge = `<div class="absolute top-0 right-0 z-20 bg-rose-500 text-white text-[10px] font-black uppercase tracking-widest py-2 px-4 rounded-bl-3xl shadow-md flex items-center gap-1"><i data-lucide="alert-triangle" class="w-3 h-3"></i> Kritik</div>`;
        }

        let imgHtml = '';
        if (r.imgUrl) {
            imgHtml = `<div class="-mx-6 -mt-6 mb-4 h-48 bg-stone-100 overflow-hidden relative border-b border-stone-200">
                <img src="${r.imgUrl}" class="w-full h-full object-cover" alt="${r.name}">
            </div>`;
        }

        return `
        <div class="bg-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_8px_30px_rgb(0,0,0,0.08)] border ${cardBorderClass} flex flex-col relative overflow-hidden transition duration-300 p-6 gap-5">
            ${criticalBadge}
            ${imgHtml}
            <div class="flex items-start justify-between relative z-10">
                <div class="pr-4">
                    <h3 class="text-xl font-black text-stone-800 tracking-tight leading-none mb-2">${r.name}</h3>
                    <div class="text-xs font-bold text-stone-400 flex items-center gap-1"><i data-lucide="clock" class="w-3.5 h-3.5"></i> Son G. ${dateStr}</div>
                </div>
                <div class="text-right shrink-0">
                    <div class="inline-flex items-baseline gap-1 bg-amber-50 text-amber-600 px-3 py-1.5 rounded-xl border border-amber-200">
                        <span class="text-xl font-black leading-none">${r.amount}</span>
                        <span class="text-[10px] font-black uppercase tracking-widest">${r.unit}</span>
                    </div>
                </div>
            </div>

            <div class="flex items-center gap-2 mt-auto pt-2 border-t border-stone-100 relative z-10">
                <button onclick="updateInventoryAmount(${r.id}, -1)" class="w-10 h-10 rounded-xl bg-stone-50 border border-stone-200 text-stone-600 font-bold text-lg hover:bg-stone-100 transition flex items-center justify-center shrink-0">-</button>
                <button onclick="updateInventoryAmount(${r.id}, 1)" class="w-10 h-10 rounded-xl bg-stone-50 border border-stone-200 text-stone-600 font-bold text-lg hover:bg-stone-100 transition flex items-center justify-center shrink-0">+</button>
                <div class="flex-1"></div>
                
                <button onclick="openInventoryModal(${r.id})" class="h-10 px-4 rounded-xl text-stone-500 hover:text-stone-800 hover:bg-stone-100 transition flex items-center gap-2 font-bold text-sm shrink-0">
                    <i data-lucide="edit-2" class="w-4 h-4"></i> Düzenle
                </button>
                
                <button onclick="deleteInventory(${r.id})" class="w-10 h-10 rounded-xl text-rose-400 hover:text-rose-600 hover:bg-rose-50 transition flex items-center justify-center shrink-0">
                    <i data-lucide="trash-2" class="w-4 h-4"></i>
                </button>
            </div>
        </div>
        `;
    };

    let hasAnyRendered = false;

    cats.forEach(c => {
        let items = displayList.filter(r => r.category === c);
        
        if (items.length > 0 || !search) {
            hasAnyRendered = true;
            let safeCatId = 'inv-cat-' + c.replace(/\s+/g, '-').replace(/[^a-zA-Z0-9-]/g, '');
            // Auto-expand if searching, otherwise collapsed by default or whatever (let's do expanded by default for now, or match toggleInvCategory state)
            let isExpanded = window.openInvCategories ? window.openInvCategories.has(safeCatId) : true;
            if (search) isExpanded = true;
            let isHidden = isExpanded ? '' : 'hidden';
            let isRotated = isExpanded ? '' : '-rotate-90';

            html += `
            <div class="mb-2">
                <div class="flex items-center justify-between mb-4 border-b border-stone-200 pb-2 cursor-pointer group" onclick="toggleInvCategory('${safeCatId}')">
                    <h2 class="text-xl font-black text-stone-800 uppercase tracking-widest flex items-center gap-2 select-none">
                        <i id="${safeCatId}-icon" data-lucide="chevron-down" class="w-5 h-5 transition-transform ${isRotated}"></i>
                        ${c}
                    </h2>
                    <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity" onclick="event.stopPropagation()">
                        <button onclick="editInvCategory('${c.replace("'", "\'")}')" class="text-stone-400 hover:text-stone-700 transition px-2" title="Kategoriyi Düzenle"><i data-lucide="edit-2" class="w-4 h-4"></i></button>
                        <button onclick="deleteInvCategory('${c.replace("'", "\'")}')" class="text-rose-400 hover:text-rose-600 transition px-2" title="Kategoriyi Sil"><i data-lucide="trash-2" class="w-4 h-4"></i></button>
                    </div>
                </div>
                <div id="${safeCatId}" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 ${isHidden}">
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
        }
    });
    
    if(uncatItems.length > 0) {
        hasAnyRendered = true;
        html += `
        <div class="mb-2">
            <h2 class="text-xl font-black text-stone-800 mb-4 border-b border-stone-200 pb-2 uppercase tracking-widest">Kategorisiz</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                ${uncatItems.sort((a,b) => b.id - a.id).map(renderCard).join('')}
            </div>
        </div>
        `;
    }

    if (!hasAnyRendered) {
        html = `<div class="col-span-full text-center py-12 text-stone-500 font-bold bg-white rounded-3xl border border-stone-200 shadow-sm flex flex-col items-center justify-center gap-2"><i data-lucide="package" class="w-10 h-10 text-stone-300"></i>Kayıt bulunamadı.</div>`;
    }

    container.innerHTML = html;
    if(typeof lucide !== 'undefined') lucide.createIcons();
};


window.updateFinancePrice = (id, type, value) => {
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    const index = prods.findIndex(p => p.id === id);
    if(index > -1) {
        if(type === 'cost') {
            prods[index].costPrice = parseFloat(value) || 0;
        } else if(type === 'sell') {
            prods[index].sellPrice = parseFloat(value) || 0;
        }
        localStorage.setItem('products', JSON.stringify(prods));
        window.renderFinance();
    }
};

// Optional: Add global toggle function at the top of this block if we want it isolated, or just attach it to window
window.toggleFinanceCategory = (catId) => {
    const rows = document.querySelectorAll(`.finance-row-${catId}`);
    const icon = document.getElementById(`finance-icon-${catId}`);
    let isHidden = false;
    
    rows.forEach(row => {
        if (row.classList.contains('hidden')) {
            row.classList.remove('hidden');
            isHidden = false;
        } else {
            row.classList.add('hidden');
            isHidden = true;
        }
    });
    
    if (icon) {
        if (isHidden) {
            icon.classList.add('-rotate-90');
        } else {
            icon.classList.remove('-rotate-90');
        }
    }
};
window.financeSortMode = window.financeSortMode || 'CATEGORY';

window.setFinanceSortMode = (mode) => {
    window.financeSortMode = mode;
    window.renderFinance();
};

window.renderFinance = () => {
    const tbody = document.getElementById('finance-tbody');
    if(!tbody) return;
    
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let cats = JSON.parse(localStorage.getItem('categories') || '[]');
    let html = '';
    
    // Calculate net profit for each product beforehand for sorting
    prods.forEach(p => {
        const produced = p.totalEntered !== undefined ? p.totalEntered : ((p.stock || 0) + (p.sales || 0) + (p.waste || 0));
        const waste = parseFloat(p.waste) || 0;
        const remaining = parseFloat(p.stock) || 0;
        let sold = parseFloat(p.sales) || 0;
        
        const costPrice = parseFloat(p.costPrice) || 0;
        const sellPrice = parseFloat(p.sellPrice) || 0;
        
        p._revenue = sold * sellPrice;
        p._costOfSold = sold * costPrice;
        p._wasteLoss = waste * costPrice;
        p._netProfit = p._revenue - p._costOfSold - p._wasteLoss;
        p._produced = produced;
        p._waste = waste;
        p._sold = sold;
    });
    
    const renderProductRow = (p, catIndex = '') => {
        const isLoss = p._netProfit < 0;
        const profitColor = isLoss ? 'text-rose-600' : 'text-emerald-600';
        const profitSign = isLoss ? '-' : '+';
        const profitIcon = isLoss ? 'trending-down' : 'trending-up';
        
        const rowClass = catIndex !== '' ? `finance-row-${catIndex}` : '';
        const paddingClass = catIndex !== '' ? 'pl-8' : '';
        const catBadge = catIndex === '' ? `<div class="text-xs font-bold text-stone-400 mt-0.5">${p.category || 'Diğer'}</div>` : '';

        return `
        <tr class="hover:bg-stone-50/50 transition ${rowClass}">
            <td class="p-4 ${paddingClass}">
                <div class="font-black text-stone-800">${p.name}</div>
                ${catBadge}
            </td>
            <td class="p-4 text-center">
                <div class="flex items-center justify-center gap-3 text-sm font-bold">
                    <span class="text-blue-600 bg-blue-50 px-2 py-0.5 rounded" title="Üretilen (Vitrine Çıkan)">${p._produced}</span>
                    <span class="text-stone-300">/</span>
                    <span class="text-rose-600 bg-rose-50 px-2 py-0.5 rounded" title="Fire">${p._waste}</span>
                    <span class="text-stone-300">/</span>
                    <span class="text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded" title="Satılan">${p._sold}</span>
                </div>
            </td>
            <td class="p-4">
                <div class="relative">
                    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-stone-400 font-bold text-sm">₺</div>
                    <input type="number" step="0.01" min="0" onchange="updateFinancePrice(${p.id}, 'cost', this.value)" value="${p.costPrice || ''}" placeholder="0.00" class="w-full bg-white border border-stone-200 rounded-lg py-1.5 pl-7 pr-2 text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-amber-500">
                </div>
            </td>
            <td class="p-4">
                <div class="relative">
                    <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none text-stone-400 font-bold text-sm">₺</div>
                    <input type="number" step="0.01" min="0" onchange="updateFinancePrice(${p.id}, 'sell', this.value)" value="${p.sellPrice || ''}" placeholder="0.00" class="w-full bg-white border border-stone-200 rounded-lg py-1.5 pl-7 pr-2 text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-amber-500">
                </div>
            </td>
            <td class="p-4 text-right font-bold text-emerald-600">
                ₺${p._revenue.toFixed(2)}
            </td>
            <td class="p-4 text-right font-bold text-rose-600">
                ₺${p._wasteLoss.toFixed(2)}
            </td>
            <td class="p-4 text-right">
                <div class="flex items-center justify-end gap-1 font-black ${profitColor}">
                    <i data-lucide="${profitIcon}" class="w-4 h-4"></i>
                    ${profitSign}₺${Math.abs(p._netProfit).toFixed(2)}
                </div>
            </td>
        </tr>`;
    };

    if (window.financeSortMode === 'CATEGORY') {
        const grouped = {};
        cats.forEach(c => grouped[c] = []);
        prods.forEach(p => {
            const cat = p.category || 'Diğer';
            if (!grouped[cat]) grouped[cat] = [];
            grouped[cat].push(p);
        });

        let catIndex = 0;
        Object.keys(grouped).sort().forEach(cat => {
            catIndex++;
            html += `
            <tr class="bg-stone-100/80 cursor-pointer hover:bg-stone-200/60 transition" onclick="toggleFinanceCategory(${catIndex})">
                <td colspan="7" class="p-3 pl-4 font-black text-stone-800 text-sm border-y border-stone-200">
                    <div class="flex items-center gap-2">
                        <i id="finance-icon-${catIndex}" data-lucide="chevron-down" class="w-4 h-4 text-stone-500 transition-transform duration-200"></i>
                        ${cat}
                    </div>
                </td>
            </tr>`;
            grouped[cat].sort((a, b) => b.id - a.id).forEach(p => {
                html += renderProductRow(p, catIndex);
            });
        });
        
        if (prods.length === 0 && cats.length === 0) {
            html = `<tr><td colspan="7" class="p-8 text-center text-stone-500 font-bold">Kayıtlı ürün veya kategori bulunmamaktadır.</td></tr>`;
        }
    } else {
        // Flat list sorting
        if (window.financeSortMode === 'PROFIT_DESC') {
            prods.sort((a, b) => b._netProfit - a._netProfit);
        } else if (window.financeSortMode === 'PROFIT_ASC') {
            prods.sort((a, b) => a._netProfit - b._netProfit);
        }
        
        if (prods.length === 0) {
            html = `<tr><td colspan="7" class="p-8 text-center text-stone-500 font-bold">Kayıtlı ürün bulunmamaktadır.</td></tr>`;
        } else {
            prods.forEach(p => {
                html += renderProductRow(p, '');
            });
        }
    }
    
    tbody.innerHTML = html;
    if(typeof lucide !== 'undefined') lucide.createIcons();
    
    // Update active state of sort buttons if they exist
    const btns = document.querySelectorAll('.finance-sort-btn');
    btns.forEach(btn => {
        if(btn.dataset.sort === window.financeSortMode) {
            btn.classList.add('bg-stone-800', 'text-white');
            btn.classList.remove('bg-stone-100', 'text-stone-600', 'hover:bg-stone-200');
        } else {
            btn.classList.remove('bg-stone-800', 'text-white');
            btn.classList.add('bg-stone-100', 'text-stone-600', 'hover:bg-stone-200');
        }
    });
};
window.expandAllFinanceCategories = () => {
    let i = 1;
    while(true) {
        const rows = document.querySelectorAll(`.finance-row-${i}`);
        const icon = document.getElementById(`finance-icon-${i}`);
        if(!icon && rows.length === 0) {
            // Give up if no more categories found. Wait, let's just check icon.
            if(i > 100) break; // safety
        }
        
        if (rows.length > 0) {
            rows.forEach(row => row.classList.remove('hidden'));
        }
        if(icon) {
            icon.classList.remove('-rotate-90');
        }
        i++;
    }
};

window.collapseAllFinanceCategories = () => {
    let i = 1;
    while(true) {
        const rows = document.querySelectorAll(`.finance-row-${i}`);
        const icon = document.getElementById(`finance-icon-${i}`);
        if(!icon && rows.length === 0) {
            if(i > 100) break; // safety
        }
        
        if (rows.length > 0) {
            rows.forEach(row => row.classList.add('hidden'));
        }
        if(icon) {
            icon.classList.add('-rotate-90');
        }
        i++;
    }
};

window.resetFinanceStats = () => {
    if(!confirm('Tüm ürünlerin satış, fire ve geçmiş analiz verileri sıfırlanacak! Sadece şu anki güncel stok miktarları kalacak. Devam etmek istiyor musunuz?')) return;
    
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    prods.forEach(p => {
        p.sales = 0;
        p.waste = 0;
        p.history = {};
        p.totalEntered = p.stock || 0; // The only "produced" amount is now whatever is currently in stock
    });
    
    localStorage.setItem('products', JSON.stringify(prods));
    if (window.renderFinance) window.renderFinance();
    if (window.renderProducts) window.renderProducts();
    if (window.updateGlobalStats) window.updateGlobalStats();
    showToast('Test verileri başarıyla sıfırlandı. Tüm istatistikler ve kar/zarar durumları baştan başlayacak.');
};

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
        totalPanel.classList.remove('hidden');
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
        document.getElementById('recipe-sell-price').value = p.sellPrice || '';
    }
    
    renderRecipeIngredients();
};

window.updateRecipeItemCost = (index, val) => {
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
        totalPanel.classList.remove('hidden');
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
    if(window.calculateRecipeProfit) window.calculateRecipeProfit();
    
    if(typeof lucide !== 'undefined') lucide.createIcons();
};window.openRecipeIngredientModal = () => {
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

window.calculateRecipeProfit = () => {
    const cost = window.currentRecipeGrandTotal || 0;
    const sellInput = document.getElementById('recipe-sell-price');
    const profitEl = document.getElementById('recipe-profit-amount');
    const percentEl = document.getElementById('recipe-profit-percent');
    
    let sell = parseFloat(sellInput.value);
    if(isNaN(sell)) sell = 0;
    
    let profit = sell - cost;
    profitEl.textContent = profit.toFixed(2);
    
    if(profit > 0) {
        profitEl.className = 'text-2xl font-black text-emerald-600 flex items-baseline gap-1';
        percentEl.className = 'text-[10px] font-bold text-emerald-600 bg-emerald-50 px-1.5 py-0.5 rounded inline-block mt-0.5';
    } else if(profit < 0) {
        profitEl.className = 'text-2xl font-black text-rose-600 flex items-baseline gap-1';
        percentEl.className = 'text-[10px] font-bold text-rose-600 bg-rose-50 px-1.5 py-0.5 rounded inline-block mt-0.5';
    } else {
        profitEl.className = 'text-2xl font-black text-stone-400 flex items-baseline gap-1';
        percentEl.className = 'text-[10px] font-bold text-stone-400 bg-stone-100 px-1.5 py-0.5 rounded inline-block mt-0.5';
    }
    
    if(cost > 0 && sell > 0) {
        let margin = (profit / sell) * 100;
        percentEl.textContent = `%${margin.toFixed(0)} Kar Marjı`;
    } else {
        percentEl.textContent = `%0 Kar Marjı`;
    }
};

window.saveRecipeCostToProduct = () => {
    if(!currentRecipeProductId) return;
    
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    let p = prods.find(x => String(x.id) === currentRecipeProductId);
    if(p) {
        p.costPrice = window.currentRecipeGrandTotal;
        
        let sell = parseFloat(document.getElementById('recipe-sell-price').value);
        if(!isNaN(sell)) p.sellPrice = sell;
        
        localStorage.setItem('products', JSON.stringify(prods));
        document.getElementById('recipe-product-old-cost').textContent = p.costPrice.toFixed(2) + " ₺";
        
        if(window.renderFinance) window.renderFinance();
        
        alert(`${p.name} fiyatları başarıyla güncellendi!
Maliyet: ${p.costPrice.toFixed(2)} ₺ 
Satış: ${p.sellPrice.toFixed(2)} ₺`);
    }
};





// ==================== B2B LEDGER LOGIC ====================

let activeB2BCustomerId = null;

window.renderB2BRecords = () => {
    // Keep this for backwards compatibility with the DOMContentLoaded call in app_v4.js
    window.renderB2BAgenda();
};

window.renderB2BAgenda = () => {
    const searchInput = document.getElementById('b2b-customer-search');
    const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
    const customerListEl = document.getElementById('b2b-customer-list');
    if(!customerListEl) return;
    
    const customers = JSON.parse(localStorage.getItem('b2b_customers') || '[]');
    const records = JSON.parse(localStorage.getItem('b2b_records') || '[]');
    
    // Calculate balances
    const balances = {};
    customers.forEach(c => balances[c.id] = 0);
    
    records.forEach(r => {
        if(!balances[r.customerId] && balances[r.customerId] !== 0) {
            balances[r.customerId] = 0; // If deleted customer?
        }
        if(r.type === 'BORC') balances[r.customerId] += r.amount;
        else if(r.type === 'TAHSILAT') balances[r.customerId] -= r.amount;
    });
    
    let html = '';
    
    let filteredCustomers = customers;
    if(query !== '') {
        filteredCustomers = customers.filter(c => c.name.toLowerCase().includes(query));
    }
    
    // Sort by name
    filteredCustomers.sort((a,b) => a.name.localeCompare(b.name, 'tr'));
    
    if(filteredCustomers.length === 0) {
        html = `<div class="p-4 text-center text-stone-400 font-bold text-sm">Firma bulunamadı.</div>`;
    } else {
        filteredCustomers.forEach(c => {
            const bal = balances[c.id] || 0;
            const isActive = activeB2BCustomerId === c.id;
            
            let balColor = bal > 0 ? 'text-indigo-600' : (bal < 0 ? 'text-emerald-600' : 'text-stone-400');
            let balText = bal > 0 ? `${bal.toFixed(2)} ₺ Alacaklıyız` : (bal < 0 ? `${Math.abs(bal).toFixed(2)} ₺ Fazla Ödeme` : 'Bakiye Yok');
            
            html += `
                <button onclick="window.selectB2BCustomer('${c.id}')" class="w-full text-left p-4 rounded-2xl border-2 transition ${isActive ? 'border-indigo-500 bg-indigo-50 shadow-sm' : 'border-transparent hover:bg-stone-50 hover:border-stone-200'}">
                    <div class="font-black text-stone-800 text-lg">${c.name}</div>
                    <div class="text-xs font-bold mt-1 ${balColor}">${balText}</div>
                </button>
            `;
        });
    }
    
    customerListEl.innerHTML = html;
    if(typeof lucide !== 'undefined') lucide.createIcons();
    
    // If there is an active customer, re-render their page
    if(activeB2BCustomerId) {
        window.selectB2BCustomer(activeB2BCustomerId);
    }
};

window.selectB2BCustomer = (customerId) => {
    activeB2BCustomerId = customerId;
    
    const customers = JSON.parse(localStorage.getItem('b2b_customers') || '[]');
    const customer = customers.find(c => c.id === customerId);
    
    // Re-render sidebar to update selected state visually
    const searchInput = document.getElementById('b2b-customer-search');
    const query = searchInput ? searchInput.value.trim().toLowerCase() : '';
    // We only need to update the classes in the DOM, but for simplicity, we can just let renderB2BAgenda do it,
    // wait, if we call renderB2BAgenda from here, it will infinite loop because it calls selectB2BCustomer.
    // Let's just do a manual class update on the sidebar elements.
    const customerListEl = document.getElementById('b2b-customer-list');
    if(customerListEl) {
        const buttons = customerListEl.querySelectorAll('button');
        buttons.forEach(btn => {
            const onclick = btn.getAttribute('onclick');
            if(onclick && onclick.includes(`'${customerId}'`)) {
                btn.className = "w-full text-left p-4 rounded-2xl border-2 transition border-indigo-500 bg-indigo-50 shadow-sm";
            } else {
                btn.className = "w-full text-left p-4 rounded-2xl border-2 transition border-transparent hover:bg-stone-50 hover:border-stone-200";
            }
        });
    }
    
    if(!customer) return;
    
    const allRecords = JSON.parse(localStorage.getItem('b2b_records') || '[]');
    let records = allRecords.filter(r => r.customerId === customerId);
    records.sort((a,b) => new Date(a.date) - new Date(b.date)); // chronological order for ledger
    
    let totalBal = 0;
    records.forEach(r => {
        if(r.type === 'BORC') totalBal += r.amount;
        else if(r.type === 'TAHSILAT') totalBal -= r.amount;
    });
    
    const pageEl = document.getElementById('b2b-page-content');
    if(!pageEl) return;
    
    let balColor = totalBal > 0 ? 'text-indigo-600' : (totalBal < 0 ? 'text-emerald-600' : 'text-stone-500');
    let balText = totalBal > 0 ? `${totalBal.toFixed(2)} ₺ Bakiye (Alacaklıyız)` : (totalBal < 0 ? `${Math.abs(totalBal).toFixed(2)} ₺ Fazla Ödeme (Borçluyuz)` : '0.00 ₺ Bakiye');
    
    let html = `
        <div class="flex items-center justify-between border-b-2 border-stone-200 pb-6 mb-6">
            <div>
                <h3 class="text-3xl font-black text-stone-900 font-serif tracking-tight">${customer.name}</h3>
                <div class="text-lg font-bold mt-1 ${balColor}">${balText}</div>
            </div>
            <div class="flex items-center gap-2">
                <button onclick="window.openB2BModal('BORC', '${customerId}')" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-xl font-black transition active:scale-95 shadow-sm text-sm">
                    + Ürün Satışı
                </button>
                <button onclick="window.openB2BModal('TAHSILAT', '${customerId}')" class="bg-emerald-600 hover:bg-emerald-700 text-white px-4 py-2 rounded-xl font-black transition active:scale-95 shadow-sm text-sm">
                    + Tahsilat
                </button>
            </div>
        </div>
        
        <div class="flex-1 overflow-y-auto pr-2 space-y-4">
    `;
    
    if(records.length === 0) {
        html += `<div class="text-center text-stone-400 font-bold italic py-12">Henüz bu deftere bir kayıt girilmemiş.</div>`;
    } else {
        html += `<div class="w-full">`;
        
        let runningTotal = 0;
        records.forEach(r => {
            if(r.type === 'BORC') runningTotal += r.amount;
            else if(r.type === 'TAHSILAT') runningTotal -= r.amount;
            
            const dateStr = new Date(r.date).toLocaleDateString('tr-TR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });
            
            const isBorc = r.type === 'BORC';
            
            html += `
                <div class="relative group flex items-start gap-4 p-4 rounded-xl hover:bg-stone-100/50 transition border-b border-stone-200/50 border-dashed">
                    <div class="w-12 h-12 rounded-xl shrink-0 flex items-center justify-center font-black ${isBorc ? 'bg-indigo-50 text-indigo-600' : 'bg-emerald-50 text-emerald-600'}">
                        ${isBorc ? '<i data-lucide="package-minus" class="w-5 h-5"></i>' : '<i data-lucide="banknote" class="w-5 h-5"></i>'}
                    </div>
                    
                    <div class="flex-1">
                        <div class="flex items-center justify-between mb-1">
                            <span class="text-xs font-black text-stone-400">${dateStr}</span>
                            <button onclick="window.deleteB2BRecord('${r.id}')" class="opacity-0 group-hover:opacity-100 w-6 h-6 rounded bg-red-50 text-red-500 flex items-center justify-center transition" title="Kaydı Sil">
                                <i data-lucide="trash-2" class="w-3 h-3"></i>
                            </button>
                        </div>
                        <div class="font-bold text-stone-800 whitespace-pre-line leading-relaxed">${r.desc || '-'}</div>
                        <div class="flex items-center justify-between mt-2">
                            <div class="text-xs font-black ${isBorc ? 'text-indigo-600' : 'text-emerald-600'}">${isBorc ? 'Satış (+)' : 'Ödeme (-)'}</div>
                            <div class="font-black ${isBorc ? 'text-indigo-600' : 'text-emerald-600'} text-lg">${r.amount.toFixed(2)} ₺</div>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += `</div>`;
    }
    
    html += `</div>`; // end scroll area
    
    pageEl.innerHTML = html;
    if(typeof lucide !== 'undefined') lucide.createIcons();
};

window.openB2BModal = (type = 'BORC', customerId = null) => {
    document.getElementById('b2b-modal').classList.remove('hidden');
    document.getElementById('b2b-desc').value = '';
    document.getElementById('b2b-amount').value = '';
    
    if(type === 'BORC') {
        document.querySelector('input[name="b2b_type"][value="BORC"]').checked = true;
    } else {
        document.querySelector('input[name="b2b_type"][value="TAHSILAT"]').checked = true;
    }
    window.toggleB2BTypeUI();
    
    window.renderCustomerOptions(customerId || activeB2BCustomerId);
};

window.toggleB2BTypeUI = () => {
    const type = document.querySelector('input[name="b2b_type"]:checked').value;
    const descInput = document.getElementById('b2b-desc');
    const select = document.getElementById('b2b-customer-select');
    
    if(type === 'BORC') {
        descInput.placeholder = 'Örn: 25 Adet Simit, 30 Adet Poğaça';
        select.classList.remove('ring-emerald-500');
        select.classList.add('ring-indigo-500');
    } else {
        descInput.placeholder = 'Örn: Havale geldi, Nakit alındı vb.';
        select.classList.remove('ring-indigo-500');
        select.classList.add('ring-emerald-500');
    }
};

window.renderCustomerOptions = (selectVal = null) => {
    const select = document.getElementById('b2b-customer-select');
    if(!select) return;
    const customers = JSON.parse(localStorage.getItem('b2b_customers') || '[]');
    let html = `<option value="">-- Müşteri Seçiniz --</option>`;
    customers.forEach(s => {
        html += `<option value="${s.id}">${s.name}</option>`;
    });
    select.innerHTML = html;
    if(selectVal) select.value = selectVal;
};

window.addNewCustomerPrompt = () => {
    document.getElementById('new-customer-input').value = '';
    document.getElementById('new-customer-modal').classList.remove('hidden');
    setTimeout(() => document.getElementById('new-customer-input').focus(), 100);
};

window.submitNewCustomer = (e) => {
    e.preventDefault();
    const name = document.getElementById('new-customer-input').value.trim();
    if(name.length > 0) {
        const customers = JSON.parse(localStorage.getItem('b2b_customers') || '[]');
        const newCustomer = { id: Date.now().toString(), name: name };
        customers.push(newCustomer);
        localStorage.setItem('b2b_customers', JSON.stringify(customers));
        window.showToast(name + " firması cari deftere eklendi.");
        window.renderCustomerOptions(newCustomer.id);
        window.closeModal('new-customer-modal');
        window.renderB2BAgenda();
        window.selectB2BCustomer(newCustomer.id);
    }
};

window.submitB2BRecord = (e) => {
    e.preventDefault();
    const type = document.querySelector('input[name="b2b_type"]:checked').value;
    const select = document.getElementById('b2b-customer-select');
    const desc = document.getElementById('b2b-desc').value.trim();
    const amount = parseFloat(document.getElementById('b2b-amount').value);
    
    if(!select.value || isNaN(amount) || amount <= 0) {
        window.showToast("Lütfen tüm alanları doldurun.", "error");
        return;
    }
    
    const customerName = select.options[select.selectedIndex].text;
    
    const records = JSON.parse(localStorage.getItem('b2b_records') || '[]');
    records.push({
        id: Date.now().toString(),
        date: new Date().toISOString(),
        type: type,
        customerId: select.value,
        customerName: customerName,
        desc: desc,
        amount: amount
    });
    localStorage.setItem('b2b_records', JSON.stringify(records));
    
    window.closeModal('b2b-modal');
    window.showToast('Cari işlem başarıyla kaydedildi.');
    
    // Automatically select this customer to show their page
    activeB2BCustomerId = select.value;
    window.renderB2BAgenda();
};

let pendingB2BDeleteId = null;
window.deleteB2BRecord = (id) => {
    pendingB2BDeleteId = id;
    document.getElementById('finance-password-verify-view').classList.remove('hidden');
    document.getElementById('finance-password-change-view').classList.add('hidden');
    document.getElementById('finance-password-input').value = '';
    document.getElementById('finance-password-modal').classList.remove('hidden');
    
    window.deleteContext = 'B2B';
    setTimeout(() => document.getElementById('finance-password-input').focus(), 100);
};


window.previewNewProdImageFile = (input) => {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            var img = new Image();
            img.onload = function() {
                var canvas = document.createElement('canvas');
                var ctx = canvas.getContext('2d');
                var MAX_WIDTH = 500;
                var width = img.width;
                var height = img.height;
                
                if (width > MAX_WIDTH) {
                    height *= MAX_WIDTH / width;
                    width = MAX_WIDTH;
                }
                
                canvas.width = width;
                canvas.height = height;
                ctx.drawImage(img, 0, 0, width, height);
                
                var dataUrl = canvas.toDataURL('image/jpeg', 0.6);
                
                document.getElementById('new-prod-url').value = dataUrl;
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    }
};


window.openInvCategories = new Set();
// Initialize with all categories open if first time
try {
    const cats = JSON.parse(localStorage.getItem('inv_categories') || '[]');
    cats.forEach(c => {
        window.openInvCategories.add('inv-cat-' + c.replace(/\s+/g, '-').replace(/[^a-zA-Z0-9-]/g, ''));
    });
} catch(e){}

window.toggleInvCategory = (id) => {
    const el = document.getElementById(id);
    const icon = document.getElementById(id + '-icon');
    if(el) {
        if(el.classList.contains('hidden')) {
            el.classList.remove('hidden');
            if(icon) icon.classList.remove('-rotate-90');
            window.openInvCategories.add(id);
        } else {
            el.classList.add('hidden');
            if(icon) icon.classList.add('-rotate-90');
            window.openInvCategories.delete(id);
        }
    }
};


// --- UNIVERSAL QUOTA FIX ---
(function() {
    try {
        let cleared = false;
        for (let i = 0; i < localStorage.length; i++) {
            let key = localStorage.key(i);
            try {
                let val = localStorage.getItem(key);
                // If the value is a massive JSON array (or object) containing data:image
                if (val && val.includes('data:image') && val.length > 100000) {
                    let parsed = JSON.parse(val);
                    if (Array.isArray(parsed)) {
                        let modified = false;
                        const walk = (obj) => {
                            for (let k in obj) {
                                if (typeof obj[k] === 'string' && obj[k].startsWith('data:image')) {
                                    obj[k] = '';
                                    modified = true;
                                } else if (typeof obj[k] === 'object' && obj[k] !== null) {
                                    walk(obj[k]);
                                }
                            }
                        };
                        parsed.forEach(item => walk(item));
                        if (modified) {
                            localStorage.setItem(key, JSON.stringify(parsed));
                            cleared = true;
                            console.log('Cleared massive base64 from', key);
                        }
                    }
                }
            } catch(e) {}
        }
        if (cleared) {
            console.log('Universal quota cleared.');
        }
    } catch(err) {
        console.error('Universal fix error', err);
    }
})();
// ---------------------------
