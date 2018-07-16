from PyQt5.QtWidgets import QMainWindow, QAction


class VanillaWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.showMaximized()
        menu_bar = self.menuBar()

        new_action = QAction('&New', self)
        new_action.setShortcut('Ctrl+N')
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(new_action)

        self.show()