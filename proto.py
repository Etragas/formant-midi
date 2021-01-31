from typing import List

import time
import rtmidi
import mido
from formant.sdk.agent.v1 import Client as FC
from formant_spec import  ButtonSpec, JoystickSpec
from config import BUTTON_LOOKUP, JOYSTICK_LOOKUP, STREAM_NAMES, BUTTON_STREAM_NAMES, JOYSTICK_STREAM_NAMES

# Constants
max_channel_val = 0x90# Chanenls range from 0-15
max_channel_val = 0x90 + 15 # Chanenls range from 0-15
max_midi_val = 0b01111111 # 127, midi reserves leading 1 in all bytes
debug_logging = True
message_polling_rate = .01 # How often we check for a message from formant api

# This queue stores every teleop command received from the formant client
# Each time a command is received, it is pushed on to the command queue
# The midi control loop will then consume these commands and send them to the synth

def print_dbg(s: str) -> None:
    if debug_logging:
        print(s)

def assert_midi_channel(name: str, val: int) -> None:
    assert (val <= max_channel_val), (f'{name} with value {val} exceeds max_channel_val of {max_channel_val}')

def assert_midi_val(name: str, val: int) -> None:
    assert (val <= max_midi_val), (f'{name} with value {val} exceeds max_midi_val of {max_midi_val}')

class MidiMessage():
    def __init__(self, channel: int, note: int, velocity: int, tempo: float = 0.1):
        assert_midi_channel('channel', channel)
        assert_midi_val('note', note)
        assert_midi_val('velocity', velocity)
        self.channel = channel
        self.note = note
        self.velocity = velocity
        self.tempo = tempo


def message_from_button_spec(spec: ButtonSpec) -> MidiMessage:
    return MidiMessage(spec.channel, spec.note, spec.velocity)

def message_from_joystick_spec(spec: JoystickSpec) -> MidiMessage:
    # TODO(etragas) What are the stick names?
    print_dbg(datapoint.twist.linear)
    joy_z = datapoint.twist.linear.z
    note = int(63 + (joy_z * 63)) # Ranges from 0 - 126

    joy_y = datapoint.twist.linear.y
    velocity= int(63 + (joy_y * 63)) # Ranges from 0 - 126

    return MidiMessage(channel=spec.channel, note=note, velocity=velocity)

message_queue = []
# rhcp = ['E', 'E', 'D', 'E', 'E', 'E', 'E', 'D', 'E', 'E', 'E', 'E', 'D', 'E', 'D', 'D', 'D', 'D', 'E', 'D', 'D', 'D', 'D'] * 4
# message_queue.extend([message_from_button_spec(BUTTON_LOOKUP.get(note)) for note in rhcp])

def midi_messages_from_formant(datapoint) -> List[MidiMessage]: # TODO(etragas) typehint formant dp
    # Get the spec for the datapoint
    # Use the spec to make a message and return it
    messages = []
    print_dbg('--- Parsing datapoint ---')
    print_dbg(datapoint)
    if datapoint.stream in BUTTON_STREAM_NAMES:
        for bit in datapoint.bitset.bits:
            spec = BUTTON_LOOKUP.get(bit.key)
            if spec is None:
                print_dbg('No spec for datapoint')
                return []
            messages.append(message_from_button_spec(spec))
    elif datapoint.stream in JOYSTICK_STREAM_NAMES:
        stick_name = datapoint.stream
        print_dbg(f' Looking up stick w name: {stick_name}')
        spec = JOYSTICK_LOOKUP.get(stick_name)
        if spec is None:
            print_dbg('No spec for datapoint')
            return []
        messages.append(message_from_joystick_spec(spec))
    else: 
        print_dbg('Unknown stream for datapoint')
    return messages

def teleop_callback(datapoint):
    messages = midi_messages_from_formant(datapoint)
    message_queue.extend(messages)

print_dbg('Listening to the following streams')
print_dbg(STREAM_NAMES)

fc_client = FC()
fc_client.register_teleop_callback(teleop_callback, STREAM_NAMES)

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

# TODO(etragas) Generalize to other synths besides Arturia
arturia_port = [x for x in available_ports if 'Arturia' in x or 'POLY' in x]
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
        if message_queue:
            message = message_queue.pop(0)
            # TODO(etragas) Instead of sleeping and sending note_off, can we send a note with time in it?
            note_on = [message.channel, message.note, message.velocity] # channel 1, middle C, velocity 112
            print_dbg(note_on)
            midiout.send_message(note_on)
            time.sleep(message.tempo)
            note_off = [message.channel, 0, 0]
            midiout.send_message(note_off)
            time.sleep(message_polling_rate)

        for key_val in range(128):
            off = [144, key_val, 0]
            midiout.send_message(off)