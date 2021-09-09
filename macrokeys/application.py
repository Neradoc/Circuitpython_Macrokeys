import os
import traceback
from . import actions

class App:
    """ Class representing a host-side application, for which we have a set
        of macro sequences. Project code was originally more complex and
        this was helpful, but maybe it's excessive now?"""
    def __init__(self, macropad, appdata):
        self.macropad = macropad
        self.name = appdata['name']
        self.macros = appdata['macros']
        self._enter = None
        if "enter" in appdata and callable(appdata['enter']):
            self._enter = appdata['enter']
        self._leave = None
        if "leave" in appdata and callable(appdata['leave']):
            self._leave = appdata['leave']


    def switch(self, prev_app=None):
        """ Activate application settings; update OLED labels and LED
            colors. """
        # the previous app's "leave" custom code
        if prev_app and prev_app._leave:
            prev_app._leave(pad=self.macropad, prev_app=prev_app, next_app=self)
        # do the switch
        self.macropad.group[13].text = self.name   # Application name
        for i in range(12):
            if i < len(self.macros): # Key in use, set label + LED color
                self.macropad.pixels[i] = self.macros[i][0]
                self.macropad.group[i].text = self.macros[i][1]
            else:  # Key not in use, no label or LED
                self.macropad.pixels[i] = 0
                self.macropad.group[i].text = ''
        self.macropad.keyboard.release_all()
        self.macropad.consumer_control.release()
        self.macropad.mouse.release_all()
        self.macropad.stop_tone()
        self.macropad.pixels.show()
        self.macropad.display.refresh()
        # the current app's "enter" custom code
        if self._enter:
            self._enter(pad=self.macropad, prev_app=prev_app, next_app=self)


def load_apps(macropad, MACRO_FOLDER):
    apps = []
    files = os.listdir(MACRO_FOLDER)
    files.sort()
    for filename in files:
        if filename.endswith('.py') and filename[0] != ".":
            try:
                module = __import__(MACRO_FOLDER + '/' + filename[:-3])
                apps.append(App(macropad, module.app))
            except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                    IndexError, TypeError) as err:
                traceback.print_exception(err, err, err.__traceback__)
    return apps


def button_press(macropad, key_number, macros):
    # the sequence is arbitrary-length
    # each item in the sequence is either
    # an action instance or a floating point value
    # Action   ==>  execute the action
    # Float    ==>  sleep in seconds
    # Funciton ==>  call it with context
    sequence = macros[2]
    if not isinstance(sequence, (list, tuple)):
        sequence = (sequence,)
    if key_number < 12: # No pixel for encoder button
        macropad.pixels[key_number] = 0xFFFFFF
        macropad.pixels.show()
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
            macropad.pixels[key_number] = item.color
        elif callable(item):
            item(pad=macropad, key=key_number, idx=index)
        elif isinstance(item, int):
            # compatibility
            if item > 0:
                macropad.keyboard.press(item)
            else:
                macropad.keyboard.release(item)
        elif isinstance(item, str):
            # compatibility
            actions.layout.write(item)
        else:
            print("Unkown action", item)


def button_release(macropad, key_number, macros):
    sequence = macros[2]
    if not isinstance(sequence, (list, tuple)):
        sequence = (sequence,)
    # Release any still-pressed keys
    for item in sequence:
        if isinstance(item, actions.MacroAction):
            item.release()
        # compatibility
        if isinstance(item, int) and item >= 0:
            macropad.keyboard.release(item)
    if key_number < 12: # No pixel for encoder button
        macropad.pixels[key_number] = macros[0]
        macropad.pixels.show()

