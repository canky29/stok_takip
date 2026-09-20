import re

with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    html = f.read()

# Replace the interior of the customer-order-form
old_form = r'<form id="customer-order-form" onsubmit="submitCustomerOrder\(event\)" class="flex flex-col gap-4">.*?</form>'

new_form = """<form id="customer-order-form" onsubmit="submitCustomerOrder(event)" class="flex flex-col gap-4">
                <input type="hidden" id="cust-order-id">
                
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-black text-stone-700 mb-1">Siparişi Düzenleyen *</label>
                        <input type="text" id="cust-creator" required class="w-full border border-stone-300 rounded-xl bg-white p-3 text-sm font-bold text-stone-800 focus:border-amber-600 focus:outline-none" placeholder="Örn: Ayşe">
                    </div>
                    <div>
                        <label class="block text-xs font-black text-stone-700 mb-1">Müşteri Adı Soyadı *</label>
                        <input type="text" id="cust-name" required class="w-full border border-stone-300 rounded-xl bg-white p-3 text-sm font-bold text-stone-800 focus:border-amber-600 focus:outline-none" placeholder="Örn: Hamide Tüysüz">
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div>
                        <label class="block text-xs font-black text-stone-700 mb-1">Telefon Numarası *</label>
                        <input type="tel" id="cust-phone" required class="w-full border border-stone-300 rounded-xl bg-white p-3 text-sm font-bold text-stone-800 focus:border-amber-600 focus:outline-none" placeholder="0555...">
                    </div>
                    <div>
                        <label class="block text-xs font-black text-stone-700 mb-1">Teslim Tarihi *</label>
                        <input type="date" id="cust-date" required class="w-full border border-stone-300 rounded-xl bg-white p-3 text-sm font-bold text-stone-800 focus:border-amber-600 focus:outline-none">
                    </div>
                    <div>
                        <label class="block text-xs font-black text-stone-700 mb-1">Teslim Saati *</label>
                        <input type="time" id="cust-time" required class="w-full border border-stone-300 rounded-xl bg-white p-3 text-sm font-bold text-stone-800 focus:border-amber-600 focus:outline-none">
                    </div>
                </div>

                <div class="border-t border-stone-200 pt-3 mt-1">
                    <label class="block text-xs font-black text-stone-700 mb-2">Pasta / Ürün Detayları</label>
                    <div class="flex flex-col gap-3">
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            <div>
                                <label class="block text-[11px] font-bold text-stone-500 mb-1">Pasta Modeli / Ürün Adı *</label>
                                <input type="text" id="cust-prod-name" required class="w-full border border-stone-300 rounded-xl bg-white p-3 text-sm font-bold text-stone-800 focus:border-amber-600 focus:outline-none" placeholder="Örn: 2 Katlı Doğum Günü Pastası">
                            </div>
                            <div>
                                <label class="block text-[11px] font-bold text-stone-500 mb-1">Pasta İçeriği *</label>
                                <input type="text" id="cust-cake-content" required class="w-full border border-stone-300 rounded-xl bg-white p-3 text-sm font-bold text-stone-800 focus:border-amber-600 focus:outline-none" placeholder="Örn: Çilekli ve Çikolatalı">
                            </div>
                        </div>

                        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
                            <div class="col-span-1">
                                <label class="block text-[11px] font-bold text-stone-500 mb-1">Kişi Sayısı/Miktar *</label>
                                <input type="number" id="cust-qty" step="1" min="1" value="10" required class="w-full border border-stone-300 rounded-xl bg-white p-2.5 text-sm font-bold text-stone-800 focus:border-amber-600 focus:outline-none">
                            </div>
                            <div class="col-span-1">
                                <label class="block text-[11px] font-bold text-stone-500 mb-1">Birim</label>
                                <select id="cust-unit" class="w-full border border-stone-300 rounded-xl bg-white p-2.5 text-sm font-bold text-stone-800 focus:border-amber-600 focus:outline-none">
                                    <option value="Kişilik">Kişilik</option>
                                    <option value="Adet">Adet</option>
                                    <option value="Kg">Kg</option>
                                </select>
                            </div>
                            <div class="col-span-1">
                                <label class="block text-[11px] font-bold text-stone-500 mb-1">Toplam Fiyat (₺)</label>
                                <input type="number" id="cust-price" step="0.01" min="0" placeholder="0" class="w-full border border-stone-300 rounded-xl bg-white p-2.5 text-sm font-bold text-amber-600 focus:border-amber-600 focus:outline-none">
                            </div>
                            <div class="col-span-1">
                                <label class="block text-[11px] font-bold text-stone-500 mb-1">Ön Ödeme (₺)</label>
                                <input type="number" id="cust-advance" step="0.01" min="0" placeholder="0" class="w-full border border-stone-300 rounded-xl bg-white p-2.5 text-sm font-bold text-emerald-600 focus:border-amber-600 focus:outline-none">
                            </div>
                        </div>
                    </div>
                </div>

                <div>
                    <label class="block text-xs font-black text-stone-700 mb-1">Müşteri Notu / Özel İstekler</label>
                    <textarea id="cust-notes" rows="2" class="w-full border border-stone-300 rounded-xl bg-white p-3 text-xs font-medium text-stone-800 focus:border-amber-600 focus:outline-none placeholder-stone-400" placeholder="Örn: Üzerine 'İyi ki Doğdun Ali' yazılacak."></textarea>
                </div>

                <div>
                    <label class="block text-xs font-black text-stone-700 mb-1">Pasta Modeli Görseli (İsteğe Bağlı)</label>
                    <div class="space-y-2">
                        <input type="file" id="cust-img-file" accept="image/*" onchange="previewCustImageFile(this)" class="w-full text-xs text-stone-500 border border-stone-300 rounded-xl bg-white p-2 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-bold file:bg-amber-100 file:text-amber-800 hover:file:bg-amber-200">
                        <input type="text" id="cust-img-url" oninput="previewCustImageUrl(this.value)" class="w-full border border-stone-300 rounded-xl bg-white p-2.5 text-xs font-bold text-stone-800 focus:border-amber-600 focus:outline-none" placeholder="Veya Görsel URL Linki Girin">
                    </div>
                    <div id="cust-img-preview-box" class="mt-2 hidden">
                        <div class="relative inline-block border-2 border-amber-400 rounded-xl overflow-hidden shadow-sm">
                            <img id="cust-img-preview" src="" alt="Önizleme" class="w-24 h-24 object-cover">
                            <button type="button" onclick="removeCustImagePreview()" class="absolute top-1 right-1 bg-red-600 text-white rounded-full p-1 shadow hover:bg-red-700 transition" title="Görseli Kaldır">
                                <i data-lucide="x" class="w-3.5 h-3.5"></i>
                            </button>
                        </div>
                    </div>
                    <input type="hidden" id="cust-img-url-input">
                </div>

                <button type="submit" class="w-full bg-amber-600 hover:bg-amber-700 text-white font-bold py-3.5 rounded-xl shadow-lg shadow-amber-600/20 transition mt-2 flex items-center justify-center gap-2">
                    <i data-lucide="save" class="w-5 h-5"></i>
                    <span id="cust-modal-btn-text">Siparişi Kaydet</span>
                </button>
            </form>"""

html = re.sub(old_form, new_form, html, flags=re.DOTALL)

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(html)
    
print("Updated HTML for Customer Order Modal.")
