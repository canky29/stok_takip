with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    content = f.read()

bad = "    if(role === 'FINANCE' && window.renderFinance) {\n        window.renderFinance();\n    }"
good = "    if(role === 'FINANCE' && window.renderFinance) {\n        window.renderFinance();\n    }\n    if(role === 'RECIPE') {\n        window.renderRecipeView();\n    }"

content = content.replace(bad, good)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(content)

print("Render hook added.")
