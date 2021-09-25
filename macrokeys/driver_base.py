import os
import traceback
from . import actions
from .application import MacrosPage

MACRO_FOLDER = "/macros"

class KeypadBase():
    def __init__(self, backend, macro_folder=None, pixels=None, play_tone=None):
        self.backend = backend
        self.pixels = pixels
        if play_tone:
            actions.play_tone = play_tone
        self._on_switch = None
        self.init_macros(macro_folder or MACRO_FOLDER)

    @property
    def keyboard(self):
        return actions.common_keyboard

    def play_tone(self, note, duration):
        if self.play_tone:
            return self.play_tone(note, duration)

    def set_led(self, pos, color):
        try:
            self.pixels[pos] = color
        except:
            pass

    def show_leds(self):
        try:
            self.pixels.show()
        except:
            pass

    def fill_leds(self, color):
        try:
            self.pixels.fill(color)
        except:
            pass

    def set_leds(self, colors):
        for i, col in enumerate(colors):
            if col is not None:
                self.set_led(i, col)

    # use as a decorator
    def on_switch(self, callback):
        self._on_switch = callback

    def do_switch(self, prev_app, next_app):
        if callable(self._on_switch):
            self._on_switch(prev_app, next_app)

    def start(self):
        self.move_page(0)

    # this is the application part

    def init_macros(self, macro_folder):
        self.pages = []
        self.index = 0
        files = os.listdir(macro_folder)
        files.sort()
        for filename in files:
            if filename.endswith(".py") and filename[0] != ".":
                try:
                    module = __import__(macro_folder + "/" + filename[:-3])
                    self.pages.append(MacrosPage(self, module.app))
                except (
                    SyntaxError,
                    ImportError,
                    AttributeError,
                    KeyError,
                    NameError,
                    IndexError,
                    TypeError,
                ) as err:
                    traceback.print_exception(err, err, err.__traceback__)
        if not self.pages:
            raise ValueError("No macros found")

    @property
    def current(self):
        return self.pages[self.index]

    @property
    def page_count(self):
        return len(self.pages)

    @property
    def macro_count(self):
        return self.pages[self.index].macro_count

    def move_page(self, delta):
        last_page = self.pages[self.index]
        self.index = (self.index + delta) % len(self.pages)
        self.pages[self.index].switch(last_page)
