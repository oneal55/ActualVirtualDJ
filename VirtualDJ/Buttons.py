import math
from math import atan2, hypot

import cv2

global radius
radius = 20


def collidesRect(pt1, pt2, x, y) -> bool:
    width = pt2[0] - pt1[0]
    height = pt2[1] - pt1[1]

    circleDistanceX = abs(x - pt1[0] - width / 2)
    circleDistanceY = abs(y - pt1[1] - height / 2)

    if circleDistanceX > (width / 2 + radius):
        return False
    if circleDistanceY > (height / 2 + radius):
        return False

    if circleDistanceX <= width // 2:
        return True
    if circleDistanceY <= height // 2:
        return True

    cornerDistance_sq = ((circleDistanceX - width // 2) ** 2) + (circleDistanceY - height // 2) ** 2;
    return cornerDistance_sq <= (radius ^ 2)


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
            return collidesRect((self.x - width // 40, self.y - width // 40),
                                (self.x + width // 40, self.y + width // 40),
                                x, y)
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
        height, width, c = img.shape
        # Considered Touched When on the outer 2/3rds of the wheel
        return radius + width // 7 > hypot(self.x - x, self.y - y) > radius + ((width // 7) // 3)

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
        currentToCoord = int(((self.current / self.max) * height / 2) + self.y - height / 4)

        cv2.rectangle(img, (self.x, int(self.y - height / 4)), (self.x, int(self.y + height / 4)), (40, 40, 40), 15)
        cv2.rectangle(img,
                      (self.x - int(width / 60), currentToCoord),
                      (self.x + int(width / 60), currentToCoord),
                      (40, 40, 40), 15)

    def beingTouched(self, x, y, img):
        height, width, c = img.shape
        currentY = (self.current / self.max * height / 2 + self.y - height / 4)

        return collidesRect((self.x - width // 60, currentY - 7),
                            (self.x + width // 60, currentY + 7), x, y)

    def handleTouch(self, x, y, img):
        height, width, c = img.shape
        yToNum = int((y + height / 4 - self.y) / (height / 2) * self.max)
        self.current = int(min(max(yToNum, self.min), self.max))


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
        cv2.rectangle(img,
                      (self.x - width // 8, self.y),
                      (self.x + width // 8, self.y),
                      (40, 40, 40), 15)
        cv2.rectangle(img,
                      (currentToX, self.y - height // 20),
                      (currentToX, self.y + height // 20),
                      (40, 40, 40), 15)

    def beingTouched(self, x, y, img):
        height, width, c = img.shape
        currentToX = int((self.current / self.max) * width / 4) + self.x - width // 8
        return collidesRect((currentToX - 7, self.y - height // 20),
                            (currentToX + 7, self.y + height // 20),
                            x, y)

    def handleTouch(self, x, y, img):
        height, width, c = img.shape
        xToNum = int((x + width // 8 - self.x) / (width // 4) * self.max)
        self.current = int(max(min(xToNum, self.max), self.min))
