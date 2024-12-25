import board
from digitalio import DigitalInOut, Pull
import gc
import os
import time
import traceback

from rainbowio import colorwheel
from adafruit_debouncer import Debouncer

from macrokeys.drivers.pimoroni_keybow2040 import KeybowDriver
from keybow2040 import Keybow2040

# CONFIGURABLES ------------------------

MACRO_FOLDER = "/macros"

# INITIALIZATION -----------------------

i2c = board.I2C()
keybow = Keybow2040(i2c)

boot_pin = DigitalInOut(board.USER_SW)
boot_pin.switch_to_input(Pull.UP)
boot = Debouncer(boot_pin)

# Attach handler functions to all of the keys
for key in keybow.keys:

    @keybow.on_press(key)
    def press_handler(key):
        macro_keypad.current.button_press(key.number)

    @keybow.on_release(key)
    def release_handler(key):
        macro_keypad.current.button_release(key.number)

# Load all the macro key setups from .py files in MACRO_FOLDER

macro_keypad = KeybowDriver(keybow, MACRO_FOLDER)
macro_keypad.start()

# MAIN LOOP ----------------------------

while True:
    gc.collect()
    boot.update()
    if boot.rose:
        if boot.last_duration > 2:
            macro_keypad.toggle_night_mode(True)
        else:
            print(f"Switching to next page")
            macro_keypad.move_page(1)
    else:
        keybow.update()
