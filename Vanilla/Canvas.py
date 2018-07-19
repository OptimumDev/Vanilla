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


class Canvas:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[Color() for y in range(height)] for x in range(width)]
        self.current_color = Color(0, 0, 0)

    def paint(self, x, y):
        self.pixels[x][y] = self.current_color

    def change_color(self, red, green, blue):
        self.current_color = Color(red, green, blue)
