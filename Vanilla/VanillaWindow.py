from PyQt5.QtWidgets import QMainWindow, QAction, QInputDialog
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import Qt
from Point import Point


class VanillaWindow(QMainWindow):

    SHIFT = 100
    CANVAS_START = Point(200 + SHIFT, SHIFT)

    def __init__(self):
        super().__init__()
        self.draw_canvas = False
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
        size, success = QInputDialog.getInt(self, 'New', 'Enter Size:')
        if success:
            self.create_canvas(size, size)

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