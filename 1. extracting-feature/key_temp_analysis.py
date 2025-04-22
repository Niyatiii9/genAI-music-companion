import librosa
import numpy as np

def analyze_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)

    # Estimate Tempo (BPM)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, onset_envelope=onset_env)

    # Ensure tempo is a single value (take first element if it's an array)
    if isinstance(tempo, np.ndarray):
        tempo = tempo[0] if len(tempo) > 0 else 0.0

    # Estimate Time Signature
    if len(beat_frames) > 1:
        beat_intervals = np.diff(librosa.frames_to_time(beat_frames, sr=sr))
        avg_beat_duration = np.median(beat_intervals)
        beats_per_bar = round(4 / avg_beat_duration)
        time_signature = f'{beats_per_bar}/4'
    else:
        time_signature = "Unknown"

    # Compute Chroma Features for Key Detection
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = chroma.mean(axis=1)

    # Map Chroma to Closest Musical Key
    key_index = np.argmax(chroma_mean)
    key_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    key = key_names[key_index]

    # Determine Major or Minor Scale
    major_template = np.array([1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0])
    minor_template = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
    
    major_score = np.dot(major_template, chroma_mean)
    minor_score = np.dot(minor_template, chroma_mean)
    scale = 'Major' if major_score > minor_score else 'Minor'

    print(f'Tempo: {tempo:.2f} BPM')
    print(f'Time Signature: {time_signature}')
    print(f'Key: {key} {scale}')

    return tempo, time_signature, key, scale

if __name__ == "__main__":
    file_path = "Ed Sheeran - Perfect (Official Music Video .mp3"  # Replace with actual file path
    analyze_audio(file_path)