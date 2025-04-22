import rtmidi
from mido import MidiFile, MidiTrack, Message

midi_out = rtmidi.MidiOut()
midi_out.open_port(1)

def create_midi_file(melody_data, filename="temp_generated.mid"):
    """Creates a MIDI file from melody data."""
    midi_file = MidiFile()
    track = MidiTrack()
    midi_file.tracks.append(track)

    for event_type, note, velocity, time in melody_data:
        msg_type = 'note_on' if event_type == "note_on" else 'note_off'
        track.append(Message(msg_type, note=note, velocity=velocity, time=time))

    midi_file.save(filename)
    return filename

def play_midi_file(filename):
    """Plays a MIDI file in real-time."""
    midi = MidiFile(filename)
    for msg in midi.play():
        if msg.type in ["note_on", "note_off"]:
            midi_out.send_message([0x90 if msg.type == "note_on" else 0x80, msg.note, msg.velocity])

def save_last_midi(saved_filename="latest_saved.mid"):
    """Saves the last played MIDI permanently if the user wants."""
    import shutil
    shutil.copy("temp_generated.mid", saved_filename)
    print(f"Saved last played MIDI as: {saved_filename}")