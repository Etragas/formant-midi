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
    def __init__(self, name: str, channel: int, note: int, velocity: int, tempo: float = 0.001):
        self.name = name
        self.channel = 0x90 + channel - 1
        self.note = note
        self.velocity = velocity
        self.tempo = tempo

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
        self.channel = 0x90 + channel - 1

class NumericSpec():
    """ Defines a mapping between a formant numeric stream and midi output

    Sliders and dials always output values from 0-127, with a center value of 63

    Args:
        name: Name of the numeric stream
        channel: What channel to emit values on
    """
    def __init__(self, name: str, channel: int):
        self.name = name
        self.channel = 0x90 + channel - 1

class NumericNoteSpec(NumericSpec):
    pass
class NumericVelocitySpec(NumericSpec):
    pass
