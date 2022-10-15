import cv2
import mediapipe as mp
import time
import Buttons as btns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import librosa
import librosa.display
from IPython.display import Audio
from pydub import AudioSegment
from pydub.playback import play


song1 = AudioSegment.from_file("test.wav", format="wav")
song2 = AudioSegment.from_file("BussDown.mp3", format="mp3")
play(song1)
# play(song2)


#Plotting the wavelengths from the song
x_1, fs = librosa.load('test.wav')

Audio(x_1, rate=fs);

fig, ax = plt.subplots()
librosa.display.waveshow(x_1, sr=fs, ax=ax)
plt.show()



cap = cv2.VideoCapture(0)
mphands = mp.solutions.hands
hands = mphands.Hands(False, 2, 1, .5, .2)
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0
success, img = cap.read()
height, width, c = img.shape


musicWheelLeft = btns.MusicWheel(0, 0, width // 4, height // 2)
bpmLeft = btns.VerticalSlider(0, 100, width // 16, height // 2)
volumeLeft = btns.VerticalSlider(0, 100, width // 2 - width // 16, height // 2)
leftButtonOne = btns.Button(2 * width // 16, height - height // 6)
leftButtonTwo = btns.Button(3 * width // 16, height - height // 6)
leftButtonThree = btns.Button(2 * width // 16, height - height // 6 + width // 16)
leftButtonFour = btns.Button(3 * width // 16, height - height // 6 + width // 16)
leftCueButton = btns.Button(4 * width // 16, height - height // 6, "C")
leftPauseButton = btns.Button(4 * width // 16, height - height // 6 + width // 16, "P")


musicWheelRight = btns.MusicWheel(0, 0, width - width // 4, height // 2)
bpmRight = btns.VerticalSlider(0, 100, width - width // 16, height // 2)
volumeRight = btns.VerticalSlider(0, 100, width // 2 + width // 16, height // 2)
rightButtonOne = btns.Button(width - 2 * width // 16, height - height // 6)
rightButtonTwo = btns.Button(width - 3 * width // 16, height - height // 6)
rightButtonThree = btns.Button(width - 2 * width // 16, height - height // 6 + width // 16)
rightButtonFour = btns.Button(width - 3 * width // 16, height - height // 6 + width // 16)
rightCueButton = btns.Button(width - 4 * width // 16, height - height // 6, "C")
rightPauseButton = btns.Button(width - 4 * width // 16, height - height // 6 + width // 16, "P")

masterVolume = btns.HorizontalSlider(0, 100, width // 2, height - 2 * height // 16)

buttons = [musicWheelLeft, bpmLeft, volumeLeft, leftButtonOne, leftButtonTwo,
           leftButtonThree, leftButtonFour, leftCueButton, leftPauseButton, rightButtonOne, rightButtonTwo,
           rightButtonThree, rightButtonFour, rightCueButton, rightPauseButton,
           musicWheelRight, bpmRight, volumeRight, masterVolume]


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    # img = cv2.flip(img, 0)
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
                if button.beingTouched(cx, cy, img):
                    button.handleTouch(cx, cy, img)
            cv2.circle(img, (cx, cy), btns.radius, (0, 139, 0), cv2.FILLED)
            # Can include mphands.HAND_CONNECTIONS to draw the lines
            # mpDraw.draw_landmarks(img, handLms,)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (139, 0, 0), 4)
    cv2.imshow("Image", img)
    cv2.waitKey(1)