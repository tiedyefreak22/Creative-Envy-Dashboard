from custom_widgets import *

Image.CUBIC = Image.BICUBIC

class Pane4(QWidget):
    def __init__(self, parent, controller, screen_width, screen_height):
        self.parent = parent
        super(QWidget, self).__init__(parent)

        self.parent = parent
        self.controller = controller
        self.width = self.controller.width()
        self.height = self.controller.height()
        self.min_dim = min(self.width, self.height)

        # ------------------------------Define Widgets------------------------------
        
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        self.disarmPushButton = QPushButton("Disarm", self)
        self.layout.addWidget(self.disarmPushButton, 0, 0)
        self.disarmPushButton.clicked.connect(self.on_disarm_click)
        # disarm_im = config_pic("moon/" + [i for i in os.listdir("moon/")][0], self.width - (11 * widget_padding), self.height - (11 * widget_padding), 0)
        # disarm_temp = disarm_im.convert('RGBA')
        # new_disarm_img = QImage(
        #     disarm_temp.tobytes('raw', "RGBA"),
        #     disarm_temp.size[0],
        #     disarm_temp.size[1],
        #     QImage.Format.Format_RGBA8888,
        # )
        # self.pushButton.setIcon(QIcon(QPixmap.fromImage(new_disarm_img)))
        self.disarmPushButton.setStyleSheet("background-color: %s; border: 2px solid %s; color: %s" % (Palettes["darkly"]["colors"]["secondary"], Palettes["darkly"]["colors"]["fg"], Palettes["darkly"]["colors"]["info"]))

        self.homePushButton = QPushButton("Home", self)
        self.layout.addWidget(self.homePushButton, 0, 1)
        self.homePushButton.clicked.connect(self.on_home_click)
        # home_im = config_pic("moon/" + [i for i in os.listdir("moon/")][0], self.width - (11 * widget_padding), self.height - (11 * widget_padding), 0)
        # home_temp = home_im.convert('RGBA')
        # new_home_img = QImage(
        #     home_temp.tobytes('raw', "RGBA"),
        #     home_temp.size[0],
        #     home_temp.size[1],
        #     QImage.Format.Format_RGBA8888,
        # )
        # self.pushButton.setIcon(QIcon(QPixmap.fromImage(new_home_img)))
        self.homePushButton.setStyleSheet("background-color: %s; border: 2px solid %s; color: %s" % (Palettes["darkly"]["colors"]["secondary"], Palettes["darkly"]["colors"]["fg"], Palettes["darkly"]["colors"]["info"]))

        self.awayPushButton = QPushButton("Away", self)
        self.layout.addWidget(self.awayPushButton, 0, 2)
        self.awayPushButton.clicked.connect(self.on_away_click)
        # arm_im = config_pic("moon/" + [i for i in os.listdir("moon/")][0], self.width - (11 * widget_padding), self.height - (11 * widget_padding), 0)
        # arm_temp = arm_im.convert('RGBA')
        # new_arm_img = QImage(
        #     arm_temp.tobytes('raw', "RGBA"),
        #     arm_temp.size[0],
        #     arm_temp.size[1],
        #     QImage.Format.Format_RGBA8888,
        # )
        # self.pushButton.setIcon(QIcon(QPixmap.fromImage(new_arm_img)))
        self.awayPushButton.setStyleSheet("background-color: %s; border: 2px solid %s; color: %s" % (Palettes["darkly"]["colors"]["secondary"], Palettes["darkly"]["colors"]["fg"], Palettes["darkly"]["colors"]["info"]))

    @pyqtSlot()
    def on_disarm_click(self):
        print("disarm button pressed\n")

    @pyqtSlot()
    def on_home_click(self):
        print("home button pressed\n")

    @pyqtSlot()
    def on_away_click(self):
        print("away button pressed\n")

    def resizeEvent(self, event):
        self.width = self.controller.width()
        self.height = self.controller.height()
        self.min_dim = min(self.width, self.height)

        font_size = int(self.min_dim * (60 / 500))
        if font_size <= 0:
            font_size = 1
        font = QFont('Arial', font_size)
        self.disarmPushButton.setFont(font)
        self.homePushButton.setFont(font)
        self.awayPushButton.setFont(font)
        
        self.disarmPushButton.setFixedSize(int(self.min_dim * (3 / 5)) - (2 * widget_padding), int(self.min_dim * (3 / 5)) - (2 * widget_padding))
        self.homePushButton.setFixedSize(int(self.min_dim * (3 / 5)) - (2 * widget_padding), int(self.min_dim * (3 / 5)) - (2 * widget_padding))
        self.awayPushButton.setFixedSize(int(self.min_dim * (3 / 5)) - (2 * widget_padding), int(self.min_dim * (3 / 5)) - (2 * widget_padding))