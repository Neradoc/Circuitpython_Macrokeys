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

main_app = application(macro_keypad, MACRO_FOLDER)

# MAIN LOOP ----------------------------

# Attach handler functions to all of the keys
for key in keybow.keys:

    @keybow.on_press(key)
    def press_handler(key):
        main_app.current.button_press(key.number)

    @keybow.on_release(key)
    def release_handler(key):
        main_app.current.button_release(key.number)


while True:
    gc.collect()
    boot.update()
    if boot.rose:
        if boot.last_duration > 2:
            main_app.toggle_night_mode(True)
        else:
            print(f"Switching to next page")
            main_app.move_page(1)
    else:
        keybow.update()
