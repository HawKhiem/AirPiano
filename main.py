import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 2560)
cap.set(4, 1440)

# higher detectionCon to avoid randomly key pressed
detector = HandDetector(detectionCon=0.8)

# draw the button onto the image every iteration, since each iteration we have a new image
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.position
        width, height = button.size
        # button - position, size, color
        if "#" in button.text:
            cv2.rectangle(img, button.position, (x + width, y + height), (0, 0, 0), cv2.FILLED)
        else:
            cv2.rectangle(img, button.position, (x + width, y + height), (255, 255, 255), cv2.FILLED)
        # text
        cv2.putText(img, button.text, (x, y + 65), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
    return img

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
keys = ["A0", "A#0", "B0",
        "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1", "A1", "A#1", "B1",
        "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2",
        "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
        "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
        "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5",
        "C6", "C#6", "D6"]
# cool way in python to keep track of the index when iterate using enhanced for loop
for x, key in enumerate(keys):
    # size is none -> default size is used
    buttons.append(Button([38 * x + 19, 1240], key))


while True:
    # every iteration a new image is drawn
    success, img = cap.read()
    # detect the hands
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        landmarkList = hand["lmList"]
        boundingBox = hand["bbox"]

    # Flip the image horizontally for display
    img = cv2.flip(img, 1)

    img = drawAll(img, buttons)

    cv2.imshow("Image", img)
    cv2.waitKey(1)