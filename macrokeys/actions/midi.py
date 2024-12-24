from .base import MacroAction

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

common_midi = None

try:
    import macros_config as _macros_config

    if hasattr(_macros_config, "default_midi"):
        common_midi = _macros_config.default_midi

except ImportError:
    pass

#####################################################################
# setup midi
#####################################################################

try:
    # try importing adafruit_midi
    from adafruit_midi import MIDI
    from adafruit_midi.note_off import NoteOff
    from adafruit_midi.note_on import NoteOn

    # midi not externally defined (like you would with BLE) try USB
    if not common_midi:
        import usb_midi
        if not usb_midi.ports:
            raise Exception("MIDI not enabled")

        common_midi = MIDI(midi_out=usb_midi.ports[1], out_channel=0)

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


#####################################################################
# Actions subclasses
#####################################################################


class Midi(MacroAction):
    """
    Action to press/release a list of midi keys together.
    """

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
            common_midi.send(NoteOn(note, velocity))

    def release(self, pad=None):
        for note, velocity in self.actions:
            common_midi.send(NoteOff(note, 0))

