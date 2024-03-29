from PyQt5.QtWidgets import QMainWindow, QAction, QColorDialog, QPushButton, QFileDialog, QSlider, QLabel, QLineEdit, \
    QScrollBar, QDesktopWidget
from PyQt5.QtGui import QPainter, QImage, QColor, QIcon, QCursor, QPixmap, QFont, QIntValidator, QBrush, QPen
from PyQt5.Qt import Qt
from SizeDialog import SizeDialog
from Canvas import Canvas
from Color import Color
from Tools import Tools
import math
from BrightnessDialog import BrightnessDialog
from LayerTable import LayerTable


class VanillaWindow(QMainWindow):

    SHIFT = 100
    MAX_BRUSH_SIZE = 500
    TOOLBAR_HEIGHT = 791
    TOOLBAR_WIDTH = 389
    BUTTON_SIZE = 64
    MENU_BAR_HEIGHT = 30
    BUTTON_SHIFT = 20
    MINIMUM_CANVAS_LEFT_SHIFT = 250

    def __init__(self):
        super().__init__()
        self.to_draw_canvas = False
        self.to_draw_line = False
        self.to_draw_rectangle = False
        self.to_draw_triangle = False
        self.to_draw_ellipse = False
        self.to_draw_selection = False
        self.cursor_on_canvas = False
        self.shape_start = None
        self.selection_left = 0
        self.selection_right = 0
        self.selection_up = 0
        self.selection_down = 0
        self.selection_width = 0
        self.selection_height = 0
        self.mouse_pressed = False
        self.picture_name = None
        self.canvas = Canvas()
        self.button_images = {}
        self.buttons = {}
        self.layer_tables = []
        self.init_ui()

    def init_ui(self):
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

        self.create_buttons()

        width = QDesktopWidget().width()
        height = QDesktopWidget().height() - 64
        size = 20

        self.layer_button_left = width - 220

        self.add_layer_button = QPushButton('Add Layer', self)
        self.add_layer_button.setGeometry(self.layer_button_left + 24, self.TOOLBAR_HEIGHT - 15, 150, 30)
        self.add_layer_button.clicked.connect(self.add_layer)
        self.add_layer_button.setFont(QFont('Arial', 14))
        self.add_layer_button.show()

        self.layers_label = QLabel('Layers', self)
        self.layers_label.setFont(QFont('Arial', 20))
        self.layers_label.setStyleSheet('color: lightGray;')
        self.layers_label.setGeometry(self.layer_button_left, 25, 197, 60)
        self.layers_label.setAlignment(Qt.AlignCenter)
        self.layers_label.show()

        self.vertical_scrollbar = QScrollBar(self)
        self.vertical_scrollbar.setGeometry(width - size, 0, size, height - size)
        self.vertical_scrollbar.valueChanged[int].connect(self.vertical_scrollbar_value_changed)

        self.horizontal_scrollbar = QScrollBar(Qt.Horizontal, self)
        self.horizontal_scrollbar.setGeometry(0, height - size, width - size, size)
        self.horizontal_scrollbar.valueChanged[int].connect(self.horizontal_scrollbar_value_changed)

        self.show()

    def create_buttons(self):
        left = 25

        brush_button = self.create_button(left, self.MENU_BAR_HEIGHT + 20, 'Brush', 'B', self.brush_button_clicked)
        self.buttons[Tools.BRUSH] = brush_button

        right = brush_button.x() + brush_button.width() + self.BUTTON_SHIFT

        eraser_button = self.create_button(right, brush_button.y(), 'Eraser', 'E', self.eraser_button_clicked)
        self.buttons[Tools.ERASER] = eraser_button

        fill_button = self.create_button(left, self.get_button_shift(brush_button), 'Fill', 'F',
                                         self.fill_button_pressed)
        self.buttons[Tools.FILL] = fill_button

        selection_button = self.create_button(right, fill_button.y(), 'Selection', 'S', self.selection_button_clicked)
        self.buttons[Tools.SELECTION] = selection_button

        line_button = self.create_button(left, self.get_button_shift(fill_button), 'Line', 'L',
                                         self.line_button_clicked)
        self.buttons[Tools.LINE] = line_button

        rectangle_button = self.create_button(right, line_button.y(), 'Rectangle', 'R', self.rectangle_button_clicked)
        self.buttons[Tools.SQUARE] = rectangle_button

        ellipse_button = self.create_button(left, self.get_button_shift(line_button), 'Ellipse', 'C',
                                            self.ellipse_button_clicked)
        self.buttons[Tools.CIRCLE] = ellipse_button

        triangle_button = self.create_button(right, ellipse_button.y(), 'Triangle', 'T', self.triangle_button_clicked)
        self.buttons[Tools.TRIANGLE] = triangle_button

        right_turn_button = self.create_button(left, self.get_button_shift(ellipse_button), 'Turn Right', 'Ctrl+R',
                                               self.turn_selection_right)
        left_turn_button = self.create_button(right, right_turn_button.y(), 'Turn Left', 'Ctrl+L',
                                              self.turn_selection_left)

        flip_horizontally_button =  self.create_button(left, self.get_button_shift(right_turn_button),
                                                       'Flip Horizontally', 'Ctrl+H', self.flip_horizontally)

        flip_vertically_button = self.create_button(right, flip_horizontally_button.y(), 'Flip Vertically', 'Ctrl+F',
                                                    self.flip_vertically)

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

        image_menu = self.menu_bar.addMenu('&Image')

        self.greyscale_action = QAction('Greyscale', self)
        self.greyscale_action.setShortcut('Ctrl+G')
        self.greyscale_action.triggered.connect(self.change_greyscale)
        self.greyscale_action.setDisabled(True)
        image_menu.addAction(self.greyscale_action)

        self.brightness_action = QAction('Brightness', self)
        self.brightness_action.setShortcut('Ctrl+B')
        self.brightness_action.triggered.connect(self.brightness)
        self.brightness_action.setDisabled(True)
        image_menu.addAction(self.brightness_action)

        selection_menu = self.menu_bar.addMenu('&Selection')

        self.deselect_action = QAction('Deselect', self)
        self.deselect_action.setShortcut('Ctrl+D')
        self.deselect_action.triggered.connect(self.deselect)
        self.deselect_action.setDisabled(True)
        selection_menu.addAction(self.deselect_action)

        self.select_all_action = QAction('Select All', self)
        self.select_all_action.setShortcut('Ctrl+A')
        self.select_all_action.triggered.connect(self.select_all)
        self.select_all_action.setDisabled(True)
        selection_menu.addAction(self.select_all_action)

        selection_menu.addSeparator()

        self.delete_selection_action = QAction('Delete', self)
        self.delete_selection_action.setShortcut('Delete')
        self.delete_selection_action.triggered.connect(self.delete_in_selection)
        self.delete_selection_action.setDisabled(True)
        selection_menu.addAction(self.delete_selection_action)

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

    def flip(self, flip_function):
        if not self.canvas.selection_is_on:
            return
        flip_function()
        self.to_draw_selection = False
        self.update_canvas()
        self.update()

    def flip_horizontally(self):
        self.flip(self.canvas.flip_horizontally)

    def flip_vertically(self):
        self.flip(self.canvas.flip_vertically)

    def get_button_shift(self, upper_button):
        return upper_button.y() + upper_button.height() + self.BUTTON_SHIFT

    def turn_selection_right(self):
        self.turn_selection(self.canvas.turn_selection_right)

    def turn_selection_left(self):
        self.turn_selection(self.canvas.turn_selection_left)

    def turn_selection(self, turn_function):
        if not self.canvas.selection_is_on:
            return
        turn_function()
        self.to_draw_selection = False
        self.update_canvas()
        self.update()

    def create_layer_button(self, x, y, layer_number):
        button = QPushButton('', self)
        button.setGeometry(x, y, 187, 100)
        button.setStyleSheet('background: transparent;')
        button.clicked.connect(lambda: self.change_layer(layer_number))
        button.show()
        return button

    def change_layer(self, number):
        self.canvas.change_layer(number)
        self.update_color_button()
        self.update()

    def delete_layer(self, layer_table):
        self.canvas.delete_layer(layer_table.layer)
        self.layer_tables.remove(layer_table)
        self.update_canvas()
        self.update_layers_buttons()
        if len(self.canvas.layers) == 5:
            self.add_layer_button.setDisabled(False)
        self.update()

    def update_layers_buttons(self):
        for table in self.layer_tables:
            table.close()
        self.layer_tables = []
        x = self.layer_button_left + 5
        for i in range(len(self.canvas.layers)):
            layer = self.canvas.layers[i]
            btn = self.create_layer_button(x, 90 + i * 105, i)
            self.layer_tables.append(LayerTable(x, 90 + i * 105, layer, btn, self))

    def add_layer(self):
        self.canvas.add_layer()
        if len(self.canvas.layers) == 6:
            self.add_layer_button.setDisabled(True)
        self.update_layers_buttons()
        self.update()

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

    def selection_button_clicked(self):
        self.canvas.choose_selection()
        self.update()

    def horizontal_scrollbar_value_changed(self, value):
        self.update()

    def vertical_scrollbar_value_changed(self, value):
        self.update()

    def change_greyscale(self):
        if self.canvas.active_layer.greyscale:
            self.canvas.turn_greyscale_off()
        else:
            self.canvas.turn_greyscale_on()
        self.update_canvas()
        self.update_color_button()
        self.update()

    def deselect(self):
        self.canvas.deselect()
        self.deselect_action.setDisabled(True)
        self.delete_selection_action.setDisabled(True)
        self.to_draw_selection = False
        self.update()

    def select_all(self):
        self.canvas.deselect()
        self.shape_start = 0, 0
        self.cursor_position = self.canvas.width - 1, self.canvas.height - 1
        self.update_selection_position()
        self.canvas.select(*self.shape_start, *self.cursor_position)
        self.to_draw_selection = True
        self.deselect_action.setDisabled(False)
        self.delete_selection_action.setDisabled(False)
        self.update()

    def change_brightness(self, brightness):
        self.canvas.change_brightness(brightness)
        self.update_canvas()
        self.update()

    def brightness(self):
        success, brightness = BrightnessDialog.get_brightness(self, self.canvas.active_layer.brightness)
        if success:
            self.change_brightness(brightness)

    def delete_in_selection(self):
        if not self.canvas.selection_is_on:
            return
        self.canvas.delete_selection()
        self.update_canvas()
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
            self.canvas.change_color(color.red(), color.green(), color.blue(), color.alpha())
            self.update_color_button()

    def update_color_button(self):
        cur_color = self.canvas.current_color
        color = QColor(cur_color.r, cur_color.g, cur_color.b)
        self.color_picker.setStyleSheet(f'background: {color.name()}')

    def ask_size(self):
        success, width, height = SizeDialog.get_size(self)
        if success:
            self.create_canvas(width, height)

    def create_canvas(self, width, height):
        old_canvas = self.canvas
        self.canvas = Canvas(width, height)
        self.canvas.current_color_rgb = old_canvas.current_color_rgb
        self.canvas.brush_size = old_canvas.brush_size
        self.canvas.current_tool = old_canvas.current_tool
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
        self.enable_actions()
        self.update_layers_buttons()

    def enable_actions(self):
        self.save_action.setDisabled(False)
        self.save_as_action.setDisabled(False)
        self.greyscale_action.setDisabled(False)
        self.brightness_action.setDisabled(False)
        self.select_all_action.setDisabled(False)

    def convert_to_image(self):
        image = QImage(self.canvas.width, self.canvas.height, QImage.Format_ARGB32)
        x = 0
        y = 0
        for layer in self.canvas.layers:
            for column in layer.pixels:
                for pixel in column:
                    image.setPixelColor(x, y, QColor(pixel.r, pixel.g, pixel.b, pixel.a))
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
                self.canvas.pixels[x][y] = Color(color.red(), color.green(), color.blue(), color.alpha())
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
        if self.cursor_on_canvas and self.canvas.current_tool == Tools.SELECTION:
            self.update_selection_position()

    def update_canvas(self):
        if not self.to_draw_canvas:
            return
        while len(self.canvas.changed_pixels) > 0:
            x, y = self.canvas.changed_pixels.pop()
            layer = len(self.canvas.layers) - 1
            pixel = self.canvas.get_pixel(x, y, layer)
            while layer > 0 and pixel.a == 0:
                layer -= 1
                pixel = self.canvas.get_pixel(x, y, layer)
            self.canvas_as_image.setPixelColor(x, y, QColor(pixel.r, pixel.g, pixel.b, pixel.a))

    def mousePressEvent(self, event):
        if self.cursor_on_canvas and event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.press_tools()

    def press_tools(self):
        if self.canvas.current_tool in [Tools.LINE, Tools.SQUARE, Tools.TRIANGLE, Tools.CIRCLE, Tools.SELECTION]:
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
        elif self.canvas.current_tool == Tools.SELECTION:
            self.deselect()
            self.deselect_action.setDisabled(False)
            self.delete_selection_action.setDisabled(False)
            self.to_draw_selection = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.to_draw_canvas:
            self.release_tools()
            self.update_canvas()
            self.update()
            self.mouse_pressed = False

    def release_tools(self):
        if self.shape_start is None:
            return
        if self.canvas.current_tool == Tools.SELECTION:
            self.canvas.select(*self.shape_start, *self.cursor_position)
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
        if self.canvas_left_edge < self.MINIMUM_CANVAS_LEFT_SHIFT:
            max = self.MINIMUM_CANVAS_LEFT_SHIFT - self.canvas_left_edge
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
        if self.to_draw_selection:
            self.draw_selection(painter)
        self.draw_edges(painter)
        self.draw_layers(painter)
        painter.drawImage(0, self.menu_bar.height(), QImage('images/ToolBar.png'))
        self.highlight_current_button(painter)
        self.draw_buttons(painter)
        painter.end()

    def draw_layers(self, painter):
        painter.drawImage(self.width() - self.TOOLBAR_WIDTH, self.menu_bar.height(), QImage('images/LayersBar.png'))
        self.draw_current_layer(painter)
        for table in self.layer_tables:
            table.draw(painter)

    def highlight_current_button(self, painter):
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(Qt.transparent)
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

    def update_selection_position(self):
        start_x = self.shape_start[0] * self.pixel_size + self.canvas_left_side
        start_y = self.shape_start[1] * self.pixel_size + self.canvas_upper_side
        end_x = self.cursor_position[0] * self.pixel_size + self.canvas_left_side
        end_y = self.cursor_position[1] * self.pixel_size + self.canvas_upper_side
        self.selection_left = min(start_x, end_x)
        self.selection_right = max(start_x, end_x) + self.pixel_size
        self.selection_up = min(start_y, end_y)
        self.selection_down = max(start_y, end_y) + self.pixel_size
        self.selection_width = abs(self.cursor_position[0] - self.shape_start[0]) + 1
        self.selection_height = abs(self.cursor_position[1] - self.shape_start[1]) + 1

    def draw_selection(self, painter):
        width = self.pixel_size / 4
        black_pen = QPen(QColor(0, 0, 0))
        black_pen.setWidth(3)
        white_pen = QPen(QColor(255, 255, 255))
        white_pen.setWidth(3)
        painter.setPen(black_pen)
        for x in range(self.selection_width):
            painter.drawLine(self.selection_left + x * self.pixel_size,
                             self.selection_up, self.selection_left + x * self.pixel_size + width, self.selection_up)
            painter.drawLine(self.selection_left + x * self.pixel_size,
                             self.selection_down, self.selection_left + x * self.pixel_size + width, self.selection_down)
            painter.setPen(white_pen)
            painter.drawLine(self.selection_left + x * self.pixel_size + width,
                             self.selection_up, self.selection_left + x * self.pixel_size + width * 3, self.selection_up)
            painter.drawLine(self.selection_left + x * self.pixel_size + width,
                             self.selection_down, self.selection_left + x * self.pixel_size + width * 3, self.selection_down)
            painter.setPen(black_pen)
            painter.drawLine(self.selection_left + x * self.pixel_size + width * 3,
                             self.selection_up, self.selection_left + x * self.pixel_size + width * 4, self.selection_up)
            painter.drawLine(self.selection_left + x * self.pixel_size + width * 3,
                             self.selection_down, self.selection_left + x * self.pixel_size + width * 4, self.selection_down)
        for y in range(self.selection_height):
            painter.drawLine(self.selection_left, self.selection_up + y * self.pixel_size,
                             self.selection_left, self.selection_up + y * self.pixel_size + width)
            painter.drawLine(self.selection_right, self.selection_up + y * self.pixel_size,
                             self.selection_right, self.selection_up + y * self.pixel_size + width)
            painter.setPen(white_pen)
            painter.drawLine(self.selection_left, self.selection_up + y * self.pixel_size + width,
                             self.selection_left, self.selection_up + y * self.pixel_size + width * 3)
            painter.drawLine(self.selection_right, self.selection_up + y * self.pixel_size + width,
                             self.selection_right, self.selection_up + y * self.pixel_size + width * 3)
            painter.setPen(black_pen)
            painter.drawLine(self.selection_left, self.selection_up + y * self.pixel_size + width * 3,
                             self.selection_left, self.selection_up + y * self.pixel_size + width * 4)
            painter.drawLine(self.selection_right, self.selection_up + y * self.pixel_size + width * 3,
                             self.selection_right, self.selection_up + y * self.pixel_size + width * 4)

    def draw_pixels(self, painter):
        painter.drawImage(self.canvas_left_side, self.canvas_upper_side,
                          self.canvas_as_image.scaled(self.canvas_width, self.canvas_height))
        painter.setBrush(Qt.transparent)
        black_pen = QPen(QColor(0, 0, 0))
        black_pen.setWidth(3)
        painter.setPen(black_pen)
        painter.drawRect(self.canvas_left_side, self.canvas_upper_side, self.canvas_width, self.canvas_height)
        painter.setPen(Qt.black)
        self.draw_grid(painter)

    def draw_grid(self, painter):
        if self.pixel_size > 10:
            for i in range(self.canvas.width + 1):
                x = self.canvas_left_side + i * self.pixel_size
                painter.drawLine(x, self.canvas_upper_side,
                                 x, self.canvas_upper_side + self.canvas_height)
            for i in range(self.canvas.height + 1):
                y = self.canvas_upper_side + i * self.pixel_size
                painter.drawLine(self.canvas_left_side, y,
                                 self.canvas_left_side + self.canvas_width, y)

    def draw_edges(self, painter):
        painter.setPen(Qt.transparent)
        painter.setBrush(QColor('#393939'))
        painter.drawRect(self.vertical_scrollbar.x(), self.vertical_scrollbar.y(),
                         self.vertical_scrollbar.width(),
                         self.vertical_scrollbar.height() + self.horizontal_scrollbar.height() + 1)
        painter.drawRect(self.horizontal_scrollbar.x(), self.horizontal_scrollbar.y(),
                         self.horizontal_scrollbar.width(), self.horizontal_scrollbar.height() + 1)

    def draw_current_layer(self, painter):
        if not self.to_draw_canvas:
            return
        painter.setBrush(Qt.white)
        table = self.layer_tables[self.canvas.current_layer]
        painter.drawRect(table.x - 1, table.y - 1, LayerTable.WIDTH + 2, LayerTable.HEIGHT + 2)

    def draw_buttons(self, painter):
        painter.setPen(Qt.transparent)
        painter.setBrush(QColor(self.canvas.current_color.r, self.canvas.current_color.g,
                                self.canvas.current_color.b))
        for button, image in self.button_images.items():
            painter.drawRect(button.x() + 3, button.y() + 3, self.BUTTON_SIZE - 6, self.BUTTON_SIZE - 6)
            painter.drawImage(button.x(), button.y(), image.scaled(self.BUTTON_SIZE, self.BUTTON_SIZE))
