import librosa
import numpy as np

# ---------------- KEY DETECTION ----------------
def estimate_key_chroma(y, sr):
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_avg = np.mean(chroma, axis=1)

    # Krumhansl-Kessler key profiles (normalized)
    major_template = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09,
                               2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    minor_template = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53,
                               2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

    def correlate(template):
        return [np.corrcoef(np.roll(template, i), chroma_avg)[0, 1] for i in range(12)]

    major_corr = correlate(major_template)
    minor_corr = correlate(minor_template)

    max_major = np.argmax(major_corr)
    max_minor = np.argmax(minor_corr)

    if major_corr[max_major] > minor_corr[max_minor]:
        key = librosa.midi_to_note(max_major + 60)[:-1] + " Major"
    else:
        key = librosa.midi_to_note(max_minor + 60)[:-1] + " Minor"

    return key

# ---------------- TEMPO & TIME SIGNATURE ----------------
def analyze_tempo_and_signature(y, sr):
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, onset_envelope=onset_env)

    if isinstance(tempo, np.ndarray):
        tempo = tempo[0] if len(tempo) > 0 else 0.0

    if len(beat_frames) > 1:
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        beat_intervals = np.diff(beat_times)
        avg_beat_duration = np.median(beat_intervals)
        beats_per_bar = round(4 / avg_beat_duration) if avg_beat_duration != 0 else 0
        time_signature = f'{beats_per_bar}/4'
    else:
        time_signature = "Unknown"

    return tempo, time_signature

# ---------------- MAIN FUNCTION ----------------
def analyze_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)
    key = estimate_key_chroma(y, sr)
    tempo, time_sig = analyze_tempo_and_signature(y, sr)

    print(f"\n🎵 Analysis for: {file_path}")
    print(f"Estimated Key: {key}")
    print(f"Estimated Tempo: {tempo:.2f} BPM")
    print(f"Estimated Time Signature: {time_sig}")

# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    file_path = "Ed Sheeran - Perfect (Official Music Video).mp3"
    analyze_audio(file_path)