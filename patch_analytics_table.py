import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

old_head = """                    <thead class="bg-white text-stone-500 font-bold border-b border-stone-100 uppercase text-[10px] tracking-wider">
                        <tr>
                            <th class="px-4 py-3">Ürün Adı</th>
                            <th class="px-4 py-3">Kapasite</th>
                            <th class="px-4 py-3">Mevcut Stok</th>
                            <th class="px-4 py-3 text-emerald-600">Satış</th>
                            <th class="px-4 py-3 text-indigo-600">Stoğa Giren</th>
                            <th class="px-4 py-3 text-rose-600">Fire</th>
                            <th class="px-4 py-3">Fire Oranı</th>
                            <th class="px-4 py-3 text-red-500">Kritik Düşüş</th>
                            <th class="px-4 py-3 text-sky-600">Yenilenme</th>
                        </tr>
                    </thead>"""

new_head = """                    <thead class="bg-white text-stone-500 font-bold border-b border-stone-100 uppercase text-[10px] tracking-wider">
                        <tr>
                            <th class="px-4 py-3">Ürün Adı</th>
                            <th class="px-4 py-3">Kapasite</th>
                            <th class="px-4 py-3 text-indigo-600">Stoğa Giren</th>
                            <th class="px-4 py-3 text-emerald-600">Satış</th>
                            <th class="px-4 py-3 text-rose-600">Fire</th>
                            <th class="px-4 py-3 text-stone-800">Elde Kalan</th>
                            <th class="px-4 py-3 text-sky-600">Yenilenme</th>
                        </tr>
                    </thead>"""

js = js.replace(old_head, new_head)

old_body = """            html += `
                        <tr class="hover:bg-stone-50 transition">
                            <td class="px-4 py-3 font-black text-stone-800 flex items-center gap-3">
                                <img src="${p.image}" class="w-8 h-8 rounded-lg object-cover shadow-sm">
                                ${p.name}
                            </td>
                            <td class="px-4 py-3 font-medium text-stone-600">${p.maxStock} ${p.unit}</td>
                            <td class="px-4 py-3 font-black text-stone-800">${p.stock} ${p.unit}</td>
                            <td class="px-4 py-3 font-black text-emerald-600">${p._calcSales}</td>
                            <td class="px-4 py-3 font-black text-indigo-600">${totalEntered}</td>
                            <td class="px-4 py-3 font-black text-rose-600">${p._calcWaste}</td>
                            <td class="px-4 py-3 ${rateColor}">%${rate}</td>
                            <td class="px-4 py-3 font-black text-red-500">${p._calcCriticalDrops || 0}</td>
                            <td class="px-4 py-3 font-black text-sky-600">${p._calcRestocks || 0}</td>
                        </tr>
            `;"""

new_body = """            html += `
                        <tr class="hover:bg-stone-50 transition">
                            <td class="px-4 py-3 font-black text-stone-800 flex items-center gap-3">
                                <img src="${p.image}" class="w-8 h-8 rounded-lg object-cover shadow-sm">
                                ${p.name}
                            </td>
                            <td class="px-4 py-3 font-medium text-stone-600">${p.maxStock} ${p.unit}</td>
                            <td class="px-4 py-3 font-black text-indigo-600">${totalEntered} <span class="text-[10px] font-bold text-indigo-400">${p.unit}</span></td>
                            <td class="px-4 py-3 font-black text-emerald-600">${p._calcSales} <span class="text-[10px] font-bold text-emerald-400">${p.unit}</span></td>
                            <td class="px-4 py-3 font-black text-rose-600">${p._calcWaste} <span class="text-[10px] font-bold text-rose-400">${p.unit}</span></td>
                            <td class="px-4 py-3 font-black text-stone-800">${p.stock} <span class="text-[10px] font-bold text-stone-400">${p.unit}</span></td>
                            <td class="px-4 py-3 font-black text-sky-600">${p._calcRestocks || 0}</td>
                        </tr>
            `;"""

js = js.replace(old_body, new_body)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)

print("Table restructured successfully.")
