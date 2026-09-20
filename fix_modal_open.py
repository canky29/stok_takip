import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

old_code = """    const select = document.getElementById('cust-prod-select');
    select.innerHTML = '<option value="">-- Menüden Seçin (veya elle yazın) --</option>';
    let prods = JSON.parse(localStorage.getItem('products') || '[]');
    prods.forEach(p => {
        let opt = document.createElement('option');
        opt.value = p.name;
        opt.textContent = p.name;
        select.appendChild(opt);
    });"""

new_code = """    const select = document.getElementById('cust-prod-select');
    if(select) {
        select.innerHTML = '<option value="">-- Menüden Seçin (veya elle yazın) --</option>';
        let prods = JSON.parse(localStorage.getItem('products') || '[]');
        prods.forEach(p => {
            let opt = document.createElement('option');
            opt.value = p.name;
            opt.textContent = p.name;
            select.appendChild(opt);
        });
    }"""

js = js.replace(old_code, new_code)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)
    
print("Fixed JS TypeError on modal open.")
