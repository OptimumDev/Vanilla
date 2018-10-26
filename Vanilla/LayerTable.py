from PyQt5.QtWidgets import QLineEdit, QPushButton
from PyQt5.QtGui import QImage, QFont
from PyQt5.QtCore import Qt


class LayerTable:

    WIDTH = 187
    HEIGHT = 100

    def __init__(self, x, y, layer, button, parent=None):
        self.background = QImage('images/LayerTable.png')
        self.x = x
        self.y = y
        self.layer = layer
        self.button = button

        shift = 5
        self.name_label = QLineEdit(self.layer.name, parent)
        self.name_label.setFont(QFont('Arial', 16))
        self.name_label.textChanged[str].connect(self.change_name)
        self.name_label.setGeometry(self.x + shift, self.y + shift, self.WIDTH - shift * 2, self.HEIGHT / 4)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.editingFinished.connect(self.name_label.clearFocus)
        self.name_label.show()

        self.delete_button = QPushButton('Delete', parent)
        self.delete_button.setGeometry(self.x + shift, self.y + self.HEIGHT / 4 * 3, self.WIDTH - shift * 2,
                                       self.HEIGHT / 4 - shift)
        self.delete_button.show()

    def change_name(self, name):
        self.layer.name = name

    def draw(self, painter):
        painter.setPen(Qt.black)
        painter.drawImage(self.x, self.y, self.background)
        painter.setFont(QFont('Arial', 12))
        painter.drawText(self.x, self.y + self.HEIGHT / 4, self.WIDTH, self.HEIGHT / 2, Qt.AlignCenter,
                         f'Mode: {"Greyscale" if self.layer.greyscale else "RGB"}\n'
                         f'Brightness: {self.layer.brightness}%')
