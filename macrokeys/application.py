import os
import traceback
from . import actions

class App:
    """ Class representing a host-side application, for which we have a set
        of macro sequences. Project code was originally more complex and
        this was helpful, but maybe it's excessive now?"""
    def __init__(self, macro_keypad, appdata):
        self.macro_keypad = macro_keypad
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
            prev_app._leave(pad=self.macro_keypad, prev_app=prev_app, next_app=self)
        # do the switch
        self.macro_keypad.do_switch(prev_app, self)
        # the current app's "enter" custom code
        if self._enter:
            self._enter(pad=self.macro_keypad, prev_app=prev_app, next_app=self)


def load_apps(macro_keypad, MACRO_FOLDER):
    apps = []
    files = os.listdir(MACRO_FOLDER)
    files.sort()
    for filename in files:
        if filename.endswith('.py') and filename[0] != ".":
            try:
                module = __import__(MACRO_FOLDER + '/' + filename[:-3])
                apps.append(App(macro_keypad, module.app))
            except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                    IndexError, TypeError) as err:
                traceback.print_exception(err, err, err.__traceback__)
    return apps
