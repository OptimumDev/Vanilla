import math


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

    def __init__(self, width = 32, height = 32):
        self.width = width
        self.height = height
        self.pixels = [[Color() for y in range(height)] for x in range(width)]
        self.current_color = Color(0, 0, 0)
        self.brush_size = 1

    @staticmethod
    def get_distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def paint(self, x, y):
        for dx in range(1 - self.brush_size, self.brush_size):
            for dy in range(1 - self.brush_size, self.brush_size):
                if 0 <= x + dx < len(self.pixels) and 0 <= y + dy < len(self.pixels[0]) and \
                        self.get_distance(x, y, x + dx, y + dy) <= self.brush_size:
                    self.pixels[x + dx][y + dy] = self.current_color

    def change_color(self, red, green, blue):
        self.current_color = Color(red, green, blue)
