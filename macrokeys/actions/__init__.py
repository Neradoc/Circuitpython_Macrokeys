import time
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
import adafruit_hid.mouse

common_mouse = adafruit_hid.mouse.Mouse(usb_hid.devices)
common_keyboard = Keyboard(usb_hid.devices)
common_control = ConsumerControl(usb_hid.devices)
play_tone = None
play_file = None

# config in macros_config.py

AUDIO_FILE_PATH = "/audio"
RELEASE_DELAY = 0.02

BASE_NOTES_MIDI = {"C": 24, "D": 26, "E": 28, "F": 29, "G": 31, "A": 33, "B": 35}
BASE_NOTES_FREQ = {
    "C": 261.63,
    "C#": 277.18,
    "D": 293.66,
    "D#": 311.13,
    "E": 329.63,
    "F": 349.23,
    "F#": 369.99,
    "G": 392.00,
    "F#": 415.30,
    "A": 440.00,
    "A#": 466.16,
    "B": 493.88,
}

keycodes = None
layout = None

try:
    import macros_config as _macros_config

    if hasattr(_macros_config, "default_keycode"):
        keycodes = _macros_config.default_keycode
    if hasattr(_macros_config, "default_layout"):
        layout = _macros_config.default_layout(common_keyboard)
    if hasattr(_macros_config, "RELEASE_DELAY"):
        RELEASE_DELAY = _macros_config.RELEASE_DELAY
    if hasattr(_macros_config, "AUDIO_FILE_PATH"):
        AUDIO_FILE_PATH = _macros_config.AUDIO_FILE_PATH

except ImportError:
    pass

if not keycodes:
    from adafruit_hid import keycode

    keycodes = keycode.Keycode
if not layout:
    from adafruit_hid import keyboard_layout_us

    layout = keyboard_layout_us.KeyboardLayoutUS(common_keyboard)

#####################################################################
# setup midi
#####################################################################

try:
    import usb_midi
    from adafruit_midi import MIDI
    from adafruit_midi.note_off import NoteOff
    from adafruit_midi.note_on import NoteOn
    MIDI_ENABLED = True
except:
    print("Midi unavailable, install adafruit_midi")
    MIDI_ENABLED = False


def note_to_midi(code):
    if isinstance(code, str):
        if len(code) and code[0] in BASE_NOTES_MIDI:
            note = BASE_NOTES_MIDI[code[0]]
        else:
            raise ValueError("Unknown note: " + repr(code))
        delta = ""
        for nn in code[1:]:
            if nn == "-":
                delta = nn
            if nn in "0123456789":
                note = note + 12 * int(delta + nn)
            if nn == "#":
                note = note + 1
        return note
    return code


def note_to_frequency(code):
    if isinstance(code, str):
        nn = code
        if "#" in code and (code[0] + "#") in BASE_NOTES_FREQ:
            note = BASE_NOTES_FREQ[code[0] + "#"]
            code = code[1:].replace("#", "")
        elif len(code) > 0 and code[0] in BASE_NOTES_FREQ:
            note = BASE_NOTES_FREQ[code[0]]
            code = code[1:]
        else:
            raise ValueError("Unknown note: " + repr(code))
        delta = 1
        if code[0] == "-":
            delta = -1
            code = code[1:]
        if code[0] in "012356789":  # don't change if 4
            if delta < 0:
                note = note / (2 ** (int(code[0]) - 4))
            else:
                note = note * (2 ** (int(code[0]) - 4))
        return note
    return code


#####################################################################
# Main action class
#####################################################################


class MacroAction:
    """
    Parent action class.
    An action describes a group of keys to press or release together.
    A normal action is for a press, a negative action is for release.
    """

    def __init__(self, *actions, neg=False):
        self.actions = actions
        self.neg = neg

    def press(self, pad=None):
        pass

    def release(self, pad=None):
        pass

    def action(self, pad=None):
        if self.neg:
            self.release(pad)
        else:
            self.press(pad)

    def __neg__(self):
        return self.__class__(*self.actions, neg=not self.neg)

    def __repr__(self):
        return (
            ("-" if self.neg else "+")
            + self.__class__.__name__
            + repr(self.actions)
        )


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

    def press(self, pad=None):
        common_keyboard.press(*self.actions)

    def release(self, pad=None):
        common_keyboard.release(*self.actions)


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


