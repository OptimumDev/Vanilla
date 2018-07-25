from PyQt5.QtWidgets import QMainWindow, QAction, QColorDialog, QPushButton, QFileDialog, QSlider
from PyQt5.QtGui import QPainter, QImage, QColor, QIcon
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
        self.picture_name = None
        self.canvas = Canvas()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Vanilla')
        self.setWindowIcon(QIcon('images/icon.png'))
        self.showMaximized()
        self.setStyleSheet('QMainWindow{background: Gray;}'
                           'QMenuBar::item:selected{background: #202020;}'
                           'QMenu::item:disabled{color: #505050;}')
        self.setMouseTracking(True)
        self.create_menu_bar()

        self.color_picker = QPushButton('', self)
        self.color_picker.setGeometry(50, 650 + self.menu_bar.height(), 100, 100)
        red = Canvas().current_color.r
        green = Canvas().current_color.g
        blue = Canvas().current_color.b
        self.color_picker.setStyleSheet(f'background: Color({red}, {green}, {blue})')
        self.color_picker.clicked.connect(self.pick_color)
        self.color_picker.show()

        size_slider = QSlider(Qt.Horizontal, self)
        size_slider.move(10,200)
        size_slider.valueChanged[int].connect(self.size_changed)
        size_slider.show()

        self.show()

    def size_changed(self, value):
        if value == 0:
            self.canvas.brush_size = 1
        else:
            self.canvas.brush_size = value

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

        file_menu.addSeparator()

        self.save_action = QAction('&Save', self)
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.triggered.connect(self.save)
        self.save_action.setDisabled(True)
        file_menu.addAction(self.save_action)

        self.save_as_action = QAction('Save as', self)
        self.save_as_action.setShortcut('Ctrl+Shift+S')
        self.save_as_action.triggered.connect(self.save_as)
        self.save_as_action.setDisabled(True)
        file_menu.addAction(self.save_as_action)

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
        old_canvas = self.canvas
        self.canvas = Canvas(width, height)
        self.canvas.current_color = old_canvas.current_color
        self.canvas.brush_size = old_canvas.brush_size
        max_size = self.height() - self.SHIFT * 2
        proportion = width / height
        if proportion > 1:
            self.canvas_width = max_size
            self.canvas_height = max_size / proportion
        else:
            self.canvas_width = max_size * proportion
            self.canvas_height = max_size
        self.pixel_size = self.canvas_width / self.canvas.width
        self.canvas_left_side = (self.width() - self.canvas_width) / 2
        self.canvas_upper_size = (self.height() - self.canvas_height) / 2
        self.canvas_as_image = self.convert_to_image()
        self.to_draw_canvas = True
        self.save_action.setDisabled(False)
        self.save_as_action.setDisabled(False)

    def convert_to_image(self):
        image = QImage(self.canvas.width, self.canvas.height, QImage.Format_RGB888)
        x = 0
        y = 0
        for column in self.canvas.pixels:
            for pixel in column:
                image.setPixelColor(x, y, QColor(pixel.r, pixel.g, pixel.b))
                y += 1
            x += 1
            y = 0
        return image

    def save(self):
        if self.picture_name is None:
            self.save_as()
        else:
            self.canvas_as_image.save(self.picture_name)

    def save_as(self):
        name = QFileDialog.getSaveFileName(self, 'Save', '',
                                           'PNG Files (*.png);;JPG Files (*.jpg);;BMP Files (*.bmp)')[0]
        if name == '':
            return False
        self.picture_name = name
        self.save()

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
            while len(self.canvas.changed_pixels) > 0:
                x, y = self.canvas.changed_pixels.pop()
                pixel = self.canvas.pixels[x][y]
                self.canvas_as_image.setPixelColor(x, y, QColor(pixel.r, pixel.g, pixel.b))
            self.update()

    def mousePressEvent(self, event):
        if self.cursor_on_canvas and event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.canvas.paint(*self.cursor_position)
            self.update()

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

    def draw_pixels(self, painter):
        painter.drawImage(self.canvas_left_side, self.canvas_upper_size,
                          self.canvas_as_image.scaled(self.canvas_width, self.canvas_height))
        if self.canvas.width < 100 and self.canvas.height < 100:
            for i in range(self.canvas.width + 1):
                x = self.canvas_left_side + i * self.pixel_size
                painter.drawLine(x, self.canvas_upper_size,
                                 x, self.canvas_upper_size + self.canvas_height)
            for i in range(self.canvas.height + 1):
                y = self.canvas_upper_size + i * self.pixel_size
                painter.drawLine(self.canvas_left_side, y,
                                 self.canvas_left_side + self.canvas_width, y)
