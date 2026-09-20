import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

# 1. Inject content and creator into the card
old_content = """                        <div>
                            <div class="text-[10px] font-black text-stone-400 uppercase tracking-widest mb-1">Sipariş Edilen</div>
                            <div class="text-lg font-black text-stone-800 leading-tight">${o.productName}</div>
                        </div>"""

new_content = """                        <div>
                            <div class="text-[10px] font-black text-stone-400 uppercase tracking-widest mb-1">Sipariş Edilen</div>
                            <div class="text-lg font-black text-stone-800 leading-tight">${o.productName}</div>
                            ${o.cakeContent ? `<div class="text-[11px] font-bold text-amber-600 mt-1 uppercase tracking-wider">İçerik: ${o.cakeContent}</div>` : ''}
                            ${o.creator ? `<div class="text-[10px] font-bold text-stone-500 mt-1">Siparişi Alan: ${o.creator}</div>` : ''}
                        </div>"""

js = js.replace(old_content, new_content)

# 2. Add print button
old_actions = """                <button onclick="completeCustomerOrder(${o.id})" class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-black py-3.5 rounded-2xl shadow-lg shadow-emerald-600/20 transition active:scale-95 flex items-center justify-center gap-2 text-sm">
                    <i data-lucide="check" class="w-5 h-5"></i> Teslim Et
                </button>
                <button onclick="openCustomerOrderModal(${o.id})" class="bg-amber-100 hover:bg-amber-200 text-amber-700 font-black p-3.5 rounded-2xl transition active:scale-95 border border-amber-200 shadow-sm" title="Düzenle"><i data-lucide="pencil" class="w-5 h-5"></i></button>"""

new_actions = """                <button onclick="completeCustomerOrder(${o.id})" class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-black py-3.5 rounded-2xl shadow-lg shadow-emerald-600/20 transition active:scale-95 flex items-center justify-center gap-2 text-sm">
                    <i data-lucide="check" class="w-5 h-5"></i> Teslim Et
                </button>
                <button onclick="openCustomerOrderModal(${o.id})" class="bg-amber-100 hover:bg-amber-200 text-amber-700 font-black p-3.5 rounded-2xl transition active:scale-95 border border-amber-200 shadow-sm" title="Düzenle"><i data-lucide="pencil" class="w-5 h-5"></i></button>
                <button onclick="printKitchenOrder(${o.id})" class="bg-stone-800 hover:bg-stone-900 text-white font-black p-3.5 rounded-2xl transition active:scale-95 shadow-sm" title="Mutfak Fişi Yazdır"><i data-lucide="printer" class="w-5 h-5"></i></button>"""

js = js.replace(old_actions, new_actions)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)
    
print("Updated renderCustomerOrders with new fields and print button.")
