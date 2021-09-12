from .. import actions
from ..driver_base import KeypadBase


def num_to_col(c):
    return (c >> 16 & 0xFF, c >> 8 & 0xFF, c & 0xFF)


class KeybowDriver(KeypadBase):
    def __init__(self, backend):
        super().__init__(backend)
        self.night_mode = False

    def colors(self, incol):
        if isinstance(incol, int):
            return num_to_col(incol)
        if isinstance(incol, (tuple, list)) and len(incol) == 3:
            return incol
        raise ValueError("Wrong color value")

    def set_led(self, pos, color):
        print(pos, color, self.colors(color))
        self.backend.keys[pos].set_led(*self.colors(color))

    def fill_leds(self, color):
        self.backend.set_all(*self.colors(color))
