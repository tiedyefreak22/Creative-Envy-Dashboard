import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class Pane4(QWidget):
    def __init__(self, parent, controller, screen_width, screen_height):
        self.parent = parent
        super(QWidget, self).__init__(parent)