with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    content = f.read()

content = content.replace('class="fixed inset-0 bg-stone-900/60 backdrop-blur-sm hidden items-center justify-center z-50 p-4"', 'class="fixed inset-0 bg-stone-900/60 backdrop-blur-sm hidden flex items-center justify-center z-50 p-4"')

with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
    f.write(content)

print("Flex added to modal.")