class Midi(MacroAction):
    """
    Action to press/release a list of midi keys together.
    """

    midi = MIDI(midi_out=usb_midi.ports[1], out_channel=0)

    def __init__(self, *actions, neg=False):
        if not MIDI_ENABLED:
            raise OSError("Midi is not enabled or adafruit_midi is missing")
        acts = []
        for data in actions:
            velocity = 127
            if isinstance(data, (tuple, list)):
                note = note_to_midi(data[0])
                if len(data) > 1:
                    velocity = data[1]
            else:
                note = note_to_midi(data)
            acts.append((note, velocity))
        super().__init__(*acts, neg=neg)

    def press(self, pad=None):
        for note, velocity in self.actions:
            self.midi.send(NoteOn(note, velocity))

    def release(self, pad=None):
        for note, velocity in self.actions:
            self.midi.send(NoteOff(note, 0))


class Type(MacroAction):
    """
    Action to write a string with a layout, use via a LayoutFactory,
    so you don't have to repeat the "layout" argument in your macros.
    """

    def __init__(self, *actions, neg=False):
        super().__init__(*actions, neg=neg)

    def press(self, pad=None):
        for action in self.actions:
            layout.write(action)

    @staticmethod
    def write(text):
        layout.write(text)


class Color:
    """
    Encodes the default color of the button.
    Encodes the temporary color when pressed, with -Color(x).
    A color value can be:
    - an int: 0xRRGGBB
    - a css color: "#RRGGBB"
    - a tuple (r, g, b)
    """

    def __init__(self, color, *, press=False):
        self.press = press
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

    def __repr__(self):
        return ("+" if self.press else "-") + f"Color{self.color}"

    def __neg__(self):
        return self.__class__(self.color, press=not self.press)


class Tone(MacroAction):
    """
    Action to play a tone - needs to be configured first.
    macrokeys.action.play_tone = lambda note, duration: pad.play_tone(note, duration)
    """

    def __init__(self, *actions, neg=False):
        acts = []
        for data in actions:
            duration = 0.5
            if isinstance(data, (tuple, list)):
                note = note_to_frequency(data[0])
                if len(data) > 1:
                    duration = data[1]
            elif isinstance(data, (int, float)):
                note = 0
                duration = data
            else:
                raise ValueError(
                    "Invalid note: " + repr(data) + " use tuple or number."
                )
            acts.append((note, duration))
        super().__init__(*acts, neg=neg)

    def press(self, pad=None):
        for note, duration in self.actions:
            if note > 0:
                if callable(play_tone):
                    play_tone(note, duration)
            else:
                time.sleep(duration)


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


class Play(MacroAction):
    """
    Action to play an audio file.
    """

    def __init__(self, *files, neg=False):
        for file in files:
            for path in [AUDIO_FILE_PATH, "", "/"]:
                file_path = path + "/" + file
                file_path = file_path.replace("//", "/")
                try:
                    with open(file_path, "r"):
                        pass
                    break
                except:
                    pass
            else:
                # for/else: no break means no file found
                # raise ValueError(f"Unkown file {file}")
                print(f"Unkown file {file}")
        super().__init__(*files, neg=neg)

    def press(self, pad=None):
        for file in self.actions:
            if callable(play_file):
                play_file(file)


class Night(MacroAction):
    """
    Action to set the night mode to a certain value, or toggle.
    """

    def __init__(self, toggle=False, neg=False):
        self.toggle = toggle
        super().__init__(toggle, neg=neg)

    def action(self, pad):
        if self.toggle:
            pad.toggle_night_mode()
        else:
            pad.toggle_night_mode(not self.neg)


def NightToggle():
    """Shortcut to Night(toggle=True)."""
    return Night(toggle = True)


class Page(MacroAction):
    """Switch to the given page number."""
    def __init__(self, number=0, neg=False):
        self.number = number
        super().__init__(neg=neg)

    def action(self, pad):
        pad.goto_page(self.number)

    @classmethod
    def next(pad, key, idx):
        """Move to next page."""
        pad.move_page(1)

    @classmethod
    def prev(pad, key, idx):
        """Move to previous page."""
        pad.move_page(-1)

    @classmethod
    def home(pad, key, idx):
        """Move to home page."""
        pad.move_page(0)
