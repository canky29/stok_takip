import re

with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    content = f.read()

recipe_view = """
        <!-- REÇETE HESAPLAMA GÖRÜNÜMÜ -->
        <div id="view-recipe" class="hidden animate-fade-in flex-col gap-6 max-w-7xl mx-auto w-full pb-12">
            <!-- Header -->
            <div class="flex items-center justify-between bg-white p-6 rounded-3xl shadow-sm border border-stone-200">
                <div class="flex items-center gap-4">
                    <div class="w-14 h-14 rounded-2xl bg-indigo-100 text-indigo-700 flex items-center justify-center shrink-0">
                        <i data-lucide="flask-conical" class="w-7 h-7"></i>
                    </div>
                    <div>
                        <h2 class="text-2xl font-black text-stone-900 tracking-tight">Reçete & Maliyet Aracı</h2>
                        <p class="text-sm font-bold text-stone-400 mt-1">Ürün içeriklerini gramajla girin, envanterden güncel maliyeti çeksin.</p>
                    </div>
                </div>
            </div>

            <!-- Content Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                
                <!-- Sol Panel: Ürün Seçimi & Kayıtlı Reçeteler -->
                <div class="lg:col-span-1 bg-white p-6 rounded-3xl shadow-sm border border-stone-200 flex flex-col gap-4">
                    <h3 class="text-lg font-black text-stone-800">1. Hangi Ürünü Hesaplıyoruz?</h3>
                    <div class="relative">
                        <select id="recipe-product-select" onchange="loadRecipeForSelectedProduct()" class="w-full bg-stone-50 border border-stone-200 rounded-xl py-3 px-4 text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 appearance-none">
                            <option value="">-- Lütfen Ürün Seçin --</option>
                        </select>
                        <i data-lucide="chevron-down" class="w-4 h-4 text-stone-400 absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none"></i>
                    </div>
                    
                    <div id="recipe-info-panel" class="hidden mt-4 bg-indigo-50 p-4 rounded-2xl border border-indigo-100">
                        <div class="flex items-center gap-3 mb-2">
                            <img id="recipe-product-img" src="" class="w-12 h-12 rounded-xl object-cover shadow-sm">
                            <div>
                                <div id="recipe-product-name" class="font-black text-stone-900"></div>
                                <div class="text-xs font-bold text-stone-500">Mevcut Kayıtlı Maliyet: <span id="recipe-product-old-cost" class="text-indigo-600">0.00 ₺</span></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Orta Panel: Malzeme (Hammadde) Listesi -->
                <div class="lg:col-span-2 bg-white p-6 rounded-3xl shadow-sm border border-stone-200 flex flex-col gap-4">
                    <div class="flex items-center justify-between">
                        <h3 class="text-lg font-black text-stone-800">2. Reçete Malzemeleri</h3>
                        <button onclick="openRecipeIngredientModal()" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-xl font-bold text-sm shadow-sm transition active:scale-95 flex items-center gap-2" id="btn-add-ingredient" disabled>
                            <i data-lucide="plus" class="w-4 h-4"></i> Malzeme Ekle
                        </button>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="w-full text-left border-collapse">
                            <thead>
                                <tr class="text-xs font-black text-stone-400 uppercase tracking-wider border-b border-stone-100">
                                    <th class="py-3 px-2">Malzeme (Envanter)</th>
                                    <th class="py-3 px-2 text-center">Kullanılan Miktar</th>
                                    <th class="py-3 px-2 text-right">Hesaplanan Maliyet</th>
                                    <th class="py-3 px-2 w-10"></th>
                                </tr>
                            </thead>
                            <tbody id="recipe-ingredients-tbody">
                                <tr>
                                    <td colspan="4" class="p-8 text-center text-stone-400 font-bold">Önce sol taraftan bir ürün seçin.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Toplam Maliyet & Kayıt -->
                    <div id="recipe-total-panel" class="hidden mt-4 pt-6 border-t border-stone-100 flex flex-col md:flex-row items-center justify-between gap-4">
                        <div>
                            <div class="text-sm font-bold text-stone-500">1 Birim (Adet/Porsiyon) İçin</div>
                            <div class="text-3xl font-black text-emerald-600">Toplam: <span id="recipe-total-cost">0.00 ₺</span></div>
                        </div>
                        <button onclick="saveRecipeCostToProduct()" class="bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-4 rounded-xl font-black shadow-lg shadow-emerald-500/30 transition active:scale-95 flex items-center gap-2">
                            <i data-lucide="save" class="w-5 h-5"></i> Yeni Maliyet Olarak Kaydet
                        </button>
                    </div>

                </div>

            </div>
        </div>

        <!-- YENİ MALZEME EKLEME MODALI -->
        <div id="add-ingredient-modal" class="fixed inset-0 bg-stone-900/60 backdrop-blur-sm hidden items-center justify-center z-50 p-4">
            <div class="bg-white rounded-3xl w-full max-w-md shadow-2xl overflow-hidden animate-slide-up relative">
                <button type="button" onclick="closeModal('add-ingredient-modal')" class="absolute top-5 right-5 w-8 h-8 flex items-center justify-center rounded-full bg-stone-100 text-stone-500 hover:bg-stone-200 transition">
                    <i data-lucide="x" class="w-4 h-4"></i>
                </button>
                <div class="p-8">
                    <h2 class="text-2xl font-black text-stone-900 mb-2">Reçeteye Malzeme Ekle</h2>
                    <p class="text-sm text-stone-500 font-medium mb-6">Envanterdeki hammaddelerden birini seçip reçetedeki kullanım miktarını girin.</p>
                    
                    <form onsubmit="submitRecipeIngredient(event)" class="flex flex-col gap-5">
                        
                        <div>
                            <label class="block text-xs font-black text-stone-500 uppercase tracking-wider mb-2">Envanter Kalemi</label>
                            <div class="relative">
                                <select id="recipe-inv-select" required onchange="updateRecipeUnitLabels()" class="w-full bg-stone-50 border border-stone-200 rounded-xl py-3 px-4 text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 appearance-none">
                                    <option value="">Seçim Yapın...</option>
                                </select>
                                <i data-lucide="chevron-down" class="w-4 h-4 text-stone-400 absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none"></i>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-black text-stone-500 uppercase tracking-wider mb-2">Miktar</label>
                                <input type="number" id="recipe-ing-qty" required step="0.01" min="0.01" placeholder="Örn: 500" class="w-full bg-stone-50 border border-stone-200 rounded-xl py-3 px-4 text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-indigo-500">
                            </div>
                            <div>
                                <label class="block text-xs font-black text-stone-500 uppercase tracking-wider mb-2">Birim</label>
                                <div class="relative">
                                    <select id="recipe-ing-unit" required class="w-full bg-stone-50 border border-stone-200 rounded-xl py-3 px-4 text-sm font-bold text-stone-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 appearance-none">
                                        <option value="g">Gram (g)</option>
                                        <option value="kg">Kilogram (kg)</option>
                                        <option value="ml">Mililitre (ml)</option>
                                        <option value="L">Litre (L)</option>
                                        <option value="adet">Adet</option>
                                    </select>
                                    <i data-lucide="chevron-down" class="w-4 h-4 text-stone-400 absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none"></i>
                                </div>
                            </div>
                        </div>
                        
                        <div class="bg-indigo-50 p-4 rounded-xl border border-indigo-100 flex items-start gap-2">
                            <i data-lucide="info" class="w-4 h-4 text-indigo-500 shrink-0 mt-0.5"></i>
                            <div class="text-xs font-bold text-indigo-700 leading-relaxed" id="recipe-inv-hint">
                                Malzeme seçtiğinizde envanterdeki birim fiyatı burada görünecektir.
                            </div>
                        </div>

                        <button type="submit" class="mt-2 w-full bg-indigo-600 hover:bg-indigo-700 text-white font-black py-4 rounded-xl shadow-lg shadow-indigo-600/30 transition active:scale-95">
                            Reçeteye Ekle
                        </button>
                    </form>
                </div>
            </div>
        </div>
"""

# Inject before Modals section
content = content.replace("<!-- MODALS -->", recipe_view + "\n\n        <!-- MODALS -->")

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(content)
print("View injected.")
