class Color:

    def __init__(self, red=255, green=255, blue=255):
        self.red = red
        self.green = green
        self.blue = blue

    @property
    def r(self):
        return self.red

    @property
    def g(self):
        return self.green

    @property
    def b(self):
        return self.blue

    def __eq__(self, other):
        return self.red == other.r and self.green == other.g and self.blue == other.b
