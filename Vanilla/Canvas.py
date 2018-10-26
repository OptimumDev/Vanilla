import math
from Color import Color
from Tools import Tools
from Layer import Layer


class Canvas:

    STANDARD_WIDTH = 32
    STANDARD_HEIGHT = 32
    STANDARD_COLOR = Color(0, 0, 0, 255)
    STANDARD_BRUSH_SIZE = 1
    GREYSCALE = 1
    BRIGHTNESS = 2
    LAYER_NAME = 3
    LAYER_STANDARD_NAME = 'Layer #'

    def __init__(self, width=STANDARD_WIDTH, height=STANDARD_HEIGHT):
        self.width = width
        self.height = height
        self.layers = [self.new_layer(self.LAYER_STANDARD_NAME + '0')]
        self.current_layer = 0
        self.changed_pixels = [(x, y) for x in range(width) for y in range(height)]
        self.current_color_rgb = self.STANDARD_COLOR
        self.brush_size = self.STANDARD_BRUSH_SIZE
        self.current_tool = Tools.BRUSH
        self.selection_is_on = False
        self.selection_edges = (0, 0, 0, 0)

    @property
    def active_layer(self):
        return self.layers[self.current_layer]

    @property
    def pixels(self):
        return self.layers[self.current_layer].pixels

    def new_layer(self, name):
        return Layer(self.width, self.height, name)

    @property
    def current_color(self):
        return self.to_greyscale(self.current_color_rgb) if self.active_layer.greyscale else self.current_color_rgb

    @staticmethod
    def get_distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def get_pixel(self, x, y, layer):
        pixel = self.layers[layer].pixels[x][y]
        color = self.to_greyscale(pixel) if self.layers[layer].greyscale else pixel
        return self.use_brightness(color, layer)

    @staticmethod
    def to_greyscale(color):
        value = 0.299 * color.r + 0.587 * color.g + 0.114 * color.b
        return Color(value, value, value, color.a)

    def use_brightness(self, color, layer):
        brightness = self.layers[layer].brightness
        multiplier = brightness / 100
        red = min(color.r * multiplier, 255)
        green = min(color.g * multiplier, 255)
        blue = min(color.b * multiplier, 255)
        return Color(red, green, blue, color.a)

    def paint(self, x, y):
        for dx in range(1 - self.brush_size, self.brush_size):
            for dy in range(1 - self.brush_size, self.brush_size):
                if 0 <= x + dx < len(self.pixels) and 0 <= y + dy < len(self.pixels[0]) and \
                        self.get_distance(x, y, x + dx, y + dy) <= self.brush_size:
                    self.paint_pixel(x + dx, y + dy,
                                     Color() if self.current_tool == Tools.ERASER else self.current_color_rgb)

    def paint_pixel(self, x, y, color=None):
        if self.selection_is_on and not self.is_in_selection(x, y):
            return
        if color is None:
            color = self.current_color_rgb
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

    def draw_rectangle(self, start_x, start_y, end_x, end_y):
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

    def draw_ellipse(self, start_x, start_y, end_x, end_y):
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
        self.build_ellipse(left_center, right_center, up_center, down_center, width // 2, height // 2)

    def build_ellipse(self, left_center, right_center, up_center, down_center, a_radius, b_radius):
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

    def fill(self, x, y):
        color = self.pixels[x][y]
        queue = [(x, y)]
        while len(queue) > 0:
            cur_x, cur_y = queue.pop()
            if (self.selection_is_on and not self.is_in_selection(cur_x, cur_y)) or \
                    not (0 <= cur_x < self.width and 0 <= cur_y < self.height) or self.pixels[cur_x][cur_y] != color:
                continue
            self.paint_pixel(cur_x, cur_y)
            for near_pos in [(cur_x, cur_y - 1), (cur_x + 1, cur_y), (cur_x, cur_y + 1), (cur_x - 1, cur_y)]:
                if (self.selection_is_on and not self.is_in_selection(*near_pos)) or \
                        not (0 <= near_pos[0] < self.width and 0 <= near_pos[1] < self.height) or \
                        self.pixels[near_pos[0]][near_pos[1]] != color:
                    continue
                queue.append(near_pos)

    def select(self, start_x, start_y, end_x, end_y):
        self.selection_is_on = True
        left = min(start_x, end_x)
        right = max(start_x, end_x)
        down = max(start_y, end_y) + 1
        up = min(start_y, end_y)
        self.selection_edges = (left, up, right, down)

    def deselect(self):
        self.selection_is_on = False

    def is_in_selection(self, x, y):
        return self.selection_edges[0] <= x <= self.selection_edges[2] \
               and self.selection_edges[1] <= y < self.selection_edges[3]

    def change_color(self, red, green, blue, alpha):
        self.current_color_rgb = Color(red, green, blue, alpha)

    def choose_eraser(self):
        self.current_tool = Tools.ERASER

    def choose_brush(self):
        self.current_tool = Tools.BRUSH

    def choose_line(self):
        self.current_tool = Tools.LINE

    def choose_rectangle(self):
        self.current_tool = Tools.SQUARE

    def choose_triangle(self):
        self.current_tool = Tools.TRIANGLE

    def choose_ellipse(self):
        self.current_tool = Tools.CIRCLE

    def choose_fill(self):
        self.current_tool = Tools.FILL

    def choose_selection(self):
        self.current_tool = Tools.SELECTION

    def update_changed_pixels(self):
        self.changed_pixels = [(x, y) for x in range(self.width) for y in range(self.height)]

    def turn_greyscale_on(self):
        self.active_layer.greyscale = True
        self.update_changed_pixels()

    def turn_greyscale_off(self):
        self.active_layer.greyscale = False
        self.update_changed_pixels()

    def choose_all(self):
        self.select(0, 0, self.width, self.height)

    def change_brightness(self, brightness):
        self.active_layer.brightness = brightness
        self.update_changed_pixels()

    def delete_selection(self):
        for x in range(self.selection_edges[0], self.selection_edges[2] + 1):
            for y in range(self.selection_edges[1], self.selection_edges[3]):
                self.paint_pixel(x, y, Color())

    def layer_info(self, number, greyscale=False, brightness=100):
        return {self.GREYSCALE : greyscale,
                self.BRIGHTNESS : brightness,
                self.LAYER_NAME : self.LAYER_STANDARD_NAME + str(number)}

    def add_layer(self):
        self.layers.append(self.new_layer(self.LAYER_STANDARD_NAME + str(len(self.layers))))

    def change_layer(self, layer):
        self.current_layer = layer
        print('current layer:', layer)

    def change_layer_name(self, layer, name):
        self.layers[layer].name = name
