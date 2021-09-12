import os
import traceback
from . import actions
from .application import App


class KeypadBase:
    def __init__(self, backend):
        self.backend = backend
        self.night_mode = False
        self._on_switch = None

    @property
    def keyboard(self):
        return actions.common_keyboard

    def play_tone(self, note, duration):
        pass

    def set_led(self, pos, value):
        pass

    def show_leds(self):
        pass

    def fill_leds(self, color):
        pass

    def on_switch(self, callback):
        self._on_switch = callback

    def do_switch(self, prev_app, next_app):
        if callable(self._on_switch):
            self._on_switch(prev_app, next_app)
