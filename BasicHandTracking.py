import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands(False, 2, 1, .5, .5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)


    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(w * lm.x), int(h * lm.y)
                if id == 8:
                    cv2.circle(img, (cx, cy), 25, (139, 0 , 0), cv2.FILLED)
            # Can include mphands.HAND_CONNECTIONS to draw the lines
            # mpDraw.draw_landmarks(img, handLms,)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str((int)(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (139, 0, 0), 4)
    cv2.imshow("Image", img)
    cv2.waitKey(1)