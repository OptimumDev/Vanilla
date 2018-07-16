import sys
from PyQt5.QtWidgets import QApplication
from VanillaWindow import VanillaWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VanillaWindow()
    sys.exit(app.exec_())