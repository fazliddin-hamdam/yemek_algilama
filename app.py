from flask import Flask, render_template, Response, jsonify
import cv2
from yolov8_inference import detect_items
from qr_reader import read_qr
from color_detector import detect_red
from utils import fiyat_hesapla
from database import kaydet, init_db, sifirla
from database import get_masa_toplam, get_siparisler, get_performans, guncelle_performans
import time
from threading import Lock

app = Flask(__name__)
camera = cv2.VideoCapture(0)
init_db()

garson = "Bilinmiyor"
reset_triggered = False
son_hesap_tutari = 0
data_lock = Lock()

# Performans kontrolü için global değişkenler
qr_okuma_zamani = None
performans_kontrol_edildi = False

def generate():
    global garson, reset_triggered, son_hesap_tutari
    global qr_okuma_zamani, performans_kontrol_edildi

    start_time = time.time()
    qr_okuma_zamani = None
    performans_kontrol_edildi = False

    while True:
        try:
            success, frame = camera.read()
            if not success:
                continue

            display_frame = frame.copy()

            with data_lock:
                # === Yemek tespiti ===
                items = detect_items(frame)
                mevcut_siparisler = get_siparisler()

                for etiket, box in items:
                    fiyat = fiyat_hesapla(etiket)
                    x1, y1, x2, y2 = map(int, box)
                    cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    if not any(siparis['item'] == etiket for siparis in mevcut_siparisler):
                        kaydet(etiket, fiyat, garson)

                # === QR kod okuma ve performans kontrolü ===
                qr_data = read_qr(frame)
                if qr_data:
                    if garson != qr_data:
                        garson = qr_data
                    qr_okuma_zamani = time.time()
                    if not performans_kontrol_edildi:
                        guncelle_performans(garson, 1)
                        performans_kontrol_edildi = True

                # Eğer QR kod hala okunmamışsa ve süre dolduysa -1 puan ver
                if qr_okuma_zamani is None and not performans_kontrol_edildi:
                    if time.time() - start_time > 60:
                        if garson != "Bilinmiyor":
                            guncelle_performans(garson, -1)
                            performans_kontrol_edildi = True

                # === Kırmızı renk tespiti ve masa sıfırlama ===
                if detect_red(frame) and not reset_triggered:
                    son_hesap_tutari = get_masa_toplam()
                    sifirla()
                    reset_triggered = True

                # === Sıfırlama mesajları ===
                if reset_triggered:
                    overlay = display_frame.copy()
                    cv2.rectangle(overlay,
                                  (0, display_frame.shape[0]//2 - 80),
                                  (display_frame.shape[1], display_frame.shape[0]//2 + 80),
                                  (0, 0, 0), -1)
                    cv2.addWeighted(overlay, 0.5, display_frame, 0.5, 0, display_frame)

                    cv2.putText(display_frame, "MASA SIFIRLANDI!",
                                (frame.shape[1]//2 - 200, frame.shape[0]//2 - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)

                    cv2.putText(display_frame, f"\u00d6denmesi Gereken: {son_hesap_tutari}\u20ba",
                                (frame.shape[1]//2 - 200, frame.shape[0]//2 + 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)

            # === JPEG frame encode ===
            ret, buffer = cv2.imencode('.jpg', display_frame)
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        except Exception as e:
            print(f"Hata olu\u015ftu: {e}")
            continue

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video")
def video():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/get_info")
def get_info():
    current_total = get_masa_toplam()
    return jsonify({
        "waiter": garson,
        "orders": get_siparisler(),
        "total": son_hesap_tutari if reset_triggered else current_total,
        "reset": reset_triggered,
        "performance": get_performans(garson)
    })


@app.route("/reset_system", methods=['POST'])
def reset_system():
    global reset_triggered
    reset_triggered = False
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
