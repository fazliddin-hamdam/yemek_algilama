# 🍽️ Yemek Tanıma ve Garson Performansı Sistemi

Bu proje, bir restorandaki masaları kamera ile izleyerek yemek türlerini otomatik tanıyan, toplam fiyatı hesaplayan ve QR kod üzerinden garsonları tanıyarak performanslarını değerlendiren bir sistemdir. 

Ayrıca yeşil renk ile masa sıfırlama, canlı video yayını ve basit bir web arayüzü içerir.

## 🔧 Kullanılan Teknolojiler

- Python & Flask (web arayüzü için)
- OpenCV (kamera işlemleri için)
- YOLOv8 (yemek tespiti için)
- Pyzbar (QR kod okuma)
- SQLite (veritabanı)
- HTML, CSS, JS (arayüz)

## 🚀 Özellikler

- Canlı kamera ile yemek algılama
- Algılanan yemeklerin otomatik fiyatlandırılması
- QR kodla garson tanıma
- 1 dakika içinde QR kod okutulmazsa -1 puan, okutulursa +1 puan
- Performans puanı masa sıfırlansa bile görünür
- Yeşil renk gösterildiğinde masa ve siparişler sıfırlanır
- Web arayüzü üzerinden canlı video, sipariş listesi ve toplam tutar takibi

## 📂 Klasör Yapısı

restaurant/
│
├── app.py # Ana uygulama dosyası
├── qr_reader.py # QR kod okuma fonksiyonu
├── yolov8_inference.py # YOLOv8 tahmin fonksiyonu
├── color_detector.py # Renk algılama (kırmızı / yeşil)
├── database.py # SQLite işlemleri
├── utils.py # Yardımcı fonksiyonlar (fiyat hesaplama vb.)
│
├── templates/
│ └── index.html # Ana HTML arayüz
│
├── static/
│ └── style.css # Arayüz stilleri
│
├── data/
│ └── yemek.db # Veritabanı dosyası
│
├── clean_db.py # (İsteğe bağlı) veritabanı sıfırlama scripti
│
├── .gitignore
└── README.md



## 🛠️ Kurulum

```bash
# Gerekli paketleri yükleyin
pip install -r requirements.txt

# Uygulamayı başlatın
python app.py
Ardından tarayıcıdan şu adrese gidin:



http://127.0.0.1:5000/

📝 Notlar
QR kodlar sadece "Fazliddin" garson için test edilmiştir.

Performans puanı sistem kapatılsa bile yemek.db veritabanında tutulur.

Masa sıfırlamak için kırmızı renk gösterilmelidir.

clean_db.py ile sistem manuel olarak da sıfırlanabilir.

Geliştirici
    Fazliddin Hamdam