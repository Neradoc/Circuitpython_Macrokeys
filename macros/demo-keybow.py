# MACROPAD Hotkeys example: Universal Numpad
from macrokeys import *

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Test Macros', # Application name
    'macros' : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0, 'Click', Mouse(1)),
        (0, 'wheel-', Mouse(wheel=-10)),
        (0, 'wheel+', Mouse(wheel=10)),
        (0, 'Space', Shortcut("SPACE")),
        # 2nd row ----------
        (0, 'V-', Control("VOLUME_DECREMENT")),
        (0, 'V+', Control("VOLUME_INCREMENT")),
        (0, 'Calc', Control(0x192)),
        (0, 'Space', Shortcut("SPACE")),
        # 3rd row ----------
        (0, 'Space', Shortcut("SPACE")),
        (0, 'Space', Shortcut("SPACE")),
        (0, 'Space', Shortcut("SPACE")),
        (0, 'Space', Shortcut("SPACE")),
        # 4th row ----------
        (0, 'a', Shortcut("A")),
        (0, 'M', [ "hello", 0x30 ]),
        (0, 'Hello', Type("Hello 123")),
        (0, 'Space', Shortcut("SPACE")),
    ],
}
