import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    content = f.read()

content = content.replace(
    "const roles = ['HOME', 'UPPER', 'LOWER', 'ORDERS', 'ANALYTICS', 'RECEIVABLES', 'INVENTORY', 'FINANCE'];",
    "const roles = ['HOME', 'UPPER', 'LOWER', 'ORDERS', 'ANALYTICS', 'RECEIVABLES', 'INVENTORY', 'FINANCE', 'RECIPE'];"
)

# And check if the render hook is correct
if "if(role === 'RECIPE') renderRecipeView();" not in content:
    content = content.replace("if(role === 'FINANCE') renderFinance();", "if(role === 'FINANCE') renderFinance();\n    if(role === 'RECIPE') renderRecipeView();")

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(content)

print("Roles array updated.")
