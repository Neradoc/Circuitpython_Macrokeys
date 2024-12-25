# MACROPAD Hotkeys example: Universal Numpad
from macrokeys import *

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Test Macros', # Application name
    'macros' : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0xFFFF00, 'a', Shortcut("A")),
        (0xFFFF00, 'M', [ "hello", 0x30 ]),
        (0xFFFF00, 'Hello', Type("Hello 123")),
        (0x00FF00, 'Green Page', Page(0)),
        # 2nd row ----------
        (0xFFFF00, 'V-', Control("VOLUME_DECREMENT")),
        (0xFFFF00, 'V+', Control("VOLUME_INCREMENT")),
        (0xFFFF00, 'Calc', Control(0x192)),
        (0xFFFF00, 'Space', Shortcut("SPACE")),
        # 3rd row ----------
        (0xFFFF00, 'Space', Shortcut("SPACE")),
        (0xFFFF00, 'Space', Shortcut("SPACE")),
        (0xFFFF00, 'Space', Shortcut("SPACE")),
        (0xFFFF00, 'Space', Shortcut("SPACE")),
        # 4th row ----------
        (0x00FFFF, 'Click', Mouse(1)),
        (0xFFFF00, 'wheel-', Mouse(wheel=-10)),
        (0x00FFFF, 'wheel+', Mouse(wheel=10)),
        (0xFFFF00, 'Space', Shortcut("SPACE")),
    ],
}
