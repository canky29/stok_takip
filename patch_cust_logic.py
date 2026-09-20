import re

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'r') as f:
    js = f.read()

# 1. Update openCustomerOrderModal
old_open = """            document.getElementById('cust-img-url').value = ord.imgUrl || '';
            document.getElementById('cust-price').value = ord.price || '';
            document.getElementById('cust-deposit').value = ord.deposit || '';"""

new_open = """            document.getElementById('cust-img-url').value = ord.imgUrl || '';
            document.getElementById('cust-price').value = ord.price || '';
            
            // New fields
            if(document.getElementById('cust-advance')) document.getElementById('cust-advance').value = ord.deposit || '';
            if(document.getElementById('cust-deposit')) document.getElementById('cust-deposit').value = ord.deposit || '';
            
            if(document.getElementById('cust-creator')) document.getElementById('cust-creator').value = ord.creator || '';
            if(document.getElementById('cust-cake-content')) document.getElementById('cust-cake-content').value = ord.cakeContent || '';"""

js = js.replace(old_open, new_open)

# 2. Update submitCustomerOrder
old_submit = """        imgUrl: document.getElementById('cust-img-url').value,
        price: parseFloat(document.getElementById('cust-price').value || 0),
        deposit: parseFloat(document.getElementById('cust-deposit').value || 0),
        status: id ? undefined : 'ACTIVE',"""

new_submit = """        imgUrl: document.getElementById('cust-img-url').value,
        price: parseFloat(document.getElementById('cust-price').value || 0),
        deposit: parseFloat((document.getElementById('cust-advance') || document.getElementById('cust-deposit')).value || 0),
        creator: document.getElementById('cust-creator') ? document.getElementById('cust-creator').value : '',
        cakeContent: document.getElementById('cust-cake-content') ? document.getElementById('cust-cake-content').value : '',
        status: id ? undefined : 'ACTIVE',"""

js = js.replace(old_submit, new_submit)

# 3. Add printKitchenOrder function right before renderCustomerOrders
print_func = """
window.printKitchenOrder = (id) => {
    let orders = JSON.parse(localStorage.getItem('customerOrders') || '[]');
    let ord = orders.find(x => x.id == id);
    if(!ord) return;
    
    const printWindow = window.open('', '', 'width=600,height=800');
    const html = `
        <html>
        <head>
            <title>Mutfak Sipariş Fişi</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; color: #000; }
                h1 { text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px; text-transform: uppercase; letter-spacing: 2px; }
                .line { margin-bottom: 15px; font-size: 16px; border-bottom: 1px dashed #ccc; padding-bottom: 5px; }
                .label { font-weight: bold; width: 150px; display: inline-block; }
                .val { font-size: 18px; }
                .highlight { font-size: 22px; font-weight: bold; background: #eee; padding: 10px; border-radius: 5px; text-align: center; margin: 20px 0; border: 2px solid #000; }
                .notes { border: 1px solid #000; padding: 15px; border-radius: 5px; min-height: 80px; }
                .print-btn { display: block; width: 100%; padding: 15px; background: #000; color: #fff; text-align: center; font-size: 18px; cursor: pointer; border: none; margin-bottom: 20px; }
                @media print { .print-btn { display: none; } }
            </style>
        </head>
        <body>
            <button class="print-btn" onclick="window.print()">YAZDIR</button>
            <h1>Mutfak Sipariş Fişi</h1>
            <div class="line"><span class="label">Siparişi Düzenleyen:</span> <span class="val">${ord.creator || '-'}</span></div>
            <div class="line"><span class="label">Müşteri Adı:</span> <span class="val">${ord.customerName}</span></div>
            <div class="line"><span class="label">Teslimat Tarihi:</span> <span class="val">${ord.date} ${ord.time}</span></div>
            
            <div class="highlight">
                ${ord.productName} <br>
                <span style="font-size: 16px; font-weight: normal;">(${ord.qty} ${ord.unit})</span>
            </div>
            
            <div class="line"><span class="label">Pasta İçeriği:</span> <span class="val"><b>${ord.cakeContent || '-'}</b></span></div>
            
            <div style="margin-top:20px; font-weight:bold;">Müşteri Notu / Özel İstek:</div>
            <div class="notes">${ord.notes || 'Not yok.'}</div>
        </body>
        </html>
    `;
    printWindow.document.write(html);
    printWindow.document.close();
};
"""

js = js.replace("window.renderCustomerOrders = () => {", print_func + "\nwindow.renderCustomerOrders = () => {")

with open('/Applications/patuli_Stok_Takip/app_v4.js', 'w') as f:
    f.write(js)
    
print("Updated openCustomerOrderModal, submitCustomerOrder, and added printKitchenOrder.")
