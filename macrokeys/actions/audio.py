import time
from .base import MacroAction

AUDIO_FILE_PATH = "/audio"

play_tone = None
play_file = None

def audio_start(config):
    global AUDIO_FILE_PATH, play_tone, play_file

    if "AUDIO_FILE_PATH" in config:
        AUDIO_FILE_PATH = config["AUDIO_FILE_PATH"]

    if "play_tone" in config:
        play_tone = config["play_tone"]

    if "play_file" in config:
        play_file = config["play_file"]


#####################################################################
# audio helper
#####################################################################


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
# Actions subclasses
#####################################################################


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

    def press(self, app, key, idx):
        for note, duration in self.actions:
            if note > 0:
                if callable(play_tone):
                    play_tone(note, duration)
            else:
                time.sleep(duration)


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

    def press(self, app, key, idx):
        for file in self.actions:
            if callable(play_file):
                play_file(file)


