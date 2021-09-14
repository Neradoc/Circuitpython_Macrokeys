import board
from digitalio import DigitalInOut, Pull
import gc
import os
import time
import traceback

from rainbowio import colorwheel
from adafruit_debouncer import Debouncer
from macrokeys import actions, application
from macrokeys.drivers.pimoroni_keybow2040 import KeybowDriver
from keybow2040 import Keybow2040

# CONFIGURABLES ------------------------

MACRO_FOLDER = "/macros-keybow"

# INITIALIZATION -----------------------

i2c = board.I2C()
keybow = Keybow2040(i2c)
macro_keypad = KeybowDriver(keybow)

boot_pin = DigitalInOut(board.USER_SW)
boot_pin.switch_to_input(Pull.UP)
boot = Debouncer(boot_pin)

# ######################################

col_index = 230
keycolors = [0] * 16


def colors_rolling():
    global col_index
    for x in range(16):
        keycolors[x] = num_to_col(colorwheel((3 * x + col_index) % 256))
        if not macro_keypad.night_mode:
            macro_keypad.set_led(x, keycolors[x])
    col_index = col_index + 1


# Load all the macro key setups from .py files in MACRO_FOLDER

apps = application.load_apps(macro_keypad, MACRO_FOLDER)

if not apps:
    while True:
        keybow.set_all(0, 0, 0)
        time.sleep(1)
        keybow.set_all(255, 0, 0)
        time.sleep(1)

# init the first app
app_index = 0
apps[app_index].switch(None)

# MAIN LOOP ----------------------------

# Attach handler functions to all of the keys
for key in keybow.keys:

    @keybow.on_press(key)
    def press_handler(key):
        apps[app_index].button_press(key.number)

    @keybow.on_release(key)
    def release_handler(key):
        apps[app_index].button_release(key.number)


while True:
    gc.collect()
    boot.update()
    if boot.rose:
        if boot.last_duration > 2:
            apps[app_index].toggle_night_mode(True)
        else:
            prev_app_index = app_index
            app_index = (app_index + 1) % len(apps)
            print(f"Switching to page {app_index}")
            apps[app_index].switch(apps[prev_app_index])
    else:
        keybow.update()
