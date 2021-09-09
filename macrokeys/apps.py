class App:
    """ Class representing a host-side application, for which we have a set
        of macro sequences. Project code was originally more complex and
        this was helpful, but maybe it's excessive now?"""
    def __init__(self, macropad, appdata):
        self.macropad = macropad
        self.name = appdata['name']
        self.macros = appdata['macros']
        self._enter = None
        if "enter" in appdata and callable(appdata['enter']):
            self._enter = appdata['enter']
        self._leave = None
        if "leave" in appdata and callable(appdata['leave']):
            self._leave = appdata['leave']


    def switch(self, prev_app=None):
        """ Activate application settings; update OLED labels and LED
            colors. """
        # the previous app's "leave" custom code
        if prev_app and prev_app._leave:
            prev_app._leave(pad=self.macropad, prev_app=prev_app, next_app=self)
        # do the switch
        self.macropad.group[13].text = self.name   # Application name
        for i in range(12):
            if i < len(self.macros): # Key in use, set label + LED color
                self.macropad.pixels[i] = self.macros[i][0]
                self.macropad.group[i].text = self.macros[i][1]
            else:  # Key not in use, no label or LED
                self.macropad.pixels[i] = 0
                self.macropad.group[i].text = ''
        self.macropad.keyboard.release_all()
        self.macropad.consumer_control.release()
        self.macropad.mouse.release_all()
        self.macropad.stop_tone()
        self.macropad.pixels.show()
        self.macropad.display.refresh()
        # the current app's "enter" custom code
        if self._enter:
            self._enter(pad=self.macropad, prev_app=prev_app, next_app=self)
