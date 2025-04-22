import numpy as np
import librosa


def estimate_key_chroma(y, sr):
    """
    Estimate the key (and scale) of an audio file using its chroma features.
    
    This simple method computes an average chroma vector and compares it to
    rotated Krumhansl key profiles for both major and minor keys.
    """
    # Compute chroma features from a constant-Q transform
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    # Average across time frames
    chroma_avg = np.mean(chroma, axis=1)
    
    # Krumhansl-Kessler key profiles (normalized)
    major_template = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    minor_template = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
    major_template /= major_template.sum()
    minor_template /= minor_template.sum()

    best_score = -np.inf
    best_key = None
    keys = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Test each key (for both major and minor)
    for i in range(12):
        rotated_major = np.roll(major_template, i)
        score_major = np.dot(chroma_avg, rotated_major)
        if score_major > best_score:
            best_score = score_major
            best_key = keys[i] + " Major"

        rotated_minor = np.roll(minor_template, i)
        score_minor = np.dot(chroma_avg, rotated_minor)
        if score_minor > best_score:
            best_score = score_minor
            best_key = keys[i] + " Minor"
    
    return best_key



def analyze_audio(file_path):
    """
    Analyze an audio file for key, scale, tempo, and time signature.
    
    Note:
      - Tempo is estimated using beat tracking.
      - Key and scale are estimated from chroma features.
      - Time signature detection is not trivial; here we use a heuristic and assume 4/4.
    """
    # Load the audio file (mono by default)
    y, sr = librosa.load(file_path)
    
    # Estimate tempo and obtain beat frames
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    
    # Key estimation using chroma features
    estimated_key = estimate_key_chroma(y, sr)
    
    # For this example, we assume the scale is synonymous with the key.
    scale = estimated_key
    
    ## Time Signature Estimation
    if len(beat_frames) > 1:
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        beat_intervals = np.diff(beat_times)
        avg_beat_duration = np.median(beat_intervals)
        beats_per_bar = round(4 / avg_beat_duration) if avg_beat_duration != 0 else 0 # Assuming 4 beats per bar
        time_signature = f'{beats_per_bar}/4'
    else:
        time_signature = 'Unknown'

    return {
        'key': estimated_key,
        'scale': scale,
        'tempo': int(tempo),
        'time_signature': time_signature
    }

if __name__ == "__main__":
    # Replace this with the path to your audio file (wav, mp3, etc.)
    file_path = '/Users/bhuman/Downloads/Despacito - Luis Fonsi & Daddy Yankee.mp3'
    
    analysis = analyze_audio(file_path)
    print("Audio Analysis Results:")
    print("Key / Scale:     ", analysis['key'])
    print("Tempo (BPM):     ", analysis['tempo'])
    print("Time Signature:  ", analysis['time_signature'])