import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class Pane3(QWidget):
    def __init__(self, parent, controller, screen_width, screen_height):
        self.parent = parent
        super(QWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)
        self.pushButton = QPushButton("PyQt5 button")
        self.layout.addWidget(self.pushButton)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())