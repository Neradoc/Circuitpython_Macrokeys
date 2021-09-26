import os
import traceback
from . import actions

MACRO_FOLDER = "/macros"


class MacrosPage:
    """
    Class representing a set of macro sequences.
    Typically a host-side application, or just a set of features.
    """

    def __init__(self, macro_keypad, page_data):
        self.macro_keypad = macro_keypad
        self.name = page_data["name"]
        self.macros = page_data["macros"]
        self.colors = [item[0] for item in self.macros]
        self._enter = None
        if "enter" in page_data:
            self._enter = page_data["enter"]
        self._leave = None
        if "leave" in page_data:
            self._leave = page_data["leave"]

    @property
    def macro_count(self):
        """The number of macros in this page."""
        return len(self.macros)

    def switch(self, prev_app=None):
        """Activate a page settings."""
        # the previous app's "leave" custom code
        if prev_app and prev_app._leave:
            if isinstance(prev_app._leave, actions.MacroAction):
                prev_app._leave.action(self.macro_keypad)
            elif callable(prev_app._leave):
                prev_app._leave(pad=self.macro_keypad, prev_app=prev_app, next_app=self)
        # set the LEDs
        if not self.macro_keypad.night_mode:
            self.macro_keypad.set_leds(self.colors)
        # do the switch
        self.macro_keypad.do_switch(prev_app, self)
        # the current page's "enter" custom code
        if self._enter:
            if isinstance(self._enter, actions.MacroAction):
                self._enter.action(self.macro_keypad)
            elif callable(self._enter):
                self._enter(pad=self.macro_keypad, prev_app=prev_app, next_app=self)

    def button_press(self, key_number):
        """
        Do an action based on the pressed button or key.
        
        The sequence is arbitrary-length.
        Each item in the sequence can be of different types:
        Action   ==>  execute the action
        Float    ==>  sleep in seconds
        Color    ==>  change the color of the button
        Function ==>  call it with context
        int      ==>  Keycode, for compatibility
        str      ==>  type with the actions layout, for compatibility
        """
        try:
            sequence = self.macros[key_number][2]
        except IndexError:
            return
        if not isinstance(sequence, (list, tuple)):
            sequence = (sequence,)
        # light the matching LED
        # TODO: this should be a parametrised value
        if not self.macro_keypad.night_mode:
            self.macro_keypad.set_led(key_number, 0xFFFFFF)
            self.macro_keypad.show_leds()
        for index, item in enumerate(sequence):
            if item == 0:
                for item in sequence:
                    if isinstance(item, actions.MacroAction):
                        item.release(self.macro_keypad)
            elif isinstance(item, actions.MacroAction):
                item.action(self.macro_keypad)
            elif isinstance(item, float):
                time.sleep(item)
            elif isinstance(item, actions.Color):
                if not self.macro_keypad.night_mode:
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
        """Do things when the button/key is released."""
        try:
            sequence = self.macros[key_number][2]
        except IndexError:
            return
        if not isinstance(sequence, (list, tuple)):
            sequence = (sequence,)
        # Release any still-pressed keys
        for item in sequence:
            if isinstance(item, actions.MacroAction):
                item.release(self.macro_keypad)
            # compatibility
            if isinstance(item, int) and item >= 0:
                self.macro_keypad.keyboard.release(item)
        if not self.macro_keypad.night_mode:
            self.macro_keypad.set_led(key_number, self.macros[key_number][0])
            self.macro_keypad.show_leds()

    def toggle_night_mode(self, value=None):
        """Toggle night mode in the keypad."""
        self.macro_keypad.toggle_night_mode(value)


####################################################################
# ControlPad base, handles all the things
####################################################################


class ControlPad:
    def __init__(
        self, backend, macro_folder=None, pixels=None, play_tone=None, play_file=None
    ):
        self.fidget_mode = False
        self.night_mode = False
        self.backend = backend
        self.pixels = pixels
        # features
        if play_tone:
            actions.play_tone = play_tone
        if play_file:
            actions.play_file = play_file
        self._on_switch = None
        self._on_night_mode = None
        # init
        self.init_macros(macro_folder or MACRO_FOLDER)

    ####################################################################
    # access to properties
    ####################################################################

    @property
    def keyboard(self):
        """Access the keyboard instance."""
        return actions.common_keyboard

    ####################################################################
    # features and callbacks
    ####################################################################

    def play_tone(self, note, duration):
        """Play a tone if the play_tone function has been set."""
        if actions.play_tone:
            return actions.play_tone(note, duration)

    def play_file(self, note, duration):
        """Play an audio file if the play_file function has been set."""
        if actions.play_file:
            return actions.play_file(note, duration)

    def do_switch(self, prev_app, next_app):
        """Call the switch callback."""
        if callable(self._on_switch):
            self._on_switch(prev_app, next_app)

    ####################################################################
    # switch modes and values
    ####################################################################

    def toggle_night_mode(self, value=None):
        """
        Set night mode to True or False.
        Toggle LEDs on or of based on the value.
        """
        if isinstance(value, bool):
            self.night_mode = value
        else:
            self.night_mode = not self.night_mode
        if self.night_mode:
            self.fill_leds(0)
        else:
            self.set_leds(self.current.colors)
        self.show_leds()
        if self._on_night_mode:
            self._on_night_mode(self)

    ####################################################################
    # setup callbacks and features, can be used as decorators
    ####################################################################

    def tone_player(self, callback):
        """Setup the tone playing function."""
        actions.play_tone = callback

    def file_player(self, callback):
        """Setup the audio file playing function."""
        actions.play_file = callback

    def on_switch(self, callback):
        """Setup the switch callback, called after every switch."""
        self._on_switch = callback

    def on_night_mode(self, callback):
        self._on_night_mode = callback

    ####################################################################
    # LED methods
    ####################################################################

    def set_led(self, pos, color):
        """Set the color of an LED, if it works (pixels exists and pos is valid)."""
        try:
            self.pixels[pos] = color
        except:
            pass

    def show_leds(self):
        """Update the LEDs if pixels is set and supports it."""
        try:
            self.pixels.show()
        except:
            pass

    def fill_leds(self, color):
        """Set the colors of the LEDs if it works (pixels exists and has fill)."""
        try:
            self.pixels.fill(color)
        except:
            pass

    def set_leds(self, colors):
        """Set the colors of each LEDs with a list."""
        for i, col in enumerate(colors):
            if col is not None:
                self.set_led(i, col)

    def reset_leds(self):
        """Set the colors of each LED to the ones defined in the current page"""
        if not self.night_mode:
            self.set_leds(self.current.colors)

    ####################################################################
    # this is the macros pages part
    ####################################################################

    def init_macros(self, macro_folder):
        """
        Read the macros files and create the list of pages.
        Does not immediately start with the first page, call start for that.
        """
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
        """The current page."""
        return self.pages[self.index]

    @property
    def page_count(self):
        """The number of pages."""
        return len(self.pages)

    @property
    def macro_count(self):
        """The number of macros on the page."""
        return self.pages[self.index].macro_count

    def start(self):
        """Start the macrokeys application."""
        self.move_page(0)

    def move_page(self, delta=1):
        """
        Change from one page to the other.
        Call the page's switch method.
        """
        last_page = self.pages[self.index]
        self.index = (self.index + delta) % len(self.pages)
        self.pages[self.index].switch(last_page)
