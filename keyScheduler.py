import cv2
import numpy as np
import time
import sys

# Define keys
keys = ["Eb1", "E1", "F1", "Gb1", "G1", "Ab1", "A1", "Bb1", "B1", "C2", "Db2", "D2",
        "Eb2", "E2", "F2", "Gb2", "G2", "Ab2", "A2", "Bb2", "B2", "C3", "Db3", "D3",
        "Eb3", "E3", "F3", "Gb3", "G3", "Ab3", "A3", "Bb3", "B3", "C4", "Db4", "D4",
        "Eb4", "E4", "F4", "Gb4", "G4", "Ab4", "A4", "Bb4", "B4", "C5", "Db5", "D5",
        "Eb5", "E5", "F5", "Gb5", "G5", "Ab5", "A5", "Bb5", "B5", "C6", "Db6", "D6"]

# Note class
class VisualNote:
    def __init__(self, key, start_time, duration):
        self.key = key
        self.start_time = start_time
        self.duration = duration

# Scheduled notes
note_schedule = [
    VisualNote("Db2", 7.5, 1.5),
    VisualNote("Db3", 7.5, 1.5),
    VisualNote("Ab3", 7.5, 1.5),
    VisualNote("Db4", 7.5, 1.5),

    VisualNote("Ab1", 10, 1.5),
    VisualNote("Ab2", 10, 1.5),
    VisualNote("B2", 10, 1.5),
    VisualNote("Eb3", 10, 1.5),
    VisualNote("Ab3", 10, 1.5),

    VisualNote("B1", 12.5, 1.5),
    VisualNote("B2", 12.5, 1.5),
    VisualNote("Gb3", 12.5, 1.5),
    VisualNote("Ab3", 12.5, 1.5),
    VisualNote("B3", 12.5, 1.5),

    VisualNote("Ab1", 15, 1.5),
    VisualNote("Ab2", 15, 1.5),
    VisualNote("Db3", 15, 1.5),
    VisualNote("Eb3", 15, 1.5),
    VisualNote("Ab3", 15, 1.5),

    VisualNote("Eb2", 17.2, 1.57),
    VisualNote("Eb3", 17.2, 1.4),
    VisualNote("E3", 17.2, 0.8),
    VisualNote("Bb3", 17.2, 1.2),
    VisualNote("Eb4", 17.2, 1.2),
    VisualNote("E3", 18.4, 1.5),

    VisualNote("Bb1", 19.5, 1.3),
    VisualNote("Bb2", 19.6, 1.3),
    VisualNote("B2", 19.6, 1.2),
    VisualNote("Gb3", 19.6, 1.3),
    VisualNote("F3", 19, 0.3),
    VisualNote("Ab3", 19.3, 0.1),
    VisualNote("G3", 19.4, 0.3),
    VisualNote("Bb3", 19.6, 1.4),

    VisualNote("B1", 21.8, 1.7),
    VisualNote("B2", 21.8, 1.5),
    VisualNote("Gb3", 21.8, 1.3),
    VisualNote("Ab3", 21.8, 0.8),
    VisualNote("B3", 21.8, 1.3),
    VisualNote("Ab3", 23, 0.3),

    VisualNote("G3", 23.5, 0.3),
    VisualNote("Bb3", 23.8, 0.2),
    VisualNote("A3", 23.85, 0.1),

    VisualNote("Ab1", 24.1, 1.63),
    VisualNote("Ab2", 24.2, 1.56),
    VisualNote("Eb3", 24.16, 2.17),
    VisualNote("Ab3", 24.16, 2.31),
    VisualNote("Db4", 24.16, 2.31),
]

# Define button class (keys)
class Button:
    def __init__(self, position, text, size=(40, 200)):
        self.position = position
        self.text = text
        self.size = size

buttons = [Button([42 * i + 20, 1240], key) for i, key in enumerate(keys)]

# Initialize video writer
frame_width, frame_height = 2560, 1440
fps = 30
duration = 30  # seconds, adjust as needed
output_path = "piano_visualizer.mp4"
out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

total_frames = int(duration * fps)
bar_length = 40  # length of the progress bar

# Render each frame
start_time = time.time()
for frame_idx in range(total_frames):
    current_time = frame_idx / fps
    img = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

    # Draw keys
    for button in buttons:
        x, y = button.position
        w, h = button.size
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
        cv2.putText(img, button.text, (x + 5, y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Draw falling notes
    for note in note_schedule:
        time_to_note = note.start_time - current_time
        if time_to_note < -note.duration:
            continue

        pixels_per_second = 200
        y_offset = int(time_to_note * pixels_per_second)
        height = int(note.duration * pixels_per_second)

        button = next((b for b in buttons if b.text == note.key), None)
        if button:
            x, y = button.position
            w, _ = button.size
            top_left = (x, y - height - y_offset)
            bottom_right = (x + w, y - y_offset)
            overlay = img.copy()
            cv2.rectangle(overlay, top_left, bottom_right, (255, 0, 0), -1)
            alpha = 0.6
            cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

    out.write(img)

    # ---- Progress Bar Output ----
    progress = (frame_idx + 1) / total_frames
    block = int(round(bar_length * progress))
    text = f"\rRendering Video: [{'#' * block + '-' * (bar_length - block)}] {progress*100:.1f}%"
    sys.stdout.write(text)
    sys.stdout.flush()

# Final message
print("\n✅ Video rendering complete.")

# Cleanup
out.release()
print(f"Video saved to {output_path}")
