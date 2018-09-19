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
    standard_canvas.change_color(new_color.r, new_color.g, new_color.b)
    assert standard_canvas.current_color == new_color


def test_canvas_paint():
    x = 0
    y = 0
    standard_canvas.paint(x, y)
    assert standard_canvas.pixels[x][y] == new_color
