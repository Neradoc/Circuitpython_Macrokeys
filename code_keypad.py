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
# Load all the macro key setups from .py files in MACRO_FOLDER

macro_keypad = KeypadModuleDriver(keypad_keys, macro_folder=MACRO_FOLDER)

# ######################################

# init colors
macro_keypad.current.reset_leds()

# MAIN LOOP ----------------------------

while True:
    gc.collect()
    boot.update()
    if boot.rose:
        print(f"Switching to next page")
        macro_keypad.move_page(1)
    else:
        macro_keypad.do_macro()
