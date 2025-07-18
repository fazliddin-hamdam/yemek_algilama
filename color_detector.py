import cv2
import numpy as np

def detect_red(frame):
    # Görüntüyü blur'la
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    
    # HSV'ye dönüştür
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    # Kırmızı renk aralıkları
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    
    # Maskeleri oluştur
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.add(mask1, mask2)
    
    # Gürültüyü azalt
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    # Kırmızı piksel oranını hesapla
    total_pixels = frame.shape[0] * frame.shape[1]
    red_pixels = cv2.countNonZero(mask)
    red_ratio = red_pixels / total_pixels
    
    # Kırmızı piksel oranı %15'ten fazlaysa true döndür
    return red_ratio > 0.15
