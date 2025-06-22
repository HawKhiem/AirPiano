import cv2
import cvzone
import numpy as np
import os
from cvzone.HandTrackingModule import HandDetector
import pygame
import time
import threading

sound_folder = "wavPianoSounds"

# Initialize Pygame Mixer with increased buffer and channels
pygame.mixer.init(buffer=512)
pygame.mixer.set_num_channels(300)  # 60 keys * 5 channels per key

key_sounds = {}
key_channels = {}
key_channel_index = {}
channels_per_key = 5

keys = ["Eb1", "E1", "F1", "Gb1", "G1", "Ab1", "A1", "Bb1", "B1", "C2", "Db2", "D2",
        "Eb2", "E2", "F2", "Gb2", "G2", "Ab2", "A2", "Bb2", "B2", "C3", "Db3", "D3",
        "Eb3", "E3", "F3", "Gb3", "G3", "Ab3", "A3", "Bb3", "B3", "C4", "Db4", "D4",
        "Eb4", "E4", "F4", "Gb4", "G4", "Ab4", "A4", "Bb4", "B4", "C5", "Db5", "D5",
        "Eb5", "E5", "F5", "Gb5", "G5", "Ab5", "A5", "Bb5", "B5", "C6", "Db6", "D6"]

channel_counter = 0
for key in keys:
    path = os.path.join(sound_folder, f"{key}.wav")
    if os.path.exists(path):
        key_sounds[key] = pygame.mixer.Sound(path)
        key_channels[key] = [pygame.mixer.Channel(channel_counter + i) for i in range(channels_per_key)]
        key_channel_index[key] = 0
        channel_counter += channels_per_key
    else:
        print(f"Warning: Sound for key {key} not found at {path}")

cap = cv2.VideoCapture(0)
cap.set(3, 2560)
cap.set(4, 1440)

detector = HandDetector(detectionCon=0.8)

def drawAllTransparent(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.position
        width, height = button.size
        cvzone.cornerRect(imgNew, (x, y, width, height), 20, rt=0)
        if "b" in button.text:
            cv2.rectangle(imgNew, button.position, (x + width, y + height), (0, 0, 0), cv2.FILLED)
        else:
            cv2.rectangle(imgNew, button.position, (x + width, y + height), (255, 255, 255), cv2.FILLED)
        cv2.putText(imgNew, button.text, (x, y + 65), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out

class Button:
    def __init__(self, position, text, size=None):
        if size is None:
            size = [40, 200]
        self.position = position
        self.text = text
        self.size = size

buttons = []
for x, key in enumerate(keys):
    buttons.append(Button([42 * x + 20, 1240], key))

def isPressed(landmarkList, button):
    x, y = button.position
    width, height = button.size
    for i in [4, 8, 12, 16, 20]:
        px, py = landmarkList[i][0], landmarkList[i][1]
        if x < px < x + width and y < py < y + height:
            return True
    return False

pressed_keys = set()

# Thread-safe overlay frame storage
overlay_frame = None
overlay_lock = threading.Lock()

def overlay_video_thread(video_path):
    global overlay_frame
    video = cv2.VideoCapture(video_path)
    while True:
        ret, frame = video.read()
        if not ret:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        # Resize once here to target size to save main loop computation
        frame_resized = cv2.resize(frame, (2560, 1440))
        with overlay_lock:
            overlay_frame = frame_resized
        time.sleep(1/30)  # try for ~30 FPS (adjust based on video FPS)

# Start the overlay video thread
threading.Thread(target=overlay_video_thread, args=("piano_visualizer.mp4",), daemon=True).start()

start_time = time.time()

while True:
    success, img = cap.read()
    if not success:
        break

    # Flip horizontally for better user experience
    img = cv2.flip(img, 1)

    # Detect hands and draw buttons
    hands, img = detector.findHands(img)
    img = drawAllTransparent(img, buttons)

    if hands:
        hand1 = hands[0]
        landmarkList1 = hand1["lmList"]
        if len(hands) == 2:
            hand2 = hands[1]
            landmarkList2 = hand2["lmList"]
        else:
            landmarkList2 = None

        for button in buttons:
            key = button.text
            if (isPressed(landmarkList1, button)) or (landmarkList2 and isPressed(landmarkList2, button)):
                if key not in pressed_keys:
                    pressed_keys.add(key)
                    sound = key_sounds.get(key)
                    if sound:
                        channels = key_channels[key]
                        idx = key_channel_index[key]
                        ch = channels[idx]
                        ch.play(sound)
                        key_channel_index[key] = (idx + 1) % channels_per_key

                # Highlight pressed key in green with transparency
                imgNew = np.zeros_like(img, np.uint8)
                x, y = button.position
                width, height = button.size
                cv2.rectangle(imgNew, button.position, (x + width, y + height), (0, 255, 0), cv2.FILLED)
                cv2.putText(imgNew, key, (x, y + 65), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
                alpha = 0.5
                mask = imgNew.astype(bool)
                out = img.copy()
                out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
                img = out
            else:
                if key in pressed_keys:
                    pressed_keys.remove(key)

    # Get the latest overlay frame safely
    with overlay_lock:
        current_overlay = overlay_frame.copy() if overlay_frame is not None else None

    if current_overlay is not None:
        # Blend overlay with webcam image
        alpha = 0.6
        img = cv2.addWeighted(img, 1.0, current_overlay, alpha, 0)

    cv2.imshow("Air Piano with Overlay", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
