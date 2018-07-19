from PyQt5.QtWidgets import QMainWindow, QAction, QColorDialog, QPushButton
from PyQt5.QtGui import QPainter, QImage, QColor
from PyQt5.Qt import Qt
from SizeDialog import SizeDialog
from Canvas import Canvas
import math


class VanillaWindow(QMainWindow):

    SHIFT = 100

    def __init__(self):
        super().__init__()
        self.to_draw_canvas = False
        self.cursor_on_canvas = False
        self.mouse_pressed = False
        self.cursor_position = (0, 0)
        self.canvas_width = 32
        self.canvas_height = 32
        self.canvas = Canvas(32, 32)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Vanilla')
        self.showMaximized()
        self.setStyleSheet('QMainWindow{background-color: Gray;} QMenuBar::item::selected{background-color: #202020;}')
        self.setMouseTracking(True)
        self.create_menu_bar()

        self.color_picker = QPushButton('', self)
        self.color_picker.setGeometry(50, 650 + self.menu_bar.height(), 100, 100)
        red = self.canvas.current_color.r
        green = self.canvas.current_color.g
        blue = self.canvas.current_color.b
        self.color_picker.setStyleSheet(f'background: Color({red}, {green}, {blue})')
        self.color_picker.clicked.connect(self.pick_color)
        self.color_picker.show()

        self.show()

    def create_menu_bar(self):
        self.menu_bar = self.menuBar()
        self.menu_bar.setStyleSheet('selection-background-color: #202020; background: #393939; color: lightGray;')

        file_menu = self.menu_bar.addMenu('&File')
        edit_menu = self.menu_bar.addMenu('&Edit')

        new_action = QAction('&New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.ask_size)
        file_menu.addAction(new_action)

        open_action = QAction('&Open', self)
        open_action.setShortcut('Ctrl+O')
        file_menu.addAction(open_action)

        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')
        file_menu.addAction(save_action)

        copy_action = QAction('&Copy', self)
        copy_action.setShortcut('Ctrl+C')
        edit_menu.addAction(copy_action)

    def pick_color(self):
        color = QColorDialog.getColor()
        self.canvas.change_color(color.red(), color.green(), color.blue())
        self.color_picker.setStyleSheet(f'background: {color.name()}')

    def ask_size(self):
        success, width, height = SizeDialog.get_size(self)
        if success:
            self.create_canvas(width, height)

    def create_canvas(self, width, height):
        self.canvas = Canvas(width, height)
        max_size = self.height() - self.SHIFT * 2
        proportion = width / height
        if proportion > 1:
            self.canvas_width = max_size
            self.canvas_height = max_size / proportion
        else:
            self.canvas_width = max_size * proportion
            self.canvas_height = max_size
        self.to_draw_canvas = True

    def mouseMoveEvent(self, event):
        if not self.to_draw_canvas:
            return
        x = math.floor((event.pos().x() - self.canvas_left_side) / self.pixel_size)
        y = math.floor((event.pos().y() - self.canvas_upper_size) / self.pixel_size)
        if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
            self.cursor_position = (x, y)
            self.cursor_on_canvas = True
        else:
            self.cursor_on_canvas = False
        if self.mouse_pressed:
            self.canvas.paint(*self.cursor_position)
            self.update()

    def mousePressEvent(self, event):
        if self.cursor_on_canvas and event.button() == Qt.LeftButton:
            self.mouse_pressed = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        if self.to_draw_canvas:
            self.draw_pixels(painter)
        painter.drawImage(0, self.menu_bar.height(), QImage('images/ToolBar.png'))
        painter.end()

    @property
    def pixel_size(self):
        return self.canvas_width // self.canvas.width

    @property
    def canvas_left_side(self):
        return (self.width() - self.canvas_width) / 2

    @property
    def canvas_upper_size(self):
        return (self.height() - self.canvas_height) / 2

    def draw_pixels(self, painter):
        x = 0
        y = 0
        for column in self.canvas.pixels:
            for pixel in column:
                painter.fillRect(self.canvas_left_side + self.pixel_size * x,
                                 self.canvas_upper_size + self.pixel_size * y,
                                 self.pixel_size, self.pixel_size,
                                 QColor(pixel.r, pixel.g, pixel.b))
                painter.drawRect(self.canvas_left_side + self.pixel_size * x,
                                 self.canvas_upper_size + self.pixel_size * y,
                                 self.pixel_size, self.pixel_size)
                y += 1
            x += 1
            y = 0
