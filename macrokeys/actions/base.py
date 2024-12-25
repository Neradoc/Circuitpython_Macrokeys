#####################################################################
# Main action class
#####################################################################


class MacroAction:
    """
    Parent action class.
    An action describes a group of keys to press or release together.
    A normal action is for a press, a negative action is for release.
    """

    def __init__(self, *actions, neg=False):
        self.actions = actions
        self.neg = neg

    def press(self, app=None, key=0, idx=0):
        pass

    def release(self, app=None, key=0, idx=0):
        pass

    def action(self, app=None, key=0, idx=0):
        if self.neg:
            self.release(app, key, idx)
        else:
            self.press(app, key, idx)

    def __neg__(self):
        return self.__class__(*self.actions, neg=not self.neg)

    def __repr__(self):
        return (
            ("-" if self.neg else "+")
            + self.__class__.__name__
            + repr(self.actions)
        )
