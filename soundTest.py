import cv2
import cvzone
import numpy as np
import os
from cvzone.HandTrackingModule import HandDetector
import pygame
import time

# ---------------- Setup Sound System ---------------- #
sound_folder = "wavPianoSounds"
pygame.mixer.init(buffer=600)
pygame.mixer.set_num_channels(600)

keys = ["Eb1", "E1", "F1", "Gb1", "G1", "Ab1", "A1", "Bb1", "B1", "C2", "Db2", "D2",
        "Eb2", "E2", "F2", "Gb2", "G2", "Ab2", "A2", "Bb2", "B2", "C3", "Db3", "D3",
        "Eb3", "E3", "F3", "Gb3", "G3", "Ab3", "A3", "Bb3", "B3", "C4", "Db4", "D4",
        "Eb4", "E4", "F4", "Gb4", "G4", "Ab4", "A4", "Bb4", "B4", "C5", "Db5", "D5",
        "Eb5", "E5", "F5", "Gb5", "G5", "Ab5", "A5", "Bb5", "B5", "C6", "Db6", "D6"]

key_sounds = {}
key_channels = {}
key_channel_index = {}
channels_per_key = 10
channel_counter = 0
for key in keys:
    path = os.path.join(sound_folder, f"{key}.wav")
    if os.path.exists(path):
        key_sounds[key] = pygame.mixer.Sound(path)
        key_channels[key] = [pygame.mixer.Channel(channel_counter + i) for i in range(channels_per_key)]
        key_channel_index[key] = 0
        channel_counter += channels_per_key

