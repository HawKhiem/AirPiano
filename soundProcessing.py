import os
from pydub import AudioSegment

input_folder = "pianoSounds"
output_folder = "wavPianoSounds"
os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".mp3"):
        mp3_path = os.path.join(input_folder, filename)
        wav_path = os.path.join(output_folder, filename.replace(".mp3", ".wav"))

        sound = AudioSegment.from_mp3(mp3_path)
        sound.export(wav_path, format="wav")
        print(f"Converted: {filename} -> {os.path.basename(wav_path)}")
