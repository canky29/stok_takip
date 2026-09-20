import http.server
import socketserver
import json
import sqlite3
import os
import urllib.parse
from datetime import datetime

PORT = 8080
DB_FILE = 'bakery.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT NOT NULL,
            stock INTEGER DEFAULT 0,
            minStock INTEGER DEFAULT 5,
            orderQuantity INTEGER DEFAULT 10,
            sales INTEGER DEFAULT 0,
            waste INTEGER DEFAULT 0,
            lastUpdated TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            productId INTEGER,
            productName TEXT,
            quantity INTEGER,
            status TEXT,
            createdAt TEXT,
            updatedAt TEXT
        )
    ''')
    conn.commit()
    
    # Check if we need to seed data
    c.execute('SELECT COUNT(*) FROM products')
    if c.fetchone()[0] == 0:
        seed_data(c)
        conn.commit()
    conn.close()

def seed_data(c):
    products = [
        # PASTALAR - HASBAHÇE
        ("ÇİLEK", "PASTALAR", "HASBAHÇE"),
        ("ÇİLEK MUZ", "PASTALAR", "HASBAHÇE"),
        ("ÇİLEK MUZ FRAMBUAZ", "PASTALAR", "HASBAHÇE"),
        ("ÇİLEK MUZ BÖĞÜRTLEN", "PASTALAR", "HASBAHÇE"),
        ("FRAMBUAZ", "PASTALAR", "HASBAHÇE"),
        ("MUZ FRAMBUAZ", "PASTALAR", "HASBAHÇE"),
        ("MUZ CEVİZ", "PASTALAR", "HASBAHÇE"),
        ("MUZ BÖĞÜRTLEN", "PASTALAR", "HASBAHÇE"),
        # PASTALAR - MUZ BÖĞÜRTLEN
        ("ÇİLEKLİ BABAROSKİ", "PASTALAR", "MUZ BÖĞÜRTLEN"),
        ("MUZLU BABAROSKİ", "PASTALAR", "MUZ BÖĞÜRTLEN"),
        ("KARA ORMAN", "PASTALAR", "MUZ BÖĞÜRTLEN"),
        ("MUZ KROKAN", "PASTALAR", "MUZ BÖĞÜRTLEN"),
        ("KARAMBOL", "PASTALAR", "MUZ BÖĞÜRTLEN"),
        ("MOİS", "PASTALAR", "MUZ BÖĞÜRTLEN"),
        ("FISTIK ÇİKOLATA", "PASTALAR", "MUZ BÖĞÜRTLEN"),
        ("GANAJ", "PASTALAR", "MUZ BÖĞÜRTLEN"),
        ("ÇİLEK ÇİKOLATA", "PASTALAR", "MUZ BÖĞÜRTLEN"),
        ("ÇİLEK OREO", "PASTALAR", "MUZ BÖĞÜRTLEN"),
        ("ÇİLEK FRAMBUAZ", "PASTALAR", "MUZ BÖĞÜRTLEN"),
        ("ÇİLEK BÖĞÜRTLEN", "PASTALAR", "MUZ BÖĞÜRTLEN"),
        ("ÇİLEK FESTİVAL", "PASTALAR", "MUZ BÖĞÜRTLEN"),
        ("FRAMBUAZ ÇİKOLATA", "PASTALAR", "MUZ BÖĞÜRTLEN"),
        ("KROKAN ÇİKOLATA", "PASTALAR", "MUZ BÖĞÜRTLEN"),
        # PASTALAR - MUZ ÇİKOLATA
        ("PROFİTEROL PASTA", "PASTALAR", "MUZ ÇİKOLATA"),
        ("ÇİLEK PROFİTEROL", "PASTALAR", "MUZ ÇİKOLATA"),
        ("KARA ORMAN (MUZ)", "PASTALAR", "MUZ ÇİKOLATA"),
        ("KESTANE MOBLAN", "PASTALAR", "MUZ ÇİKOLATA"),
        ("ÇİLEK VOLKANİK", "PASTALAR", "MUZ ÇİKOLATA"),
        ("VİŞNE VOLKANİK", "PASTALAR", "MUZ ÇİKOLATA"),
        # ADET PASTA - FISTIK
        ("GANAJ", "ADET PASTA", "FISTIK"),
        ("ÇİLEK", "ADET PASTA", "FISTIK"),
        ("ÇİLEK OREO", "ADET PASTA", "FISTIK"),
        ("PROFİTEROL", "ADET PASTA", "FISTIK"),
        ("ÇİLEK FRAMBUAZ", "ADET PASTA", "FISTIK"),
        ("ÇİLEK BÖĞÜRTLEN", "ADET PASTA", "FISTIK"),
        ("KRANBOL", "ADET PASTA", "FISTIK"),
        # ADET PASTA - ORMAN MEYVE
        ("KESTANELİ MOBLAN", "ADET PASTA", "ORMAN MEYVE"),
        ("ÇİLEK VOLKANİK (ORMAN)", "ADET PASTA", "ORMAN MEYVE"),
        ("MUZLU VOLKANİK", "ADET PASTA", "ORMAN MEYVE"),
        ("VİŞNELİ VOLKANİK", "ADET PASTA", "ORMAN MEYVE"),
        # ADET PASTA - HASBAHÇE
        ("ÇİLEK (ADET)", "ADET PASTA", "HASBAHÇE"),
        ("ÇİLEK MUZ (ADET)", "ADET PASTA", "HASBAHÇE"),
        ("FRAMBUAZ", "ADET PASTA", "HASBAHÇE"),
        ("MUZ CEVİZ", "ADET PASTA", "HASBAHÇE"),
        ("ÇİLEKLİ BABOROSKİ", "ADET PASTA", "HASBAHÇE"),
        ("MUZLU BABOROSKİ", "ADET PASTA", "HASBAHÇE"),
        # PETİFÜR - TARTOLET
        ("SARMA", "PETİFÜR", "TARTOLET"),
        ("EKLER", "PETİFÜR", "TARTOLET"),
        ("LANÇOP FRAM.", "PETİFÜR", "TARTOLET"),
        ("LANÇOP KARAMEL", "PETİFÜR", "TARTOLET"),
        ("MOZAIK", "PETİFÜR", "TARTOLET"),
        ("MİNİ İBİZA", "PETİFÜR", "TARTOLET"),
        # PETİFÜR - DOLGULU ÇİKOLATA
        ("KARAMEL", "PETİFÜR", "DOLGULU ÇİKOLATA"),
        ("FRAMBUAZ", "PETİFÜR", "DOLGULU ÇİKOLATA"),
        ("VİŞNE", "PETİFÜR", "DOLGULU ÇİKOLATA"),
        ("LİMON", "PETİFÜR", "DOLGULU ÇİKOLATA"),
        ("PROFİTEROL (ÇİKOLATA)", "PETİFÜR", "DOLGULU ÇİKOLATA"),
        ("CHEESCAKE FRAMB.", "PETİFÜR", "DOLGULU ÇİKOLATA"),
        ("CHEESCAKE LİMON", "PETİFÜR", "DOLGULU ÇİKOLATA"),
        ("TREMİSU", "PETİFÜR", "DOLGULU ÇİKOLATA"),
        ("BİTTER PORTAKAL", "PETİFÜR", "DOLGULU ÇİKOLATA"),
        ("FRAMBUAZ BAMBU", "PETİFÜR", "DOLGULU ÇİKOLATA"),
        ("FISTIKLI BAMBU", "PETİFÜR", "DOLGULU ÇİKOLATA"),
        ("OREO BAMBU", "PETİFÜR", "DOLGULU ÇİKOLATA"),
        ("DELEGORDA KARAMEL", "PETİFÜR", "DOLGULU ÇİKOLATA"),
        ("SHİNESUN", "PETİFÜR", "DOLGULU ÇİKOLATA"),
        # PETİFÜR - ORTA DOLAP
        ("KAŞIK PASTA", "PETİFÜR", "ORTA DOLAP"),
        ("PROFİTEROL (DOLAP)", "PETİFÜR", "ORTA DOLAP"),
        ("SÜTLAÇ", "PETİFÜR", "ORTA DOLAP"),
        ("SUPANGLE", "PETİFÜR", "ORTA DOLAP"),
        ("ADET RULO", "PETİFÜR", "ORTA DOLAP"),
    ]
    for p in products:
        c.execute('''
            INSERT INTO products (name, category, subcategory, stock, minStock, orderQuantity, sales, waste, lastUpdated)
            VALUES (?, ?, ?, 10, 5, 10, 0, 0, ?)
        ''', (p[0], p[1], p[2], datetime.now().isoformat()))

class BakeryHandler(http.server.SimpleHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        if self.path == '/api/products':
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM products ORDER BY category, subcategory, id')
            products = [dict(row) for row in c.fetchall()]
            conn.close()
            self.send_json(products)
        elif self.path == '/api/orders':
            conn = sqlite3.connect(DB_FILE)
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute('SELECT * FROM orders ORDER BY id DESC')
            orders = [dict(row) for row in c.fetchall()]
            conn.close()
            self.send_json(orders)
        else:
            if self.path == '/':
                self.path = '/index.html'
            return super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        if not post_data:
            self.send_error(400)
            return
            
        data = json.loads(post_data.decode('utf-8'))
        
        if self.path == '/api/products/update':
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            now = datetime.now().isoformat()
            
            product_id = data.get('id')
            new_stock = data.get('stock')
            new_sales = data.get('sales')
            new_waste = data.get('waste')
            
            c.execute('SELECT stock, minStock, orderQuantity, name FROM products WHERE id=?', (product_id,))
            row = c.fetchone()
            if row:
                old_stock, min_stock, order_qty, p_name = row
                
                # Check for automatic ordering BEFORE saving new stock
                # If new stock <= min_stock AND it wasn't already an active order.
                # Actually, rule: "Mevcut stok minimum stok seviyesine eşit veya altına düştüğünde otomatik olarak imalathane siparişi oluştur."
                # AND "Sipariş durumu "Bekliyor" ise tekrar 10 adet sipariş oluşturma."
                # We will just check if any open order exists for this product.
                
                c.execute('''
                    UPDATE products SET stock=?, sales=?, waste=?, lastUpdated=? WHERE id=?
                ''', (new_stock, new_sales, new_waste, now, product_id))
                
                if new_stock <= min_stock:
                    c.execute("SELECT COUNT(*) FROM orders WHERE productId=? AND status IN ('Bekliyor', 'Hazırlanıyor')", (product_id,))
                    pending = c.fetchone()[0]
                    if pending == 0:
                        c.execute('''
                            INSERT INTO orders (productId, productName, quantity, status, createdAt, updatedAt)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (product_id, p_name, order_qty, 'Bekliyor', now, now))
                
            conn.commit()
            conn.close()
            self.send_json({"success": True})
            
        elif self.path == '/api/orders/update':
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            order_id = data.get('id')
            status = data.get('status')
            now = datetime.now().isoformat()
            c.execute('UPDATE orders SET status=?, updatedAt=? WHERE id=?', (status, now, order_id))
            conn.commit()
            conn.close()
            self.send_json({"success": True})
        else:
            self.send_error(404)

if __name__ == '__main__':
    init_db()
    with socketserver.TCPServer(("", PORT), BakeryHandler) as httpd:
        print(f"Serving API and UI at http://localhost:{PORT}")
        httpd.serve_forever()
