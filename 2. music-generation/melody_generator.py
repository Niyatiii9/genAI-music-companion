import random
from thaat_key import get_key_scale, key, scale
from ornaments import apply_ornament

note_types = {
    "whole": 4,
    "half": 2,
    "quarter": 1,
    "eighth": 0.5,
    "sixteenth": 0.25
}

def generate_melody(key_name, scale_name, num_bars, BPM):
    """Generates a MIDI melody with quantized timing."""
    tonal_values = get_key_scale(key(key_name), scale(scale_name))
    ticks_per_beat = int((60 / BPM) * 1000)
    
    melody_data = []
    current_time = 0

    for _ in range(num_bars * 4):  # Assuming 4 beats per bar
        note = random.choice(tonal_values)
        velocity = random.randint(50, 100)
        ornaments = "none"  # Change this to random.choice([...]) for variety
        apply_ornament(note, ornaments)

        note_type_selection = "whole"  # Change to random.choice([...]) for variety
        duration_in_beats = note_types[note_type_selection]
        final_time = int(duration_in_beats * ticks_per_beat)

        melody_data.append(("note_on", note, velocity, current_time))
        melody_data.append(("note_off", note, 0, current_time + final_time))
        
        current_time += final_time
    
    return melody_data
