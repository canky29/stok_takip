import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

# Let's find renderAnalyticsFloor and look at the table header HTML
# We can search for the FİRE ORANI column text

header_old = """
                                    <th class="py-4 px-4 text-center">SATIŞ</th>
                                    <th class="py-4 px-4 text-center">STOĞA GİREN</th>
                                    <th class="py-4 px-4 text-center">FİRE</th>
                                    <th class="py-4 px-4 text-center">FİRE ORANI</th>
                                    <th class="py-4 px-4 text-center">KRİTİK DÜŞÜŞ</th>
                                    <th class="py-4 px-4 text-center">YENİLENME</th>"""

header_new = """
                                    <th class="py-4 px-4 text-center">STOĞA GİREN</th>
                                    <th class="py-4 px-4 text-center">SATIŞ</th>
                                    <th class="py-4 px-4 text-center">FİRE</th>
                                    <th class="py-4 px-4 text-center">ELDE KALAN</th>
                                    <th class="py-4 px-4 text-center">YENİLENME SIKLIĞI</th>"""

js = js.replace(header_old, header_new)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)

print("Headers updated.")
