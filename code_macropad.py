import os
import time
import displayio
import terminalio
import traceback

from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad

from macrokeys import actions, application
from macrokeys.drivers.adafruit_macropad import MacroPadDriver


# CONFIGURABLES ------------------------

MACRO_FOLDER = "/macros-macropad"

# INITIALIZATION -----------------------

macropad = MacroPad()
macro_keypad = MacroPadDriver(macropad)

# Set up displayio group with all the labels
group = displayio.Group()
for key_index in range(12):
    x = key_index % 3
    y = key_index // 3
    group.append(
        label.Label(
            terminalio.FONT,
            text="",
            color=0xFFFFFF,
            anchored_position=(
                (macropad.display.width - 1) * x / 2,
                macropad.display.height - 1 - (3 - y) * 12,
            ),
            anchor_point=(x / 2, 1.0),
        )
    )
group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF))
group.append(
    label.Label(
        terminalio.FONT,
        text="",
        color=0x000000,
        anchored_position=(macropad.display.width // 2, -2),
        anchor_point=(0.5, 0.0),
    )
)
macropad.display.show(group)
macropad.group = group

# Load all the macro key setups from .py files in MACRO_FOLDER

apps = application.load_apps(macro_keypad, MACRO_FOLDER)

if not apps:
    group[13].text = "NO MACRO FILES FOUND"
    macropad.display.refresh()
    while True:
        pass


@macro_keypad.on_switch
def on_switch(prev_app, next_app):
    macropad.group[13].text = next_app.name  # Application name
    for i in range(12):
        if i < len(next_app.macros):  # Key in use, set label + LED color
            macropad.pixels[i] = next_app.macros[i][0]  # not necessary
            macropad.group[i].text = next_app.macros[i][1]
        else:  # Key not in use, no label or LED
            macropad.pixels[i] = 0  # not necessary
            macropad.group[i].text = ""
    macropad.keyboard.release_all()
    macropad.consumer_control.release()
    macropad.mouse.release_all()
    macropad.stop_tone()
    macropad.pixels.show()
    macropad.display.refresh()


# the last position being None makes the loop start with switching to a page
last_position = macropad.encoder
app_index = 0
apps[app_index].switch(None)

# MAIN LOOP ----------------------------

while True:
    # Read encoder position. If it's changed, switch apps.
    position = macropad.encoder
    if position != last_position:
        prev_app_index = app_index
        app_index = position % len(apps)
        print(f"Switching to page {app_index}")
        apps[app_index].switch(apps[prev_app_index])
        last_position = position

    # Handle encoder button. If state has changed, and if there's a
    # corresponding macro, set up variables to act on this just like
    # the keypad keys, as if it were a 13th key/macro.
    macropad.encoder_switch_debounced.update()
    encoder_switch_pressed = macropad.encoder_switch_debounced.pressed
    if encoder_switch_pressed:
        if len(apps[app_index].macros) < 13:
            continue  # No 13th macro, just resume main loop
        key_number = 12  # else process below as 13th macro
        pressed = True
    else:
        event = macropad.keys.events.get()
        if not event or event.key_number >= len(apps[app_index].macros):
            continue  # No key events, or no corresponding macro, resume loop
        key_number = event.key_number
        pressed = event.pressed

    # If code reaches here, a key or the encoder button WAS pressed/released
    # and there IS a corresponding macro available for it...other situations
    # are avoided by 'continue' statements above which resume the loop.

    if pressed:
        apps[app_index].button_press(key_number)
    else:
        apps[app_index].button_release(key_number)
