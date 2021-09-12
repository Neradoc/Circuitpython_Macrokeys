import os

machine = os.uname().machine.lower()
if "macropad" in machine:
    import code_macropad
elif "keybow" in machine:
    import code_keybow
