# MACROPAD Hotkeys example: Minecraft Messaging

# NOTE: There appears to be a line length limit. Exceeding that limit appears
#       to result in silent failure.  Therefore, the key sequences are split
#       across multiple lines.

from macro_actions import K, L

# NOTE: There appears to be some delay when bringing up the command screen.

DELAY_AFTER_SLASH  = 0.80 # required so minecraft has time to bring up command screen
DELAY_BEFORE_RETURN = 0.10

# NOTE: On PC, characters are sometimes lost due to lag.  No simple fix for
#       lost keystrokes is known.  However, the commands do work most of the time.


app = {                              # REQUIRED dict, must be named 'app'
    'name' : 'Minecraft (/msg)',     # Application name
    'macros' : [                     # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x000020, 'list', [
            L("/"), DELAY_AFTER_SLASH,
            L("list"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN")]),
        (0x000020, 'list', [
            L("/"), DELAY_AFTER_SLASH,
            L("list"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN")]),
        (0x000020, 'list', [
            L("/"), DELAY_AFTER_SLASH,
            L("list"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN")]),
        # 2nd row ----------
        (0x000000, '',     []),
        (0x000000, '',     []),
        (0x000000, '',     []),
        # 3rd row ----------
        (0x000000, '',     []),
        (0x000000, '',     []),
        (0x000000, '',     []),
        # 4th row ----------
        (0x101010, 'bed', [
            L("/"), DELAY_AFTER_SLASH,
            L("msg @a Time for bed!"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN")]),
        (0x101010, 'bed', [
            L("/"), DELAY_AFTER_SLASH,
            L("msg @a Time for bed!"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN")]),
        (0x101010, 'bed', [
            L("/"), DELAY_AFTER_SLASH,
            L("msg @a Time for bed!"),
            DELAY_BEFORE_RETURN, K("RETURN"), -K("RETURN")]),
        # Encoder button ---
        (0x000000, '', [])
    ]
}
