from .. import actions
from ..driver_base import KeypadBase

class MacroPadDriver(KeypadBase):
    def __init__(self, backend):
        super().__init__(backend)
        actions.play_tone = self.backend.play_tone

    def play_tone(self, note, duration):
        return self.backend.play_tone(note, duration)

    def set_led(self, pos, color):
        self.backend.pixels[pos] = color

    def show_leds(self):
        self.backend.pixels.show()

    def fill_leds(self, color):
        self.backend.pixels.fill(color)
