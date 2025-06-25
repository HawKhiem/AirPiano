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
# TODO: Check name and time of keys in the first 9 blocks
note_schedule = [
    VisualNote("Db2", 7.43, 1.7),
    VisualNote("Db3", 7.43, 1.7),
    VisualNote("E3", 7.43, 1.7),
    VisualNote("Ab3", 7.43, 1.7),
    VisualNote("Db4", 7.43, 1.7),

    VisualNote("Ab1", 9.93, 1.73),
    VisualNote("Ab2", 9.93, 1.73),
    VisualNote("B2", 9.93, 1.73),
    VisualNote("Eb3", 9.93, 1.73),
    VisualNote("Ab3", 9.93, 1.73),

    VisualNote("B1", 12.43, 1.5),
    VisualNote("B2", 12.43, 1.5),
    VisualNote("Gb3", 12.43, 1.5),
    VisualNote("Ab3", 12.43, 1.5),
    VisualNote("B3", 12.43, 1.5),

    VisualNote("Gb1", 14.87, 1.47),
    VisualNote("Gb2", 14.87, 1.47),
    VisualNote("Bb2", 14.87, 1.47),
    VisualNote("Db3", 14.87, 1.47),
    VisualNote("Gb3", 14.87, 1.47),

    VisualNote("Db2", 17.23, 1.57),
    VisualNote("Db3", 17.23, 1.4),
    VisualNote("E3", 17.23, 0.8),
    VisualNote("Ab3", 17.23, 1.2),
    VisualNote("Db4", 17.23, 1.2),
    VisualNote("E3", 18.4, 1.5),

    VisualNote("Ab1", 19.5, 1.3),
    VisualNote("Ab2", 19.6, 1.3),
    VisualNote("B2", 19.6, 1.2),
    VisualNote("Eb3", 19.6, 1.3),
    VisualNote("F3", 18.93, 0.3),
    VisualNote("Gb3", 19.3, 0.1),
    VisualNote("G3", 19.4, 0.3),
    VisualNote("Ab3", 19.6, 1.4),

    VisualNote("B1", 21.8, 1.7),
    VisualNote("B2", 21.8, 1.5),
    VisualNote("Eb3", 21.8, 1.3),
    VisualNote("Gb3", 21.8, 0.8),
    VisualNote("B3", 21.8, 1.3),
    VisualNote("Gb3", 23, 0.3),

    VisualNote("G3", 23.5, 0.3),
    VisualNote("Ab3", 23.8, 0.2),
    VisualNote("A3", 23.85, 0.1),

    VisualNote("Gb1", 24.1, 1.63),
    VisualNote("Gb2", 24.2, 1.56),
    VisualNote("Db3", 24.16, 2.17),
    VisualNote("Gb3", 24.16, 2.31),
    VisualNote("Bb3", 24.16, 2.31),

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

    VisualNote("E1", 100.73, 1.43),
    VisualNote("E2", 100.73, 1.43),
    VisualNote("Gb3", 100.67, 0.13),
    VisualNote("Gb3", 101.1, 0.5),
    VisualNote("Ab3", 100.73, 0.47),
    VisualNote("Ab3", 101.53, 0.1),
    VisualNote("Ab3", 101.83, 0.43),

    VisualNote("Eb1", 104.03, 0.33),
    VisualNote("Gb1", 103, 0.5),
    VisualNote("Eb2", 104.03, 0.37),
    VisualNote("Gb2", 103, 0.43),
    VisualNote("B3", 103.73, 0.1),
    VisualNote("B3", 104.03, 0.47),
    VisualNote("Db4", 103, 0.37),
    VisualNote("Db4", 103.5, 0.3),
    VisualNote("Eb4", 103.23, 0.43),

    VisualNote("Ab1", 105.17, 1.43),
    VisualNote("Ab2", 105.17, 1.43),
    VisualNote("Gb3", 106.83, 0.67),
    VisualNote("Ab3", 105.17, 0.33),
    VisualNote("Ab3", 105.73, 0.17),
    VisualNote("Ab3", 106, 0.13),
    VisualNote("Ab3", 106.3, 0.63),
    VisualNote("Db4", 104.8, 0.2),
    VisualNote("D4", 104.93, 0.33),
    VisualNote("Eb4", 105.17, 0.7),

    VisualNote("B1", 107.4, 1.53),
    VisualNote("B2", 107.4, 1.37),
    VisualNote("Ab3", 109.03, 0.57),
    VisualNote("B3", 108.2, 0.1),
    VisualNote("B3", 108.47, 0.6),
    VisualNote("Db4", 107.4, 0.33),
    VisualNote("Db4", 107.93, 0.3),
    VisualNote("Eb4", 107.67, 0.43),

    VisualNote("E1", 109.6, 1.9),
    VisualNote("E1", 111.7, 1.37),
    VisualNote("E2", 109.6, 1.1),
    VisualNote("E2", 110.9, 0.17),
    VisualNote("E2", 111.1, 0.2),
    VisualNote("E2", 111.4, 0.2),
    VisualNote("E2", 111.67, 1.47),
    VisualNote("B3", 110.13, 0.17),
    VisualNote("B3", 110.63, 0.27),
    VisualNote("B3", 111.13, 0.2),
    VisualNote("B3", 111.67, 0.27),
    VisualNote("B3", 113.27, 0.3),
    VisualNote("Db4", 113, 0.2),
    VisualNote("Db4", 113.5, 0.13),
    VisualNote("Eb4", 109.6, 0.53),
    VisualNote("Eb4", 110.63, 0.27),
    VisualNote("Eb4", 111.13, 0.2),
    VisualNote("Eb4", 111.67, 0.3),
    VisualNote("Eb4", 112.73, 0.3),
    VisualNote("E4", 112.6, 0.17),
    VisualNote("F4", 112.5, 0.2),
    VisualNote("Gb4", 110.63, 0.33),
    VisualNote("Gb4", 112.2, 0.23),
    VisualNote("G4", 111.13, 0.2),
    VisualNote("Ab4", 111.67, 0.23),

    VisualNote("Db2", 113.77, 1.2),
    VisualNote("Db3", 113.77, 1.23),
    VisualNote("Ab3", 114.03, 0.43),
    VisualNote("Ab3", 114.87, 0.17),
    VisualNote("B3", 114.37, 0.6),
    VisualNote("Db4", 113.77, 1.23),

    VisualNote("Ab1", 115.9, 0.1),
    VisualNote("Ab1", 116.47, 1.1),
    VisualNote("Eb2", 115.4, 0.17),
    VisualNote("Ab2", 115.9, 0.1),
    VisualNote("Ab2", 116.47, 1.1),
    VisualNote("Eb3", 115.37, 0.1),
    VisualNote("Ab3", 116.17, 0.43),
    VisualNote("B3", 115.4, 0.33),
    VisualNote("B3", 116.47, 0.27),
    VisualNote("B3", 117.53, 0.33),
    VisualNote("Db4", 115.67, 0.2),
    VisualNote("Db4", 117.27, 0.33),
    VisualNote("Db4", 117.77, 0.13),
    VisualNote("D4", 115.73, 0.27),
    VisualNote("D4", 116.97, 0.1),
    VisualNote("Eb4", 115.9, 0.67),
    VisualNote("Eb4", 117.03, 0.37),

    VisualNote("B1", 118.07, 1.37),
    VisualNote("B2", 118.07, 1.27),
    VisualNote("Ab3", 118.3, 0.37),
    VisualNote("Ab3", 119.1, 0.23),
    VisualNote("B3", 118.6, 0.6),
    VisualNote("Db4", 118.07, 1.17),

    VisualNote("Gb1", 120.17, 0.17),
    VisualNote("Gb1", 120.7, 1.1),
    VisualNote("Gb2", 120.17, 0.17),
    VisualNote("Gb2", 120.7, 1.1),
    VisualNote("Ab3", 120.43, 0.4),
    VisualNote("B3", 119.67 , 0.33),
    VisualNote("B3", 120.73, 0.23),
    VisualNote("B3", 121.77, 0.33),
    VisualNote("Db4", 119.93 , 0.17),
    VisualNote("Db4", 121.2, 0.33),
    VisualNote("Db4", 122.03, 0.13),
    VisualNote("D4", 120.03, 0.27),
    VisualNote("D4", 121.2, 0.13),
    VisualNote("Eb4", 120.17, 0.6),
    VisualNote("Eb4", 121.27, 0.37),

    VisualNote("Db2", 122.3, 1.17),
    VisualNote("Db3", 122.3, 1.2),
    VisualNote("Ab3", 122.57, 0.4),
    VisualNote("Ab3", 123.4, 0.2),
    VisualNote("B3", 122.87, 0.63),
    VisualNote("Db4", 122.3, 1.23),

    VisualNote("Ab1", 124.43, 0.17),
    VisualNote("Ab1", 125, 0.9),
    VisualNote("Eb2", 123.9, 0.17),
    VisualNote("Ab2", 124.43, 0.13),
    VisualNote("Ab2", 125, 1),
    VisualNote("Eb3", 123.9, 0.1),
    VisualNote("Ab3", 124.7, 0.4),
    VisualNote("B3", 123.9, 0.37),
    VisualNote("B3", 125, 0.23),
    VisualNote("B3", 126.1, 0.37),
    VisualNote("Db4", 124.2, 0.2),
    VisualNote("Db4", 125.76, 0.4),
    VisualNote("Db4", 126.37, 0.17),
    VisualNote("D4", 124.3, 0.27),
    VisualNote("Eb4", 124.47, 0.67),
    VisualNote("Eb4", 125.57, 0.37),

    VisualNote("B1", 126.63, 0.13),
    VisualNote("B1", 127.17, 0.77),
    VisualNote("B2", 126.6, 0.17),
    VisualNote("B2", 127.17, 0.7),
    VisualNote("Ab3", 126.9, 0.37),
    VisualNote("B3", 127.17, 0.73),
    VisualNote("Db4", 126.63, 0.63),

    VisualNote("Gb1", 128.83, 0.27),
    VisualNote("Gb1", 129.37, 0.1),
    VisualNote("Gb1", 130.43, 0.17),
    VisualNote("Bb1", 129.93, 0.17),
    VisualNote("Gb2", 128.83, 0.27),
    VisualNote("Gb2", 129.37, 0.13),
    VisualNote("Gb2", 130.43, 0.13),
    VisualNote("Bb2", 129.93, 0.1),
    VisualNote("Gb3", 130.67, 0.1),
    VisualNote("Bb3", 128.9, 1.83),

    VisualNote("E1", 130.9, 1.27),
    VisualNote("Ab1", 130.9, 1.4),
    VisualNote("B1", 130.97, 1.37),
    VisualNote("E2", 130.97, 1.4),
    VisualNote("Gb3", 130.97, 0.33),
    VisualNote("Gb3", 131.77, 0.37),
    VisualNote("Ab3", 131.2, 0.17),
    VisualNote("Ab3", 131.5, 0.3),
    VisualNote("Ab3", 132.06, 0.57),
    VisualNote("Eb4", 132.6, 0.17),

    VisualNote("Ab1", 133.06, 1.47),
    VisualNote("B1", 133.13, 1.4),
    VisualNote("Eb2", 133.1, 1.43),
    VisualNote("Ab2", 133.17, 1.4),
    VisualNote("Gb3", 133.93, 0.4),
    VisualNote("Gb3", 135.07, 0.13),
    VisualNote("Ab3", 133.67, 0.3),
    VisualNote("Ab3", 134.23, 0.9),
    VisualNote("B3", 133.4, 0.33),
    VisualNote("Db4", 133.17, 0.3),
    VisualNote("Eb4", 132.87, 0.43),

    VisualNote("B1", 135.27, 1.6),
    VisualNote("Eb2", 135.33, 1.6),
    VisualNote("Gb2", 135.33, 1.5),
    VisualNote("B2", 135.37, 1.33),
    VisualNote("Gb3", 135.33, 0.33),
    VisualNote("Gb3", 136.13, 0.33),
    VisualNote("Ab3", 135.63, 0.17),
    VisualNote("Ab3", 135.9, 0.3),
    VisualNote("Ab3", 136.47, 0.17),

    VisualNote("Gb1", 137.53, 1.53),
    VisualNote("Bb1", 137.57, 1.5),
    VisualNote("Db2", 137.57, 1.43),
    VisualNote("Gb2", 137.6, 1.33),
    VisualNote("Gb3", 138.37, 0.4),
    VisualNote("Gb3", 139.57, 0.13),
    VisualNote("Ab3", 138.13, 0.3),
    VisualNote("Ab3", 138.67, 1),
    VisualNote("B3", 137.83, 0.37),
    VisualNote("Db4", 137.57, 0.33),
    VisualNote("Eb4", 137, 0.17),
    VisualNote("Eb4", 137.27, 0.43),

    VisualNote("E1", 139.73, 1.27),
    VisualNote("Ab1", 139.77, 1.4),
    VisualNote("B1", 139.8, 1.37),
    VisualNote("E2", 139.8, 1.4),
    VisualNote("Gb3", 139.77, 0.33),
    VisualNote("Gb3", 140.6, 0.37),
    VisualNote("Ab3", 140.07, 0.17),
    VisualNote("Ab3", 140.37, 0.27),
    VisualNote("Ab3", 140.9, 0.63),
    VisualNote("Eb4", 141.47, 0.1),

    VisualNote("Ab1", 141.97, 1.7),
    VisualNote("B1", 142, 1.63),
    VisualNote("Eb2", 142.03, 1.67),
    VisualNote("Ab2", 142.03, 1.7),
    VisualNote("Gb3", 142.83, 0.4),
    VisualNote("Ab3", 142.57, 0.33),
    VisualNote("Ab3",143.13, 0.63),
    VisualNote("B3", 142.3, 0.37),
    VisualNote("Db4", 142.03, 0.33),
    VisualNote("Eb4", 141.73, 0.6),
    VisualNote("Eb4", 143.67, 0.67),

    VisualNote("B1", 144.2, 1.47),
    VisualNote("Eb2", 144.23, 1.47),
    VisualNote("Gb2", 144.23, 1.4),
    VisualNote("B2", 144.27, 1.23),
    VisualNote("Gb3", 145.03, 0.4),
    VisualNote("Ab3", 144.77, 0.33),
    VisualNote("Ab3", 145.67, 0.6),
    VisualNote("B3", 144.5, 0.37),
    VisualNote("B3", 145.9, 0.6),
    VisualNote("Db4", 144.23, 0.33),

    VisualNote("Gb1", 146.37, 1.37),
    VisualNote("Bb1", 146.43, 1.37),
    VisualNote("Db2", 146.43, 1.37),
    VisualNote("Gb2", 146.47, 1.4),
    VisualNote("Bb3", 146.43, 0.73),
    VisualNote("B3", 148.17, 0.3),
    VisualNote("Db4", 147.9, 0.3),
    VisualNote("Db4", 148.43, 0.13),
    VisualNote("Eb4", 147.63, 0.37),
]

# 00:02:28:17

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
duration = 150  # seconds, adjust as needed
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
