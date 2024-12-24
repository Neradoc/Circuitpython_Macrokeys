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

    def press(self, pad=None):
        pass

    def release(self, pad=None):
        pass

    def action(self, pad=None):
        if self.neg:
            self.release(pad)
        else:
            self.press(pad)

    def __neg__(self):
        return self.__class__(*self.actions, neg=not self.neg)

    def __repr__(self):
        return (
            ("-" if self.neg else "+")
            + self.__class__.__name__
            + repr(self.actions)
        )
