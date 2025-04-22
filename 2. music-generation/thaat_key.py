def get_key_scale(note_name, scale_name):
    """
    Convert a manually provided Thaat (as relative MIDI steps) into actual MIDI notes.
    
    :param root_midi: The MIDI number of the root note.
    :param custom_intervals: Manually entered list of MIDI steps.
    :return: List of MIDI note numbers.
    """
    return [note_name + interval for interval in scale_name]

def key(note_name):
    midi_mapping = {
        "C4": 60, "C#4": 61, "D4": 62, "D#4": 63, "E4": 64, "F4": 65,
        "F#4": 66, "G4": 67, "G#4": 68, "A4": 69, "A#4": 70, "B4": 71
    }

    return midi_mapping[note_name]

def scale(scale_name):
    thaat_dict = {
        "Bilawal": [0, 2, 4, 5, 7, 9, 11],   # Major Scale (Ionian)
        "Kalyan": [0, 2, 4, 6, 7, 9, 11],    # Lydian
        "Khamaj": [0, 2, 4, 5, 7, 9, 10],    # Mixolydian
        "Bhairav": [0, 1, 4, 5, 7, 8, 11],   # Phrygian ♮4
        "Bhairavi": [0, 1, 3, 5, 7, 8, 10],  # Phrygian
        "Asavari": [0, 2, 3, 5, 7, 8, 10],   # Natural Minor (Aeolian)
        "Todi": [0, 1, 3, 6, 7, 8, 11],      # Augmented Phrygian
        "Purvi": [0, 1, 4, 6, 7, 8, 11],     # Similar to Todi but major third
        "Marwa": [0, 1, 4, 6, 7, 9, 11],     # Similar to Purvi but different Ni
        "Kaafi": [0, 2, 3, 5, 7, 9, 10]      # Dorian
    }
    return thaat_dict[scale_name]

