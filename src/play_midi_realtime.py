import time
import random
import mido
import rtmidi
from mido import MidiFile, MidiTrack, Message
from thaat_key import get_key_scale, key, scale
from ornaments import apply_ornament

midi_out = rtmidi.MidiOut()
midi_out.open_port(1)

key = key("C#4")
scale = scale("Asavari")
num_bars = 4
tonal_values = get_key_scale(key, scale)

# User-defined tempo (BPM)
BPM = 200

note_types = {
        "whole": 4,
        "half": 2,
        "quarter": 1,
        "eighth": 0.5,
        "sixteenth": 0.25
    }
# Define available note types
def note_duration(BPM,note_types):
    for note,beats in note_types.items():
        duration = (beats/BPM) * 60

        return duration

# MIDI File Setup
midi_file = MidiFile()
track = MidiTrack()
midi_file.tracks.append(track)

sequence = ["whole", "half", "quarter", "eighth", "sixteenth"]


# Genrate melody
for _ in range (num_bars):
    note = random.choice(tonal_values)
    velocity = random.randint(50, 100)
    # duration = random.choice([0.6,0.8,0.10])
    duration = 0.5
    # ornaments = random.choice(["grace", "andolan", "mordent", "murki", "meend", "gamak", "none"])
    ornaments = 'grace'
    apply_ornament(note, ornaments)

    # track.append(Message('note_on', note=note, velocity=velocity, time=int(duration * 480)))
    # time_selection = random.choice(sequence)
    note_types = 'quarter'
    final_time = note_duration[BPM,note_types]
    track.append(Message('note_on', note=note, velocity=velocity, time=final_time))
    track.append(Message('note_off', note=note, velocity=0, time=final_time))
    
# Save the MIDI file
midi_filename = ('latest_generated.mid')
midi_file.save(midi_filename)
print(f"MIDI file saved: {midi_filename}")


# Playing last generated MIDI file
def play_midi_file(filename):
    '''play a midi file in real time'''
    midi = MidiFile(filename)
    for msg in midi.play():
        if msg.type == 'note_on':
            midi_out.send_message([0x90, msg.note, msg.velocity])
        elif msg.type == 'note_off':
            midi_out.send_message([0x80, msg.note, msg.velocity])

print ("playing MIDI file")
play_midi_file(midi_filename)
print('Playback Completed')




# for note_type in sequence:
#     note = random.choice(tonal_values)
#     play_note(note, note_type)

# # Play a simple Yaman Raga phrase in real-time
# print ("playing live MIDI") 
# for _ in range(16):
#     note = random.choice(tonal_values)
#     velocity = random.randint(50, 100)
#     duration = random.choice([0.6,0.8,0.10])
#     play_note(note, duration, velocity)
# print('Done')