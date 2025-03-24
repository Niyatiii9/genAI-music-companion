import time
import random
import rtmidi

def send_pitch_bend(value):
    """Send pitch bend message for smooth gliding effect."""
    bend_value = int((value + 1) * 8192)  # Convert -1 to 1 range into 0-16383
    lsb = bend_value & 0x7F  # Lower 7 bits
    msb = (bend_value >> 7) & 0x7F  # Upper 7 bits
    midi_out.send_message([0xE0, lsb, msb])  # Pitch Bend message

midi_out = rtmidi.MidiOut()
midi_out.open_port(1)

def grace_note(note, velocity=90, duration=0.1): #Grace Note
    """Play a grace note just before the main note."""
    grace = note - 1  # One step below as a grace note
    midi_out.send_message([0x90, grace, velocity])
    time.sleep(duration)
    midi_out.send_message([0x80, grace, 0])

def andolan(note, velocity=90, duration=0.1): #Vibrato or Slow Oscillation
    midi_out.send_message([0x90, note, velocity])
    for i in range(4): #Slow wavering
        send_pitch_bend((-1)**i * 0.2)
        time.sleep(duration / 10)
    send_pitch_bend(0)  # Reset pitch bend
    time.sleep(duration)
    midi_out.send_message([0x80, note, 0])

def mordent(note, velocity=90, duration=0.1):
    """Quick alternation between the note and the one above."""
    upper = note + 1  # One step above
    midi_out.send_message([0x90, note, velocity])
    time.sleep(duration)
    midi_out.send_message([0x90, upper, velocity])
    time.sleep(duration)
    midi_out.send_message([0x80, upper, 0])
    time.sleep(duration)
    midi_out.send_message([0x80, note, 0])

def meend(note1, note2, steps=5, velocity=90, duration=0.4): #Pitch Glide Effect
    """Glide smoothly from note1 to note2 using pitch bends."""
    interval = (note2 - note1) / steps
    for i in range(steps):
        midi_out.send_message([0x90, int(note1 + i * interval), velocity])
        time.sleep(duration / steps)
        midi_out.send_message([0x80, int(note1 + i * interval), 0])

def gamak(note, velocity=90, duration=0.3, oscillations=3): #Rapid Oscillation
    """Oscillate between two close notes rapidly."""
    lower = note - 1
    upper = note + 1
    for _ in range(oscillations):
        midi_out.send_message([0x90, upper, velocity])
        time.sleep(duration / (2 * oscillations))
        midi_out.send_message([0x90, lower, velocity])
        time.sleep(duration / (2 * oscillations))
    midi_out.send_message([0x90, note, velocity])
    time.sleep(duration)
    midi_out.send_message([0x80, note, 0])

def murki(note, velocity=90, duration=0.1): #Quick Flourish
    murti_notes = [note-1,note+1, note]
    for murki_note in murti_notes:
        midi_out.send_message([0x90, murki_note, velocity])
        time.sleep(duration/10)
        midi_out.send_message([0x80, murki_note, 0])
    time.sleep(duration/2)

def apply_ornament(note, ornament_type):
    """Apply the selected ornament type."""
    if ornament_type == "grace":
        grace_note(note)
    elif ornament_type == "mordent":
        mordent(note)
    elif ornament_type == "meend":
        next_note = note + random.choice([-2, 2])  # Small glide up/down
        meend(note, next_note)
    elif ornament_type == "gamak":
        gamak(note)
    elif ornament_type == "murki":
        murki(note)
    else:
        pass  # No ornament applied
