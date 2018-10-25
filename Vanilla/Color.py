class Color:

    def __init__(self, red=255, green=255, blue=255, alpha=0):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    @property
    def r(self):
        return self.red

    @property
    def g(self):
        return self.green

    @property
    def b(self):
        return self.blue

    @property
    def a(self):
        return self.alpha

    def __eq__(self, other):
        return self.red == other.r and self.green == other.g and self.blue == other.b and self.alpha == other.a
