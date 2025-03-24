import rtmidi

midi_out = rtmidi.MidiOut()
available_ports = midi_out.get_ports()

if available_ports:
    print('Available MIDI ports:')
    for i, p in enumerate(available_ports):
        print(f'{i}: {p}')
    else:
        print('No MIDI ports available')



# Select MIDI Output
# midi_out = rtmidi.MidiOut()
# available_ports = midi_out.get_ports()

# if available_ports:
#     midi_out.open_port(1)
#     print(f'Connected to MIDI port:{available_ports[0]}')
# else:
#     midi_out.open_virtual_port("My virtual output")
#     print('Connected to virtual MIDI port')