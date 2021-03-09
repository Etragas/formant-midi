from formant_spec import ButtonSpec, JoystickSpec, NumericSpec

BUTTON_SPEC = [
    ButtonSpec(name='RUN', channel=0, note=0, velocity=0),
    ButtonSpec(name='STOP', channel=0, note=0, velocity=0),
    ButtonSpec(name='A', channel=1, note=57, velocity=127),
    ButtonSpec(name='B', channel=1, note=59, velocity=127),
    ButtonSpec(name='C', channel=1, note=60, velocity=127),
    ButtonSpec(name='D', channel=1, note=62, velocity=127),
    ButtonSpec(name='E', channel=1, note=64, velocity=127),
    ButtonSpec(name='F', channel=1, note=65, velocity=127),
    ButtonSpec(name='G', channel=1, note=67, velocity=127),
]

# Example stick that sends notes when moved left-right and velocities when moved up/down
JOYSTICK_SPEC = [
    JoystickSpec(name='joystick_a', channel = 2)
]


NUMERIC_SPEC = [
    NumericSpec(name='bpm', channel = 0),
    NumericSpec(name='echo', channel = 3),
    NumericSpec(name='filter', channel = 4),
    NumericSpec(name='Octave', channel = 5),
    NumericSpec(name='Legato', channel = 6),
    NumericSpec(name='war-peace', channel = 7),
    NumericSpec(name='deep-crispy', channel = 8)
]

BUTTON_STREAM_NAMES = ['Buttons']
JOYSTICK_STREAM_NAMES = [spec.name for spec in JOYSTICK_SPEC]
NUMERIC_STREAM_NAMES = [spec.name for spec in NUMERIC_SPEC]


BUTTON_LOOKUP = {v.name: v for v in BUTTON_SPEC}
JOYSTICK_LOOKUP = {v.name: v for v in JOYSTICK_SPEC}
NUMERIC_LOOKUP = {v.name: v for v in NUMERIC_SPEC}
STREAM_NAMES = BUTTON_STREAM_NAMES + JOYSTICK_STREAM_NAMES + NUMERIC_STREAM_NAMES

