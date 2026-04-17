import cv2
import base64
import numpy as np
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.8)

def process_hand_image(image_data):
    img = cv2.imdecode(
        np.frombuffer(base64.b64decode(image_data.split(",")[1]), np.uint8),
        cv2.IMREAD_COLOR
    )

    img = cv2.flip(img, 1)
    _, img = detector.findHands(img, flipType=False)

    _, buffer = cv2.imencode(".jpg", img)

    return "data:image/jpeg;base64," + base64.b64encode(buffer).decode()