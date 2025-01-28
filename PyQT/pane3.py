from custom_widgets import *

Image.CUBIC = Image.BICUBIC

class Pane3(QWidget):
    def __init__(self, parent, controller, screen_width, screen_height):
        self.parent = parent
        super(QWidget, self).__init__(parent)
        grid = QGridLayout(self)

        grid.addWidget(PhotoButton(self, controller), 0, 0)
        self.setLayout(grid)