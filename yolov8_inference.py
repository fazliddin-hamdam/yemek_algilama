from ultralytics import YOLO
import cv2

model = YOLO("best.pt")

def detect_items(frame):
    results = model(frame)
    items = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            if conf > 0.75:  # Güven değerini 0.75'e yükselttik
                name = model.names[cls]
                xyxy = box.xyxy[0].cpu().numpy()
                items.append((name, xyxy))
    return items
