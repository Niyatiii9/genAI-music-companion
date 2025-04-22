from melody_generator import generate_melody
from midi_utils import create_midi_file, play_midi_file, save_last_midi

# User-defined settings
key_name = "C#4"
scale_name = "Bhairav"
num_bars = 1
BPM = 200

# Generate melody
melody_data = generate_melody(key_name, scale_name, num_bars, BPM)

# Create and play MIDI file
midi_filename = create_midi_file(melody_data)
print("Playing MIDI file...")
play_midi_file(midi_filename)
print("Playback Completed")

# Ask user if they want to save the MIDI file
save_input = input("Save this melody? (y/n): ").strip().lower()
if save_input == "y":
    save_last_midi()
