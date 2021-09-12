import os
import traceback
from . import actions
from .application import App

class KeypadBase():
    def __init__(self, backend):
        self.backend = backend
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

    def load_apps(self, macro_folder):
        apps = []
        files = os.listdir(macro_folder)
        files.sort()
        for filename in files:
            if filename.endswith('.py') and filename[0] != ".":
                try:
                    module = __import__(macro_folder + '/' + filename[:-3])
                    apps.append(App(self, module.app))
                except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                        IndexError, TypeError) as err:
                    traceback.print_exception(err, err, err.__traceback__)
        return apps

    def button_press(self, key_number, macros):
        # the sequence is arbitrary-length
        # each item in the sequence is either
        # an action instance or a floating point value
        # Action   ==>  execute the action
        # Float    ==>  sleep in seconds
        # Function ==>  call it with context
        sequence = macros[2]
        if not isinstance(sequence, (list, tuple)):
            sequence = (sequence,)
        if key_number < 12: # No pixel for encoder button
            self.set_led(key_number, 0xFFFFFF)
            self.show_leds()
        for index, item in enumerate(sequence):
            if item == 0:
                for item in sequence:
                    if isinstance(item, actions.MacroAction):
                        item.release()
            elif isinstance(item, actions.MacroAction):
                item.action()
            elif isinstance(item, float):
                time.sleep(item)
            elif isinstance(item, actions.Color):
                self.set_led(key_number, item.color)
                self.show_leds()
            elif callable(item):
                item(pad=self, key=key_number, idx=index)
            elif isinstance(item, int):
                # compatibility
                if item > 0:
                    self.keyboard.press(item)
                else:
                    self.keyboard.release(item)
            elif isinstance(item, str):
                # compatibility
                actions.layout.write(item)
            else:
                print("Unkown action", item)


    def button_release(self, key_number, macros):
        sequence = macros[2]
        if not isinstance(sequence, (list, tuple)):
            sequence = (sequence,)
        # Release any still-pressed keys
        for item in sequence:
            if isinstance(item, actions.MacroAction):
                item.release()
            # compatibility
            if isinstance(item, int) and item >= 0:
                self.keyboard.release(item)
        if key_number < 12: # No pixel for encoder button
            self.set_led(key_number, macros[0])
            self.show_leds()

