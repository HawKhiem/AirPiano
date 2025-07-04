import cv2
import cvzone
import numpy as np
import os
import pygame
import time
import threading
from cvzone.HandTrackingModule import HandDetector

# ========== Config ========== #
CAM_WIDTH, CAM_HEIGHT = 2560, 1440
SOUND_FOLDER = "wavPianoSounds"
CHANNELS_PER_KEY = 5
DETECTION_CONFIDENCE = 0.8

# ========== Sound Setup ========== #
pygame.mixer.init(buffer=512)
pygame.mixer.set_num_channels(300)

keys = ["Eb1", "E1", "F1", "Gb1", "G1", "Ab1", "A1", "Bb1", "B1", "C2", "Db2", "D2",
        "Eb2", "E2", "F2", "Gb2", "G2", "Ab2", "A2", "Bb2", "B2", "C3", "Db3", "D3",
        "Eb3", "E3", "F3", "Gb3", "G3", "Ab3", "A3", "Bb3", "B3", "C4", "Db4", "D4",
        "Eb4", "E4", "F4", "Gb4", "G4", "Ab4", "A4", "Bb4", "B4", "C5", "Db5", "D5",
        "Eb5", "E5", "F5", "Gb5", "G5", "Ab5", "A5", "Bb5", "B5", "C6", "Db6", "D6"]

key_sounds = {}
key_channels = {}
key_channel_index = {}
channel_counter = 0

for key in keys:
    path = os.path.join(SOUND_FOLDER, f"{key}.wav")
    if os.path.exists(path):
        key_sounds[key] = pygame.mixer.Sound(path)
        key_channels[key] = [pygame.mixer.Channel(channel_counter + i) for i in range(CHANNELS_PER_KEY)]
        key_channel_index[key] = 0
        channel_counter += CHANNELS_PER_KEY
    else:
        print(f"Warning: Missing sound: {key}")

# ========== Video Stream Class ========== #
class VideoStream:
    def __init__(self, path, width, height):
        self.cap = cv2.VideoCapture(path)
        self.width = width
        self.height = height
        self.frame = None
        self.stopped = False
        self.lock = threading.Lock()

        # Get video FPS
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.delay = 1.0 / self.fps if self.fps > 0 else 1.0 / 30  # fallback

    def start(self):
        threading.Thread(target=self.update, daemon=True).start()
        return self

    def update(self):
        while not self.stopped:
            start_time = time.time()
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (self.width, self.height))
                with self.lock:
                    self.frame = frame

            # Throttle to video FPS
            elapsed = time.time() - start_time
            time_to_wait = self.delay - elapsed
            if time_to_wait > 0:
                time.sleep(time_to_wait)

    def read(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        self.stopped = True
        self.cap.release()


# ========== Button Class ========== #
class Button:
    def __init__(self, position, text, size=None):
        self.position = position
        self.text = text
        self.size = size if size else [40, 200]

def draw_buttons(img, button_list):
    imgNew = np.zeros_like(img, np.uint8)
    for button in button_list:
        x, y = button.position
        w, h = button.size
        color = (0, 0, 0) if "b" in button.text else (255, 255, 255)
        cvzone.cornerRect(imgNew, (x, y, w, h), 20, rt=0)
        cv2.rectangle(imgNew, (x, y), (x + w, y + h), color, cv2.FILLED)
        cv2.putText(imgNew, button.text, (x, y + 65), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
    mask = imgNew.astype(bool)
    img[mask] = cv2.addWeighted(img, 0.5, imgNew, 0.5, 0)[mask]
    return img

def is_pressed(landmarks, button):
    x, y = button.position
    w, h = button.size
    for i in [4, 8, 12, 16, 20]:
        px, py = CAM_WIDTH - landmarks[i][0], landmarks[i][1]
        if x < 2560 - px < x + w and y < py < y + h:
            return True
    return False

# ========== Threaded Hand Tracking ========== #
class HandTrackingThread(threading.Thread):
    def __init__(self, cap, buttons, detector):
        super().__init__(daemon=True)
        self.cap = cap
        self.buttons = buttons
        self.detector = detector
        self.pressed_keys = set()
        self.running = True
        self.lock = threading.Lock()
        self.latest_landmarks = []  # Store landmarks for drawing

    def run(self):
        while self.running:
            success, frame = self.cap.read()
            if not success:
                continue
            frame = cv2.flip(frame, 1)
            hands, _ = self.detector.findHands(frame)

            current_pressed = set()
            if hands:
                lms1 = hands[0]["lmList"]
                lms2 = hands[1]["lmList"] if len(hands) == 2 else []

                for button in self.buttons:
                    if is_pressed(lms1, button) or (lms2 and is_pressed(lms2, button)):
                        current_pressed.add(button.text)

            with self.lock:
                self.pressed_keys = current_pressed
                self.latest_landmarks = [hand["lmList"] for hand in hands] if hands else []

    def get_pressed_keys(self):
        with self.lock:
            return self.pressed_keys.copy()

    def get_landmarks(self):
        with self.lock:
            return self.latest_landmarks.copy()

    def stop(self):
        self.running = False


# ========== Main Program ========== #
def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, CAM_WIDTH)
    cap.set(4, CAM_HEIGHT)

    detector = HandDetector(detectionCon=DETECTION_CONFIDENCE)
    buttons = [Button([42 * x + 20, 1240], key) for x, key in enumerate(keys)]
    video_stream = VideoStream("piano_visualizer.mp4", CAM_WIDTH, CAM_HEIGHT).start()
    hand_thread = HandTrackingThread(cap, buttons, detector)
    hand_thread.start()

    prev_time = time.time()
    played_keys = set()

    while True:
        ret, img = cap.read()
        if not ret:
            continue
        img = cv2.flip(img, 1)
        img = draw_buttons(img, buttons)

        # Get pressed keys and landmarks from thread
        pressed_keys = hand_thread.get_pressed_keys()
        landmarks_list = hand_thread.get_landmarks()

        # Handle sound + key highlighting
        for button in buttons:
            key = button.text
            x, y = button.position
            w, h = button.size

            if key in pressed_keys:
                if key not in played_keys:
                    sound = key_sounds.get(key)
                    if sound:
                        idx = key_channel_index[key]
                        key_channels[key][idx].play(sound)
                        key_channel_index[key] = (idx + 1) % CHANNELS_PER_KEY
                    played_keys.add(key)

                # Highlight
                overlay = np.zeros_like(img, np.uint8)
                cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
                mask = overlay.astype(bool)
                img[mask] = cv2.addWeighted(img, 0.5, overlay, 0.5, 0)[mask]
            else:
                played_keys.discard(key)

        # Draw fingertip landmarks from detected hands
        for landmarks in landmarks_list:
            for tip_id in [4, 8, 12, 16, 20]:
                x, y = landmarks[tip_id][:2]  # Unpack only x and y
                cv2.circle(img, (x, y), 10, (0, 0, 255), cv2.FILLED)

        # Overlay piano video
        video_frame = video_stream.read()
        if video_frame is not None:
            img = cv2.addWeighted(img, 1.0, video_frame, 0.6, 0)

        # FPS
        now = time.time()
        fps = 1 / (now - prev_time)
        prev_time = now
        cv2.putText(img, f"FPS: {fps:.2f}", (30, 80), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        cv2.imshow("Virtual Piano", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup
    hand_thread.stop()
    video_stream.stop()
    cap.release()
    cv2.destroyAllWindows()

# ========== Run ========== #
if __name__ == "__main__":
    main()
