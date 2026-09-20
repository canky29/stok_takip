import re

with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    html = f.read()

old_modal = """
    <!-- AUTH MODAL -->
    <div id="auth-modal" class="fixed inset-0 bg-stone-900/80 backdrop-blur-md hidden flex items-center justify-center z-[110] p-4">
        <div class="bg-white rounded-3xl w-full max-w-sm shadow-2xl overflow-hidden animate-slide-up relative">
            <button type="button" onclick="closeAuthModal()" class="absolute top-5 right-5 w-8 h-8 flex items-center justify-center rounded-full bg-stone-100 text-stone-500 hover:bg-stone-200 transition">
                <i data-lucide="x" class="w-4 h-4"></i>
            </button>
            <div class="p-8 flex flex-col items-center text-center">
                <div class="w-16 h-16 rounded-2xl bg-rose-100 text-rose-600 flex items-center justify-center mb-4">
                    <i data-lucide="lock" class="w-8 h-8"></i>
                </div>
                <h2 class="text-2xl font-black text-stone-900 mb-2">Yetkili Erişimi</h2>
                <p class="text-sm text-stone-500 font-medium mb-6">Maliyet ve Reçete sayfaları sadece yöneticilere açıktır.</p>
                
                <form onsubmit="submitAuth(event)" class="w-full flex flex-col gap-4">
                    <input type="password" id="auth-password" required placeholder="Şifrenizi girin..." class="w-full bg-stone-50 border border-stone-200 rounded-xl py-3 px-4 text-center text-lg font-black text-stone-800 focus:outline-none focus:ring-2 focus:ring-rose-500">
                    <button type="submit" class="w-full bg-rose-600 hover:bg-rose-700 text-white font-black py-4 rounded-xl shadow-lg shadow-rose-600/30 transition active:scale-95">
                        Giriş Yap
                    </button>
                </form>
                <div class="mt-4 text-[10px] text-stone-400 font-bold">Varsayılan şifre: 1234</div>
            </div>
        </div>
    </div>
"""

new_modal = """
    <!-- AUTH MODAL -->
    <div id="auth-modal" class="fixed inset-0 bg-stone-900/80 backdrop-blur-md hidden flex items-center justify-center z-[110] p-4">
        <div class="bg-white rounded-3xl w-full max-w-sm shadow-2xl overflow-hidden animate-slide-up relative">
            <button type="button" onclick="closeAuthModal()" class="absolute top-5 right-5 w-8 h-8 flex items-center justify-center rounded-full bg-stone-100 text-stone-500 hover:bg-stone-200 transition">
                <i data-lucide="x" class="w-4 h-4"></i>
            </button>
            <div class="p-8 flex flex-col items-center text-center">
                <div class="w-16 h-16 rounded-2xl bg-rose-100 text-rose-600 flex items-center justify-center mb-4">
                    <i data-lucide="lock" class="w-8 h-8"></i>
                </div>
                
                <!-- LOGIN MODE -->
                <div id="auth-login-view" class="w-full flex flex-col items-center">
                    <h2 class="text-2xl font-black text-stone-900 mb-2">Yetkili Erişimi</h2>
                    <p class="text-sm text-stone-500 font-medium mb-6">Maliyet ve Reçete sayfaları sadece yöneticilere açıktır.</p>
                    
                    <form onsubmit="submitAuth(event)" class="w-full flex flex-col gap-4">
                        <input type="password" id="auth-password" required placeholder="Şifrenizi girin..." class="w-full bg-stone-50 border border-stone-200 rounded-xl py-3 px-4 text-center text-lg font-black text-stone-800 focus:outline-none focus:ring-2 focus:ring-rose-500">
                        <button type="submit" class="w-full bg-rose-600 hover:bg-rose-700 text-white font-black py-4 rounded-xl shadow-lg shadow-rose-600/30 transition active:scale-95">
                            Giriş Yap
                        </button>
                    </form>
                    <button type="button" onclick="toggleAuthMode('CHANGE')" class="mt-4 text-[11px] font-bold text-stone-400 hover:text-stone-600 transition">Şifremi Değiştir</button>
                </div>
                
                <!-- CHANGE PASSWORD MODE -->
                <div id="auth-change-view" class="hidden w-full flex flex-col items-center">
                    <h2 class="text-2xl font-black text-stone-900 mb-2">Şifre Değiştir</h2>
                    
                    <form onsubmit="submitChangePassword(event)" class="w-full flex flex-col gap-3 mt-4">
                        <input type="password" id="change-old-password" required placeholder="Mevcut Şifre" class="w-full bg-stone-50 border border-stone-200 rounded-xl py-3 px-4 text-center text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-stone-500">
                        <input type="password" id="change-new-password" required placeholder="Yeni Şifre" class="w-full bg-stone-50 border border-stone-200 rounded-xl py-3 px-4 text-center text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                        <input type="password" id="change-new-password-confirm" required placeholder="Yeni Şifre (Tekrar)" class="w-full bg-stone-50 border border-stone-200 rounded-xl py-3 px-4 text-center text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                        <button type="submit" class="mt-2 w-full bg-stone-900 hover:bg-black text-white font-black py-4 rounded-xl shadow-lg shadow-black/20 transition active:scale-95">
                            Şifreyi Güncelle
                        </button>
                    </form>
                    <button type="button" onclick="toggleAuthMode('LOGIN')" class="mt-4 text-[11px] font-bold text-stone-400 hover:text-stone-600 transition">İptal Et ve Geri Dön</button>
                </div>
                
            </div>
        </div>
    </div>
"""

html = html.replace(old_modal.strip(), new_modal.strip())

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(html)


with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

new_js_logic = """
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
"""

js = js.replace("let pendingRole = null;", "let pendingRole = null;\n" + new_js_logic)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)

print("Change password logic implemented.")
