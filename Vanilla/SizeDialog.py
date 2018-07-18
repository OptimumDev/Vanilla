from PyQt5.QtWidgets import QDialog, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class SizeDialog(QDialog):

    BUTTON_WIDTH = 80
    BUTTON_HEIGHT = 30
    MIDDLE_BUTTON_SHIFT = 20
    BOTTOM_BUTTON_SHIFT = 20 + BUTTON_HEIGHT
    BUTTON_FONT = QFont('Arial', 12)

    LABEL_FONT = QFont('Arial', 16)
    LABEL_HEIGHT = 50

    WIDTH = 300
    HEIGHT = LABEL_HEIGHT * 3 + BOTTOM_BUTTON_SHIFT

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
        cancel_button.setGeometry(self.WIDTH / 2 - cancel_button.width() - self.MIDDLE_BUTTON_SHIFT,
                                  self.HEIGHT - self.BOTTOM_BUTTON_SHIFT,
                                  self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        cancel_button.setFont(self.BUTTON_FONT)
        cancel_button.clicked.connect(self.cancel)

        ok_button = QPushButton('Ok', self)
        ok_button.setGeometry(self.WIDTH / 2 + self.MIDDLE_BUTTON_SHIFT, self.HEIGHT - self.BOTTOM_BUTTON_SHIFT,
                              self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        ok_button.setFont(self.BUTTON_FONT)
        ok_button.clicked.connect(self.ok)

        enter_label = QLabel('Please Enter Canvas Size:', self)
        enter_label.setGeometry(0, 0, self.WIDTH, self.LABEL_HEIGHT)
        enter_label.setFont(self.LABEL_FONT)
        enter_label.setAlignment(Qt.AlignCenter)

        width_label = QLabel('Width', self)
        width_label.setGeometry(10, self.LABEL_HEIGHT, self.WIDTH / 2, self.LABEL_HEIGHT)
        width_label.setFont(self.LABEL_FONT)

        height_label = QLabel('Height', self)
        height_label.setGeometry(10, self.LABEL_HEIGHT * 2, self.WIDTH / 2, self.LABEL_HEIGHT)
        height_label.setFont(self.LABEL_FONT)

        # TO DO: width and height input with validator

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
