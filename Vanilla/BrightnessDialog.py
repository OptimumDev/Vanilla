from PyQt5.QtWidgets import QDialog


class BrightnessDialog(QDialog):

    def __init__(self, root):
        super().__init__(parent=root)
        self.brightness = 100
        self.resize(300, 200)
        self.setWindowTitle("Brightness")
        self.show()

    @staticmethod
    def get_brightness(root):
        dialog = BrightnessDialog(root)
        dialog.exec()
        return dialog.brightness
