from Canvas import Canvas
from Color import Color


standard_canvas = Canvas()


def test_canvas_standard_width():
    assert standard_canvas.width == Canvas.STANDARD_WIDTH


def test_canvas_standard_height():
    assert standard_canvas.height == Canvas.STANDARD_HEIGHT


def test_canvas_standard_color():
    assert standard_canvas.current_color == Canvas.STANDARD_COLOR


def test_canvas_standard_brush_size():
    assert standard_canvas.brush_size == Canvas.STANDARD_BRUSH_SIZE


def test_canvas_standard_pixels():
    assert standard_canvas.pixels == \
           [[Color() for y in range(standard_canvas.height)] for x in range(standard_canvas.width)]


def test_canvas_standard_changed_pixels():
    assert standard_canvas.changed_pixels == \
           [(x, y) for x in range(standard_canvas.width) for y in range(standard_canvas.height)]


new_color = Color(1, 2, 3)


def test_canvas_color_change():
    standard_canvas.change_color(new_color.r, new_color.g, new_color.b, new_color.a)
    assert standard_canvas.current_color == new_color


def test_canvas_paint():
    x = 0
    y = 0
    standard_canvas.paint(x, y)
    assert standard_canvas.pixels[x][y] == new_color


red = Color(255, 0, 0, 255)
blue = Color(0, 0, 255, 255)


def test_canvas_flip_horizontally():
    canvas = Canvas(2, 1)
    canvas.paint_pixel(0, 0, red)
    canvas.paint_pixel(1, 0, blue)
    canvas.select(0, 0, 1, 0)
    canvas.flip_horizontally()
    assert canvas.pixels[0][0] == blue


def test_canvas_flip_vertically():
    canvas = Canvas(1, 2)
    canvas.paint_pixel(0, 0, red)
    canvas.paint_pixel(0, 1, blue)
    canvas.select(0, 0, 0, 1)
    canvas.flip_vertically()
    assert canvas.pixels[0][0] == blue


def test_brightness():
    standard_canvas.change_brightness(50)
    assert standard_canvas.active_layer.brightness == 50


def test_greyscacle():
    standard_canvas.turn_greyscale_on()
    assert standard_canvas.active_layer.greyscale == True


def test_get_pixel():
    standard_canvas.paint_pixel(0, 0, blue)
    pixel =  standard_canvas.get_pixel(0, 0, standard_canvas.current_layer)
    assert pixel == Color(14.535, 14.535, 14.535, 255)


def test_rectangle():
    canvas = Canvas()
    canvas.draw_rectangle(0, 0, canvas.width - 1, canvas.height - 1)
    assert canvas.pixels[-1][-1] == canvas.current_color


def test_triangle():
    canvas = Canvas()
    canvas.draw_triangle(0, 0, canvas.width - 1, canvas.height - 1)
    assert canvas.pixels[-1][-1] == canvas.current_color


def test_ellipse():
    canvas = Canvas()
    canvas.draw_ellipse(0, 0, canvas.width - 1, canvas.height - 1)
    assert canvas.pixels[canvas.width // 2][0] == canvas.current_color


def test_turn_right():
    canvas = Canvas(3, 3)
    canvas.paint_pixel(1, 0)
    canvas.paint_pixel(1, 1)
    canvas.paint_pixel(1, 2)
    canvas.select(0, 0, 2, 2)
    canvas.turn_selection_right()
    assert canvas.pixels[0][1] == canvas.current_color
