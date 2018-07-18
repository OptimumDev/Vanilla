class Color:

    def __init__(self, red, green, blue):
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


class Canvas:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = [[Color(255, 255, 255) for y in range(height)] for x in range(width)]