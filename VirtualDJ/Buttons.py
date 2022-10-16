from multiprocessing import Process
from threading import Thread
import os
import cv2
import pydub
from pydub import AudioSegment, playback

global radius
radius = 30


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

    cornerDistance_sq = ((circleDistanceX - width // 2) ** 2) + (circleDistanceY - height // 2) ** 2
    return cornerDistance_sq <= (radius ^ 2)


class Button:
    def __init__(self, x: int, y: int, word=""):
        self.word = word
        self.x = x
        self.y = y
        self.on = False
        self.isColliding = False
        self.index = -1

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
        return collidesRect((self.x - width // 40, self.y - width // 40),
                            (self.x + width // 40, self.y + width // 40),
                            x, y)

    def handleTouch(self, x, y, img):
        self.on = not self.on
        self.isColliding = True


class MusicWheel:
    def __init__(self, song: AudioSegment, currentBeat: int, endBeat: int, x: int, y: int, buttonsToCheck, img):
        self.ogSong = song
        self.song = song
        self.currentBeat = currentBeat
        self.endBeat = endBeat
        self.x = x
        self.y = y
        self.cues = []
        self.time = 0
        self.buttonsToCheck = buttonsToCheck
        self.thread = playback._play_with_simpleaudio(self.song)
        self.paused = False
        self.img = img

    def go(self, newTimeDiff):
        if self.paused:
            self.thread.stop()
        else:
            self.time += newTimeDiff

    def draw(self, img):
        height, width, c = img.shape
        cv2.resize(self.img, width // 7, width //7)
        cv2.circle(img, (self.x, self.y), width // 7, (40, 40, 40), cv2.FILLED)
        for button in self.buttonsToCheck:
            button.draw(img)

    def beingTouched(self, x, y, img):
        for button in self.buttonsToCheck:
            if button.beingTouched(x, y, img):
                return True
        return False

    def handleTouch(self, x, y, img):
        for button in self.buttonsToCheck[0: 4]:
            if not button.beingTouched(x, y, img):
                button.isColliding = False

        if self.buttonsToCheck[0].beingTouched(x, y, img):
            self.buttonsToCheck[0].handleTouch(x, y, img)
            self.thread.stop()
            self.thread = playback._play_with_simpleaudio(self.song[self.time:]
                                                          + (50 - self.buttonsToCheck[0].current) / 50 * 30)

        if self.buttonsToCheck[1].beingTouched(x, y, img):
            if not self.buttonsToCheck[1].isColliding:
                if self.buttonsToCheck[1].on:
                    print(f"Test: {self.time}")
                    self.thread.stop()
                    self.thread = playback._play_with_simpleaudio(self.song[self.buttonsToCheck[1].index:]
                                                                  + (50 - self.buttonsToCheck[0].current) / 50 * 30)
                else:
                    self.buttonsToCheck[1].handleTouch(x, y, img)
                    self.buttonsToCheck[1].index = self.time
                    self.cues += [self.time]
                self.buttonsToCheck[1].isColliding = True

        if self.buttonsToCheck[2].beingTouched(x, y, img):
            if not self.buttonsToCheck[2].isColliding:
                if self.buttonsToCheck[2].on:
                    self.thread.stop()
                    self.thread = playback._play_with_simpleaudio(self.song[self.buttonsToCheck[2].index:]
                                                                  + (50 - self.buttonsToCheck[0].current) / 50 * 30)
                else:
                    self.buttonsToCheck[2].handleTouch(x, y, img)
                    self.buttonsToCheck[2].index = self.time
                    self.cues += [self.time]
            self.buttonsToCheck[2].isColliding = True

        if self.buttonsToCheck[3].beingTouched(x, y, img):
            if not self.buttonsToCheck[3].isColliding:
                if self.buttonsToCheck[3].on:
                    self.thread.stop()
                    self.thread = playback._play_with_simpleaudio(self.song[self.buttonsToCheck[3].index:]
                                                                  + (50 - self.buttonsToCheck[0].current) / 50 * 30)
                else:
                    self.buttonsToCheck[3].handleTouch(x, y, img)
                    self.buttonsToCheck[3].index = self.time
                    self.cues += [self.time]
            self.buttonsToCheck[3].isColliding = True

        if self.buttonsToCheck[4].beingTouched(x, y, img):
            if not self.buttonsToCheck[4].isColliding:
                if self.buttonsToCheck[4].on:
                    self.thread.stop()
                    self.thread = playback._play_with_simpleaudio(self.song[self.buttonsToCheck[4].index:]
                                                                  + (50 - self.buttonsToCheck[0].current) / 50 * 30)
                else:
                    self.buttonsToCheck[4].handleTouch(x, y, img)
                    self.buttonsToCheck[4].index = self.time
                    self.cues += [self.time]
            self.buttonsToCheck[4].isColliding = True

        if self.buttonsToCheck[5].beingTouched(x, y, img):
            if len(self.cues) > 0:
                self.thread.stop()
                self.thread = playback._play_with_simpleaudio(self.song[self.cues[-1]:]
                                                              + (50 - self.buttonsToCheck[0].current) / 50 * 30)

        if self.buttonsToCheck[6].beingTouched(x, y, img):
            if not self.buttonsToCheck[6].isColliding:
                if self.paused:
                    self.thread = playback._play_with_simpleaudio(self.song[self.time:]
                                                                  + (50 - self.buttonsToCheck[0].current) / 50 * 30)
                    self.paused = False
                else:
                    self.paused = True
                self.buttonsToCheck[-1].handleTouch(x, y, img)


class VerticalSlider:
    def __init__(self, min: int, max: int, x: int, y: int):
        self.min = min
        self.max = max
        self.current = (min + max) // 2
        self.x = x
        self.y = y
        self.isColliding = False

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
        self.isColliding = True


class HorizontalSlider:
    def __init__(self, min: int, max: int, x: int, y: int):
        self.min = min
        self.max = max
        self.current = (min + max) // 2
        self.x = x
        self.y = y
        self.isColliding = False

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
                            (currentToX + 7, self.y + height // 20), x, y)

    def handleTouch(self, x, y, img):
        height, width, c = img.shape
        xToNum = int((x + width // 8 - self.x) / (width // 4) * self.max)
        self.current = int(max(min(xToNum, self.max), self.min))
        self.isColliding = True
