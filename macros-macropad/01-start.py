# MACROPAD Hotkeys example: Universal Numpad
from macrokeys import *
import time

def onoff(app, key, idx):
    app.toggle_night_mode()
    app.macro_keypad.backend.group.hidden = app.night_mode
    app.macro_keypad.backend.display.refresh()

beep = Tone(("C6", 0.08), 0.05, ("E6", 0.10))

def entering(pad, prev_app, next_app):
    beep.action()

def leaving(pad, prev_app, next_app):
    next_app.toggle_night_mode(False)
    pad.backend.group.hidden = False
    pad.backend.display.refresh()

def die(*argv, **kwargv):
    raise OSError("Testing Exceptions")

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Test Macros', # Application name
    'enter' : entering,
    'leave' : leaving,
    'macros' : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x202000, 'Click', Mouse(1)),
        (0x202000, 'wheel-', Mouse(wheel=-10)),
        (0x202000, 'Die', die),
        # 2nd row ----------
        (0x202000, 'V-', Control("VOLUME_DECREMENT")),
        (0x202000, 'V+', Control("VOLUME_INCREMENT")),
        (0x202000, 'Calc', Control(0x192)),
        # 3rd row ----------
        (0x202000, 'Beep',
            [
                Tone( ("A4", 0.5) ),
                Tone( ("A5", 0.5) ),
            ]
        ),
        (0x202000, 'Tadah', Tone(
            ("A5", 0.2), 0.2,
            ("B5", 0.2), ("C6", 0.2), 0.2,
            ("D6", 0.2), ("D#6", 0.2)
        ) ),
        (0x202000, 'Arpg', Tone(
            ("C6", 0.2), ("E6", 0.2), ("G6", 0.2), ("C7", 0.2),
            ("G6", 0.2), ("E6", 0.2), ("C6", 0.5),
        ) ),
        # 4th row ----------
        (0x101010, 'a', Shortcut("A")),
        (0x800000, 'M', [ "hello", 0x30 ]),
        (0x101010, 'Hello', Type("Hello 123")),
        # Encoder button ---
        (0x000000, '', onoff)
    ],
}
