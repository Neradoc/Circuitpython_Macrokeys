import board
from digitalio import DigitalInOut, Pull
import gc
import keypad
import os
import time
import traceback

from adafruit_debouncer import Debouncer
from macrokeys import actions, application
from macrokeys.drivers.generic_keypad import KeypadModuleDriver

# CONFIGURABLES ------------------------

MACRO_FOLDER = "/macros-keypad"

# INITIALIZATION -----------------------

KEY_PINS = (board.SW0, board.SW1, board.SW2, board.SW3, board.SW4, board.SW5, board.SW6, board.SW7, board.SW8, board.SW9, board.SW10, board.SW11, board.SW12, board.SW13, board.SW14, board.SW15)

keypad_keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)

boot_pin = DigitalInOut(board.USER_SW)
boot_pin.switch_to_input(Pull.UP)
boot = Debouncer(boot_pin)

# ######################################

macro_keypad = KeypadModuleDriver(keypad_keys)

# ######################################
# Load all the macro key setups from .py files in MACRO_FOLDER

apps = application.load_apps(macro_keypad, MACRO_FOLDER)

if not apps:
	raise ValueError("Not apps!")

# the last position being None makes the loop start with switching to a page
app_index = 0

# init colors
apps[app_index].reset_leds()

# MAIN LOOP ----------------------------

while True:
    gc.collect()
    boot.update()
    if boot.rose:
        prev_app_index = app_index
        app_index = (app_index + 1) % len(apps)
        print(f"Switching to page {app_index}")
        apps[app_index].switch(apps[prev_app_index])
    else:
        macro_keypad.do_macro(apps[app_index])
