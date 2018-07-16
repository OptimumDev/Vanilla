from PyQt5.QtWidgets import QMainWindow


class VanillaWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.show()