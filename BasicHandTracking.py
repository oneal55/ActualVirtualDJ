import math
from math import hypot, atan2

import cv2
import mediapipe as mp
import time

def collidesRect(pt1, pt2, x, y, r) -> bool:

    circleDistanceX = abs(x - pt1[0]);
    circleDistanceY = abs(y - pt1[1]);

    if circleDistanceX > (pt1[0] +  + r):
        return False
    if circleDistanceY > (7.5 + 15):
        return False

    if circleDistanceX <= width / 60:
        return True
    if circleDistanceY <= height / 4:
        return True

    cornerDistance_sq = ((circleDistanceX - width / 2) ** 2) + (circleDistanceY - height / 2) ** 2;
    return (cornerDistance_sq <= (15 ^ 2));
class Button:
    def __init__(self, x: int, y: int, word=""):
        self.word = word
        self.x = x
        self.y = y
        self.on = False

    def draw(self, img):
        height, width, c = img.shape
        if self.on:
            cv2.rectangle(img,
                          (self.x - width // 40, self.y - width // 40),
                          (self.x + width // 40, self.y + width // 40),
                          (40, 100, 40), cv2.FILLED)
        else:
            cv2.rectangle(img,
                          (self.x - width // 40, self.y - width // 40),
                          (self.x + width // 40, self.y + width // 40),
                          (40, 40, 100), cv2.FILLED)
        cv2.putText(img, self.word, (self.x - width // 40, self.y), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 4)

    def beingTouched(self, x, y, img):
        height, width, c = img.shape
        if not self.on:
            return x + 15 > self.x - width // 40\
                   and x - 15 < self.x + width // 40 and\
                   y + 15 > self.y - width // 40 and\
                   y - 15 < self.y + width // 40
        return False

    def handleTouch(self, x, y, img):
        self.on = True


class MusicWheel:
    def __init__(self, currentBeat: int, endBeat: int, x: int, y: int):
        self.currentBeat = currentBeat
        self.endBeat = endBeat
        self.x = x
        self.y = y

    def draw(self, img):
        height, width, c = img.shape
        cv2.circle(img, (self.x, self.y), width // 7, (40, 40, 40), cv2.FILLED)

    def beingTouched(self, x, y, img):
        #Considered Touched When on the outer 2/3rds of the wheel
        return 30 + width // 7 > hypot(self.x - x, self.y - y) > 30 + ((width // 7) // 3)

    def handleTouch(self, x, y, img):
        angle = -atan2(y - self.y, x - self.x)
        if angle < 0:
            angle = atan2(y - self.y, self.x - x) + math.pi
        # print((int(angle * 180 / math.pi) - 90) % 360 // 90)
class VerticalSlider:
    def __init__(self, min: int, max: int, x: int, y: int):
        self.min = min
        self.max = max
        self.current = (min + max) // 2
        self.x = x
        self.y = y

    def draw(self, img):
        height, width, c = img.shape
        currentToCoord = int(((self.current / self.max) * height / 2) + height / 4)

        cv2.rectangle(img, (self.x, int(self.y - height / 4)), (self.x, int(self.y + height / 4)), (40, 40, 40), 15)
        cv2.rectangle(img,
                      (self.x - int(width / 60), currentToCoord),
                      (self.x + int(width / 60), currentToCoord), (40, 40, 40), 15)

    def beingTouched(self, x, y, img):
        height, width, c = img.shape
        half = (self.min + self.max) / 2
        currentY = (self.current - half) * (self.max) / height / 2 + height / 2
        circleDistanceX = abs(x - self.x);
        circleDistanceY = abs(y - currentY);

        if circleDistanceX > (width / 60 + 15):
            return False
        if circleDistanceY > (7.5 + 15):
            return False

        if circleDistanceX <= width / 60:
            return True
        if circleDistanceY <= height / 4:
            return True

        cornerDistance_sq = ((circleDistanceX - width / 2) ** 2) + (circleDistanceY - height / 2) ** 2;
        return (cornerDistance_sq <= (15 ^ 2));

    def handleTouch(self, x, y, img):
        height, width, c = img.shape

        yToNum = int((y - height / 4) / (height / 2) * self.max)

        self.current = int(yToNum)

class HorizontalSlider:
    def __init__(self, min: int, max: int, x: int, y: int):
        self.min = min
        self.max = max
        self.current = (min + max) // 2
        self.x = x
        self.y = y

    def draw(self, img):
        height, width, c = img.shape
        currentToX = int((self.current / self.max) * width / 4) + self.x - width // 8
        cv2.rectangle(img, (self.x - width // 8, self.y), (self.x + width // 8, self.y), (40, 40, 40), 15)
        cv2.rectangle(img, (currentToX, self.y - height // 20), (currentToX, self.y + height // 20), (40, 40, 40), 15)

    def beingTouched(self, x, y, img):
        return False


cap = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands(False, 2, 1, .5, .5)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0
succes, img = cap.read()

height, width, c = img.shape

musicWheelLeft = MusicWheel(0, 0, width // 4, height // 2)
bpmLeft = VerticalSlider(0, 100, width // 16, height // 2)
volumeLeft = VerticalSlider(0, 100, width // 2 - width // 16, height // 2)
leftButtonOne = Button(2 * width // 16, height - height // 6)
leftButtonTwo = Button(3 * width // 16, height - height // 6)
leftButtonThree = Button(2 * width // 16, height - height // 6 + width // 16)
leftButtonFour = Button(3 * width // 16, height - height // 6 + width // 16)
leftCueButton = Button(4 * width // 16, height - height // 6, "C")
leftPauseButton = Button(4 * width // 16, height - height // 6 + width // 16, "P")


musicWheelRight = MusicWheel(0, 0, width - width // 4, height // 2)
bpmRight = VerticalSlider(0, 100, width - width // 16, height // 2)
volumeRight = VerticalSlider(0, 100, width // 2 + width // 16, height // 2)
rightButtonOne = Button(width - 2 * width // 16, height - height // 6)
rightButtonTwo = Button(width - 3 * width // 16, height - height // 6)
rightButtonThree = Button(width - 2 * width // 16, height - height // 6 + width // 16)
rightButtonFour = Button(width - 3 * width // 16, height - height // 6 + width // 16)
rightCueButton = Button(width - 4 * width // 16, height - height // 6, "C")
rightPauseButton = Button(width - 4 * width // 16, height - height // 6 + width // 16, "P")

masterVolume = HorizontalSlider(0, 100, width // 2, height - 2 * height // 16)

buttons = [musicWheelLeft, bpmLeft, volumeLeft, leftButtonOne, leftButtonTwo,
           leftButtonThree, leftButtonFour, leftCueButton, leftPauseButton, rightButtonOne, rightButtonTwo,
           rightButtonThree, rightButtonFour, rightCueButton, rightPauseButton,
           musicWheelRight, bpmRight, volumeRight, masterVolume]


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    overlay = img.copy()
    height, width, c = img.shape

    for button in buttons:
        button.draw(overlay)
    alpha = 0.6
    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            indexPointer = handLms.landmark[8]
            cx, cy = int(width * indexPointer.x), int(height * indexPointer.y)
            for button in buttons:
                if (button.beingTouched(cx, cy, img)):
                    button.handleTouch(cx, cy, img)
            cv2.circle(img, (cx, cy), 30, (0, 0, 139), cv2.FILLED)
            # Can include mphands.HAND_CONNECTIONS to draw the lines
            # mpDraw.draw_landmarks(img, handLms,)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str((int)(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (139, 0, 0), 4)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
