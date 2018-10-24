from PyQt5.QtWidgets import QDialog, QLabel, QSlider, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QFont


class BrightnessDialog(QDialog):

    WIDTH = 300
    HEIGHT = 150
    FONT = QFont('Arial', 16)
    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 35
    BOTTOM_BUTTON_SHIFT = 10 + BUTTON_HEIGHT
    MIDDLE_BUTTON_SHIFT = 10
    MAXIMUM = 200

    def __init__(self, root, current):
        super().__init__()
        self.brightness = current
        self.success = False
        self.resize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("Brightness")
        self.setWindowIcon(root.windowIcon())
        self.setModal(True)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.WindowCloseButtonHint)

        label = QLabel('Choose Brightness Level:', self)
        label.setFont(self.FONT)
        label.resize(self.WIDTH, self.HEIGHT // 3)
        label.setAlignment(Qt.AlignCenter)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setGeometry(10, label.height() + self.HEIGHT // 24, self.WIDTH // 3 * 2 - 20, self.HEIGHT // 6)
        self.slider.setMaximum(self.MAXIMUM)
        self.slider.setMinimum(0)
        self.slider.setValue(current)
        self.slider.show()
        self.slider.valueChanged[int].connect(self.slider_changed)

        self.edit = QLineEdit(self)
        self.edit.setFont(self.FONT)
        self.edit.setGeometry(self.slider.width() + 20, label.height(), self.WIDTH // 3 - 30, self.HEIGHT // 12 * 3)
        self.edit.textChanged[str].connect(self.text_changed)
        self.edit.setValidator(QIntValidator(0, self.MAXIMUM))
        self.slider_changed(current)

        percent = QLabel('%', self)
        percent.setFont(self.FONT)
        percent.setGeometry(self.edit.x() + self.edit.width(), self.edit.y(), 30, self.edit.height())
        percent.setAlignment(Qt.AlignCenter)

        ok_button = QPushButton('Ok', self)
        ok_button.setGeometry(self.WIDTH / 2 - self.BUTTON_WIDTH - self.MIDDLE_BUTTON_SHIFT,
                              self.HEIGHT - self.BOTTOM_BUTTON_SHIFT,
                              self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        ok_button.setFont(self.FONT)
        ok_button.clicked.connect(self.ok)

        cancel_button = QPushButton('Cancel', self)
        cancel_button.setGeometry(self.WIDTH / 2 + self.MIDDLE_BUTTON_SHIFT,
                                  self.HEIGHT - self.BOTTOM_BUTTON_SHIFT,
                                  self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        cancel_button.setFont(self.FONT)
        cancel_button.clicked.connect(self.cancel)

        self.show()

    def slider_changed(self, value):
        self.brightness = value
        self.edit.setText(str(value))

    def text_changed(self, text):
        if text == "":
            text = 0
        self.brightness = int(text)
        self.slider.setValue(int(text))

    def ok(self):
        self.success = True
        self.close()

    def cancel(self):
        self.close()

    @staticmethod
    def get_brightness(root, current):
        dialog = BrightnessDialog(root, current)
        dialog.exec()
        return dialog.success, dialog.brightness
