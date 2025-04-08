import mido

midi_file = 'random_melody.mid'
# Example function to adjust MIDI notes based on a raga
def adjust_midi_to_raga(midi_file, raga_notes):
    mid = mido.MidiFile(midi_file)
    output = mido.MidiFile()

    for track in mid.tracks:
        new_track = mido.MidiTrack()
        for msg in track:
            if msg.type == 'note_on'and msg.note % 12 not in raga_notes:
                msg.note = min(raga_notes, key=lambda x:abs(x-msg.note % 12))
            new_track.append(msg)
            output.tracks.append(new_track)

        output.save("adjusted_"+midi_file)
        print(f"Processed MIDI saved as adjusted_{midi_file}")


# Define a raga scale (Example: Raga Yaman)
raga_yaman = [0,2,4,6,7,9,11] # C D E F# G A B

# Run the conversion
adjust_midi_to_raga("random_melody.mid", raga_yaman)