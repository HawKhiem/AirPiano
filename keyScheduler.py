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
    VisualNote("E3", 7.5, 1.5),
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

    VisualNote("Ab1", 26.43, 1.5),
    VisualNote("Ab2", 26.43, 1.5),

    VisualNote("Gb3", 26.43, 0.17),
    VisualNote("Gb3", 27.53, 0.17),
    VisualNote("Gb3", 27.8, 0.17),
    VisualNote("Gb3", 28.07, 0.17),
    VisualNote("Gb3", 28.33, 0.17),

    VisualNote("B1", 28.63, 1.74),
    VisualNote("B2", 28.63, 1.44),
    VisualNote("Eb3", 29.4, 0.17),
    VisualNote("Eb3", 29.7, 0.43),
    VisualNote("Gb3", 28.63, 0.3),
    VisualNote("Gb3", 29.13, 0.17),
    VisualNote("B3", 28.87, 0.36),
    VisualNote("B3", 29.4, 0.17),
    VisualNote("B3", 29.7, 0.83),
    VisualNote("Db4", 28.63, 0.27),
    VisualNote("Db4", 29.13, 0.17),
    VisualNote("Eb4", 28.87, 0.2),

    VisualNote("E1", 30.77, 1.3),
    VisualNote("E2", 30.77, 1.3),
    VisualNote("E3", 30.46, 0.97),
    VisualNote("Ab3", 30.46, 1.07),

    VisualNote("Gb3", 32.2, 0.1),
    VisualNote("Gb3", 32.5, 0.1),
    VisualNote("Gb3", 32.77, 0.1),

    VisualNote("Gb1", 33.03, 0.27),
    VisualNote("Gb2", 33.03, 0.27),
    VisualNote("Db4", 33.03, 0.27),

    VisualNote("Gb1", 33.8, 0.1),
    VisualNote("Db4", 33.57, 0.23),
    VisualNote("Eb4", 33.3, 0.4),

    VisualNote("Eb1", 34.1, 0.37),
    VisualNote("Eb2", 34.1, 0.47),
    VisualNote("B3", 34.1, 0.57),

    VisualNote("Db4", 34.87, 0.13),
    VisualNote("D4", 35, 0.2),

    VisualNote("Ab1", 35.17, 1.43),
    VisualNote("Ab2", 35.17, 1.5),
    VisualNote("Ab3", 35.17, 1.1),
    VisualNote("Eb4", 35.17, 1.06),

    VisualNote("Gb3", 36.5, 0.13),
    VisualNote("Gb3", 36.77, 0.16),

    VisualNote("B1", 37.3, 1.6),
    VisualNote("B2", 37.3, 1.47),
    VisualNote("Eb3", 38.1, 0.13),
    VisualNote("Eb3", 38.37, 0.4),
    VisualNote("Gb3", 37.3, 0.33),
    VisualNote("Gb3", 37.83, 0.17),
    VisualNote("B3", 37.57, 0.36),
    VisualNote("B3", 38.1, 0.13),
    VisualNote("B3", 38.37, 0.8),
    VisualNote("Db4", 37.3, 0.6),
    VisualNote("Db4", 37.83, 0.1),
    VisualNote("Eb4", 37.57, 0.2),

    VisualNote("E1", 39.47, 1.63),
    VisualNote("E1", 41.63, 1.37),
    VisualNote("E2", 39.47, 1.63),
    VisualNote("E2", 41.63, 1.37),
    VisualNote("E3", 39.13, 2.8),
    VisualNote("Gb3", 39.13, 2.6),
    VisualNote("Ab3", 39.13, 2.87),

    VisualNote("E3", 42.63, 0.17),
    VisualNote("G3", 42.9, 0.13),
    VisualNote("Ab3", 42.63, 0.27),
    VisualNote("Bb3", 42.9, 0.2),
    VisualNote("Db4", 42.63, 0.3),
    VisualNote("D4", 42.9, 0.2),

    VisualNote("Ab1", 43.77, 1.63),
    VisualNote("Ab2", 43.77, 1.63),
    VisualNote("Ab3", 43.77, 1.1),
    VisualNote("B3", 43.77, 1.1),
    VisualNote("Eb4", 43.77, 1.1),

    VisualNote("B1", 45.9, 1.47),
    VisualNote("B2", 45.9, 1.33),
    VisualNote("Gb3", 45.37, 0.13),
    VisualNote("Gb3", 45.63, 0.37),
    VisualNote("B3", 46.73, 0.1),
    VisualNote("B3", 47, 0.83),
    VisualNote("Db4", 45.9, 0.37),
    VisualNote("Db4", 46.47, 0.33),
    VisualNote("Eb4", 46.2, 0.4),

    VisualNote("E1", 48.1, 1.7),
    VisualNote("E2", 48.1, 1.7),
    VisualNote("Ab3", 47.77, 1.15),

    VisualNote("Gb3", 49.5, 0.1),
    VisualNote("Gb3", 49.8, 0.1),
    VisualNote("Gb3", 50.03, 0.4),

    VisualNote("Gb1", 50.3, 0.57),
    VisualNote("Gb2", 50.3, 0.43),
    VisualNote("Db4", 50.3, 0.37),

    VisualNote("B3", 51.07, 0.1),
    VisualNote("Db4", 50.83, 0.27),
    VisualNote("Eb4", 50.57, 0.43),

    VisualNote("Eb1", 51.37, 0.4),
    VisualNote("Eb2", 51.37, 0.43),
    VisualNote("B3", 51.37, 0.53),

    VisualNote("Db4", 52.17, 0.13),
    VisualNote("D4", 52.23, 0.2),

    VisualNote("Ab1", 52.43, 1.34),
    VisualNote("Ab2", 52.43, 1.44),
    VisualNote("Gb3", 53.2, 0.33),
    VisualNote("Gb3", 53.77, 0.17),
    VisualNote("Gb3", 54.07, 0.37),
    VisualNote("Ab3", 52.43, 0.97),
    VisualNote("B3", 53.5, 0.27),
    VisualNote("Eb4", 52.43, 1.1),

    VisualNote("B1", 54.6, 1.4),
    VisualNote("B2", 54.6, 1.3),
    VisualNote("B3", 55.4, 0.1),
    VisualNote("B3", 55.7, 0.37),
    VisualNote("Db4", 54.6, 0.33),
    VisualNote("Db4", 55.17, 0.27),
    VisualNote("Eb4", 54.87, 0.43),

    VisualNote("E1", 56.8, 3.37),
    VisualNote("E2", 56.8, 3.5),
    VisualNote("Gb3", 56.5, 0.43),
    VisualNote("Gb3", 58.47, 0.1),
    VisualNote("Ab3", 56.23, 0.3),
    VisualNote("Ab3", 56.8, 0.57),
    VisualNote("Ab3", 57.9, 0.63),
    VisualNote("Ab3", 59.07, 0.2),
    VisualNote("B3", 57.37, 0.63),
    VisualNote("B3", 60.57, 0.3),
    VisualNote("Db4", 60.3, 0.23),
    VisualNote("Db4", 60.8, 0.1),
    VisualNote("Eb4", 60.03, 0.3),
    VisualNote("E4", 59.93, 0.2),
    VisualNote("F4", 59.83, 0.2),
    VisualNote("Gb4", 59.53, 0.23),

    VisualNote("Db2", 61.1, 1.2),
    VisualNote("Db3", 61.1, 1.2),
    VisualNote("Ab3", 61.37, 0.33),
    VisualNote("Ab3", 62.17, 0.7),
    VisualNote("B3", 61.63, 0.6),
    VisualNote("Db4", 61.1, 0.6),

    VisualNote("Eb2", 62.73, 0.23),
    VisualNote("Eb3", 62.73, 0.13),
    VisualNote("B3", 62.73, 0.47),

    VisualNote("Ab1", 63.27, 0.2),
    VisualNote("Ab1", 63.8, 1.1),
    VisualNote("Ab2", 63.27, 0.2),
    VisualNote("Ab2", 63.8, 1.1),
    VisualNote("Ab3", 63.53, 0.37),
    VisualNote("B3", 63.8, 0.27),
    VisualNote("B3", 64.87, 0.33),
    VisualNote("Db4", 63.03, 0.2),
    VisualNote("Db4", 64.6, 0.33),
    VisualNote("Db4", 65.13, 0.1),
    VisualNote("D4", 63.13, 0.2),
    VisualNote("D4", 64.3, 0.1),
    VisualNote("Eb4", 63.27, 0.6),
    VisualNote("Eb4", 64.37, 0.37),

    VisualNote("B1", 65.4, 1.43),
    VisualNote("B2", 65.4, 1.3),
    VisualNote("Ab3", 65.67, 0.4),
    VisualNote("Ab3", 66.5, 0.17),
    VisualNote("B3", 66, 0.57),
    VisualNote("Db4", 65.4, 0.67),

    VisualNote("Gb1", 67.6, 0.17),
    VisualNote("Gb1", 68.17, 1.13),
    VisualNote("Gb2", 67.6, 0.17),
    VisualNote("Gb2", 68.17, 1.13),
    VisualNote("Ab3", 67.87, 0.43),
    VisualNote("B3", 67.07, 0.33),
    VisualNote("B3", 68.17, 0.27),
    VisualNote("B3", 69.23, 0.33),
    VisualNote("Db4", 67.33, 0.2),
    VisualNote("Db4", 68.93, 0.37),
    VisualNote("Db4", 69.5, 0.1),
    VisualNote("D4", 67.43, 0.27),
    VisualNote("D4", 68.67, 0.1),
    VisualNote("Eb4", 67.6, 0.63),
    VisualNote("Eb4", 68.73, 0.37),

    VisualNote("Db2", 69.77, 1.16),
    VisualNote("Db3", 69.77, 1.23),
    VisualNote("Ab3", 70.03, 0.37),
    VisualNote("Ab3", 70.87, 0.13),
    VisualNote("B3", 70.33, 0.67),
    VisualNote("Db4", 69.77, 1.16),

    VisualNote("Ab1", 71.93, 0.17),
    VisualNote("Ab1", 72.47, 1),
    VisualNote("Eb2", 71.4, 0.17),
    VisualNote("Ab2", 71.93, 0.13),
    VisualNote("Ab2", 72.47, 1),
    VisualNote("Eb3", 71.4, 0.1),
    VisualNote("Ab3", 72.17, 0.4),
    VisualNote("B3", 71.4, 0.37),
    VisualNote("B3", 72.47, 0.2),
    VisualNote("B3", 73.5, 0.33),
    VisualNote("Db4", 71.67, 0.2),
    VisualNote("Db4", 73.23, 0.3),
    VisualNote("Db4", 73.77, 0.1),
    VisualNote("D4", 71.77, 0.27),
    VisualNote("Eb4", 71.93, 0.64),
    VisualNote("Eb4", 73, 0.4),

    VisualNote("B1", 74.03, 0.17),
    VisualNote("B1", 74.57, 1.07),
    VisualNote("B2", 74.03, 0.17),
    VisualNote("B2", 74.57, 1.07),
    VisualNote("Ab3", 74.27, 0.4),
    VisualNote("B3", 74.57, 1.8),
    VisualNote("Db4", 74.03, 0.63),

    VisualNote("Gb1", 76.3, 0.3),
    VisualNote("Gb1", 76.87, 0.1),
    VisualNote("Ab1", 78.6, 1.7),
    VisualNote("Bb1", 77.47, 0.2),
    VisualNote("F2", 78, 0.3),
    VisualNote("Gb2", 76.3, 0.3),
    VisualNote("Gb2", 76.87, 0.13),
    VisualNote("Gb2", 78.3, 0.1),
    VisualNote("G2", 78.3, 0.1),
    VisualNote("Ab2", 78.6, 1.7),
    VisualNote("Bb2", 77.47, 0.1),
    VisualNote("Gb3", 79.37, 0.33),
    VisualNote("Ab3", 79.13, 0.33),
    VisualNote("Ab3", 79.67, 0.1),
    VisualNote("Ab3", 80.2, 0.1),
    VisualNote("Bb3", 76.37, 2.53),

    VisualNote("B1", 80.77, 1.56),
    VisualNote("B2", 80.77, 1.46),
    VisualNote("Eb3", 81.57, 0.1),
    VisualNote("Eb3", 81.83, 0.4),
    VisualNote("Gb3", 80.77, 0.33),
    VisualNote("Gb3", 81.3, 0.1),
    VisualNote("B3", 81.03, 0.33),
    VisualNote("B3", 81.57, 0.1),
    VisualNote("B3", 81.83, 0.9),
    VisualNote("Db4", 80.77, 0.3),
    VisualNote("Db4", 81.3, 0.1),
    VisualNote("Eb4", 81.03, 0.2),

    VisualNote("E1", 83, 1.57),
    VisualNote("E2", 83, 1.57),
    VisualNote("E3", 82.67, 0.73),
    VisualNote("Gb3", 83.3, 0.3),
    VisualNote("Gb3", 83.8, 0.4),
    VisualNote("Ab3", 82.67, 0.63),
    VisualNote("Ab3", 83.53, 0.33),
    VisualNote("Ab3", 84.1, 0.17),
    VisualNote("Ab3", 84.37, 0.17),
    VisualNote("Ab3", 84.63, 0.2),

    VisualNote("Eb1", 86.3, 0.5),
    VisualNote("Gb1", 85.2, 0.57),
    VisualNote("Eb2", 86.3, 0.57),
    VisualNote("Gb2", 85.2, 0.5),
    VisualNote("B3", 86, 0.1),
    VisualNote("B3", 86.3, 0.5),
    VisualNote("Db4", 85.2, 0.33),
    VisualNote("Db4", 85.7, 0.3),
    VisualNote("Eb4", 85.47, 0.43),

    VisualNote("Ab1", 87.4, 1.7),
    VisualNote("Ab2", 87.4, 1.7),
    VisualNote("Gb3", 88.23, 0.17),
    VisualNote("Gb3", 89.1, 0.13),
    VisualNote("Gb3", 89.37, 0.37),
    VisualNote("Ab3", 87.43, 0.33),
    VisualNote("Ab3", 88, 0.27),
    VisualNote("Ab3", 88.57, 0.17),
    VisualNote("Db4", 87.1, 0.2),
    VisualNote("D4", 87.2, 0.27),
    VisualNote("Eb4", 87.43, 0.4),

    VisualNote("B1", 89.67, 1.43),
    VisualNote("B2", 89.67, 1.3),
    VisualNote("Ab3", 91.3, 0.63),
    VisualNote("B3", 90.47, 0.1),
    VisualNote("B3", 90.73, 0.6),
    VisualNote("Db4", 89.67, 0.33),
    VisualNote("Db4", 90.2, 0.33),
    VisualNote("Eb4", 89.93, 0.5),

    VisualNote("E1", 91.83, 3.4),
    VisualNote("E2", 91.83, 3.54),
    VisualNote("Eb4", 91.83, 0.5),
    VisualNote("Db5", 93.23, 0.2),
    VisualNote("Db5", 93.53, 0.17),
    VisualNote("Db5", 93.8, 0.17),
    VisualNote("Db5", 94.07, 1),
    VisualNote("Db6", 93.23, 0.2),
    VisualNote("Db6", 93.53, 0.17),
    VisualNote("Db6", 93.8, 0.17),
    VisualNote("Db6", 94.07, 0.93),

    VisualNote("Ab1", 96.37, 1.27),
    VisualNote("Ab2", 96.37, 1.3),
    VisualNote("Gb3", 96.63, 0.37),
    VisualNote("Gb3", 97.2, 0.43),
    VisualNote("Ab3", 96.37, 0.37),
    VisualNote("Ab3", 96.93, 0.3),
    VisualNote("Ab3", 97.5, 0.73),
    VisualNote("B3", 96.37, 1.27),
    VisualNote("Eb4", 96.37, 1.3),

    VisualNote("B1", 98.57, 1.43),
    VisualNote("B2", 98.57, 1.27),
    VisualNote("B3", 99.33, 0.13),
    VisualNote("B3", 99.63, 0.33),
    VisualNote("Db4", 98.57, 0.3),
    VisualNote("Db4", 99.1, 0.3),
    VisualNote("Eb4", 98.8, 0.5),
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
duration = 100  # seconds, adjust as needed
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
