with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

# Modify setRole to always ask for password if bypassAuth is false
old_setrole = """window.setRole = (role, bypassAuth = false) => {
    if(!bypassAuth && (role === 'FINANCE' || role === 'RECIPE')) {
        if(sessionStorage.getItem('isAdmin') !== 'true') {
            pendingRole = role;
            document.getElementById('auth-password').value = '';
            document.getElementById('auth-modal').classList.remove('hidden');
            setTimeout(() => document.getElementById('auth-password').focus(), 100);
            return;
        }
    }"""

new_setrole = """window.setRole = (role, bypassAuth = false) => {
    if(!bypassAuth && (role === 'FINANCE' || role === 'RECIPE')) {
        pendingRole = role;
        document.getElementById('auth-password').value = '';
        document.getElementById('auth-modal').classList.remove('hidden');
        setTimeout(() => document.getElementById('auth-password').focus(), 100);
        return;
    }"""

js = js.replace(old_setrole, new_setrole)

# Modify submitAuth to not use sessionStorage
old_submit = """        sessionStorage.setItem('isAdmin', 'true');
        closeAuthModal();"""

new_submit = """        closeAuthModal();"""

js = js.replace(old_submit, new_submit)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)

print("Strict auth applied.")
