import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    content = f.read()

def repl(match):
    return """        const produced = p.totalEntered !== undefined ? p.totalEntered : ((p.stock || 0) + (p.sales || 0) + (p.waste || 0));
        const waste = parseFloat(p.waste) || 0;
        const remaining = parseFloat(p.stock) || 0;
        let sold = parseFloat(p.sales) || 0;
        
        const costPrice = parseFloat(p.costPrice) || 0;
        const sellPrice = parseFloat(p.sellPrice) || 0;"""

pattern = re.compile(r'        const produced = parseFloat\(p\._calcEntered\) \|\| 0;\n.*?const sellPrice = parseFloat\(p\.sellPrice\) \|\| 0;', re.DOTALL)
content = pattern.sub(repl, content)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(content)

print("Calculation fixed!")
