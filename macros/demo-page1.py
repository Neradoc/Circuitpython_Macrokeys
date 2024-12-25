# MACROPAD Hotkeys example: Universal Numpad
from macrokeys import *

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Test Macros', # Application name
    'macros' : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x00FF00, 'M', [ "hello", 0x30 ]),
        (0x00FF00, 'Hello', Type("Hello 123")),
        (0, 'Night', NightToggle()),
        (0xFFFF00, 'Yellow Page', Page.next),
        # 2nd row ----------
        (0xFF00FF, 'V-', Control("VOLUME_DECREMENT")),
        (0xFF00FF, 'V+', Control("VOLUME_INCREMENT")),
        (0x00FF00, 'Calc', Control(0x192)),
        (0x800000, 'Mash Space', MashKeys("SPACE")),
        # 3rd row ----------
        (0x0000FF, 'Holds', [ HoldKeys("SPACE"), HoldMouse(1) ]),
        (0x000080, 'Mashes', [ MashKeys("SPACE"), MashMouse(1) ]),
        (0x8888FF, 'Space', Shortcut("SPACE")),
        (0xFF0000, 'Hold Space', HoldKeys("SPACE")),
        # 4th row ----------
        (0x00FFFF, 'Click', Mouse(1)),
        (0x00FF00, 'wheel-', Mouse(wheel=-10)),
        (0x00FFFF, 'wheel+', Mouse(wheel=10)),
        (0x00FF00, 'Space', Shortcut("SPACE")),
    ],
}
