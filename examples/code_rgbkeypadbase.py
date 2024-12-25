from macrokeys.drivers.pimoroni_rgbkeypadbase import RGBKeypadDriver
from pmk import PMK
from pmk.platform.rgbkeypadbase import RGBKeypadBase as Hardware

# CONFIGURABLES ------------------------

MACRO_FOLDER = "/macros"

# INITIALIZATION -----------------------

keybow = PMK(Hardware())
macro_keypad = RGBKeypadDriver(keybow, MACRO_FOLDER)
macro_keypad.brightness = 0.1
macro_keypad.start()

# MAIN LOOP ----------------------------

import asyncio

async def main():
    while True:
        macro_keypad.update()
        await asyncio.sleep(0)

asyncio.run(main())
