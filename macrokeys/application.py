import os
import traceback
from . import actions


class MacrosPage:
    """
    Class representing a host-side application, for which we have a set
    of macro sequences.
    """
    fidget_mode = False
    night_mode = False

    def __init__(self, macro_keypad, page_data):
        self.macro_keypad = macro_keypad
        self.name = page_data["name"]
        self.macros = page_data["macros"]
        self.colors = [item[0] for item in self.macros]
        self._enter = None
        if "enter" in page_data and callable(page_data["enter"]):
            self._enter = page_data["enter"]
        self._leave = None
        if "leave" in page_data and callable(page_data["leave"]):
            self._leave = page_data["leave"]

    @property
    def macro_count(self):
        return len(self.macros)

    def switch(self, prev_app=None):
        """Activate application settings."""
        # the previous app's "leave" custom code
        if prev_app and prev_app._leave:
            prev_app._leave(pad=self.macro_keypad, prev_app=prev_app, next_app=self)
        # set the LEDs
        if not self.night_mode:
            self.macro_keypad.set_leds(self.colors)
        # do the switch
        self.macro_keypad.do_switch(prev_app, self)
        # the current app's "enter" custom code
        if self._enter:
            self._enter(pad=self.macro_keypad, prev_app=prev_app, next_app=self)

    def button_press(self, key_number):
        # the sequence is arbitrary-length
        # each item in the sequence is either
        # an action instance or a floating point value
        # Action   ==>  execute the action
        # Float    ==>  sleep in seconds
        # Function ==>  call it with context
        sequence = self.macros[key_number][2]
        if not isinstance(sequence, (list, tuple)):
            sequence = (sequence,)
        # light the matching LED
        # TODO: this should be a parametrised value
        if not self.night_mode:
            self.macro_keypad.set_led(key_number, 0xFFFFFF)
            self.macro_keypad.show_leds()
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
                if not self.night_mode:
                    self.macro_keypad.set_led(key_number, item.color)
                    self.macro_keypad.show_leds()
            elif callable(item):
                item(app=self, key=key_number, idx=index)
            elif isinstance(item, int):
                # compatibility
                if item > 0:
                    self.macro_keypad.keyboard.press(item)
                else:
                    self.macro_keypad.keyboard.release(item)
            elif isinstance(item, str):
                # compatibility
                actions.layout.write(item)
            else:
                print("Unkown action", item)

    def button_release(self, key_number):
        sequence = self.macros[key_number][2]
        if not isinstance(sequence, (list, tuple)):
            sequence = (sequence,)
        # Release any still-pressed keys
        for item in sequence:
            if isinstance(item, actions.MacroAction):
                item.release()
            # compatibility
            if isinstance(item, int) and item >= 0:
                self.macro_keypad.keyboard.release(item)
        if not self.night_mode:
            self.macro_keypad.set_led(key_number, self.macros[key_number][0])
            self.macro_keypad.show_leds()

    def toggle_night_mode(self, value=None):
        if isinstance(value, bool):
            self.night_mode = value
        else:
            self.night_mode = not self.night_mode
        if self.night_mode:
            self.macro_keypad.fill_leds(0)
        else:
            self.macro_keypad.set_leds(self.colors)
        self.macro_keypad.show_leds()
