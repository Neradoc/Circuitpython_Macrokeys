from ..controller import ControlPad


class KeypadModuleDriver(ControlPad):
    def __init__(self, backend, macro_folder=None, pixels=None, play_tone=None):
        super().__init__(
            macro_folder=macro_folder,
            pixels=pixels,
            play_tone=play_tone,
        )
        self.backend = backend

    def update_keys(self):
        event = self.backend.events.get()
        if event:
            key_number = event.key_number
            if event.pressed:
                self.current.button_press(key_number)
            else:
                self.current.button_release(key_number)
