import mido
import random

# Create a new MIDI file
mid = mido.MidiFile()
track = mido.MidiTrack()
mid.tracks.append(track)

# Set tempo (120 BPM)
track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))

# Notes in C major
c_major_scale = [60,62,64,65,67,69,71]

# Generate 1-2 bars of melody
for _ in range(8):
    note = random.choice(c_major_scale)
    track.append(mido.Message('note_on', note=note, velocity=64, time=0))
    track.append(mido.Message('note_off', note=note, velocity=64, time=340))

# Save MIDI file
mid.save('random_melody.mid')
print("MIDI file saved as random_melody.mid")