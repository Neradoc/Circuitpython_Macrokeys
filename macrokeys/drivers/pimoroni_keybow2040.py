from ..driver_base import KeypadBase


def num_to_col(c):
    return (c >> 16 & 0xFF, c >> 8 & 0xFF, c & 0xFF)


class KeybowDriver(KeypadBase):
    def __init__(self, backend, macro_folder=None):
        super().__init__(backend, macro_folder)
        self.night_mode = False

    def colors(self, incol):
        if isinstance(incol, int):
            return num_to_col(incol)
        if isinstance(incol, (tuple, list)) and len(incol) == 3:
            return incol
        raise ValueError(f"Wrong color value: {repr(incol)}")

    def set_led(self, pos, color):
        self.backend.keys[pos].set_led(*self.colors(color))

    def fill_leds(self, color):
        self.backend.set_all(*self.colors(color))
