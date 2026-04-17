import cv2
import base64
import numpy as np
from pyzbar.pyzbar import decode

def process_barcode(image_data):
    img = cv2.imdecode(
        np.frombuffer(base64.b64decode(image_data.split(",")[1]), np.uint8),
        cv2.IMREAD_COLOR
    )

    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1,1,2))

        pts2 = barcode.rect

        cv2.polylines(img, [pts], True, (0,255,0), 5)
        cv2.putText(img, f'Data: {myData}', (pts2[0], pts2[1]),
                    cv2.FONT_HERSHEY_DUPLEX, 0.9, (0,255,0), 2)

    _, buffer = cv2.imencode(".jpg", img)

    return "data:image/jpeg;base64," + base64.b64encode(buffer).decode()