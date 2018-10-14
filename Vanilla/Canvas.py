import math
from Color import Color
from Tools import Tools


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
        self.current_tool = Tools.BRUSH

    @staticmethod
    def get_distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def paint(self, x, y):
        for dx in range(1 - self.brush_size, self.brush_size):
            for dy in range(1 - self.brush_size, self.brush_size):
                if 0 <= x + dx < len(self.pixels) and 0 <= y + dy < len(self.pixels[0]) and \
                        self.get_distance(x, y, x + dx, y + dy) <= self.brush_size:
                    self.paint_pixel(x + dx, y + dy, Color() if self.current_tool == Tools.ERASER else self.current_color)

    def paint_pixel(self, x, y, color=None):
        if color is None:
            color = self.current_color
        self.pixels[x][y] = color
        self.changed_pixels.append((x, y))

    def draw_line(self, start_x, start_y, end_x, end_y):
        width = abs(end_x - start_x) + 1
        height = abs(end_y - start_y) + 1
        if height == 0:
            for x in range(width):
                self.paint_pixel(start_x + x, start_y)
            return
        if width == 0:
            for y in range(height):
                self.paint_pixel(start_x, start_y + y)
            return
        sign_x = 1 if start_x < end_x else -1
        sign_y = 1 if start_y < end_y else -1
        longest = width if width > height else height
        error_x = 0
        error_y = 0
        x = start_x
        y = start_y
        self.paint_pixel(x, y)
        while x != end_x or y != end_y:
            error_x += width
            error_y += height
            if error_x >= longest:
                error_x -= longest
                x += sign_x
            if error_y >= longest:
                error_y -= longest
                y += sign_y
            self.paint_pixel(x, y)

    def draw_square(self, start_x, start_y, end_x, end_y):
        left = min(start_x, end_x)
        up = min(start_y, end_y)
        width = abs(end_x - start_x)
        height = abs(end_y - start_y)
        for x in range(width + 1):
            self.paint_pixel(left + x, start_y)
            self.paint_pixel(left + x, end_y)
        for y in range(height):
            self.paint_pixel(start_x, up + y)
            self.paint_pixel(end_x, up + y)

    def draw_triangle(self, start_x, start_y, end_x, end_y):
        left = min(start_x, end_x)
        right = max(start_x, end_x)
        up = min(start_y, end_y)
        down = max(start_y, end_y)
        width = right - left
        left_up = left + width // 2
        right_up = left_up + (width % 2)
        self.draw_line(left_up, up, left, down)
        self.draw_line(right_up, up, right, down)
        self.draw_line(left, down, right, down)

    def draw_circle(self, start_x, start_y, end_x, end_y):
        left = min(start_x, end_x)
        right = max(start_x, end_x)
        up = min(start_y, end_y)
        down = max(start_y, end_y)
        width = right - left
        height = down - up
        left_center = left + width // 2
        right_center = left_center + (width % 2)
        up_center = up + height // 2
        down_center = up_center + (height % 2)
        self.build_circle(left_center, right_center, up_center, down_center, width // 2, height // 2)

    def build_circle(self, left_center, right_center, up_center, down_center, a_radius, b_radius):
        a_sqr = a_radius ** 2
        b_sqr = b_radius ** 2
        four_a_sqr = 4 * a_sqr
        four_b_sqr = 4 * b_sqr
        x = 0
        y = b_radius
        delta = 2 * b_sqr + a_sqr * (1 - 2 * b_radius)
        while b_sqr * x < a_sqr * y:
            self.paint_pixel(right_center + x, up_center - y)
            self.paint_pixel(right_center + x, down_center + y)
            self.paint_pixel(left_center - x, down_center + y)
            self.paint_pixel(left_center - x, up_center - y)
            if delta >= 0:
                delta += four_a_sqr * (1 - y)
                y -= 1
            delta += b_sqr * (4 * x + 6)
            x += 1
        x = a_radius
        y = 0
        delta = 2 * a_sqr + b_sqr * (1 - 2 * a_radius)
        while a_sqr * y <= b_sqr * x:
            self.paint_pixel(right_center + x, up_center - y)
            self.paint_pixel(right_center + x, down_center + y)
            self.paint_pixel(left_center - x, down_center + y)
            self.paint_pixel(left_center - x, up_center - y)
            if delta >= 0:
                delta += four_b_sqr * (1 - x)
                x -= 1
            delta += a_sqr * (4 * y + 6)
            y += 1

    def change_color(self, red, green, blue):
        self.current_color = Color(red, green, blue)

    def choose_eraser(self):
        self.current_tool = Tools.ERASER

    def choose_brush(self):
        self.current_tool = Tools.BRUSH

    def choose_line(self):
        self.current_tool = Tools.LINE

    def choose_square(self):
        self.current_tool = Tools.SQUARE

    def choose_triangle(self):
        self.current_tool = Tools.TRIANGLE

    def choose_circle(self):
        self.current_tool = Tools.CIRCLE
