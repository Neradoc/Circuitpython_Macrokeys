import board
import neopixel
from macrokeys.controller import ControlPad


def num_to_col(c):
    return (c >> 16 & 0xFF, c >> 8 & 0xFF, c & 0xFF)


class RGBKeypadDriver(ControlPad):
    def __init__(self, keybow, macro_folder=None):
        super().__init__(macro_folder)
        self.key = keybow.keys
        self.keybow = keybow
        self.night_mode = False

        self.status_led = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.05)
        self.status_led.fill(0)

        macro_keypad = self

        # Attach handler functions to all of the keys
        for key in keybow.keys:

            @keybow.on_press(key)
            def press_handler(key):
                macro_keypad.current.button_press(key.number)

            @keybow.on_release(key)
            def release_handler(key):
                macro_keypad.current.button_release(key.number)


    def colors(self, incol):
        if isinstance(incol, int):
            return num_to_col(incol)
        if isinstance(incol, (tuple, list)) and len(incol) == 3:
            return incol
        raise ValueError(f"Wrong color value: {repr(incol)}")

    def set_led(self, pos, color):
        self.keybow.keys[pos].set_led(*self.colors(color))

    def fill_leds(self, color):
        self.keybow.set_all(*self.colors(color))

    @property
    def brightness(self):
        return self.keybow.hardware._display._pixels.brightness

    @brightness.setter
    def brightness(self, value):
        self.keybow.hardware._display._pixels.brightness = value
        self.keybow.hardware._display._pixels.show()

    def update(self):
        self.keybow.update()
