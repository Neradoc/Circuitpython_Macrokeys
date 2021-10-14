import board
from digitalio import DigitalInOut, Pull
import gc
import os
import time
import traceback

from rainbowio import colorwheel
from macrokeys import controller

import math
import array
import audioio
import audiocore

import displayio
import terminalio
from adafruit_display_text import bitmap_label
from adafruit_displayio_layout.layouts.grid_layout import GridLayout
from adafruit_displayio_layout.widgets.icon_widget import IconWidget

from adafruit_touchscreen import Touchscreen

# CONFIGURABLES ------------------------

MACRO_FOLDER = "/macros"
GRID_COL_NUM = 4

# INITIALIZATION -----------------------

# from adafruit_pyportal import PyPortal
# pyportal = PyPortal(status_neopixel=board.NEOPIXEL)

#####################################################################
# setup a screen

display = board.DISPLAY
# touchscreen = pyportal.peripherals.touchscreen
touchscreen = Touchscreen(
    board.TOUCH_XL,
    board.TOUCH_XR,
    board.TOUCH_YD,
    board.TOUCH_YU,
    calibration=((5200, 59000), (5800, 57000)),
    size=(320, 240),
)


# Make the main_group to hold everything
main_group = displayio.Group()
display.show(main_group)

# loading screen
loading_group = displayio.Group()

# black background, screen size minus side buttons
loading_background = displayio.Bitmap(
    (display.width - 40) // 20, display.height // 20, 1
)
loading_palette = displayio.Palette(1)
loading_palette[0] = 0x0

# scaled group to match screen size minus side buttons
loading_background_scale_group = displayio.Group(scale=20)
loading_background_tilegrid = displayio.TileGrid(
    loading_background, pixel_shader=loading_palette
)
loading_background_scale_group.append(loading_background_tilegrid)

