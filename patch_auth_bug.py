with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

bad_submit = """    if(pass === correctPass) {
        closeAuthModal();
        showToast('Giriş başarılı, yetki onaylandı.', 'success');
        if(pendingRole) {
            setRole(pendingRole, true);
        }
    }"""

good_submit = """    if(pass === correctPass) {
        const roleToLoad = pendingRole;
        closeAuthModal();
        showToast('Giriş başarılı, yetki onaylandı.', 'success');
        if(roleToLoad) {
            window.setRole(roleToLoad, true);
        }
    }"""

js = js.replace(bad_submit, good_submit)

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)

print("Auth bug fixed.")
