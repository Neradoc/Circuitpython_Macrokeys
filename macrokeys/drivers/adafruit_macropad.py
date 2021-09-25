from ..driver_base import KeypadBase

class MacroPadDriver(KeypadBase):
    def __init__(self, macropad, macro_folder=None):
        macropad.display.auto_refresh = False
        macropad.pixels.auto_write = False
        super().__init__(
            backend=macropad,
            macro_folder=macro_folder,
            play_tone=macropad.play_tone,
        )

    def play_tone(self, note, duration):
        return self.backend.play_tone(note, duration)

    def set_led(self, pos, color):
        if pos in range(12):
            self.backend.pixels[pos] = color

    def show_leds(self):
        self.backend.pixels.show()

    def fill_leds(self, color):
        self.backend.pixels.fill(color)
