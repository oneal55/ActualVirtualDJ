import cv2
import mediapipe as mp
import time

import pydub.effects

import Buttons as btns
import matplotlib.pyplot as plt

import librosa
import librosa.display
from pydub import AudioSegment


song1 = AudioSegment.from_file("test.wav", format="wav")
song2 = AudioSegment.from_file("BussDown.mp3", format="mp3") - 30

#Plotting the wavelengths from the song
# x_1, fs = librosa.load('test.wav')

# fig, ax = plt.subplots()
# librosa.display.waveshow(x_1, sr=fs, ax=ax)
# plt.show()

wheel1 = []
cv2.imread("blueTurnTable.png", wheel1)

wheel2 = []
cv2.imread("purpleTurnTable.png", wheel2)


def game():

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 20)
    mphands = mp.solutions.hands
    hands = mphands.Hands(False, 2, 1, .5, .2)
    mpDraw = mp.solutions.drawing_utils

    success, img = cap.read()
    height, width, c = img.shape

    bpmLeft = btns.VerticalSlider(0, 100, width // 16, height // 2)
    volumeLeft = btns.VerticalSlider(0, 100, width // 2 - width // 16, height // 2)
    leftButtonOne = btns.Button(2 * width // 16, height - height // 6)
    leftButtonTwo = btns.Button(3 * width // 16, height - height // 6)
    leftButtonThree = btns.Button(2 * width // 16, height - height // 6 + width // 16)
    leftButtonFour = btns.Button(3 * width // 16, height - height // 6 + width // 16)
    leftCueButton = btns.Button(4 * width // 16, height - height // 6, "C")
    leftPauseButton = btns.Button(4 * width // 16, height - height // 6 + width // 16, "P")
    musicWheelLeft = btns.MusicWheel(song1,
                                     0, 0, width // 4, height // 2,
                                     [volumeLeft, leftButtonOne, leftButtonTwo,
                                      leftButtonThree, leftButtonFour, leftCueButton, leftPauseButton], wheel1)

    bpmRight = btns.VerticalSlider(0, 100, width - width // 16, height // 2)
    volumeRight = btns.VerticalSlider(0, 100, width // 2 + width // 16, height // 2)
    rightButtonOne = btns.Button(width - 2 * width // 16, height - height // 6)
    rightButtonTwo = btns.Button(width - 3 * width // 16, height - height // 6)
    rightButtonThree = btns.Button(width - 2 * width // 16, height - height // 6 + width // 16)
    rightButtonFour = btns.Button(width - 3 * width // 16, height - height // 6 + width // 16)
    rightCueButton = btns.Button(width - 4 * width // 16, height - height // 6, "C")
    rightPauseButton = btns.Button(width - 4 * width // 16, height - height // 6 + width // 16, "P")
    musicWheelRight = btns.MusicWheel(song2,
                                      0, 0, width - width // 4, height // 2,
                                      [volumeRight, rightButtonOne, rightButtonTwo,
                                       rightButtonThree, rightButtonFour, rightCueButton, rightPauseButton], wheel2)

    masterVolume = btns.HorizontalSlider(0, 100, width // 2, height - 2 * height // 16)

    buttons = [musicWheelLeft, musicWheelRight]

    pTime = time.time()
    totalTime = 0
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = cv2.flip(img, 0)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        overlay = img.copy()
        height, width, c = img.shape

        for button in buttons:
            button.go(totalTime)
            button.draw(overlay)

        alpha = 0.6
        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:

                indexPointer = handLms.landmark[8]
                cx, cy = int(width * indexPointer.x), int(height * indexPointer.y)
                for button in buttons:
                    button.handleTouch(cx, cy, img)
                cv2.circle(img, (cx, cy), btns.radius, (0, 139, 0), cv2.FILLED)
                # Can include mphands.HAND_CONNECTIONS to draw the lines
                # mpDraw.draw_landmarks(img, handLms,)

        cTime = time.time()
        totalTime = int((cTime - pTime) * 1000)
        pTime = cTime
        cv2.putText(img, str(int(totalTime)), (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0))
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    game()