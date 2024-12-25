from .base import MacroAction
from .audio import (
    audio_start,
    Tone,
    Play,
)
from .hid import (
    hid_start,
    Shortcut,
    HoldKeys,
    Type,
    Control,
    Mouse,
    HoldMouse,
)
from .midi import (
    midi_start,
    Midi,
)
from .status import (
    Color,
    Night,
    NightToggle,
    Page,
)

# async

try:
    import asyncio

    from .hid import (
        MashKeys,
        MashMouse,
    )
    from .status import (
        ColorBlink,
    )

except ImportError:
    pass
