import time
import rtmidi
import mido
from formant.sdk.agent.v1 import Client as FC

max_midi_val = 0b01111111 # 127, midi reserves leading 1 in all bytes

debug_logging = True
# Constants
temp = .1
button_to_key = {
        'Boop': 60,
        'C': 60,
        'D': 62,
        'E': 64,
        }

# This queue stores every teleop command received from the formant client
# Each time a command is received, it is pushed on to the command queue
# The midi control loop will then consume these commands and send them to the synth
command_queue = []

def print_dbg(s: str) -> None:
    if debug_logging:
        print(s)

def assert_midi_val(name: str, val: int) -> None:
    assert (val <= max_midi_val), (f'{name} with value {val} exceeds max_midi_val of {max_midi_val}')

# TODO(etragas) Unify the Pitch and Note classes
class Pitch():
    def __init__(self, msb: int, lsb: int):
        assert_midi_val('msb', msb)
        assert_midi_val('lsb', lsb)
        self.msb = msb 
        self.lsb = lsb 

class Note():
    def __init__(self, key: int, tempo: float = temp):
        assert_midi_val('key', note_val)
        self.key = note_val
        self.tempo = tempo
    
    @property
    def velocity(self):
        # TODO(etragas) Make this adjustable
        return 127
    
    @property
    def channel(self):
        return 0x90


def teleop_callback(datapoint):
    if datapoint.stream == "Buttons":
        print_dbg(datapoint)
        # For loop in case multiple buttons are pressed concurrently
        for bit in datapoint.bitset.bits:
            key = button_to_key[bit.key]
            command_queue.append(Note(key))
    if datapoint.stream == "Stick":
        print_dbg(datapoint.twist.linear)
        joy_y = datapoint.twist.linear.y
        msb = 63 + (joy_y * 63) # Ranges from 0 - 126

        joy_z = datapoint.twist.linear.z
        lsb = 63 + (joy_z * 63) # Ranges from 0 - 126

        command_queue.append(Pitch(lsb, msb))
    print_dbg("point received")

fc_client = FC()
fc_client.register_teleop_callback(teleop_callback, ["Buttons", "Stick"])

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

# TODO(etragas) Generalize to other synths besides Arturia
arturia_port = [x for x in available_ports if 'Arturia' in x]
assert(len(arturia_port) == 1)
arturia_port = arturia_port[0]
port_int = available_ports.index(arturia_port)
midiout.open_port(port_int)
print_dbg(midiout)

with midiout:
    # Set all note volumes to 0
    for key_val in range(128):
        off = [144, key_val, 0]
        midiout.send_message(off)
    while 1:
        if command_queue:
            note = command_queue.pop(0)
            # TODO(etragas) Unify PItch and Note cases
            if isinstance(note, Note):
                #TODO(etragas) Instead of sleeping and sending note_off, can we send a note with time in it?
                note_on = [note.channel, note.key, note.velocity] # channel 1, middle C, velocity 112
                print_dbg(note_on)
                midiout.send_message(note_on)
                time.sleep(tempo)
                note_off = [note.channel, note.key, 0]
                midiout.send_message(note_off)
            elif isinstance(note, Pitch):
                msb, lsb = note.msb, note.lsb
                pitch_set= [0xE0, lsb, msb] # channel 1, middle C, velocity 112
                midiout.send_message(pitch_set)


            time.sleep(0.01)
