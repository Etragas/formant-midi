""" Use this file to define how formant-midi should treat tele-op messages. """

NOTE = 'note'
VELOCITY = 'velocity'

class ButtonSpec():
    """ Defines a mapping between a formant button and midi output.

    Velocity is always 127 for buttons.

    Args:
        name: Name of the formant button
        channel: Midi channel to output to
        note: The note to emit
        velocity: The velocity to emit
    """
    def __init__(self, name: str, channel: int, note: int, velocity: int):
        self.name = name
        self.channel = 0x90 + channel
        self.note = note
        self.velocity = velocity

BUTTON_SPEC = [
    ButtonSpec(name='A', channel=0, note=57, velocity=127),
    ButtonSpec(name='B', channel=0, note=59, velocity=127),
    ButtonSpec(name='C', channel=0, note=60, velocity=127),
    ButtonSpec(name='D', channel=0, note=62, velocity=127),
    ButtonSpec(name='E', channel=0, note=64, velocity=127),
    ButtonSpec(name='F', channel=0, note=65, velocity=127),
    ButtonSpec(name='G', channel=0, note=67, velocity=127),
]

class JoystickSpec():
    """ Defines a mapping between a formant joystick and midi output

    Joysticks always output values ranging from 0-127, with a neutral joystick position corresponding to note 63
    Left-Right movement always emits Notes and Up-Down always emites Velocities
    Args:
        name: Name of the formant stick
        channel: What channel to emit values on
    """
    def __init__(self, name: str, channel: int):
        self.name = name
        self.channel = 0x90 + channel

# Example stick that sends notes when moved left-right and velocities when moved up/down
JOYSTICK_SPEC = [
    JoystickSpec(name='Stick', channel = 1)
]

BUTTON_LOOKUP = {v.name: v for v in BUTTON_SPEC}
JOYSTICK_LOOKUP = {v.name: v for v in JOYSTICK_SPEC}