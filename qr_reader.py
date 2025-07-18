from pyzbar.pyzbar import decode
import cv2

def read_qr(frame):
    decoded = decode(frame)
    if decoded:
        return "Fazliddin"  # QR kod okunduğunda her zaman Fazliddin döndür
    return None
