import re

with open('app_v4.js', 'r') as f:
    js = f.read()

filter_logic = """
let currentFilter = 'ALL';
window.setStockFilter = (filter) => {
    currentFilter = filter;
    renderProducts();
    
    // Update button styles
    const filters = ['ALL', 'CRITICAL', 'EMPTY', 'NORMAL'];
    filters.forEach(f => {
        const btn = document.getElementById('filter-btn-' + f);
        if(!btn) return;
        if(f === filter) {
            btn.classList.add('ring-2', 'ring-offset-2', 'ring-amber-500');
        } else {
            btn.classList.remove('ring-2', 'ring-offset-2', 'ring-amber-500');
        }
    });
};
"""

js = re.sub(r'let currentFilter = \'ALL\';\nwindow\.setStockFilter = \(filter\) => \{\n    currentFilter = filter;\n    renderProducts\(\);\n\};', filter_logic, js)

with open('app_v4.js', 'w') as f:
    f.write(js)
