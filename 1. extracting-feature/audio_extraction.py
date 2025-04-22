import librosa
import numpy as np

def detect_features(audio_path):
    y, sr = librosa.load(audio_path)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)

    # Key detection using the Krumhansl-Schmuckler algorithm
    key_index = np.argmax(chroma_mean)
    
    ## Key Mapping
    key_mapping = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    detected_key = key_mapping[key_index]

    ## Tempo
    tempo,beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    print(beat_frames)
    if len(beat_frames) > 1:
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        beat_intervals = np.diff(beat_times)
        avg_interval = np.median(beat_intervals)
        # Assume a typical bar length and approximate the number of beats per bar.
        beats_per_bar = round(4 / avg_interval) if avg_interval != 0 else 0
        time_signature = f"{beats_per_bar}/4"
    else:
        time_signature = "Unknown"
    

    return int(tempo), detected_key, time_signature

audio_path = '/Users/bhuman/Desktop/`Perfect - Ed Sheeran.mp3'
tempo, key, time_signature = detect_features(audio_path)
print("Audio Analysis Results:")
print("Key (Tonic): ", key)
# print("Scale:           ", )
print("Tempo (BPM): ", tempo)
print("Time Signature: ", time_signature)