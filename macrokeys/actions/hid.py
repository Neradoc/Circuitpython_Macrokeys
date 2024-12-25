from .base import MacroAction

from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
import adafruit_hid.mouse

mouse = None
keyboard = None
control = None
keycodes = None
layout = None


def hid_start(config):
    """Configure the keyboards and other devices from the user config"""
    global mouse, keyboard, control, keycodes, layout

    hid = config.get("hid", None)
    keycodes = config.get("keycodes", None)
    layout_class = config.get("layout", None)

    if hid is None:
        try:
            import macros_config as _macros_config
            hid = _macros_config.default_hid

        except (ImportError, AttributeError):
            pass

        try:
            import usb_hid
            hid = usb_hid

        except ImportError:
            pass

    # here hid should be defined, otherwise, we are not using shortcuts
    if not hid:
        return

    mouse = adafruit_hid.mouse.Mouse(hid.devices)
    keyboard = Keyboard(hid.devices)
    control = ConsumerControl(hid.devices)

    # default US windows keycodes
    if not keycodes:
        from adafruit_hid import keycode as keycode_module

        keycodes = keycode_module.Keycode

    # keyboard layout from config or default US windows layout
    if layout_class:
        layout = layout_class(keyboard)

    else:
        from adafruit_hid import keyboard_layout_us

        layout = keyboard_layout_us.KeyboardLayoutUS(keyboard)


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
                if hasattr(keycodes, action):
                    code = getattr(keycodes, action)
                    acts.append(code)
                elif len(action) == 1:
                    acts += layout.keycodes(action)
            else:
                raise ValueError("Bad type of Shortcut action:" + repr(action))
        super().__init__(*acts, neg=neg)

    def press(self, app, key, idx):
        keyboard.press(*self.actions)

    def release(self, app, key, idx):
        keyboard.release(*self.actions)


class HoldKeys(Shortcut):
    """
    Action to auto hold a key, release when activated again.
    """

    def __init__(self, *args, **nargs):
        super().__init__(*args, **nargs)
        self.pressed = False

    def press(self, app, key, idx):
        if self.pressed:
            super().release(app, key, idx)
        else:
            super().press(app, key, idx)
        self.pressed = not self.pressed

    def release(self, **args):
        pass


class Type(MacroAction):
    """
    Action to write a string with a layout, use via a LayoutFactory,
    so you don't have to repeat the "layout" argument in your macros.
    """

    def __init__(self, *actions, neg=False):
        super().__init__(*actions, neg=neg)

    def press(self, app, key, idx):
        for action in self.actions:
            layout.write(action)

    @staticmethod
    def write(text):
        layout.write(text)


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

    def press(self, app, key, idx):
        control.press(*self.actions)

    def release(self, app, key, idx):
        control.release()  # only one key at a time anyway


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

    def press(self, **args):
        if self.button == 1:
            mouse.press(adafruit_hid.mouse.Mouse.LEFT_BUTTON)
        elif self.button == 2:
            mouse.press(adafruit_hid.mouse.Mouse.RIGHT_BUTTON)
        elif self.button == 3:
            mouse.press(adafruit_hid.mouse.Mouse.MIDDLE_BUTTON)
        mouse.move(self.x, self.y, self.wheel)

    def release(self, **args):
        if self.button == 1:
            mouse.release(adafruit_hid.mouse.Mouse.LEFT_BUTTON)
        elif self.button == 2:
            mouse.release(adafruit_hid.mouse.Mouse.RIGHT_BUTTON)
        elif self.button == 3:
            mouse.release(adafruit_hid.mouse.Mouse.MIDDLE_BUTTON)


class HoldMouse(Mouse):
    """
    Action to auto hold a key, release when activated again.
    """

    def __init__(self, *args, **nargs):
        super().__init__(*args, **nargs)
        self.pressed = False

    def press(self, app, key, idx):
        if self.pressed:
            super().release(app, key, idx)
        else:
            super().press(app, key, idx)
        self.pressed = not self.pressed

    def release(self, app, key, idx):
        pass


#####################################################################
# Async Actions
#####################################################################


try:
    import asyncio

    class MashKeys(Shortcut):
        """
        Action to repeatedly mash a key, until the button is pressed again
        Requires asyncio to be available, and used in the main loop
        """

        def __init__(self, *actions, neg=False, delay=0.01):
            super().__init__(*actions, neg=neg)
            self.delay = delay
            self.task = None

        async def MASH(self, app, key, idx):
            while True:
                super().press()
                await asyncio.sleep(0.01)
                super().release()
                await asyncio.sleep(self.delay)

        def action(self, app, key, idx):
            if self.task:
                self.task.cancel()
                self.task = None
            else:
                self.task = asyncio.create_task(self. MASH(app, key, idx))


    class MashMouse(Mouse):
        """
        Action to repeatedly mash a key, until the button is pressed again
        Requires asyncio to be available, and used in the main loop
        """

        def __init__(self, *actions, neg=False, delay=0.01):
            super().__init__(*actions, neg=neg)
            self.delay = delay
            self.task = None

        async def MASH(self, app, key, idx):
            while True:
                super().press()
                await asyncio.sleep(0.01)
                super().release()
                await asyncio.sleep(self.delay)

        def action(self, app, key, idx):
            if self.task:
                self.task.cancel()
                self.task = None
            else:
                self.task = asyncio.create_task(self. MASH(app, key, idx))


except ImportError:
    pass