# loading screen label
loading_label = bitmap_label.Label(terminalio.FONT, text="Loading...", scale=3)
loading_label.anchor_point = (0.5, 0.5)
loading_label.anchored_position = (display.width // 2, display.height // 2)

# append background and label to the group
loading_group.append(loading_background_scale_group)
loading_group.append(loading_label)

# GridLayout to hold the icons
# size and location can be adjusted to fit
# different sized screens.
layout = GridLayout(
    x=0,
    y=0,
    width=280,
    height=240,
    grid_size=(GRID_COL_NUM, 3),
    cell_padding=0,
)

# list that holds the IconWidget objects for each icon.
_icons = []

# layer label at the top of the screen
layer_label = bitmap_label.Label(terminalio.FONT)
layer_label.anchor_point = (0.5, 0.0)
layer_label.anchored_position = (display.width // 2 - 20, 0)
# main_group.append(layer_label)

SIDE_BUTTON_BB = (40, 72)
# NOTE: anchor_point ne fonctionne pas (bounding_box is 0000)

# right side layer buttons
home_layer_btn = IconWidget("", "touch_deck_icons/layer_home.bmp", on_disk=True)
home_layer_btn.x = display.width - SIDE_BUTTON_BB[0]
home_layer_btn.y = 0
main_group.append(home_layer_btn)

prev_layer_btn = IconWidget("", "touch_deck_icons/layer_prev.bmp", on_disk=True)
prev_layer_btn.x = display.width - SIDE_BUTTON_BB[0]
prev_layer_btn.y = display.height // 2 - SIDE_BUTTON_BB[1] // 2
main_group.append(prev_layer_btn)

next_layer_btn = IconWidget("", "touch_deck_icons/layer_next.bmp", on_disk=True)
next_layer_btn.x = display.width - SIDE_BUTTON_BB[0]
next_layer_btn.y = display.height - SIDE_BUTTON_BB[1]
main_group.append(next_layer_btn)

# append the grid layout to the main_group
# so it gets shown on the display
main_group.append(layout)
main_group.append(loading_group)
loading_group.hidden = True
gc.collect()


#####################################################################
# setup a driver class

class TonePlayer:
    def __init__(self, backend):
        self.backend = backend

    @staticmethod
    def _sine_sample(length):
        """From adafruit_macropad."""
        tone_volume = (2 ** 15) - 1
        shift = 2 ** 15
        for i in range(length):
            yield int(tone_volume * math.sin(2 * math.pi * (i / length)) + shift)

    def _generate_sample(self, length=100):
        """From adafruit_macropad."""
        self._sine_wave = array.array("H", self._sine_sample(length))
        self._sine_wave_sample = audiocore.RawSample(self._sine_wave)

    def play_tone(self, frequency, duration):
        """From adafruit_macropad."""
        self.start_tone(frequency)
        time.sleep(duration)
        self.stop_tone()

    def start_tone(self, frequency):
        """From adafruit_macropad."""
        self.backend.peripherals._speaker_enable.value = True
        length = 100
        if length * frequency > 350000:
            length = 350000 // frequency
        self._generate_sample(length)
        # Start playing a tone of the specified frequency (hz).
        self._sine_wave_sample.sample_rate = int(len(self._sine_wave) * frequency)
        if not self.backend.peripherals.audio.playing:
            self.backend.peripherals.audio.play(self._sine_wave_sample, loop=True)

    def stop_tone(self):
        """From adafruit_macropad."""
        # Stop playing any tones.
        if self.backend.peripherals.audio.playing:
            self.backend.peripherals.audio.stop()
        self.backend.peripherals._speaker_enable.value = False

class PyPortalDriver(controller.ControlPad):

    def __init__(self, pyportal, macro_folder=None):
        self.pyportal = pyportal
        self.touch = touchscreen # pyportal.peripherals.touchscreen
        # self.player = TonePlayer(pyportal)
        super().__init__(
            macro_folder=macro_folder,
            # play_tone=self.player.play_tone,
            # play_file=pyportal.peripherals.play_file,
        )

    def update_press(self):
        pt = self.touch.touch_point
        if not pt:
            return

        if next_layer_btn.contains(pt):
            self.move_page(1)
            while pt and next_layer_btn.contains(pt):
                pt = self.touch.touch_point
                time.sleep(0.1)
            return

        if prev_layer_btn.contains(pt):
            self.move_page(-1)
            while pt and next_layer_btn.contains(pt):
                pt = self.touch.touch_point
                time.sleep(0.1)
            return

        if home_layer_btn.contains(pt):
            self.goto_page(0)
            while pt and home_layer_btn.contains(pt):
                pt = self.touch.touch_point
                time.sleep(0.1)
            return

        for number, icon in enumerate(_icons):
            if icon.contains(pt):
                self.current.button_press(number)

                while pt and icon.contains(pt):
                    pt = self.touch.touch_point

                self.current.button_release(number)
                return


# Load all the macro key setups from .py files in MACRO_FOLDER

pyportal = None
macro_keypad = PyPortalDriver(pyportal, MACRO_FOLDER)
gc.collect()

#####################################################################

@macro_keypad.on_switch
def switch_page(prev_app, next_app):
    global _icons
    
    # show the loading screen
    loading_group.hidden = False

    # resets icon lists to empty
    _icons = []
    layout._cell_content_list = []

    # remove previous layer icons from the layout
    while len(layout) > 0:
        layout.pop()

    gc.collect()

    # set the layer labed at the top of the screen
    layer_label.text = next_app.name

    # loop over each shortcut and it's index
    for i, macro in enumerate(next_app.macros[0:3*GRID_COL_NUM]):
        gc.collect()
        # test if the icon exists (if not do a text)
        icon_path = f"/touch_deck_icons/{macro[0]}.bmp"
        print(icon_path)
        try:
            s = os.stat(icon_path)
        except OSError:
            icon_path = f"/touch_deck_icons/td_white.bmp"

        # create an icon for the current shortcut
        _new_icon = IconWidget(macro[1], icon_path, on_disk=True)
        # add it to the list of icons
        _icons.append(_new_icon)

        # add it to the grid layout
        # calculate it's position from the index
        layout.add_content(_new_icon, grid_position=(i % GRID_COL_NUM, i // GRID_COL_NUM), cell_size=(1, 1))

    gc.collect()
    print(gc.mem_free())

    # hide the loading screen
    loading_group.hidden = True

#####################################################################

# MAIN LOOP ----------------------------

macro_keypad.start()

while True:
    gc.collect()
    macro_keypad.update_press()
