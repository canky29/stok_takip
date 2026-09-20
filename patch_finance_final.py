import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    content = f.read()

# Replace toggleFinanceCategory with a version that uses rotation
new_toggle = """window.toggleFinanceCategory = (catId) => {
    const rows = document.querySelectorAll(`.finance-row-${catId}`);
    const icon = document.getElementById(`finance-icon-${catId}`);
    let isHidden = false;
    
    rows.forEach(row => {
        if (row.classList.contains('hidden')) {
            row.classList.remove('hidden');
            isHidden = false;
        } else {
            row.classList.add('hidden');
            isHidden = true;
        }
    });
    
    if (icon) {
        if (isHidden) {
            icon.classList.add('-rotate-90');
        } else {
            icon.classList.remove('-rotate-90');
        }
    }
};"""

content = re.sub(r'window\.toggleFinanceCategory\s*=\s*\(catId\)\s*=>\s*\{.*?(?=\nwindow\.renderFinance)', new_toggle, content, flags=re.DOTALL)

# Add expand/collapse back to the end of the file
expand_collapse = """
window.expandAllFinanceCategories = () => {
    let i = 1;
    while(true) {
        const rows = document.querySelectorAll(`.finance-row-${i}`);
        const icon = document.getElementById(`finance-icon-${i}`);
        if(!icon && rows.length === 0) {
            // Give up if no more categories found. Wait, let's just check icon.
            if(i > 100) break; // safety
        }
        
        if (rows.length > 0) {
            rows.forEach(row => row.classList.remove('hidden'));
        }
        if(icon) {
            icon.classList.remove('-rotate-90');
        }
        i++;
    }
};

window.collapseAllFinanceCategories = () => {
    let i = 1;
    while(true) {
        const rows = document.querySelectorAll(`.finance-row-${i}`);
        const icon = document.getElementById(`finance-icon-${i}`);
        if(!icon && rows.length === 0) {
            if(i > 100) break; // safety
        }
        
        if (rows.length > 0) {
            rows.forEach(row => row.classList.add('hidden'));
        }
        if(icon) {
            icon.classList.add('-rotate-90');
        }
        i++;
    }
};
"""

content += expand_collapse

# Finally, update the chevron in renderFinance to include transition class
content = content.replace('data-lucide="chevron-down" class="w-4 h-4 text-stone-500"', 'data-lucide="chevron-down" class="w-4 h-4 text-stone-500 transition-transform duration-200"')

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(content)

print("Patched toggle and re-added expand/collapse!")
