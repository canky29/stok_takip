import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

# Change totalPanel.classList.add('hidden'); to remove('hidden');
bad_code = "        totalPanel.classList.add('hidden');"
good_code = "        totalPanel.classList.remove('hidden');"

js = js.replace(bad_code, good_code)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)

print("Fixed total panel visibility.")
