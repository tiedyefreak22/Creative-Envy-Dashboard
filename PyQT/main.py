'''
  library imports
        |
    settings.py
        |
functions_and_classes.py
        |
  custom_widgets.py
       /\\
   pane1..4.py
       \\/
     main.py
'''

from pane1 import *
from pane2 import *
from pane3 import *
from pane4 import *

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Creative Envy'
        self.setWindowTitle(self.title)
        self.setMaximumWidth(1920)
        self.setMaximumHeight(1200)
        self.setGeometry(0, 0, screen_width, screen_height) # Left, Top, Width, Height
        self.showMaximized()
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()
    
class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = Pane1(self, parent, screen_width, screen_height)
        self.tab2 = Pane2(self, parent, screen_width, screen_height)
        self.tab3 = Pane3(self, parent, screen_width, screen_height)
        self.tab4 = Pane4(self, parent, screen_width, screen_height)
        
        # Add tabs
        self.tabs.addTab(self.tab1, "Weather")
        self.tabs.addTab(self.tab2, "Bees")
        self.tabs.addTab(self.tab3, "Photos")
        self.tabs.addTab(self.tab4, "Alarm")
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        stylesheet = """ 
            QTabBar::tab:selected {background: %s;}
            QTabWidget>QWidget {background: %s;}
            """ % (Palettes["darkly"]["colors"]["light"], Palettes["darkly"]["colors"]["bg"])
        self.setStyleSheet(stylesheet)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    size = app.primaryScreen().size()
    screen_width = 1920 #size.width()
    screen_height = 1200 #size.height()
    ex = App()
    sys.exit(app.exec_())