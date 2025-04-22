from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import librosa
import numpy as np
import soundfile as sf

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def hello():
    return "Flask Audio Feature Extractor is running!"

@app.route('/extract-features', methods=['POST'])
def extract_features():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    filename = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    audio_file.save(filename)

    try:
        # Load audio file
        y, sr = librosa.load(filename, sr=None)

        # Tempo/BPM
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        bpm_val = float(tempo.item())  # Safe scalar extraction

        # Chroma Feature -> Scale Estimation
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        chroma_mean = np.mean(chroma, axis=1)
        scale = int(np.argmax(chroma_mean))

        # Pitch Tracking (for key)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        index = magnitudes.argmax()
        pitch_val = pitches.flatten()[index]
        key = round(float(pitch_val), 2) if pitch_val > 0 else 'Unknown'

        # Debug output
        print(f"Extracted Features - BPM: {bpm_val:.2f}, Key: {key}, Scale: {scale}")

        return jsonify({
            'bpm': round(bpm_val, 2),
            'key': key,
            'scale': scale
        })

    except Exception as e:
        print(f"Error during feature extraction: {e}")
        return jsonify({'error': f'Feature extraction failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