# ---------------- Scheduled Notes ---------------- #
class VisualNote:
    def __init__(self, key, start_time, duration):
        self.key = key
        self.start_time = start_time
        self.duration = duration
        self.active = False  # track if currently touching
        self.played = False  # ensure it only starts once

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

    VisualNote("Ab1", 19.47, 1.3),
    VisualNote("Ab2", 19.53, 1.3),
    VisualNote("B2", 19.53, 1.2),
    VisualNote("Eb3", 19.53, 1.3),
    VisualNote("F3", 18.93, 0.3),
    VisualNote("Gb3", 19.27, 0.1),
    VisualNote("G3", 19.3, 0.27),
    VisualNote("Ab3", 19.53, 1.4),

    VisualNote("B1", 21.8, 1.7),
    VisualNote("B2", 21.8, 1.5),
    VisualNote("Eb3", 21.8, 1.3),
    VisualNote("Gb3", 21.8, 0.8),
    VisualNote("B3", 21.8, 1.3),
    VisualNote("Gb3", 22.97, 0.3),

    VisualNote("G3", 23.53, 0.3),
    VisualNote("Ab3", 23.8, 0.2),
    VisualNote("A3", 23.83, 0.1),

    VisualNote("Gb1", 24.13, 1.63),
    VisualNote("Gb2", 24.13, 1.56),
    VisualNote("Db3", 24.13, 2.17),
    VisualNote("Gb3", 24.13, 2.31),
    VisualNote("Bb3", 24.13, 2.31),

    VisualNote("Ab1", 26.43, 1.5),
    VisualNote("Ab2", 26.43, 1.5),

    VisualNote("Gb3", 27.23, 0.17),
    VisualNote("Gb3", 27.53, 0.17),
    VisualNote("Gb3", 27.8, 0.17),
    VisualNote("Gb3", 28.07, 0.17),
    VisualNote("Gb3", 28.33, 0.17),

    VisualNote("B1", 28.63, 1.74),
    VisualNote("B2", 28.63, 1.44),
    VisualNote("Eb3", 29.4, 0.17),
    VisualNote("Eb3", 29.7, 0.43),
    VisualNote("Gb3", 28.6, 0.33),
    VisualNote("Gb3", 29.13, 0.17),
    VisualNote("B3", 28.87, 0.36),
    VisualNote("B3", 29.4, 0.17),
    VisualNote("B3", 29.7, 0.83),
    VisualNote("Db4", 28.6, 0.33),
    VisualNote("Db4", 29.13, 0.17),
    VisualNote("Eb4", 28.87, 0.2),

    VisualNote("E1", 30.77, 1.3),
    VisualNote("E2", 30.77, 1.3),
    VisualNote("E3", 30.47, 0.97),
    VisualNote("Ab3", 30.47, 1.07),

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
    VisualNote("D4", 34.97, 0.2),

    VisualNote("Ab1", 35.1, 1.43),
    VisualNote("Ab2", 35.17, 1.5),
    VisualNote("Ab3", 35.2, 1.1),
    VisualNote("Eb4", 35.2, 1.07),

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
    VisualNote("Db4", 121.5, 0.33),
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
    VisualNote("Db4", 125.77, 0.4),
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
    VisualNote("Bb3", 128.87, 1.83),

    VisualNote("E1", 130.9, 1.27),
    VisualNote("Ab1", 130.9, 1.4),
    VisualNote("B1", 130.97, 1.37),
    VisualNote("E2", 130.97, 1.4),
    VisualNote("Gb3", 130.97, 0.33),
    VisualNote("Gb3", 131.77, 0.37),
    VisualNote("Ab3", 131.2, 0.17),
    VisualNote("Ab3", 131.5, 0.3),
    VisualNote("Ab3", 132.07, 0.57),
    VisualNote("Eb4", 132.6, 0.17),

    VisualNote("Ab1", 133.07, 1.47),
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
    VisualNote("Ab3", 145.33, 0.6),
    VisualNote("B3", 144.5, 0.37),
    VisualNote("B3", 145.9, 0.6),
    VisualNote("Db4", 144.23, 0.33),

    VisualNote("Gb1", 146.37, 1.37),
    VisualNote("Bb1", 146.43, 1.37),
    VisualNote("Db2", 146.43, 1.37),
    VisualNote("Gb2", 146.47, 1.4),
    VisualNote("Bb3", 146.47, 0.73),
    VisualNote("B3", 148.17, 0.3),
    VisualNote("Db4", 147.9, 0.3),
    VisualNote("Db4", 148.43, 0.13),
    VisualNote("Eb4", 147.63, 0.37),

    VisualNote("Db2", 148.73, 1.17),
    VisualNote("Db3", 148.73, 1.27),
    VisualNote("Ab3", 149, 0.33),
    VisualNote("Ab3", 149.9, 0.33),
    VisualNote("B3", 149.33, 0.6),
    VisualNote("Db4", 148.73, 0.6),

    VisualNote("Ab1", 151.03, 0.43),
    VisualNote("Ab1", 151.6, 1.2),
    VisualNote("Eb2", 150.47, 0.2),
    VisualNote("Ab2", 151.03, 0.43),
    VisualNote("Ab2", 151.6, 1.27),
    VisualNote("Eb3", 150.47, 0.1),
    VisualNote("Ab3", 151.33, 0.4),
    VisualNote("B3", 150.5, 0.4),
    VisualNote("B3", 151.6, 0.6),
    VisualNote("B3", 152.73, 0.4),
    VisualNote("Db4", 150.8, 0.2),
    VisualNote("Db4", 152.43, 0.3),
    VisualNote("Db4", 153, 0.13),
    VisualNote("D4", 150.9, 0.23),
    VisualNote("Eb4", 151.07, 0.6),
    VisualNote("Eb4", 152.17, 0.37),

    VisualNote("B1", 153.3, 1.67),
    VisualNote("B2", 153.3, 1.5),
    VisualNote("Ab3", 153.6, 0.33),
    VisualNote("Ab3", 154.4, 0.23),
    VisualNote("B3", 153.87,  0.6),
    VisualNote("Db4", 153.3, 0.4),

    VisualNote("Gb1", 155.53, 0.2),
    VisualNote("Gb1", 156.1, 0.93),
    VisualNote("Gb2", 155.5, 0.17),
    VisualNote("Gb2", 156.1, 1.07),
    VisualNote("Ab3", 155.83, 0.43),
    VisualNote("B3", 154.97, 0.37),
    VisualNote("B3", 156.13, 0.23),
    VisualNote("B3", 157.2, 0.37),
    VisualNote("Db4", 155.27, 0.2),
    VisualNote("Db4", 156.97, 0.33),
    VisualNote("Db4", 157.5, 0.1),
    VisualNote("D4", 155.4, 0.23),
    VisualNote("D4", 156.63, 0.17),
    VisualNote("Eb4", 155.57, 0.63),
    VisualNote("Eb4", 156.7, 0.47),

    VisualNote("Db2", 157.8, 1.13),
    VisualNote("Db3", 157.77, 1.27),
    VisualNote("Ab3", 158.1, 0.3),
    VisualNote("Ab3", 158.9, 0.2),
    VisualNote("B3", 158.37, 0.53),
    VisualNote("Db4", 157.77, 0.4),

    VisualNote("Ab1", 160, 0.13),
    VisualNote("Ab1", 160.53, 1),
    VisualNote("Eb2", 159.43, 0.17),
    VisualNote("Ab2", 159.97, 0.1),
    VisualNote("Ab2", 160.53, 1.03),
    VisualNote("Eb3", 159.43, 0.1),
    VisualNote("Ab3", 160.27, 0.4),
    VisualNote("B3", 159.43, 0.37),
    VisualNote("B3", 160.57, 0.2),
    VisualNote("B3", 161.63, 0.37),
    VisualNote("Db4", 159.73, 0.17),
    VisualNote("Db4", 161.37, 0.33),
    VisualNote("Db4", 161.9, 0.17),
    VisualNote("D4", 159.83, 0.23),
    VisualNote("Eb4", 160, 0.63),
    VisualNote("Eb4", 161.13, 0.4),

    VisualNote("B1", 162.17, 0.27),
    VisualNote("B1", 162.7, 0.67),
    VisualNote("B2", 162.17, 0.27),
    VisualNote("B2", 162.7, 0.57),
    VisualNote("Ab3", 162.43, 0.33),
    VisualNote("B3", 162.7, 0.53),
    VisualNote("Db4", 162.17, 0.63),

    VisualNote("Eb1", 165.4, 0.4),
    VisualNote("Gb1", 164.37, 0.27),
    VisualNote("Gb1", 164.9, 0.17),
    VisualNote("Eb2", 165.4, 0.5),
    VisualNote("Gb2", 164.37, 0.27),
    VisualNote("Gb2", 164.9, 0.13),
    VisualNote("Db4", 164.37, 0.27),
    VisualNote("Db4", 164.9, 0.13),
    VisualNote("Eb4", 165.4, 0.33),
    VisualNote("Gb4", 164.37, 0.6),
    VisualNote("G4", 164.9, 0.17),
    VisualNote("B4", 165.97, 0.3),
    VisualNote("Db5", 165.67, 0.37),
    VisualNote("Db5", 166.2, 0.1),
    VisualNote("Eb5", 165.4, 0.4),

    VisualNote("Db2", 166.5, 0.2),
    VisualNote("Db3", 166.5, 0.2),
    VisualNote("Db3", 167.57, 0.17),
    VisualNote("E3", 167.57, 0.13),
    VisualNote("Ab3", 167.57, 0.1),
    VisualNote("Db4", 166.5, 0.5),
    VisualNote("Ab4", 166.73, 0.37),
    VisualNote("Ab4", 167.57, 0.17),
    VisualNote("B4", 167, 0.63),
    VisualNote("Db5", 166.47, 0.47),

    VisualNote("Ab1", 168.63, 0.17),
    VisualNote("Ab2", 168.63, 0.17),
    VisualNote("Db4", 168.1, 0.1),
    VisualNote("Db4", 168.37, 0.13),
    VisualNote("Db4", 168.63, 0.37),
    VisualNote("Ab4", 168.9, 0.33),
    VisualNote("B4", 169.2, 0.17),
    VisualNote("Db5", 168.1, 0.1),
    VisualNote("Db5", 168.37, 0.13),
    VisualNote("Db5", 168.63, 0.37),

    VisualNote("B1", 170.77, 0.3),
    VisualNote("Ab2", 169.73, 0.2),
    VisualNote("B2", 169.73, 0.13),
    VisualNote("B2", 170.77, 0.37),
    VisualNote("Eb3", 169.73, 0.1),
    VisualNote("Db4", 170.77, 0.37),
    VisualNote("Eb4", 169.73, 0.2),
    VisualNote("Ab4", 171.03, 0.33),
    VisualNote("B4", 170.23, 0.33),
    VisualNote("B4", 171.3, 0.17),
    VisualNote("Db5", 169.97, 0.3),
    VisualNote("Db5", 170.47, 0.1),
    VisualNote("Db5", 170.77, 0.6),
    VisualNote("Eb5", 169.73, 0.33),

    VisualNote("Gb1", 172.93, 0.17),
    VisualNote("Gb2", 172.93, 0.17),
    VisualNote("B2", 171.83, 0.1),
    VisualNote("Eb3", 171.83, 0.17),
    VisualNote("Gb3", 171.83, 0.1),
    VisualNote("Db4", 172.37, 0.17),
    VisualNote("Db4", 172.67, 0.1),
    VisualNote("Db4", 172.93, 0.33),
    VisualNote("Ab4", 171.83, 0.17),
    VisualNote("Ab4", 173.2, 0.33),
    VisualNote("B4", 173.5, 0.1),
    VisualNote("Db5", 172.37, 0.17),
    VisualNote("Db5", 172.67, 0.17),
    VisualNote("Db5", 172.93, 0.37),

    VisualNote("Db2", 175.07, 0.2),
    VisualNote("Gb2", 174.03, 0.2),
    VisualNote("Bb2", 174.03, 0.2),
    VisualNote("Db3", 174.03, 0.17),
    VisualNote("Db3", 175.07, 0.23),
    VisualNote("Db3", 176.13, 0.23),
    VisualNote("E3", 176.13, 0.2),
    VisualNote("Ab3", 176.13, 0.1),
    VisualNote("Db4", 175.07, 0.33),
    VisualNote("Eb4", 174.03, 0.2),
    VisualNote("Ab4", 175.3, 0.33),
    VisualNote("Ab4", 176.13, 0.13),
    VisualNote("B4", 174.53, 0.3),
    VisualNote("B4", 175.57, 0.63),
    VisualNote("Db5", 174.3, 0.33),
    VisualNote("Db5", 174.77, 0.13),
    VisualNote("Db5", 175.07, 0.4),
    VisualNote("Eb5", 174.03, 0.23),

    VisualNote("Ab1", 177.23, 0.2),
    VisualNote("Ab2", 177.23, 0.3),
    VisualNote("Db4", 176.7, 0.13),
    VisualNote("Db4", 176.93, 0.13),
    VisualNote("Db4", 177.23, 0.23),
    VisualNote("Ab4", 177.5, 0.37),
    VisualNote("B4", 177.8, 0.1),
    VisualNote("Db5", 176.7, 0.17),
    VisualNote("Db5", 176.93, 0.17),
    VisualNote("Db5", 177.23, 0.37),

    VisualNote("B1", 179.37, 0.3),
    VisualNote("Ab2", 178.33, 0.23),
    VisualNote("B2", 178.33, 0.2),
    VisualNote("B2", 179.37, 0.33),
    VisualNote("Eb3", 178.33, 0.13),
    VisualNote("Db4", 179.37, 0.43),
    VisualNote("Eb4", 178.3, 0.2),
    VisualNote("Ab4", 179.6, 0.33),
    VisualNote("B4", 178.83, 0.27),
    VisualNote("B4", 179.93, 0.57),
    VisualNote("Db5", 178.57, 0.3),
    VisualNote("Db5", 179.1, 0.1),
    VisualNote("Db5", 179.37, 0.4),
    VisualNote("Eb5", 178.3, 0.23),

    VisualNote("Gb1", 181.57, 0.5),
    VisualNote("Gb2", 181.57, 0.57),
    VisualNote("B2", 180.47, 0.23),
    VisualNote("Eb3", 180.47, 0.2),
    VisualNote("Gb3", 180.47, 0.1),
    VisualNote("Ab4", 181, 0.63),
    VisualNote("Bb4", 180.47, 0.6),
    VisualNote("Bb4", 181.57, 1.27),

    VisualNote("Gb2", 182.67, 0.53),
    VisualNote("Bb2", 182.67, 0.47),
    VisualNote("Db3", 182.67, 0.4),
    VisualNote("Eb4", 183.27, 0.37),
    VisualNote("Gb4", 182.93, 0.37),
    VisualNote("Gb4", 183.57, 0.1),

    VisualNote("E1", 183.83, 1.9),
    VisualNote("Ab1", 183.87, 1.97),
    VisualNote("B1", 183.9, 1.93),
    VisualNote("E2", 183.9, 1.9),
    VisualNote("Eb4 ", 183.9, 0.23),
    VisualNote("Eb4 ", 184.7, 0.13),
    VisualNote("E4", 184.23, 0.13),
    VisualNote("E4", 184.47, 0.17),
    VisualNote("E4", 185, 0.1),
    VisualNote("Gb4", 183.87, 0.43),
    VisualNote("Gb4", 184.7, 0.3),
    VisualNote("G4", 185.53, 0.27),
    VisualNote("Ab4", 184.2, 0.13),
    VisualNote("Ab4", 184.47, 0.27),
    VisualNote("Ab4", 185, 0.1),
    VisualNote("B4", 185.53, 0.27),
    VisualNote("Eb5", 185.6, 0.27),

    VisualNote("Ab1", 186.4, 1.3),
    VisualNote("B1", 186.47, 1.53),
    VisualNote("Eb2", 186.43, 1.6),
    VisualNote("Ab2", 186.5, 1.6),
    VisualNote("Gb4", 187.27, 0.3),
    VisualNote("Gb4", 188.33, 0.1),
    VisualNote("Ab4", 186.43, 0.4),
    VisualNote("Ab4", 187.03, 0.27),
    VisualNote("Ab4", 187.57, 0.83),
    VisualNote("B4", 186.8, 0.3),
    VisualNote("Db5", 186.47, 0.47),
    VisualNote("Eb5", 185.93, 0.53),

    VisualNote("B1", 188.63, 1.6),
    VisualNote("Eb2", 188.67, 1.6),
    VisualNote("Gb2", 188.67, 1.5),
    VisualNote("B2", 188.7, 1.4),
    VisualNote("Eb4", 188.7, 0.3),
    VisualNote("Gb4", 188.7, 0.37),
    VisualNote("Gb4", 189.5, 0.33),
    VisualNote("Gb4", 190.3, 0.47),
    VisualNote("Ab4", 189, 0.1),
    VisualNote("Ab4", 189.23, 0.3),
    VisualNote("Ab4", 189.77, 0.13),
    VisualNote("Eb5", 190.3, 0.23),
    VisualNote("Eb5", 190.6, 0.17),

    VisualNote("Gb1", 190.93, 1.73),
    VisualNote("Bb1", 191.03, 1.63),
    VisualNote("Db2", 191.03, 1.57),
    VisualNote("Gb2", 191.03, 1.43),
    VisualNote("Gb4", 191.9, 0.33),
    VisualNote("Gb4", 192.73, 0.17),
    VisualNote("Ab4", 191.67, 0.3),
    VisualNote("Ab4", 192.2, 0.6),
    VisualNote("Bb4", 191.03, 0.37),
    VisualNote("B4", 191.43, 0.3),
    VisualNote("Db5", 191.03, 0.5),

    VisualNote("E1", 193.23, 1.63),
    VisualNote("Ab1", 193.27, 1.73),
    VisualNote("B1", 193.3, 1.67),
    VisualNote("E2", 193.3, 1.67),
    VisualNote("E4", 193.3, 0.43),
    VisualNote("E4", 193.9, 0.3),
    VisualNote("E4", 194.37, 0.1),
    VisualNote("Gb4", 193.3, 0.43),
    VisualNote("Gb4", 194.13, 0.3),
    VisualNote("G4", 194.9, 0.4),
    VisualNote("Ab4", 193.67, 0.1),
    VisualNote("Ab4", 193.9, 0.33),
    VisualNote("Ab4", 194.37, 0.17),
    VisualNote("B4",194.9, 0.3),
    VisualNote("Eb5", 194.97, 0.43),

    VisualNote("Ab1", 195.47, 1.8),
    VisualNote("B1", 195.53, 1.73),
    VisualNote("Eb2", 195.5, 1.8),
    VisualNote("Ab2", 195.57, 1.9),
    VisualNote("Gb4", 196.37, 0.37),
    VisualNote("G4", 197.17, 0.17),
    VisualNote("Ab4", 195.53, 0.37),
    VisualNote("Ab4", 196.13, 0.3),
    VisualNote("Ab4", 196.67, 0.17),
    VisualNote("B4", 195.9, 0.3),
    VisualNote("B4", 197.2, 0.17),
    VisualNote("Db5", 195.57, 0.43),
    VisualNote("Eb5", 197.23, 0.17),

    VisualNote("B1", 197.7, 1.43),
    VisualNote("Eb2", 197.77, 1.47),
    VisualNote("Gb2", 197.77, 1.43),
    VisualNote("B2", 197.77, 1.37),
    VisualNote("Eb4", 197.7, 0.4),
    VisualNote("Eb4", 199.37, 0.17),
    VisualNote("Gb4", 197.77, 0.43),
    VisualNote("Gb4", 198.6, 0.37),
    VisualNote("Ab4", 198.37, 0.3),
    VisualNote("Ab4", 198.87, 0.6),
    VisualNote("B4", 198.13, 0.33),
    VisualNote("B4", 199.37, 0.17),
    VisualNote("Db5", 197.8, 0.4),

    VisualNote("Gb1", 199.83, 1.47),
    VisualNote("Bb1", 199.93, 1.47),
    VisualNote("Db2", 199.97, 1.43),
    VisualNote("Gb2", 200, 1.43),
    VisualNote("Db4", 199.93, 1.5),
    VisualNote("Gb4", 200, 1.5),
    VisualNote("Bb4", 200, 1.43),

    VisualNote("Ab1", 204.7, 1.17),
    VisualNote("Db2", 202.43, 1.63),
    VisualNote("Ab2", 204.7, 1.2),
    VisualNote("Db3", 202.43, 1.53),
    VisualNote("E4", 202.43, 0.17),
    VisualNote("Gb4", 202.73, 0.1),
    VisualNote("Ab4", 203.03, 1.33),
    VisualNote("B4", 204.73, 0.3),
    VisualNote("B4", 205.3, 0.23),
    VisualNote("Db5", 202.43, 0.33),
    VisualNote("Db5", 204.43, 0.3),
    VisualNote("Db5", 204.97, 0.33),
    VisualNote("Eb5", 202.73, 0.17),
    VisualNote("Eb5", 204.17, 0.33),
    VisualNote("Eb5", 204.73, 0.5),
    VisualNote("E5", 203.03, 1.17),

    VisualNote("Gb1", 209.2, 1.13),
    VisualNote("B1", 207.03, 1.13),
    VisualNote("Gb2", 209.2, 1.23),
    VisualNote("B2", 207.03, 1),
    VisualNote("Eb4", 207.03, 0.2),
    VisualNote("E4", 207.3, 0.13),
    VisualNote("Gb4", 207.6, 1.2),
    VisualNote("Bb4", 209.23, 0.3),
    VisualNote("Bb4", 209.8, 1.1),
    VisualNote("B4", 207.03, 0.37),
    VisualNote("B4", 208.93, 0.3),
    VisualNote("B4", 209.5, 0.3),
    VisualNote("Db5", 207.3, 0.33),
    VisualNote("Db5", 208.63, 0.27),
    VisualNote("Db5", 209.23, 0.47),
    VisualNote("Eb5", 207.6, 1.13),

    VisualNote("Ab1", 213.7, 1.47),
    VisualNote("Db2", 211.5, 1.3),
    VisualNote("Ab2", 213.7, 1.5),
    VisualNote("Db3", 211.5, 1.03),
    VisualNote("E4", 211.5, 0.17),
    VisualNote("Gb4", 211.77, 0.17),
    VisualNote("Ab4", 212.03, 1.37),
    VisualNote("B4", 213.73, 0.3),
    VisualNote("B4", 214.27, 0.27),
    VisualNote("Db5", 211.5, 0.4),
    VisualNote("Db5", 213.43, 0.3),
    VisualNote("Db5", 213.97, 0.37),
    VisualNote("Eb5", 211.8, 0.17),
    VisualNote("Eb5", 213.2, 0.27),
    VisualNote("Eb5", 213.73, 0.5),
    VisualNote("E5", 212.03, 1.17),

    VisualNote("B1", 216.13, 1.63),
    VisualNote("B2", 216.13, 1.53),
    VisualNote("Eb4", 216.13, 0.2),
    VisualNote("E4", 216.43, 0.13),
    VisualNote("Gb4", 216.8, 1.6),
    VisualNote("B4", 216.13, 0.4),
    VisualNote("B4", 218.53, 0.13),
    VisualNote("Db5", 216.43, 0.4),
    VisualNote("Db5", 218.13, 0.37),
    VisualNote("Eb5", 216.8, 1.43),

    VisualNote("Gb1", 219.03, 1.5),
    VisualNote("Gb2", 219.03, 1.47),
    VisualNote("Bb4", 219.03, 0.63),
    VisualNote("Bb4", 220.17, 0.23),
    VisualNote("B4", 219.57, 0.67),
    VisualNote("Db5", 219.03, 1.23),
]
# END

