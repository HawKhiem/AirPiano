from pydub import AudioSegment
import os

folder_path = "wavPianoSounds"
output_path = "processedWavPianoSounds"
os.makedirs(output_path, exist_ok=True)

cut_duration = 50  # Cut 150 ms from start
fade_duration = 20  # Fade-in duration (in ms)

for filename in os.listdir(folder_path):
    if filename.endswith(".wav"):
        file_path = os.path.join(folder_path, filename)
        audio = AudioSegment.from_wav(file_path)

        # Cut and apply fade-in
        trimmed_audio = audio[cut_duration:].fade_in(fade_duration)

        trimmed_path = os.path.join(output_path, filename)
        trimmed_audio.export(trimmed_path, format="wav")
        print(f"Trimmed and faded: {filename}")
