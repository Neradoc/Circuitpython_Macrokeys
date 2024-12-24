from .base import MacroAction

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
import adafruit_hid.mouse

# config in macros_config.py

RELEASE_DELAY = 0.02


common_mouse = None
common_keyboard = None
common_control = None

common_keycodes = None
common_layout = None

try:
    import macros_config as _macros_config
    common_hid = _macros_config.default_hid

except (ImportError, AttributeError):
    pass

try:
    import usb_hid as common_hid

    common_mouse = adafruit_hid.mouse.Mouse(common_hid.devices)
    common_keyboard = Keyboard(common_hid.devices)
    common_control = ConsumerControl(common_hid.devices)

except ImportError:
    pass

try:
    import macros_config as _macros_config

    if hasattr(_macros_config, "default_keycode"):
        common_keycodes = _macros_config.default_keycode
    if hasattr(_macros_config, "default_layout"):
        common_layout = _macros_config.default_layout(common_keyboard)
    if hasattr(_macros_config, "RELEASE_DELAY"):
        RELEASE_DELAY = _macros_config.RELEASE_DELAY

except ImportError:
    pass

if not common_keycodes:
    from adafruit_hid import keycode

    common_keycodes = keycode.Keycode
if not common_layout:
    from adafruit_hid import keyboard_layout_us

    common_layout = keyboard_layout_us.KeyboardLayoutUS(common_keyboard)

#####################################################################
# Actions subclasses
#####################################################################

class Shortcut(MacroAction):
    """
    Action to press/release a list of keycodes together.
    Do multiple actions to press/release independently.
    The Keycode class used can be changed at the class level.
    Takes ints or converts strings using getattr on the Keycode class.
    Defaults to layout.keycodes() if code not found.
    """

    def __init__(self, *actions, neg=False):
        acts = []
        for action in actions:
            if isinstance(action, int):
                acts.append(action)
            elif isinstance(action, str):
                if hasattr(common_keycodes, action):
                    code = getattr(common_keycodes, action)
                    acts.append(code)
                elif len(action) == 1:
                    acts += common_layout.keycodes(action)
            else:
                raise ValueError("Bad type of Shortcut action:" + repr(action))
        super().__init__(*acts, neg=neg)

    def press(self, pad=None):
        common_keyboard.press(*self.actions)

    def release(self, pad=None):
        common_keyboard.release(*self.actions)


class Type(MacroAction):
    """
    Action to write a string with a layout, use via a LayoutFactory,
    so you don't have to repeat the "layout" argument in your macros.
    """

    def __init__(self, *actions, neg=False):
        super().__init__(*actions, neg=neg)

    def press(self, pad=None):
        for action in self.actions:
            common_layout.write(action)

    @staticmethod
    def write(text):
        common_layout.write(text)


class Control(MacroAction):
    """
    Action to press/release a ConsumerControl key (only one at a time).
    """

    def __init__(self, action, *, neg=False):
        if isinstance(action, int):
            code = action
        elif isinstance(action, str):
            code = getattr(ConsumerControlCode, action)
        else:
            raise ValueError("Bad type of Control action:" + repr(action))
        super().__init__(code, neg=neg)

    def press(self, pad=None):
        common_control.press(*self.actions)

    def release(self, pad=None):
        common_control.release()  # only one key at a time anyway


class Mouse(MacroAction):
    """
    Action to press/release a mouse button or move the mouse.
    """

    def __init__(self, button=0, x=0, y=0, wheel=0, neg=False):
        self.button = button
        self.x = x
        self.y = y
        self.wheel = wheel
        self.neg = neg
        super().__init__(button, x, y, wheel, neg=neg)

    def press(self, pad=None):
        if self.button == 1:
            common_mouse.press(adafruit_hid.mouse.Mouse.LEFT_BUTTON)
        elif self.button == 2:
            common_mouse.press(adafruit_hid.mouse.Mouse.RIGHT_BUTTON)
        elif self.button == 3:
            common_mouse.press(adafruit_hid.mouse.Mouse.MIDDLE_BUTTON)
        common_mouse.move(self.x, self.y, self.wheel)

    def release(self, pad=None):
        if self.button == 1:
            common_mouse.release(adafruit_hid.mouse.Mouse.LEFT_BUTTON)
        elif self.button == 2:
            common_mouse.release(adafruit_hid.mouse.Mouse.RIGHT_BUTTON)
        elif self.button == 3:
            common_mouse.release(adafruit_hid.mouse.Mouse.MIDDLE_BUTTON)
