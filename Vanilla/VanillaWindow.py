from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtGui import QPainter, QImage


class VanillaWindow(QMainWindow):

    def __init__(self):
        super().__init__()

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
        

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        painter.drawImage(0, self.menu_bar.height(), QImage('images/ToolBar.png'))

        painter.end()