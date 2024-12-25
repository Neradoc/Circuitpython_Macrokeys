import os

machine = os.uname().machine.lower()
if "macropad" in machine:
    import examples.code_macropad
elif "keybow" in machine:
    import examples.code_keybow
elif "pyportal" in machine:
    import examples.code_pyportal
