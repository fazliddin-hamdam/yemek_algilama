import sqlite3

def init_db():
    conn = sqlite3.connect("data/yemek.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS siparisler
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, yemek TEXT, fiyat REAL, garson TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS performans
                 (garson TEXT PRIMARY KEY, puan INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def kaydet(yemek, fiyat, garson):
    conn = sqlite3.connect("data/yemek.db")
    c = conn.cursor()
    c.execute("INSERT INTO siparisler (yemek, fiyat, garson) VALUES (?, ?, ?)", (yemek, fiyat, garson))
    conn.commit()
    conn.close()

def sifirla():
    conn = sqlite3.connect("data/yemek.db")
    c = conn.cursor()
    c.execute("DELETE FROM siparisler")
    conn.commit()
    conn.close()

def get_masa_toplam():
    conn = sqlite3.connect("data/yemek.db")
    c = conn.cursor()
    c.execute("SELECT SUM(fiyat) FROM siparisler")
    toplam = c.fetchone()[0]
    conn.close()
    return toplam if toplam else 0

def get_siparisler():
    conn = sqlite3.connect("data/yemek.db")
    c = conn.cursor()
    c.execute("SELECT yemek, fiyat FROM siparisler")
    siparisler = c.fetchall()
    conn.close()
    return [{"item": yemek, "price": fiyat} for yemek, fiyat in siparisler]

# === Yeni Eklenen Fonksiyonlar ===

def guncelle_performans(garson, puan_degisim):
    conn = sqlite3.connect("data/yemek.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO performans (garson, puan) VALUES (?, 0)", (garson,))
    c.execute("UPDATE performans SET puan = puan + ? WHERE garson = ?", (puan_degisim, garson))
    conn.commit()
    conn.close()

def get_performans(garson):
    conn = sqlite3.connect("data/yemek.db")
    c = conn.cursor()
    c.execute("SELECT puan FROM performans WHERE garson = ?", (garson,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0

