import re

# 1. Add Toast HTML container to index.html
with open('/Applications/patuli_Stok_Takip/index.html', 'r') as f:
    html = f.read()

if 'id="toast-container"' not in html:
    toast_html = """
    <!-- TOAST CONTAINER -->
    <div id="toast-container" class="fixed top-5 left-1/2 -translate-x-1/2 z-[100] flex flex-col gap-3 items-center pointer-events-none"></div>
    """
    html = html.replace('</body>', toast_html + '\n</body>')
    with open('/Applications/patuli_Stok_Takip/index.html', 'w') as f:
        f.write(html)

# 2. Add showToast function and replace alerts in app_v4.js
with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

toast_js = """
// --- TOAST NOTIFICATIONS ---
window.showToast = (message, type = 'success') => {
    const container = document.getElementById('toast-container');
    if(!container) return;
    
    const toast = document.createElement('div');
    
    // Style variations based on type
    let bgClass = 'bg-stone-900 text-white';
    let icon = '<i data-lucide="check-circle-2" class="w-5 h-5 text-emerald-400"></i>';
    
    if (type === 'error') {
        bgClass = 'bg-rose-600 text-white';
        icon = '<i data-lucide="alert-circle" class="w-5 h-5 text-white"></i>';
    } else if (type === 'info') {
        bgClass = 'bg-indigo-600 text-white';
        icon = '<i data-lucide="info" class="w-5 h-5 text-white"></i>';
    }

    toast.className = `flex items-center gap-3 px-6 py-4 rounded-full shadow-2xl transform transition-all duration-500 translate-y-[-20px] opacity-0 ${bgClass}`;
    
    // Preserve line breaks for messages with \n
    const formattedMessage = message.replace(/\\n/g, '<br>');
    
    toast.innerHTML = `
        ${icon}
        <span class="font-bold text-sm leading-tight">${formattedMessage}</span>
    `;
    
    container.appendChild(toast);
    
    if(typeof lucide !== 'undefined') lucide.createIcons();
    
    // Animate in
    requestAnimationFrame(() => {
        toast.classList.remove('translate-y-[-20px]', 'opacity-0');
        toast.classList.add('translate-y-0', 'opacity-100');
    });
    
    // Animate out and remove
    setTimeout(() => {
        toast.classList.remove('translate-y-0', 'opacity-100');
        toast.classList.add('translate-y-[-20px]', 'opacity-0');
        setTimeout(() => toast.remove(), 500);
    }, 3500);
};
"""

if 'window.showToast =' not in js:
    js = toast_js + "\n" + js

# Replace alerts
js = re.sub(r"alert\('(.*?)'\);", r"showToast('\1');", js)
js = re.sub(r"alert\(`(.*?)`\);", r"showToast(`\1`);", js)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)

print("Toast system added and alerts replaced.")
