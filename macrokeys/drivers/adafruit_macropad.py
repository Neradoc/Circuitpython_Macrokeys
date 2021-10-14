from ..controller import ControlPad


class MacroPadDriver(ControlPad):
    def __init__(self, macropad, macro_folder=None):
        macropad.display.auto_refresh = False
        macropad.pixels.auto_write = False
        super().__init__(
            macro_folder=macro_folder,
            play_tone=macropad.play_tone,
            play_file=macropad.play_file,
        )
        self.macropad = macropad

    def play_tone(self, note, duration):
        return self.macropad.play_tone(note, duration)

    def set_led(self, pos, color):
        if pos in range(12):
            self.macropad.pixels[pos] = color

    def show_leds(self):
        self.macropad.pixels.show()

    def fill_leds(self, color):
        self.macropad.pixels.fill(color)
