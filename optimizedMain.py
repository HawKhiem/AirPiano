import cv2
import cvzone
import numpy as np
import os
from cvzone.HandTrackingModule import HandDetector
import pygame
import time
import threading
from collections import deque
from queue import Queue

# ---- Init Pygame Sound System ----
pygame.mixer.init(buffer=512)
pygame.mixer.set_num_channels(300)

SOUND_FOLDER = "wavPianoSounds"
CHANNELS_PER_KEY = 5
VIDEO_OVERLAY_PATH = "piano_visualizer.mp4"

keys = ["Eb1", "E1", "F1", "Gb1", "G1", "Ab1", "A1", "Bb1", "B1", "C2", "Db2", "D2",
        "Eb2", "E2", "F2", "Gb2", "G2", "Ab2", "A2", "Bb2", "B2", "C3", "Db3", "D3",
        "Eb3", "E3", "F3", "Gb3", "G3", "Ab3", "A3", "Bb3", "B3", "C4", "Db4", "D4",
        "Eb4", "E4", "F4", "Gb4", "G4", "Ab4", "A4", "Bb4", "B4", "C5", "Db5", "D5",
        "Eb5", "E5", "F5", "Gb5", "G5", "Ab5", "A5", "Bb5", "B5", "C6", "Db6", "D6"]

# ---- Load Sounds ----
key_sounds, key_channels, key_channel_index = {}, {}, {}
channel_counter = 0
for key in keys:
    path = os.path.join(SOUND_FOLDER, f"{key}.wav")
    if os.path.exists(path):
        key_sounds[key] = pygame.mixer.Sound(path)
        key_channels[key] = [pygame.mixer.Channel(channel_counter + i) for i in range(CHANNELS_PER_KEY)]
        key_channel_index[key] = 0
        channel_counter += CHANNELS_PER_KEY
    else:
        print(f"Warning: {key} sound not found.")

# ---- Webcam & Hand Detector ----
cap = cv2.VideoCapture(0)
cap.set(3, 2560)
cap.set(4, 1440)
detector = HandDetector(detectionCon=0.8)

# ---- Piano UI Setup ----
class Button:
    def __init__(self, pos, text, size=(40, 200)):
        self.position = pos
        self.text = text
        self.size = size

buttons = [Button([42 * i + 20, 1240], key) for i, key in enumerate(keys)]
pressed_keys = set()

# ---- Helpers ----
def draw_transparent_overlay(img, overlays):
    img_new = np.zeros_like(img, np.uint8)
    for overlay in overlays:
        overlay(img_new)
    out = img.copy()
    mask = img_new.astype(bool)
    out[mask] = cv2.addWeighted(img, 0.5, img_new, 0.5, 0)[mask]
    return out

def is_pressed(landmarks, button):
    x, y, w, h = *button.position, *button.size
    return any(x < lm[0] < x + w and y < lm[1] < y + h for i, lm in enumerate(landmarks) if i in [4, 8, 12, 16, 20])

# ---- Decouple Sound Playback via Queue (Optional) ----
note_queue = Queue()

def sound_player_thread():
    while True:
        key = note_queue.get()
        if key in key_sounds:
            idx = key_channel_index[key]
            key_channels[key][idx].play(key_sounds[key])
            key_channel_index[key] = (idx + 1) % CHANNELS_PER_KEY
        note_queue.task_done()

threading.Thread(target=sound_player_thread, daemon=True).start()

# ---- Multithreaded Overlay Video ----
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
        frame = cv2.resize(frame, (2560, 1440))
        with overlay_lock:
            overlay_frame = frame
        time.sleep(1 / 90)  # ~30 FPS for visualizer

threading.Thread(target=overlay_video_thread, args=(VIDEO_OVERLAY_PATH,), daemon=True).start()

# ---- Multithreaded Hand Detection ----
frame_queue = deque(maxlen=1)     # Only keep the most recent frame
hand_data = {}
hand_lock = threading.Lock()

def hand_detection_thread():
    while True:
        if frame_queue:
            frame = frame_queue[-1]
            hands, img_with_hands = detector.findHands(frame, draw=True)
            with hand_lock:
                hand_data["hands"] = hands
                hand_data["img_with_hands"] = img_with_hands
        time.sleep(0.01)

threading.Thread(target=hand_detection_thread, daemon=True).start()

# ---- Main Rendering Loop ----
while True:
    success, img = cap.read()
    if not success:
        break
    img = cv2.flip(img, 1)

    # Push latest frame into queue for background hand detection
    frame_queue.append(img.copy())

    # Get detected hands from shared object
    with hand_lock:
        hands = hand_data.get("hands", [])
        img = hand_data.get("img_with_hands", img)  # Fallback to original if not ready
    # Draw piano buttons
    img = draw_transparent_overlay(img, [
        lambda im, b=b: (
            cvzone.cornerRect(im, (*b.position, *b.size), 20, rt=0),
            cv2.rectangle(im, b.position, (b.position[0]+b.size[0], b.position[1]+b.size[1]),
                          (0, 0, 0) if 'b' in b.text else (255, 255, 255), cv2.FILLED),
            cv2.putText(im, b.text, (b.position[0], b.position[1] + 65),
                        cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
        ) for b in buttons
    ])

    # Check key presses using shared hand detection data
    for button in buttons:
        key = button.text
        active = False
        for hand in hands:
            if is_pressed(hand["lmList"], button):
                active = True
                if key not in pressed_keys:
                    pressed_keys.add(key)
                    note_queue.put(key)  # Use the sound thread
                break
        if active:
            img = draw_transparent_overlay(img, [
                lambda im: (
                    cv2.rectangle(im, button.position,
                                  (button.position[0]+button.size[0], button.position[1]+button.size[1]),
                                  (0, 255, 0), cv2.FILLED),
                    cv2.putText(im, key, (button.position[0], button.position[1] + 65),
                                cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
                )
            ])
        elif key in pressed_keys:
            pressed_keys.remove(key)

    # Blend overlay video frame
    with overlay_lock:
        current_overlay = overlay_frame.copy() if overlay_frame is not None else None

    if current_overlay is not None:
        alpha = 0.6
        img = cv2.addWeighted(img, 1.0, current_overlay, alpha, 0)

    # Display final result
    cv2.imshow("Air Piano 🎹", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
