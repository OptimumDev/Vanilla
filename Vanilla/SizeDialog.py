from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import Qt


class SizeDialog(QDialog):

    BUTTON_WIDTH = 80
    BUTTON_HEIGHT = 30
    MIDDLE_BUTTON_SHIFT = 20
    BOTTOM_BUTTON_SHIFT = 20 + BUTTON_HEIGHT
    BUTTON_FONT = QFont('Arial', 12)

    LABEL_FONT = QFont('Arial', 16)
    LABEL_HEIGHT = 30
    LABEL_WIDTH = 80
    LABEL_SIDE_SHIFT = 10
    LABEL_UPPER_SHIFT = 20

    WIDTH = 300
    HEIGHT = (LABEL_HEIGHT + LABEL_UPPER_SHIFT) * 3 + BOTTOM_BUTTON_SHIFT

    def __init__(self, root):
        super().__init__()
        self.root = root
        self.success = False
        self.canvas_width = 32
        self.canvas_height = 32
        self.initUI()

    def initUI(self):
        self.setWindowTitle('New')
        self.setWindowIcon(self.root.windowIcon())
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.WindowCloseButtonHint)
        self.resize(self.WIDTH, self.HEIGHT)

        cancel_button = QPushButton('Cancel', self)
        cancel_button.setGeometry(self.WIDTH / 2 - self.BUTTON_WIDTH - self.MIDDLE_BUTTON_SHIFT,
                                  self.HEIGHT - self.BOTTOM_BUTTON_SHIFT,
                                  self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        cancel_button.setFont(self.BUTTON_FONT)
        cancel_button.clicked.connect(self.cancel)

        self.ok_button = QPushButton('Ok', self)
        self.ok_button.setGeometry(self.WIDTH / 2 + self.MIDDLE_BUTTON_SHIFT, self.HEIGHT - self.BOTTOM_BUTTON_SHIFT,
                              self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.ok_button.setFont(self.BUTTON_FONT)
        self.ok_button.clicked.connect(self.ok)

        enter_label = QLabel('Please Enter Canvas Size:', self)
        enter_label.setGeometry(0, 0, self.WIDTH, self.LABEL_HEIGHT)
        enter_label.setFont(self.LABEL_FONT)
        enter_label.setAlignment(Qt.AlignCenter)

        width_label = QLabel('Width', self)
        width_label.setGeometry(self.LABEL_SIDE_SHIFT, self.LABEL_HEIGHT + self.LABEL_UPPER_SHIFT,
                                self.LABEL_WIDTH, self.LABEL_HEIGHT)
        width_label.setFont(self.LABEL_FONT)

        height_label = QLabel('Height', self)
        height_label.setGeometry(self.LABEL_SIDE_SHIFT, (self.LABEL_HEIGHT + self.LABEL_UPPER_SHIFT) * 2,
                                 self.LABEL_WIDTH, self.LABEL_HEIGHT)
        height_label.setFont(self.LABEL_FONT)

        validator = QIntValidator(1, 2000)

        width_input = QLineEdit(f'{self.canvas_width}', self)
        width_input.setGeometry(self.LABEL_WIDTH, width_label.y(),
                                self.WIDTH - self.LABEL_SIDE_SHIFT - self.LABEL_WIDTH, self.LABEL_HEIGHT)
        width_input.setFont(self.BUTTON_FONT)
        width_input.setValidator(validator)
        width_input.textChanged[str].connect(self.width_changed)

        height_input = QLineEdit(f'{self.canvas_height}', self)
        height_input.setGeometry(self.LABEL_WIDTH, height_label.y(),
                                 self.WIDTH - self.LABEL_SIDE_SHIFT - self.LABEL_WIDTH, self.LABEL_HEIGHT)
        height_input.setFont(self.BUTTON_FONT)
        height_input.setValidator(validator)
        height_input.textChanged[str].connect(self.height_changed)

    def width_changed(self, width):
        if width == '' or int(width) <= 0:
            self.ok_button.setDisabled(True)
        else:
            self.canvas_width = int(width)
            self.ok_button.setDisabled(False)

    def height_changed(self, height):
        if height == '' or int(height) <= 0:
            self.ok_button.setDisabled(True)
        else:
            self.canvas_height = int(height)
            self.ok_button.setDisabled(False)

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
