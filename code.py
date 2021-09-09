"""
A fairly straightforward macro/hotkey program for Adafruit MACROPAD.
Macro key setups are stored in the /macros folder (configurable below),
load up just the ones you're likely to use. Plug into computer's USB port,
use dial to select an application macro set, press MACROPAD keys to send
key sequences.
"""

# pylint: disable=import-error, unused-import, too-few-public-methods

import os
import time
import displayio
import terminalio
import traceback

from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad

from macrokeys import actions, apps


# CONFIGURABLES ------------------------

MACRO_FOLDER = '/macros'

# INITIALIZATION -----------------------

macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False

def _play_tone(note, duration):
    macropad.play_tone(note, duration)

actions.play_tone = _play_tone

# Set up displayio group with all the labels
group = displayio.Group()
for key_index in range(12):
    x = key_index % 3
    y = key_index // 3
    group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                             anchored_position=((macropad.display.width - 1) * x / 2,
                                                macropad.display.height - 1 -
                                                (3 - y) * 12),
                             anchor_point=(x / 2, 1.0)))
group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF))
group.append(label.Label(terminalio.FONT, text='', color=0x000000,
                         anchored_position=(macropad.display.width//2, -2),
                         anchor_point=(0.5, 0.0)))
macropad.display.show(group)
macropad.group = group

# Load all the macro key setups from .py files in MACRO_FOLDER

apps = apps.load_apps(macropad, MACRO_FOLDER)

if not apps:
    group[13].text = 'NO MACRO FILES FOUND'
    macropad.display.refresh()
    while True:
        pass

# the last position being None makes the loop start with switching to a page
last_position = None
app_index = 0


# MAIN LOOP ----------------------------

while True:
    # Read encoder position. If it's changed, switch apps.
    position = macropad.encoder
    if position != last_position:
        prev_app_index = app_index
        app_index = position % len(apps)
        apps[app_index].switch(apps[prev_app_index])
        last_position = position

    # Handle encoder button. If state has changed, and if there's a
    # corresponding macro, set up variables to act on this just like
    # the keypad keys, as if it were a 13th key/macro.
    macropad.encoder_switch_debounced.update()
    encoder_switch_pressed = macropad.encoder_switch_debounced.pressed
    if encoder_switch_pressed:
        if len(apps[app_index].macros) < 13:
            continue    # No 13th macro, just resume main loop
        key_number = 12 # else process below as 13th macro
        pressed = encoder_switch
    else:
        event = macropad.keys.events.get()
        if not event or event.key_number >= len(apps[app_index].macros):
            continue # No key events, or no corresponding macro, resume loop
        key_number = event.key_number
        pressed = event.pressed

    # If code reaches here, a key or the encoder button WAS pressed/released
    # and there IS a corresponding macro available for it...other situations
    # are avoided by 'continue' statements above which resume the loop.

    sequence = apps[app_index].macros[key_number][2]
    if not isinstance(sequence, (list, tuple)):
        sequence = (sequence,)
    if pressed:
        # the sequence is arbitrary-length
        # each item in the sequence is either
        # an action instance or a floating point value
        # Action   ==>  execute the action
        # Float    ==>  sleep in seconds
        # Funciton ==>  call it with context
        if key_number < 12: # No pixel for encoder button
            macropad.pixels[key_number] = 0xFFFFFF
            macropad.pixels.show()
        past_items = []
        past_keycodes = set()  # for compatibility
        for index, item in enumerate(sequence):
            past_items.append(item)
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
                actions.Type.write(item)
            else:
                print("Unkown action", item)
    else:
        # Release any still-pressed keys
        for item in sequence:
            if isinstance(item, actions.MacroAction):
                item.release()
            # compatibility
            if isinstance(item, int) and item >= 0:
                macropad.keyboard.release(item)
        if key_number < 12: # No pixel for encoder button
            macropad.pixels[key_number] = apps[app_index].macros[key_number][0]
            macropad.pixels.show()
