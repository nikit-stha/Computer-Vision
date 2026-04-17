import cv2
import base64
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import math
import os

detector = HandDetector(detectionCon=0.8)

def process_hand_image(image_data):
    img = cv2.imdecode(
        np.frombuffer(base64.b64decode(image_data.split(",")[1]), np.uint8),
        cv2.IMREAD_COLOR
    )

    hands, img = detector.findHands(img, flipType=True)

    if hands:
        lmList = hands[0]['lmList']

        if len(lmList) != 0:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]

            dist = math.hypot((x2-x1), (y2-y1))

            vol = ((dist - 20) / (180)) * 100

            os.system(f"pactl set-sink-volume @DEFAULT_SINK@ {vol}%")
        
            cv2.putText(img, f'VOLUME : {int(vol)}%', (20, 80), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 0, 255), 2)


    _, buffer = cv2.imencode(".jpg", img)

    return "data:image/jpeg;base64," + base64.b64encode(buffer).decode()