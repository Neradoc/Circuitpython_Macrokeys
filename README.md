An extended macro keys library/framework using action classes.

## Macros With Action Classes

Action classes let you encapsulate actions with a class instance, serving as markups in the macros. I tend to prefer short names, but more explicit longer names are available. A macro can be a single item or a list (that reduces the number of parenthesis when there's only one).

<!--
## Defining macros in the macros folder

### Base syntax (TBD)

### Advanced things (TBD)

### Low level things (TBD)
-->

## Shortcuts and Keycodes

Press or release one or more keys with a keycode name as strings. It presses the key and only releases it at the end of the macro, unless you specify to release in two ways: a negative shortcut, or `0`. Keycodes can also be represented with the Keycode.THING int. If the key code is not found, it defaults to `layout.keycodes()`.

```py
# long version, with key names
    (0x004000, 'Redo', [ Shortcut("COMMAND", "SHIFT", "Z") ]),
# short version:
    (0x004000, 'Undo', [ S("COMMAND", "Z") ]),
# importing Keycode
    (0x004000, 'Undo Win', [ Shortcut(Keycode.CONTROL, Keycode.Z) ]),
# releasing all (prefered)
    (0x004000, 'Things', [ S("ALT", "A"), 0, S("ALT", "B") ]),
# releasing one (holding ALT)
    (0x004000, 'Other', [ S("ALT", "A"), -S("A"), S("B") ]),
# hold keys (toggle)
    (0x0000FF, 'Hold Key', [ HoldKeys("SPACE") ]),
# hold a mouse button
    (0x0000FF, 'Hold Mouse', [ HoldMouse(1) ]),
```

### Type a string

```py
# long version
    (0x004000, 'Hello', [ Type("Hello world") ]),
# short version
    (0x004000, 'Taco', [ T(" :taco:") ]),
```

### Consumer Control keys

The `consumer_control_extended` module can be found in the [Layout Repository](https://github.com/Neradoc/Circuitpython_Keyboard_Layouts) and contains a bunch of names for consumer control functions, basically dumped from the USB HID specifications. Some might even do something !

```py
# as strings
    (0x202000, 'Volume-', Control("VOLUME_DECREMENT")),
    (0x202000, 'Volume+', Control("VOLUME_INCREMENT")),
# as int (start calculator)
    (0x202000, 'Calc', Control(0x192)),
# with ConsumerControlExtended
from consumer_control_extended.ConsumerControlExtended import *
...
    (0x202000, 'Calc', Control(AL_CALCULATOR)),
```

### Button Mashing

Button mashing requires running the main loop with asyncio, and will be incompatible with pauses and other actions that require synchronous execution.

```py
# mashing a key and the mouse
    (0x000080, 'Mashes', [ MashKeys("SPACE"), MashMouse(1) ]),
```


### Mouse

Note that mouse movements are relative, and depend on the computer's setup. They are only done once on press and not repeated in this implementation. Mouse buttons are held until the macro key is released.

```py
# click 1 = left, 2 = right, 3 = middle
    (0x202000, 'Click', Mouse(1)),
# mouse move
    (0x202000, 'Zipzap', Mouse(x=100, y=100)),
# mouse wheel
    (0x202000, 'Wheel+', Mouse(wheel=10)),
```

### Midi notes

```py
# midi notes as strings, with or without velocity (127 by default)
    (0x004000, 'Hello', [ Midi( "A-1#", ("C1", 64) ) ]),
# midi notes as numbers
    (0x004000, 'Taco', [ M( 10 ), M( (11, 100) ) ]),
```

### Play tones

```py
# arpeggio
    (0x202000, 'Arpeggio',
        Tone(
            ("C6", 0.2), ("E6", 0.2), ("G6", 0.2), ("C7", 0.2),
            ("G6", 0.2), ("E6", 0.2), ("C6", 0.5),
        )
    ),
```

### Play files

```py
# play an audio file with its full path
    (0x202000, 'Honk', Sound("/audio/honk.wav") ),
```

### Night mode

```py
# disable night mode when leaving the page
    'leave' : -Night(),
# enable night mode on a button
    (0x000000, 'Night', Night()),
# toggle night mode on and off
    (0x000000, 'Night', NightToggle()),
```

### Custom function calls

Instead of an action, you can put a function, expecting 3 parameters, the Macropad Instance, the number of the key being pressed, the index of the action in the current macro's list.

```py
# turn off the lights when pressing the encoder, and hide the interface

def onoff(pad, key, idx):
    # pad.display.brightness = 0
    pad.group.hidden = not pad.group.hidden
    pad.display.refresh()
    if pad.group.hidden:
        pad.pixels.fill(0)
        pad.pixels.show()

app = {
    ...
    'macros' : [
    ...
        # Encoder button ---
        (0x000000, '', onoff)
    ]
}
```

## Mixing

```py
# type a bold string in some text editor, possibly, and beep
    (0x004000, 'Bold String',
        [
            Shortcut("CONTROL", "B"), # shortcut
            0,                        # release
            Type("Is this bold ?",    # type
            0.5,                      # wait
            Tone( ("C6", 0.08) ),     # beep
        ]
    ),
```

## Enter and leave

You can specify a function to be called when switching apps (macro pages), one when you enter, one when you leave. They take the MacroPad instance, the previous app and the current app (instances of App).

```py
# beep when we start this page
# restore the lights and screen when we leave it
# or we won't know where we are when switching pages

beep = Tone(("C6", 0.08), 0.05, ("E6", 0.10))

def entering(pad, prev_app, next_app):
    beep.action()

def leaving(pad, prev_app, next_app):
    pad.group.hidden = False
    pad.display.refresh()

app = {
    'name' : 'Test Macros', # Application name
    'enter' : entering,
    'leave' : leaving,
    'macros' : [
    # ...
    ]
}
```

## International keyboards support

The keyboard layout and keycode can be configured in the `macros_config.py` file, with modules from the [Layout Repository](https://github.com/Neradoc/Circuitpython_Keyboard_Layouts).

```py
from keyboard_layout_mac_fr import KeyboardLayout
from keycode_mac_fr import Keycode

macros_config = {
	"layout": KeyboardLayout,
	"keycodes": Keycode,
}
```


### Async calling

Running the loop with asyncio allows macros to setup actions as tasks that will keep running until canceled. This requires a main run loop like this:

```py
import asyncio

async def main():
    while True:
        macro_keypad.update()
        await asyncio.sleep(0)

asyncio.run(main())
```


<!-- 
## Support for different types of keypads

The generic case in `driver_base`. (TBD)

### How to extend it for your keypad (TBD)

### Existing "drivers" for most cases (TBD)

#### Generic macropad and neopixels (TBD)

#### Generic I2C Neokeys and others (TBD)

#### Macropad (TBD)

#### Keybow (TBD)
 -->
