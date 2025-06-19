import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 2560)
cap.set(4, 1440)

# higher detectionCon to avoid randomly key pressed
detector = HandDetector(detectionCon=0.8)

# TODO: We need 27 blacks and 39 white buttons
class Button:
    # similar to java constructor
    def __init__(self, position, text, size=None):
        if size is None:
            size = [100, 100]
        self.position = position
        self.text = text
        self.size = size

    def draw(self, img):
        x, y = self.position
        width, height = self.size
        # button - position, size, color
        cv2.rectangle(img, self.position, (x + width, y + height), (255, 0, 255), cv2.FILLED)
        # text
        cv2.putText(img, self.text, (x + 20, y + 50), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
        return img

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

    # size is none -> default size is used
    button = Button([100, 100], "Q")
    # draw the button onto the image every iteration, since each iteration we have a new image
    button.draw(img)

    cv2.imshow("Image", img)
    cv2.waitKey(1)