from Color import Color


class Layer:

    def __init__(self, width, height, name, greyscale=False, brightness=100):
        self.name = name
        self.greyscale = greyscale
        self.brightness = brightness
        self.pixels = [[Color() for y in range(height)] for x in range(width)]