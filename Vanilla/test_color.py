from Canvas import Color


def test_color_red_returns_given_values():
    r = 1
    color = Color(r, 2, 3)
    assert color.r == r


def test_color_green_returns_given_values():
    g = 2
    color = Color(1, g, 3)
    assert color.g == g


def test_color_blue_returns_given_values():
    b = 3
    color = Color(1, 2, b)
    assert color.b == b