# ---------------- Webcam + Hand + UI Setup ---------------- #
cap = cv2.VideoCapture(0)
cap.set(3, 2560)
cap.set(4, 1440)
detector = HandDetector(detectionCon=0.8)

class Button:
    def __init__(self, position, text, size=None):
        self.position = position
        self.text = text
        self.size = size if size else [40, 200]

buttons = [Button([42 * i + 20, 1240], key) for i, key in enumerate(keys)]

def drawAllTransparent(img, buttonList):
    imgNew = np.zeros_like(img, np.uint8)
    for button in buttonList:
        x, y = button.position
        w, h = button.size
        cvzone.cornerRect(imgNew, (x, y, w, h), 20, rt=0)
        color = (0, 0, 0) if "b" in button.text else (255, 255, 255)
        cv2.rectangle(imgNew, button.position, (x + w, y + h), color, cv2.FILLED)
        cv2.putText(imgNew, button.text, (x, y + 65), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
    return out

def play_note(key):
    if key in key_sounds:
        idx = key_channel_index[key]
        ch = key_channels[key][idx]
        ch.play(key_sounds[key])
        key_channel_index[key] = (idx + 1) % channels_per_key

# ---------------- With Webcam and Hand Detection ---------------- #
# pixels_per_second = 200
# start_time = time.time()
#
# while True:
#     success, img = cap.read()
#     img = cv2.flip(img, 1)
#     hands, img = detector.findHands(img)
#     img = drawAllTransparent(img, buttons)
#
#     current_time = time.time() - start_time
#
#     for note in note_schedule:
#         elapsed = current_time - note.start_time
#         if elapsed < -note.duration:
#             continue  # not yet time
#
#         if elapsed > note.duration + 2:
#             continue  # already done
#
#         button = next((b for b in buttons if b.text == note.key), None)
#         if button:
#             x, y = button.position
#             w, h = button.size
#
#             y_offset = int((note.start_time - current_time) * pixels_per_second)
#             height = int(note.duration * pixels_per_second)
#             top_left = (x, y - height - y_offset)
#             bottom_right = (x + w, y - y_offset)
#
#             if bottom_right[1] >= y and not note.played:
#                 note.played = True
#                 play_note(note.key)
#
#             overlay = img.copy()
#             cv2.rectangle(overlay, top_left, bottom_right, (255, 0, 0), -1)
#             alpha = 0.6
#             cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, dst=img)
#
#     cv2.imshow("Piano Visualizer Live", img)
#     cv2.waitKey(1)

# ---------------- Without Webcam and Hand Detection ---------------- #
start_time = time.time()
max_time = max(note.start_time + note.duration for note in note_schedule)

print("🎹 Playing scheduled notes...")

while True:
    current_time = time.time() - start_time

    for note in note_schedule:
        if not note.played and current_time >= note.start_time:
            play_note(note.key)
            note.played = True
            print(f"Played: {note.key} at {current_time:.2f}s")

    if current_time >= max_time + 1:
        break

    time.sleep(0.01)

print("✅ Playback finished.")
