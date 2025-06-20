import cv2
import cvzone
import numpy as np
import os
from cvzone.HandTrackingModule import HandDetector
import pygame

sound_folder = "pianoSounds"
key_sounds = {}
pygame.mixer.init()

# TODO: List of corresponding keys of the online piano
#   keys = ["A0", "A#0", "B0",
#          "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1",
#          "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2",
#          "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
#          "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
#          "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5",
#          "C6", "C#6", "D6"]

keys = ["A0", "Bb0", "B0",
        "C1", "Db1", "D1", "Eb1", "E1", "F1", "Gb1", "G1", "Ab1", "A1", "Bb1", "B1",
        "C2", "Db2", "D2", "Eb2", "E2", "F2", "Gb2", "G2", "Ab2", "A2", "Bb2", "B2",
        "C3", "Db3", "D3", "Eb3", "E3", "F3", "Gb3", "G3", "Ab3", "A3", "Bb3", "B3",
        "C4", "Db4", "D4", "Eb4", "E4", "F4", "Gb4", "G4", "Ab4", "A4", "Bb4", "B4",
        "C5", "Db5", "D5", "Eb5", "E5", "F5", "Gb5", "G5", "Ab5", "A5", "Bb5", "B5",
        "C6", "Db6", "D6"]

for key in keys:
    path = os.path.join(sound_folder, f"{key}.mp3")
    if os.path.exists(path):
        key_sounds[key] = pygame.mixer.Sound(path)
    else:
        print(f"Warning: Sound for key {key} not found at {path}")
cap = cv2.VideoCapture(0)
cap.set(3, 2560)
cap.set(4, 1440)

# higher detectionCon to avoid randomly key pressed
detector = HandDetector(detectionCon=0.8)


# draw the button onto the image every iteration, since each iteration we have a new image
def drawAllTransparent(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.position
        width, height = button.size
        cvzone.cornerRect(imgNew, (button.position[0], button.position[1], button.size[0], button.size[1]), 20, rt=0)

        # button
        if "b" in button.text:
            # black buttons
            cv2.rectangle(imgNew, button.position, (x + width, y + height), (0, 0, 0), cv2.FILLED)
        else:
            # white buttons
            cv2.rectangle(imgNew, button.position, (x + width, y + height), (255, 255, 255), cv2.FILLED)
        # text
        cv2.putText(imgNew, button.text, (x, y + 65), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out

# TODO: We need 27 blacks and 39 white buttons (out of 36 blacks and 52 whites)
class Button:
    # similar to java constructor
    def __init__(self, position, text, size=None):
        if size is None:
            size = [35, 200]
        self.position = position
        self.text = text
        self.size = size

buttons = []




# cool way in python to keep track of the index when iterate using enhanced for loop
for x, key in enumerate(keys):
    # size is none -> default size is used
    buttons.append(Button([38 * x + 19, 1240], key))

def isPressed(landmarkList, button):
    x, y = button.position
    width, height = button.size
    # flip horizontally by taking the difference from 2560 (which is the width of the display screen)
    return ((x < 2560 - landmarkList[4][0] < x + width and y < landmarkList[4][1] < y + height) or
                    (x < 2560 - landmarkList[8][0] < x + width and y < landmarkList[8][1] < y + height) or
                    (x < 2560 - landmarkList[12][0] < x + width and y < landmarkList[12][1] < y + height) or
                    (x < 2560 - landmarkList[16][0] < x + width and y < landmarkList[16][1] < y + height) or
                    (x < 2560 - landmarkList[20][0] < x + width and y < landmarkList[20][1] < y + height))


while True:
    # every iteration a new image is drawn
    success, img = cap.read()
    # detect the hands
    hands, img = detector.findHands(img)

    # Flip the image horizontally for display
    img = cv2.flip(img, 1)

    img = drawAllTransparent(img, buttons)

    if hands:
        hand1 = hands[0]
        landmarkList1 = hand1["lmList"]
        boundingBox1 = hand1["bbox"]
        if len(hands) == 2:
            hand2 = hands[1]
            landmarkList2 = hand2["lmList"]
            boundingBox2 = hand2["bbox"]

        # check if finger clicking a button
        for button in buttons:
            x, y = button.position
            width, height = button.size
            # landmarkList[8] is the index finger, 12 is the middle, etc.
            # see https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker
            if (isPressed(landmarkList1, button)) or (len(hands) == 2 and isPressed(landmarkList2, button)):
                # pressed buttons are colored green
                cv2.rectangle(img, button.position, (x + width, y + height), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x, y + 65), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)

                # play the sound of the pressed key
                sound = key_sounds.get(button.text)
                if sound:
                    sound.play()
                    print(f"{button.text} pressed")

    cv2.imshow("Image", img)
    cv2.waitKey(1)