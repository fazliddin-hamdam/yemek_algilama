import sqlite3
import os

db_path = "data/yemek.db"

def reset_database():
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Eski veritabanı dosyası silindi.")
    else:
        print("Veritabanı dosyası bulunamadı, yeni oluşturulacak.")

    # Yeni boş veritabanı oluştur ve tabloları baştan oluştur
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # siparisler tablosu
    c.execute('''CREATE TABLE IF NOT EXISTS siparisler
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, yemek TEXT, fiyat REAL, garson TEXT)''')

    # performans tablosu (örnek)
    c.execute('''CREATE TABLE IF NOT EXISTS performans
                 (garson TEXT PRIMARY KEY, puan INTEGER)''')

    conn.commit()
    conn.close()
    print("Veritabanı sıfırlandı ve tablolar yeniden oluşturuldu.")

if __name__ == "__main__":
    reset_database()
