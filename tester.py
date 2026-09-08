import cv2
import numpy as np
from mss import mss
from ultralytics import YOLO

# 1. Carica il modello pre-addestrato (YOLOv8 Nano è il più veloce)
model = YOLO("yolov8n.pt")

# 2. Configura la cattura dello schermo
monitor = {"top": 0, "left": 0, "width": 800, "height": 600}

with mss() as sct:
    print("Premi 'q' per chiudere...")
    
    while True:
        # Cattura lo screenshot
        img = np.array(sct.grab(monitor))
        
        # Converte da BGRA a BGR (necessario per OpenCV/YOLO)
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # 3. Esegui il rilevamento degli oggetti
        results = model.predict(frame, conf=0.5, verbose=False)

        # 4. Disegna i risultati sul frame
        annotated_frame = results[0].plot()

        # Mostra la finestra con i rettangoli
        cv2.imshow("Desktop Object Detection", annotated_frame)

        # Esci premendo il tasto 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()