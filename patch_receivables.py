import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

view_html = """
        <!-- RECEIVABLES VIEW -->
        <div id="view-receivables" class="flex flex-col gap-6 max-w-7xl mx-auto w-full pb-12" style="display: none;">
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-white p-5 rounded-2xl border border-stone-200 shadow-sm flex items-center gap-4">
                    <div class="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-black">
                        <i data-lucide="wallet" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <div class="text-xs font-black text-stone-400 uppercase tracking-wider">Toplam Açık Alacak (Veresiye)</div>
                        <div id="stat-total-receivables" class="text-2xl font-black text-emerald-600">0 ₺</div>
                    </div>
                </div>
            </div>

            <div class="bg-white p-5 rounded-2xl border border-stone-200 shadow-sm flex flex-col md:flex-row justify-between items-center gap-4">
                <div class="relative w-full md:w-96">
                    <i data-lucide="search" class="w-4 h-4 text-stone-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
                    <input type="text" id="receivable-search" oninput="renderReceivables()" placeholder="Müşteri veya not ara..." class="w-full pl-10 pr-4 py-3 bg-stone-50 border border-stone-200 rounded-xl text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-emerald-500">
                </div>
                <button onclick="openReceivableModal()" class="w-full md:w-auto bg-emerald-600 hover:bg-emerald-700 text-white font-black py-3 px-6 rounded-xl shadow-lg shadow-emerald-600/20 transition active:scale-95 flex items-center justify-center gap-2">
                    <i data-lucide="plus" class="w-5 h-5"></i> Yeni Kayıt
                </button>
            </div>

            <div id="receivables-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-2">
                <!-- populated by JS -->
            </div>
        </div>
"""

modal_html = """
    <!-- Receivable Modal -->
    <div id="receivable-modal" class="fixed inset-0 bg-stone-900/60 backdrop-blur-sm hidden flex items-center justify-center z-[80]">
        <div class="bg-white p-8 rounded-3xl shadow-2xl w-[28rem] max-w-[95vw] transform scale-95 transition-transform border border-stone-200" id="receivable-modal-content">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-2xl font-black text-stone-800" id="receivable-modal-title">Yeni Alacak Ekle</h3>
                <button type="button" onclick="closeReceivableModal()" class="text-stone-400 hover:text-stone-600 transition"><i data-lucide="x" class="w-6 h-6"></i></button>
            </div>
            
            <form onsubmit="submitReceivable(event)" class="space-y-4">
                <input type="hidden" id="receivable-id" value="">
                
                <div>
                    <label class="block text-xs font-black text-stone-500 uppercase tracking-widest mb-1.5">Müşteri Adı / Ünvanı</label>
                    <input type="text" id="receivable-name" required class="w-full bg-stone-50 border border-stone-200 rounded-xl px-4 py-3 font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-emerald-500">
                </div>
                
                <div>
                    <label class="block text-xs font-black text-stone-500 uppercase tracking-widest mb-1.5">Telefon Numarası</label>
                    <input type="tel" id="receivable-phone" class="w-full bg-stone-50 border border-stone-200 rounded-xl px-4 py-3 font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-emerald-500" placeholder="05XX XXX XX XX">
                </div>
                
                <div>
                    <label class="block text-xs font-black text-stone-500 uppercase tracking-widest mb-1.5">Tutar (₺)</label>
                    <input type="number" step="0.01" id="receivable-amount" required class="w-full bg-stone-50 border border-stone-200 rounded-xl px-4 py-3 font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-emerald-500">
                </div>
                
                <div>
                    <label class="block text-xs font-black text-stone-500 uppercase tracking-widest mb-1.5">Not / Açıklama</label>
                    <textarea id="receivable-notes" rows="2" class="w-full bg-stone-50 border border-stone-200 rounded-xl px-4 py-3 font-medium text-stone-800 focus:outline-none focus:ring-2 focus:ring-emerald-500" placeholder="Örn: 2 tepsi baklava eksik ödemesi"></textarea>
                </div>
                
                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-black py-3.5 rounded-xl shadow-lg shadow-emerald-600/20 transition active:scale-95 mt-6">
                    Kaydet
                </button>
            </form>
        </div>
    </div>
"""

content = content.replace("    </main>", view_html + "\n    </main>")
content = content.replace("</body>", modal_html + "\n</body>")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

