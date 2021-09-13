import os
import traceback
from . import actions
from .application import App


class KeypadBase:
    def __init__(self, backend, pixels=None, play_tone=None):
        self.backend = backend
        self.night_mode = False
        self.pixels = pixels
        if play_tone:
            actions.play_tone = play_tone
        self._on_switch = None

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

    def on_switch(self, callback):
        self._on_switch = callback

    def do_switch(self, prev_app, next_app):
        if callable(self._on_switch):
            self._on_switch(prev_app, next_app)
