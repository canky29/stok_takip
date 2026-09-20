with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    html = f.read()

auth_modal_html = """
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

if 'id="auth-modal"' not in html:
    html = html.replace('<!-- Modal for Adding New Product -->', auth_modal_html + '\n    <!-- Modal for Adding New Product -->')
    with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
        f.write(html)
        print("Auth modal injected.")
else:
    print("Auth modal already exists.")
