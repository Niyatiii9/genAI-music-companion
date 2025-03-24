import mido

midi_out = mido.open_output()
midi_out.open_port(1)

def send_pitch_bend(value):
    """Send pitch bend message for smooth gliding effect."""
    bend_value = int((value + 1) * 8192)  # Convert -1 to 1 range into 0-16383
    lsb = bend_value & 0x7F  # Lower 7 bits
    msb = (bend_value >> 7) & 0x7F  # Upper 7 bits
    midi_out.send_message([0xE0, lsb, msb])  # Pitch Bend message