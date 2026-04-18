import cv2
from cvzone.HandTrackingModule import HandDetector
import base64
import numpy as np
import time
import json
import cvzone

from app import db
from app.models.quiz_model import Quiz

detector = HandDetector(detectionCon=0.8, maxHands=1)


class MCQ():
    def __init__(self, data):
        self.question = data.question
        self.choice1 = data.option1
        self.choice2 = data.option2
        self.choice3 = data.option3
        self.choice4 = data.option4
        self.answer = int(data.answer)

        self.userAns = None

    def update(self, img, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)


def getData():
    return Quiz.query.all()

mcqList = []
qNo = 0
qTotal = 0


def process_image(image_data):
    global qNo, qTotal, mcqList
    if not mcqList:
        dataAll = getData()
        for q in dataAll:
            mcqList.append(MCQ(q))
        qTotal = len(dataAll)

    img = cv2.imdecode(
        np.frombuffer(base64.b64decode(image_data.split(",")[1]), np.uint8),
        cv2.IMREAD_COLOR
    )

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, flipType=False)

    if qNo < qTotal:
        mcq = mcqList[qNo]

        img, bbox = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2, offset=50, border=5)
        img, bbox1 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2, offset=50, border=5)
        img, bbox2 = cvzone.putTextRect(img, mcq.choice2, [400, 250], 2, 2, offset=50, border=5)
        img, bbox3 = cvzone.putTextRect(img, mcq.choice3, [100, 400], 2, 2, offset=50, border=5)
        img, bbox4 = cvzone.putTextRect(img, mcq.choice4, [400, 400], 2, 2, offset=50, border=5)

        if hands:
            lmList = hands[0]['lmList']

            if len(lmList) >= 13:
                x, y = lmList[8][0], lmList[8][1]

                p1 = lmList[8][0:2]
                p2 = lmList[12][0:2]

                length, info, img = detector.findDistance(p1, p2, img)

                if length < 40:
                    mcq.update(img, (x, y), [bbox1, bbox2, bbox3, bbox4])

                    if mcq.userAns is not None:
                        time.sleep(0.5)
                        qNo += 1

    else:
        score = 0
        for mcq in mcqList:
            if mcq.answer == mcq.userAns:
                score += 1

        if qTotal > 0:
            score = round((score / qTotal) * 100, 2)
        else:
            score = 0

        img, _ = cvzone.putTextRect(img, "Quiz Completed", [250, 300], 2, 2, offset=50, border=5)
        img, _ = cvzone.putTextRect(img, f'Your Score: {score}%', [700, 300], 2, 2, offset=50, border=5)

    # Progress Bar
    # if qTotal > 0:
    #     barValue = 150 + (950 // qTotal) * qNo
    #     cv2.rectangle(img, (150, 600), (barValue, 650), (0, 255, 0), cv2.FILLED)
    #     cv2.rectangle(img, (150, 600), (1100, 650), (255, 0, 255), 5)
    #     img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [1130, 635], 2, 2, offset=16)

    _, buffer = cv2.imencode(".jpg", img)

    return "data:image/jpeg;base64," + base64.b64encode(buffer).decode()


def add_new_question(question, option1, option2, option3, option4, answer):

    quiz = Quiz(
        question=question,
        option1=option1,
        option2=option2,
        option3=option3,
        option4=option4,
        answer=answer
    )

    db.session.add(quiz)
    db.session.commit()

    return True, "Registered"