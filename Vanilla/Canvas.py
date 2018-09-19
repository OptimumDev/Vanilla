import math
from Color import Color


class Canvas:

    STANDARD_WIDTH = 32
    STANDARD_HEIGHT = 32
    STANDARD_COLOR = Color(0, 0, 0)
    STANDARD_BRUSH_SIZE = 1

    def __init__(self, width=STANDARD_WIDTH, height=STANDARD_HEIGHT):
        self.width = width
        self.height = height
        self.pixels = [[Color() for y in range(height)] for x in range(width)]
        self.changed_pixels = [(x, y) for x in range(width) for y in range(height)]
        self.current_color = self.STANDARD_COLOR
        self.brush_size = self.STANDARD_BRUSH_SIZE

    @staticmethod
    def get_distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def paint(self, x, y):
        for dx in range(1 - self.brush_size, self.brush_size):
            for dy in range(1 - self.brush_size, self.brush_size):
                if 0 <= x + dx < len(self.pixels) and 0 <= y + dy < len(self.pixels[0]) and \
                        self.get_distance(x, y, x + dx, y + dy) <= self.brush_size:
                    self.pixels[x + dx][y + dy] = self.current_color
                    self.changed_pixels.append((x + dx, y + dy))

    def change_color(self, red, green, blue):
        self.current_color = Color(red, green, blue)
