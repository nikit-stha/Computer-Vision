import cv2
import numpy as np
import face_recognition
import os
import json
import base64
from uuid import uuid4

from app import db
from app.models.user_model import User
from app.models.face_model import Face

path = os.path.join("app", "static", "temp_faces")
os.makedirs(path, exist_ok=True)


def getKnownEncodings():
    encodeListKnown = []
    classNames = []

    faces = Face.query.all()

    for face in faces:
        encode = np.array(json.loads(face.encoding))
        user = db.session.get(User, face.user_id)

        encodeListKnown.append(encode)
        classNames.append(user.username)

    return encodeListKnown, classNames


def process_face(image_data):
    img = cv2.imdecode(
        np.frombuffer(base64.b64decode(image_data.split(",")[1]), np.uint8),
        cv2.IMREAD_COLOR
    )

    img = cv2.flip(img, 1)

    encodeListKnown, classNames = getKnownEncodings()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    recognized = False
    name = None
    temp_face = None

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = 4 * y1, 4 * x2, 4 * y2, 4 * x1

        if len(encodeListKnown) > 0:
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                recognized = True

                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, name, (x1 + 6, y2 - 6),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            else:
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(img, "STRANGER", (x1 + 6, y2 - 6),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

                if temp_face is None:
                    filename = f"{uuid4().hex}.jpg"
                    filepath = os.path.join(path, filename)
                    cv2.imwrite(filepath, img)

                    temp_face = {
                        "filename": filename,
                        "location": [y1, x2, y2, x1]
                    }

        else:
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(img, "STRANGER", (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

            if temp_face is None:
                filename = f"{uuid4().hex}.jpg"
                filepath = os.path.join(path, filename)
                cv2.imwrite(filepath, img)

                temp_face = {
                    "filename": filename,
                    "location": [y1, x2, y2, x1]
                }

    _, buffer = cv2.imencode(".jpg", img)
    processed_image = "data:image/jpeg;base64," + base64.b64encode(buffer).decode()

    return {
        "image": processed_image,
        "face_detected": len(facesCurFrame) > 0,
        "recognized": recognized,
        "name": name,
        "temp_face": temp_face
    }


def register_face_from_temp(username, temp_face_filename, face_location_json):
    filepath = os.path.join(path, temp_face_filename)

    img = cv2.imread(filepath)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    y1, x2, y2, x1 = json.loads(face_location_json)

    encodes = face_recognition.face_encodings(imgRGB, [(y1, x2, y2, x1)])
    encode = encodes[0]

    user = User(username=username)
    db.session.add(user)
    db.session.commit()

    face = Face(
        user_id=user.id,
        encoding=json.dumps(encode.tolist())
    )
    db.session.add(face)
    db.session.commit()

    os.remove(filepath)

    return True, "Registered"