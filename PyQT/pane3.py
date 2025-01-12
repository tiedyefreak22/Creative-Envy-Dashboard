import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QGridLayout
from PyQt5.QtGui import QIcon, QPixmap, QImage, QColor, QFont
from PyQt5.QtCore import pyqtSlot, Qt, QTimer, QTime
from settings import *
from custom_widgets import *

class Pane3(QWidget):
    def __init__(self, parent, controller, screen_width, screen_height):
        self.parent = parent
        super(QWidget, self).__init__(parent)
        grid = QGridLayout(self)

        grid.addWidget(PhotoButton(self, controller), 0, 0)
        self.setLayout(grid)