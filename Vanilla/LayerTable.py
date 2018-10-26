from PyQt5.QtWidgets import QLineEdit, QPushButton
from PyQt5.QtGui import QImage, QFont
from PyQt5.QtCore import Qt


class LayerTable:

    WIDTH = 187
    HEIGHT = 100

    def __init__(self, x, y, layer, button, parent):
        self.background = QImage('images/LayerTable.png')
        self.x = x
        self.y = y
        self.layer = layer
        self.button = button
        self.parent = parent

        shift = 5
        self.name_edit = QLineEdit(self.layer.name, parent)
        self.name_edit.setFont(QFont('Arial', 16))
        self.name_edit.textChanged[str].connect(self.change_name)
        self.name_edit.setGeometry(self.x + shift, self.y + shift, self.WIDTH - shift * 2, self.HEIGHT / 4)
        self.name_edit.setAlignment(Qt.AlignCenter)
        self.name_edit.editingFinished.connect(self.name_edit.clearFocus)
        self.name_edit.show()

        self.delete_button = QPushButton('Delete', parent)
        self.delete_button.setGeometry(self.x + shift, self.y + self.HEIGHT / 4 * 3, self.WIDTH - shift * 2,
                                       self.HEIGHT / 4 - shift)
        self.delete_button.clicked.connect(self.delete)
        self.delete_button.show()

    def change_name(self, name):
        self.layer.name = name

    def delete(self):
        if len(self.parent.canvas.layers) == 1:
            return
        self.close()
        self.parent.delete_layer(self)

    def close(self):
        self.button.hide()
        self.button.close()
        self.delete_button.hide()
        self.delete_button.close()
        self.name_edit.hide()
        self.name_edit.close()

    def draw(self, painter):
        painter.setPen(Qt.black)
        painter.drawImage(self.x, self.y, self.background)
        painter.setFont(QFont('Arial', 12))
        painter.drawText(self.x, self.y + self.HEIGHT / 4, self.WIDTH, self.HEIGHT / 2, Qt.AlignCenter,
                         f'Mode: {"Greyscale" if self.layer.greyscale else "RGB"}\n'
                         f'Brightness: {self.layer.brightness}%')
