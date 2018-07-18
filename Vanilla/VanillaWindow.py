from PyQt5.QtWidgets import QMainWindow, QAction, QDialog, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QImage, QFont
from PyQt5.QtCore import Qt
from Point import Point


class SizeDialog(QDialog):

    WIDTH = 300
    HEIGHT = 300
    FONT = QFont('Arial', 16)

    BUTTON_WIDTH = 80
    BUTTON_HEIGHT = 30
    MIDDLE_BUTTON_SHIFT = 20
    BOTTOM_BUTTON_SHIFT = 20 + BUTTON_HEIGHT
    BUTTON_FONT = QFont('Arial', 12)

    LABEL_HEIGHT = 50


    def __init__(self, root):
        super().__init__()
        self.root = root
        self.success = False
        self.canvas_width = 32
        self.canvas_height = 32
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.WindowCloseButtonHint)
        self.resize(self.WIDTH, self.HEIGHT)

        cancel_button = QPushButton('Cancel', self)
        cancel_button.resize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        cancel_button.move(self.WIDTH / 2 - cancel_button.width() - self.MIDDLE_BUTTON_SHIFT,
                           self.HEIGHT - self.BOTTOM_BUTTON_SHIFT)
        cancel_button.setFont(self.BUTTON_FONT)
        cancel_button.clicked.connect(self.cancel)

        ok_button = QPushButton('Ok', self)
        ok_button.resize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        ok_button.move(self.HEIGHT / 2 + self.MIDDLE_BUTTON_SHIFT, self.HEIGHT - self.BOTTOM_BUTTON_SHIFT)
        ok_button.setFont(self.BUTTON_FONT)
        ok_button.clicked.connect(self.ok)

        enter_label = QLabel('Please Enter Canvas Size:', self)
        enter_label.setGeometry(0, 0, self.width(), self.LABEL_HEIGHT)
        enter_label.setFont(self.FONT)
        enter_label.setAlignment(Qt.AlignCenter)

    def cancel(self):
        self.close()

    def ok(self):
        self.success = True
        self.close()

    @staticmethod
    def get_size(root):
        dialog = SizeDialog(root)
        dialog.exec()
        return dialog.success, dialog.canvas_width, dialog.canvas_height


class VanillaWindow(QMainWindow):

    SHIFT = 100
    CANVAS_START = Point(200 + SHIFT, SHIFT)

    def __init__(self):
        super().__init__()
        self.draw_canvas = False
        self.canvas_width = 32
        self.canvas_height = 32
        self.initUI()

    def initUI(self):
        self.showMaximized()
        self.setStyleSheet('QMainWindow{background-color: Gray;} QMenuBar::item::selected{background-color: #202020;}')
        self.create_menu_bar()

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

    def ask_size(self):
        success, width, height = SizeDialog.get_size(self)
        if success:
            self.create_canvas(width, height)

    def create_canvas(self, width, height):
        self.canvas_width = width
        self.canvas_height = height
        self.draw_canvas = True

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        if self.draw_canvas:
            size = self.height() - self.CANVAS_START.y - self.SHIFT
            painter.fillRect(# self.CANVAS_START.x, self.CANVAS_START.y,
                             (self.width() - size) / 2, self.SHIFT,
                             # self.width() - self.CANVAS_START.x - self.SHIFT,
                             # self.height() - self.CANVAS_START.y - self.SHIFT,
                             size, size,
                             Qt.white)
            painter.drawRect((self.width() - size) / 2, self.SHIFT, size, size,)
            for i in range(1, self.canvas_height):
                painter.drawLine((self.width() - size) / 2, self.SHIFT + size / self.canvas_height * i,
                                 (self.width() - size) / 2 + size, self.SHIFT + size / self.canvas_height * i)
            for i in range(1, self.canvas_width):
                painter.drawLine((self.width() - size) / 2 + size / self.canvas_width * i, self.SHIFT,
                                 (self.width() - size) / 2 + size / self.canvas_width * i, self.SHIFT + size)
        painter.drawImage(0, self.menu_bar.height(), QImage('images/ToolBar.png'))

        painter.end()