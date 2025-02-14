from .base import MacroAction

#####################################################################
# Actions subclasses
#####################################################################


class Color(MacroAction):
    """
    Encodes the default color of the button.
    Encodes the temporary color when pressed, with -Color(x).
    A color value can be:
    - an int: 0xRRGGBB
    - a css color: "#RRGGBB"
    - a tuple (r, g, b)
    """

    def __init__(self, color, *, hold=True):
        self.toggled = False
        self.hold = hold
        if isinstance(color, tuple):
            self.color = color
        elif isinstance(color, int):
            c = color
            self.color = (c >> 16 & 0xFF, c >> 8 & 0xFF, c & 0xFF)
        elif isinstance(color, str):
            c = int(color.replace("#", ""), 16)
            self.color = (c >> 16 & 0xFF, c >> 8 & 0xFF, c & 0xFF)
        else:
            raise ValueError("Color value invalid, give tuple, int or hexa string")

    def action(self, app, key, idx):
        if not app.macro_keypad.night_mode:
            color = self.color
            if self.hold:
                # toggle the color
                if self.toggled:
                    app.colors[key] = app.macros[key][0]
                else:
                    app.colors[key] = self.color
                self.toggled = not self.toggled
                # change the color until change again
                app.macro_keypad.set_led(key, self.color)
                app.macro_keypad.show_leds()
            else:
                # change the color temporarily on press
                app.macro_keypad.set_led(key, self.color)
                app.macro_keypad.show_leds()

    def __repr__(self):
        return ("+" if self.hold else "-") + f"Color{self.color}"

    def __neg__(self):
        return self.__class__(self.color, hold=False)


class Night(MacroAction):
    """
    Action to set the night mode to a certain value, or toggle.
    """

    def __init__(self, toggle=False, neg=False):
        self.toggle = toggle
        super().__init__(toggle, neg=neg)

    def action(self, app, key, idx):
        if self.toggle:
            app.macro_keypad.toggle_night_mode()
        else:
            app.macro_keypad.toggle_night_mode(not self.neg)

    @classmethod
    def Toggle(cls):
        """Shortcut to Night(toggle=True)."""
        return Night(toggle=True)


def NightToggle():
    """Shortcut to Night(toggle=True)."""
    return Night(toggle=True)


class Page(MacroAction):
    """Switch to the given page number."""

    def __init__(self, number=0, neg=False):
        self.number = number
        super().__init__(neg=neg)

    def action(self, app, key, idx):
        app.macro_keypad.goto_page(self.number)

    @classmethod
    def next(cls, app, key, idx):
        """Move to next page."""
        app.macro_keypad.move_page(1)

    @classmethod
    def prev(cls, app, key, idx):
        """Move to previous page."""
        app.macro_keypad.move_page(-1)

    @classmethod
    def home(cls, app, key, idx):
        """Move to home page."""
        app.macro_keypad.move_page(0)


try:
    import asyncio

    class ColorBlink(Color):
        """
        Blink a color with asyncio
        """

        def __init__(self, color):
            super().__init__(color)


except ImportError:
    pass
