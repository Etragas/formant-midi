from formant_spec import ButtonSpec, JoystickSpec, NumericSpec

BUTTON_SPEC = [
    ButtonSpec(name='A', channel=0, note=57, velocity=127),
    ButtonSpec(name='B', channel=0, note=59, velocity=127),
    ButtonSpec(name='C', channel=0, note=60, velocity=127),
    ButtonSpec(name='D', channel=4, note=62, velocity=127),
    ButtonSpec(name='E', channel=0, note=64, velocity=127),
    ButtonSpec(name='F', channel=0, note=65, velocity=127),
    ButtonSpec(name='G', channel=0, note=67, velocity=127),
]

# Example stick that sends notes when moved left-right and velocities when moved up/down
JOYSTICK_SPEC = [
    JoystickSpec(name='joystick_a', channel = 1)
]


NUMERIC_SPEC = [
    NumericSpec(name='echo', channel = 2),
    NumericSpec(name='filter', channel = 3)
]

BUTTON_STREAM_NAMES = ['Buttons']
JOYSTICK_STREAM_NAMES = ['joystick_a']
NUMERIC_STREAM_NAMES = ['echo', 'filter']

BUTTON_LOOKUP = {v.name: v for v in BUTTON_SPEC}
JOYSTICK_LOOKUP = {v.name: v for v in JOYSTICK_SPEC}
NUMERIC_LOOKUP = {v.name: v for v in NUMERIC_SPEC}
STREAM_NAMES = BUTTON_STREAM_NAMES + JOYSTICK_STREAM_NAMES + NUMERIC_STREAM_NAMES

