from PyQt5.QtWidgets import QMainWindow, QAction, QColorDialog, QPushButton, QFileDialog, QSlider, QLabel, QLineEdit, \
    QScrollBar, QDesktopWidget
from PyQt5.QtGui import QPainter, QImage, QColor, QIcon, QCursor, QPixmap, QFont, QIntValidator, QBrush
from PyQt5.Qt import Qt
from SizeDialog import SizeDialog
from Canvas import Canvas
from Color import Color
from Tools import Tools
import math


class VanillaWindow(QMainWindow):

    SHIFT = 100
    MAX_BRUSH_SIZE = 500
    TOOLBAR_HEIGHT = 791
    BUTTON_SIZE = 64
    MENU_BAR_HEIGHT = 30
    MINIMUM_CANVAST_LEFT_SHIFT = 250

    def __init__(self):
        super().__init__()
        self.to_draw_canvas = False
        self.to_draw_line = False
        self.to_draw_rectangle = False
        self.to_draw_triangle = False
        self.to_draw_ellipse = False
        self.cursor_on_canvas = False
        self.shape_start = None
        self.mouse_pressed = False
        self.picture_name = None
        self.canvas = Canvas()
        self.button_images = {}
        self.buttons = {}
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Vanilla')
        self.setWindowIcon(QIcon('images/icon.png'))
        self.showMaximized()
        self.setStyleSheet('QMainWindow{background: Gray;}'
                           'QMenuBar::item:selected{background: #202020;}'
                           'QMenu::item:disabled{color: #505050;}'
                           'QToolTip{background : black; font-size: 16px; color: white; '
                           'border: black solid 1px}')
        self.setMouseTracking(True)
        self.create_menu_bar()

        self.color_picker = QPushButton('', self)
        color_picker_height = 100
        self.color_picker.setGeometry(50, self.TOOLBAR_HEIGHT + self.MENU_BAR_HEIGHT - color_picker_height - 50,
                                      100, color_picker_height)
        red = Canvas().current_color.r
        green = Canvas().current_color.g
        blue = Canvas().current_color.b
        self.color_picker.setStyleSheet(f'background: Color({red}, {green}, {blue})')
        self.color_picker.clicked.connect(self.pick_color)
        self.color_picker.show()

        self.size_slider = QSlider(Qt.Horizontal, self)
        slider_height = 20
        self.size_slider.setGeometry(10, self.color_picker.y() - slider_height - 60, 145, slider_height)
        self.size_slider.setMinimum(1)
        self.size_slider.setMaximum(self.MAX_BRUSH_SIZE)
        self.size_slider.valueChanged[int].connect(self.size_changed)
        self.size_slider.show()

        validator = QIntValidator(1, self.MAX_BRUSH_SIZE)
        self.size_edit = QLineEdit('1', self)
        self.size_edit.setGeometry(self.size_slider.x() + self.size_slider.width() + 5, self.size_slider.y(), 35, 20)
        self.size_edit.setFont(QFont('Arial', 10))
        self.size_edit.setAlignment(Qt.AlignCenter)
        self.size_edit.setValidator(validator)
        self.size_edit.textChanged[str].connect(self.size_edited)
        self.size_edit.show()

        self.size_label = QLabel('Brush Size:', self)
        self.size_label.setFont(QFont('Arial', 16))
        self.size_label.setStyleSheet('color: lightGray;')
        self.size_label.setGeometry(self.size_slider.x(), self.size_slider.y() - self.size_slider.height() - 10,
                                    self.size_slider.width() + self.size_edit.width() + 5, 30)
        self.size_label.show()

        brush_button = self.create_button(20, self.MENU_BAR_HEIGHT + 10, 'Brush', 'B', self.brush_button_clicked)
        self.buttons[Tools.BRUSH] = brush_button

        eraser_button = self.create_button(brush_button.x() + brush_button.width() + self.MENU_BAR_HEIGHT,
                                           brush_button.y(), 'Eraser', 'E', self.eraser_button_clicked)
        self.buttons[Tools.ERASER] = eraser_button

        fill_button = self.create_button(brush_button.x(),
                                         brush_button.y() + brush_button.height() + self.MENU_BAR_HEIGHT, 'Fill', 'F',
                                         self.fill_button_pressed)
        self.buttons[Tools.FILL] = fill_button

        selection_button = self.create_button(eraser_button.x(), fill_button.y(), 'Selection', 'S')
        self.buttons[Tools.SELECTION] = selection_button

        line_button = self.create_button(20, 300, 'Line', 'L', self.line_button_clicked)
        self.buttons[Tools.LINE] = line_button

        rectangle_button = self.create_button(line_button.x() + line_button.width() + self.MENU_BAR_HEIGHT,
                                           line_button.y(), 'Rectangle', 'R', self.rectangle_button_clicked)
        self.buttons[Tools.SQUARE] = rectangle_button

        ellipse_button = self.create_button(line_button.x(),
                                            line_button.y() + line_button.height() + self.MENU_BAR_HEIGHT, 'Ellipse',
                                            'C', self.ellipse_button_clicked)
        self.buttons[Tools.CIRCLE] = ellipse_button

        triangle_button = self.create_button(rectangle_button.x(), ellipse_button.y(), 'Triangle', 'T',
                                             self.triangle_button_clicked)
        self.buttons[Tools.TRIANGLE] = triangle_button

        width = QDesktopWidget().width()
        height = QDesktopWidget().height() - 64
        size = 20

        self.vertical_scrollbar = QScrollBar(self)
        self.vertical_scrollbar.setGeometry(width - size, 0, size, height - size)
        self.vertical_scrollbar.valueChanged[int].connect(self.vertical_scrollbar_value_changed)
        
        self.horizontal_scrollbar = QScrollBar(Qt.Horizontal, self)
        self.horizontal_scrollbar.setGeometry(0, height - size, width - size, size)
        self.horizontal_scrollbar.valueChanged[int].connect(self.horizontal_scrollbar_value_changed)

        self.show()

    def create_menu_bar(self):
        self.menu_bar = self.menuBar()
        self.menu_bar.setStyleSheet('selection-background-color: #202020; background: #393939; color: lightGray;')

        file_menu = self.menu_bar.addMenu('&File')

        new_action = QAction('&New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.ask_size)
        file_menu.addAction(new_action)

        open_action = QAction('&Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open)
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

    def create_button(self, x, y, image, shortcut='', action=lambda: None):
        button = QPushButton('', self)
        button.setGeometry(x, y, self.BUTTON_SIZE, self.BUTTON_SIZE)
        button.setStyleSheet('background: transparent;')
        button.setShortcut(shortcut)
        button.setToolTip(f'{image} ({shortcut})')
        button.clicked.connect(action)
        self.button_images[button] = QImage(f'images/{image}.png')
        button.show()
        return button

    def eraser_button_clicked(self):
        self.canvas.choose_eraser()
        self.update()

    def brush_button_clicked(self):
        self.canvas.choose_brush()
        self.update()

    def line_button_clicked(self):
        self.canvas.choose_line()
        self.update()

    def rectangle_button_clicked(self):
        self.canvas.choose_rectangle()
        self.update()

    def triangle_button_clicked(self):
        self.canvas.choose_triangle()
        self.update()

    def ellipse_button_clicked(self):
        self.canvas.choose_ellipse()
        self.update()

    def fill_button_pressed(self):
        self.canvas.choose_fill()
        self.update()

    def horizontal_scrollbar_value_changed(self, value):
        self.update()

    def vertical_scrollbar_value_changed(self, value):
        self.update()

    @property
    def canvas_left_side(self):
        return self.canvas_left_edge - self.horizontal_scrollbar.value()

    @property
    def canvas_upper_side(self):
        return self.canvas_upper_edge - self.vertical_scrollbar.value()

    def size_edited(self, size):
        if size == '':
            value = 1
        else:
            value = int(size)
        if value == 0:
            self.size_edit.setText('1')
        else:
            self.size_slider.setValue(value)

    def size_changed(self, value):
        if value == 0:
            self.canvas.brush_size = 1
        else:
            self.canvas.brush_size = value
        if self.to_draw_canvas:
            self.change_cursor()
        self.size_edit.setText(f'{self.canvas.brush_size}')

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
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
        self.canvas_left_edge = (self.width() - self.canvas_width) / 2
        self.canvas_upper_edge = (self.height() - self.canvas_height) / 2
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

    def open(self):
        load_file_name = QFileDialog.getOpenFileName(self, 'Chose Image File', '',
                                                     'PNG Files (*.png);;JPG Files (*.jpg);;BMP Files (*.bmp)')[0]
        if load_file_name == '':
            return False
        self.picture_name = load_file_name
        image = QImage(load_file_name)
        self.create_canvas(image.width(), image.height())
        for x in range(self.canvas.width):
            for y in range(self.canvas.height):
                color = image.pixelColor(x, y)
                if color.alpha() == 0:
                    color = QColor(255, 255, 255)
                self.canvas.pixels[x][y] = Color(color.red(), color.green(), color.blue())
        self.update_canvas()
        self.to_draw_canvas = True
        self.update()

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

    def change_cursor(self):
        if self.canvas.current_tool == Tools.BRUSH:
            self.setCursor(self.get_brush_cursor())
        elif self.canvas.current_tool == Tools.ERASER:
            self.setCursor(self.get_eraser_cursor())
        elif self.canvas.current_tool == Tools.FILL:
            self.setCursor(self.get_fill_cursor())

    def get_brush_cursor(self):
        size = (2 * self.canvas.brush_size - 1) * self.pixel_size
        cursor = QPixmap(size, size)
        cursor.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(cursor)
        painter.setPen(QColor(self.canvas.current_color.r, self.canvas.current_color.g, self.canvas.current_color.b))
        painter.drawEllipse(0, 0, size - 1, size - 1)
        painter.drawLine(size / 2, size / 4, size / 2, size / 4 * 3)
        painter.drawLine(size / 4, size / 2, size / 4 * 3, size / 2)
        painter.end()
        return QCursor(cursor)

    def get_eraser_cursor(self):
        size = (2 * self.canvas.brush_size - 1) * self.pixel_size
        cursor = QPixmap(size, size)
        cursor.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(cursor)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(0, 0, size - 1, size - 1)
        painter.end()
        return QCursor(cursor)

    def get_fill_cursor(self):
        fill = QImage('images/FillCursor.png')
        cursor = QPixmap(fill.width(), fill.height())
        cursor.fill(Qt.transparent)
        painter = QPainter()
        painter.begin(cursor)
        painter.setBrush(QColor(self.canvas.current_color.r, self.canvas.current_color.g, self.canvas.current_color.b))
        painter.drawRect(10, 10, 10, 4)
        painter.drawImage(0, 0, fill)
        painter.end()
        return QCursor(cursor)

    def mouseMoveEvent(self, event):
        if not self.to_draw_canvas:
            return
        x = math.floor((event.pos().x() - self.canvas_left_side) / self.pixel_size)
        y = math.floor((event.pos().y() - self.canvas_upper_side) / self.pixel_size)
        if 0 <= x < self.canvas.width and 0 <= y < self.canvas.height:
            self.cursor_position = (x, y)
            self.change_cursor()
            self.cursor_on_canvas = True
        else:
            if not self.mouse_pressed:
                self.shape_start = None
            self.cursor_on_canvas = False
            self.setCursor(Qt.ArrowCursor)
        if self.mouse_pressed:
            self.move_tools()
            self.update_canvas()
            self.update()

    def move_tools(self):
        if self.canvas.current_tool in [Tools.BRUSH, Tools.ERASER]:
            self.canvas.paint(*self.cursor_position)

    def update_canvas(self):
        if not self.to_draw_canvas:
            return
        while len(self.canvas.changed_pixels) > 0:
            x, y = self.canvas.changed_pixels.pop()
            pixel = self.canvas.pixels[x][y]
            self.canvas_as_image.setPixelColor(x, y, QColor(pixel.r, pixel.g, pixel.b))

    def mousePressEvent(self, event):
        if self.cursor_on_canvas and event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.press_tools()

    def press_tools(self):
        if self.canvas.current_tool in [Tools.LINE, Tools.SQUARE, Tools.TRIANGLE, Tools.CIRCLE]:
            self.shape_start = self.cursor_position
        if self.canvas.current_tool in [Tools.BRUSH, Tools.ERASER]:
            self.canvas.paint(*self.cursor_position)
        elif self.canvas.current_tool == Tools.LINE:
            self.to_draw_line = True
        elif self.canvas.current_tool == Tools.SQUARE:
            self.to_draw_rectangle = True
        elif self.canvas.current_tool == Tools.TRIANGLE:
            self.to_draw_triangle = True
        elif self.canvas.current_tool == Tools.CIRCLE:
            self.to_draw_ellipse = True
        elif self.canvas.current_tool == Tools.FILL:
            self.canvas.fill(*self.cursor_position)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.to_draw_canvas:
            self.release_tools()
            self.update_canvas()
            self.update()
            self.mouse_pressed = False

    def release_tools(self):
        if self.shape_start is None:
            return
        if self.canvas.current_tool == Tools.LINE:
            self.to_draw_line = False
            self.canvas.draw_line(*self.shape_start, *self.cursor_position)
        elif self.canvas.current_tool == Tools.SQUARE:
            self.to_draw_rectangle = False
            self.canvas.draw_rectangle(*self.shape_start, *self.cursor_position)
        elif self.canvas.current_tool == Tools.TRIANGLE:
            self.to_draw_triangle = False
            self.canvas.draw_triangle(*self.shape_start, *self.cursor_position)
        elif self.canvas.current_tool == Tools.CIRCLE:
            self.to_draw_ellipse = False
            self.canvas.draw_ellipse(*self.shape_start, *self.cursor_position)

    def wheelEvent(self, event):
        if not self.to_draw_canvas:
            return
        delta = event.angleDelta().y() / 120
        old_width = self.canvas_width
        old_height = self.canvas_height
        if self.canvas.width * (self.pixel_size + delta) > 0 and self.canvas.height * (self.pixel_size + delta) > 0:
            self.pixel_size += delta
            self.canvas_width = self.canvas.width * self.pixel_size
            self.canvas_height = self.canvas.height * self.pixel_size
            self.canvas_left_edge += (old_width - self.canvas_width) / 2
            self.canvas_upper_edge += (old_height - self.canvas_height) / 2
            self.change_cursor()
            self.update()
        if self.canvas_left_edge < self.MINIMUM_CANVAST_LEFT_SHIFT:
            max = self.MINIMUM_CANVAST_LEFT_SHIFT - self.canvas_left_edge
            self.horizontal_scrollbar.setMaximum(max)
            self.horizontal_scrollbar.setMinimum(-max)
            self.horizontal_scrollbar.show()
        else:
            self.horizontal_scrollbar.hide()
        if self.canvas_upper_edge < self.MENU_BAR_HEIGHT:
            max = self.MENU_BAR_HEIGHT - self.canvas_upper_edge
            self.vertical_scrollbar.setMinimum(-max)
            self.vertical_scrollbar.setMaximum(max)
            self.vertical_scrollbar.show()
        else:
            self.vertical_scrollbar.hide()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        if self.to_draw_canvas:
            self.draw_pixels(painter)
        painter.setPen(QColor(self.canvas.current_color.r, self.canvas.current_color.g, self.canvas.current_color.b))
        if self.to_draw_line:
            self.draw_line(painter)
        if self.to_draw_rectangle:
            self.draw_rectangle(painter)
        if self.to_draw_triangle:
            self.draw_triangle(painter)
        if self.to_draw_ellipse:
            self.draw_ellipse(painter)
        painter.drawImage(0, self.menu_bar.height(), QImage('images/ToolBar.png'))
        self.highlight_current_button(painter)
        self.draw_buttons(painter)
        painter.end()

    def highlight_current_button(self, painter):
        painter.setBrush(QColor(255, 255, 255))
        button = self.buttons[self.canvas.current_tool]
        painter.drawRect(button.x(), button.y(), self.BUTTON_SIZE, self.BUTTON_SIZE)

    def get_start_end_position(self):
        start_x, start_y = self.shape_start
        end_x, end_y = self.cursor_position
        start_x = start_x * self.pixel_size + self.canvas_left_side + self.pixel_size / 2
        start_y = start_y * self.pixel_size + self.canvas_upper_side + self.pixel_size / 2
        end_x = end_x * self.pixel_size + self.canvas_left_side + self.pixel_size / 2
        end_y = end_y * self.pixel_size + self.canvas_upper_side + self.pixel_size / 2
        return start_x, start_y, end_x, end_y

    def draw_line(self, painter):
        start_x, start_y, end_x, end_y = self.get_start_end_position()
        painter.drawLine(start_x, start_y, end_x, end_y)

    def draw_rectangle(self, painter):
        start_x, start_y, end_x, end_y = self.get_start_end_position()
        left = min(start_x, end_x)
        up = min(start_y, end_y)
        painter.drawRect(left, up, abs(end_x - start_x), abs(end_y - start_y))

    def draw_triangle(self, painter):
        start_x, start_y, end_x, end_y = self.get_start_end_position()
        left = min(start_x, end_x)
        right = max(start_x, end_x)
        up = min(start_y, end_y)
        down = max(start_y, end_y)
        width = right - left
        left_up = left + width // 2
        right_up = left_up + (width % 2)
        painter.drawLine(left_up, up, left, down)
        painter.drawLine(right_up, up, right, down)
        painter.drawLine(left, down, right, down)

    def draw_ellipse(self, painter):
        start_x, start_y, end_x, end_y = self.get_start_end_position()
        left = min(start_x, end_x)
        up = min(start_y, end_y)
        painter.drawEllipse(left, up, abs(end_x - start_x), abs(end_y - start_y))

    def draw_pixels(self, painter):
        painter.drawImage(self.canvas_left_side, self.canvas_upper_side,
                          self.canvas_as_image.scaled(self.canvas_width, self.canvas_height))
        if self.pixel_size > 10:
            for i in range(self.canvas.width + 1):
                x = self.canvas_left_side + i * self.pixel_size
                painter.drawLine(x, self.canvas_upper_side,
                                 x, self.canvas_upper_side + self.canvas_height)
            for i in range(self.canvas.height + 1):
                y = self.canvas_upper_side + i * self.pixel_size
                painter.drawLine(self.canvas_left_side, y,
                                 self.canvas_left_side + self.canvas_width, y)

    def draw_buttons(self, painter):
        for button, image in self.button_images.items():
            painter.setBrush(QColor(self.canvas.current_color.r, self.canvas.current_color.g,
                                    self.canvas.current_color.b))
            painter.drawRect(button.x() + 2, button.y() + 2, self.BUTTON_SIZE - 4, self.BUTTON_SIZE - 4)
            painter.drawImage(button.x(), button.y(), image.scaled(self.BUTTON_SIZE, self.BUTTON_SIZE))
