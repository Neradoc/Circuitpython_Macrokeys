from .. import actions
from ..driver_base import KeypadBase

class KeypadModuleDriver(KeypadBase):
    def __init__(self, backend, pixels=None, play_tone=None):
        super().__init__(backend, pixels, play_tone)

    def do_macro(self, app):
        event = self.backend.events.get()
        if event:
            key_number = event.key_number
            if event.pressed:
                app.button_press(key_number)
            else:
                app.button_release(key_number)

