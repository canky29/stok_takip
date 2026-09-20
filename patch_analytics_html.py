import re

with open('index.html', 'r') as f:
    html = f.read()

# Insert the time filter buttons above KPIs
kpi_section = """            <div class="flex flex-col gap-6">
                <!-- TOP HEADER -->"""

new_kpi_section = """            <div class="flex flex-col gap-6">
                <!-- TIME FILTER BAR -->
                <div class="bg-white p-3 rounded-2xl border border-stone-200 shadow-sm flex items-center justify-between gap-4 overflow-x-auto">
                    <span class="text-xs font-black text-stone-500 uppercase tracking-widest pl-2">Zaman Aralığı:</span>
                    <div class="flex gap-2">
                        <button onclick="setAnalyticsTimeFilter('7D')" id="btn-time-7D" class="px-4 py-2 text-xs font-black rounded-lg transition bg-stone-100 text-stone-600 hover:bg-stone-200">Son 7 Gün</button>
                        <button onclick="setAnalyticsTimeFilter('30D')" id="btn-time-30D" class="px-4 py-2 text-xs font-black rounded-lg transition bg-stone-100 text-stone-600 hover:bg-stone-200">Son 30 Gün</button>
                        <button onclick="setAnalyticsTimeFilter('ALL')" id="btn-time-ALL" class="px-4 py-2 text-xs font-black rounded-lg transition bg-amber-600 text-white shadow-sm ring-2 ring-offset-2 ring-amber-500">Tüm Zamanlar</button>
                    </div>
                </div>

                <!-- TOP HEADER -->"""

html = html.replace(kpi_section, new_kpi_section)
with open('index.html', 'w') as f:
    f.write(html)
