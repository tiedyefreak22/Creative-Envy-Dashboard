import sys
from PyQt5.QtGui import QPixmap, QImage, QColor, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QTime, pyqtSlot, QSize
from PyQt5.QtWidgets import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure
import matplotlib.patches as patches
import numpy as np
import PIL
from PIL import Image, ImageDraw
import pandas as pd
import time
from datetime import datetime, timedelta
from settings import *
from functions_and_classes import *
from math import ceil
import warnings
warnings.filterwarnings("ignore")

class GraphWidget(QtWidgets.QWidget):
    def __init__(self, parent, controller, text, lf_values, dpi = 100, *args, **kwargs):
        super().__init__()
        self.parent = parent
        self.controller = controller
        self.width = int(self.controller.width() / 5)
        self.height = int(self.controller.height() / 3)
        self.text = text
        self.lf_values = lf_values
        self.dpi = dpi
        self.min_dim = min(self.width, self.height)
        self.figsize = ((self.min_dim  - (2 * widget_padding)) / self.dpi, (self.min_dim  - (2 * widget_padding)) / self.dpi)
        
        # ------------------------------Define Widgets------------------------------
        
        self.layout = QtWidgets.QGridLayout(self)
        self.setLayout(self.layout)
        
        self.canvas1 = FigureCanvas(Figure(facecolor=Palettes["darkly"]["colors"]["bg"]))
        self.layout.addWidget(self.canvas1, 0, 0, 7, 2)
        
        self.master_label = QLabel(self)
        self.layout.addWidget(self.master_label, 0, 0, 7, 2)
        
        self.main_graph_label = QLabel(self)
        self.main_graph_label.setStyleSheet("color: %s" % (Palettes["darkly"]["colors"]["info"]))
        self.layout.addWidget(self.main_graph_label, 3, 0, 1, 2)

        self.graph_label_left = QLabel(self)
        self.graph_label_left.setStyleSheet("color: %s" % (Palettes["darkly"]["colors"]["light"]))
        self.layout.addWidget(self.graph_label_left, 4, 0, 1, 1)

        self.graph_label_right = QLabel(self)
        self.graph_label_right.setStyleSheet("color: %s" % (Palettes["darkly"]["colors"]["light"]))
        self.layout.addWidget(self.graph_label_right, 4, 1, 1, 1)

        self.graph_text = QLabel(self)
        self.graph_text.setStyleSheet("color: %s" % (Palettes["darkly"]["colors"]["fg"]))
        self.layout.addWidget(self.graph_text, 5, 0, 7, 2)

        # ------------------------------Timer------------------------------

        self.update_widgets()
        timer = QTimer(self)
        timer.timeout.connect(self.update_widgets)
        timer.start(300000)

    def update_widgets(self):
        self.main_graph_label.setText(str(round(self.lf_values.values[-1], 1)))
        self.graph_label_left.setText(str(round(min(self.lf_values.values), 1)))
        self.graph_label_right.setText(str(round(max(self.lf_values.values), 1)))
        self.graph_text.setText(self.text)

        self.canvas1.figure.clf()
        self.ax1 = self.canvas1.figure.subplots()
        self.ax1.set_axis_off()
        circ = patches.Circle(tuple([(i * self.dpi / 2) for i in self.figsize]), radius=self.figsize[0] * self.dpi / 2, transform=self.ax1.transData, facecolor='none')
        self.ax1.plot(self.lf_values, color=Palettes["darkly"]["colors"]["primary"], clip_on=False)
        self.canvas1.draw()
        
        # Now we can save it to a numpy array.
        data = np.frombuffer(self.canvas1.buffer_rgba(), dtype=np.uint8)
        data = data.reshape(self.canvas1.get_width_height()[::-1] + (4,))

        if np.size(data) > 0:
            im = self.ax1.imshow(data)
            im.set_clip_path(circ)
            self.ax1.set_axis_off()

        self.ax2 = self.canvas1.figure.subplots()
        data = [self.lf_values.values[-1], max(self.lf_values.values) - self.lf_values.values[-1]]
        if not sum(data) == 0:
            self._wedges, _ = self.ax2.pie(data, wedgeprops=dict(width=0.15), startangle=-90 + ((data[1] / (2 * sum(data))) * 360), radius=1.5, colors=[Palettes["darkly"]["colors"]["info"], Palettes["darkly"]["colors"]["secondary"]])
        else:
            self._wedges, _ = self.ax2.pie([1, 1], wedgeprops=dict(width=0.15), startangle=0, radius=1.5, colors=[Palettes["darkly"]["colors"]["info"], Palettes["darkly"]["colors"]["secondary"]])
        self.canvas1.draw()

    def resizeEvent(self, event):
        self.width = int(self.controller.width() / 5)
        self.height = int(self.controller.height() / 3)
        self.min_dim = min(self.width, self.height)

        self.update_widgets()

        font_size = int(self.min_dim * (70 / 500))
        if font_size <= 0:
            font_size = 1
        font = QFont('Arial', font_size)
        self.main_graph_label.setFont(font)

        font_size = int(self.min_dim * (25 / 500))
        if font_size <= 0:
            font_size = 1
        font = QFont('Arial', font_size)
        self.graph_label_left.setFont(font)

        font_size = int(self.min_dim * (25 / 500))
        if font_size <= 0:
            font_size = 1
        font = QFont('Arial', font_size)
        self.graph_label_right.setFont(font)
        
        font_size = int(self.min_dim * (35 / 500))
        if font_size <= 0:
            font_size = 1
        font = QFont('Arial', font_size)
        self.graph_text.setFont(font)

        offset = 0.32
        master_geom = (
            widget_padding,
            widget_padding,
            self.min_dim - (2 * widget_padding),
            self.min_dim - (2 * widget_padding),
        )
        sublabel_geom = (
            int(((self.width - self.min_dim) / 2) + self.min_dim * offset),
            int(((self.height - self.min_dim) / 2) + self.min_dim * offset),
            int(self.min_dim - 2 * (self.min_dim * offset)),
            int(self.min_dim - 2 * (self.min_dim * offset)),
        )
        self.master_label.setGeometry(*master_geom)
        self.main_graph_label.setGeometry(*master_geom)
        self.graph_label_left.setGeometry(*sublabel_geom)
        self.graph_label_right.setGeometry(*sublabel_geom)
        self.graph_text.setGeometry(*master_geom)
        self.master_label.setStyleSheet("border : 2px solid %s" % Palettes["darkly"]["colors"]["fg"]) 

        self.master_label.setAlignment(Qt.AlignCenter)
        self.main_graph_label.setAlignment(Qt.AlignCenter)
        self.graph_label_left.setAlignment(Qt.AlignCenter)
        self.graph_label_right.setAlignment(Qt.AlignCenter)
        self.graph_text.setAlignment(Qt.AlignHCenter)

class EmptyLF(QWidget):
    def __init__(self, parent, controller, width = None, height = None, border = True, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.controller = controller
        if (width is None) or (height is None):
            min_dim = min(int(self.controller.width() / 5), int(self.controller.height() / 3))
            self.width = min_dim
            self.height = min_dim
        else:
            self.width = width
            self.height = height
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.empty_label = QLabel()
        self.empty_label.setGeometry(widget_padding, widget_padding, self.width - (2 * widget_padding), self.height - (2 * widget_padding))
        self.empty_label.setAlignment(Qt.AlignCenter)
        if border:
            self.empty_label.setStyleSheet("background-color: %s; border: 2px solid %s" % (Palettes["darkly"]["colors"]["bg"], Palettes["darkly"]["colors"]["fg"]))
        else:
            self.empty_label.setStyleSheet("background-color: %s" % (Palettes["darkly"]["colors"]["bg"]))
        self.layout.addWidget(self.empty_label)

class WeatherWidget(QWidget):
    def __init__(self, parent, controller, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        super(QWidget, self).__init__(parent, *args, **kwargs)
        self.width = int(self.controller.width() * 2 / 5)
        self.height = int(self.controller.height() / 3)
        self.min_dim = min(int(self.width / 2), self.height)
        
        # ------------------------------Define Widgets------------------------------
        
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        self.canvas1 = FigureCanvas(Figure(facecolor=Palettes["darkly"]["colors"]["bg"]))
        self.layout.addWidget(self.canvas1, 0, 0, 7, 3)
        
        self.master_label = QLabel(self)
        self.layout.addWidget(self.master_label, 0, 0, 7, 3)
        
        self.weather_text = QLabel(self)
        self.weather_text.setStyleSheet("color: %s" % (Palettes["darkly"]["colors"]["fg"]))
        self.layout.addWidget(self.weather_text, 5, 0, 7, 3)

        self.forecast_thumb1 = QLabel(self)
        self.weather_text.setStyleSheet("color: %s" % (Palettes["darkly"]["colors"]["fg"]))
        self.layout.addWidget(self.forecast_thumb1, 5, 0, 7, 3)

        self.forecast_thumb2 = QLabel(self)
        self.weather_text.setStyleSheet("color: %s" % (Palettes["darkly"]["colors"]["fg"]))
        self.layout.addWidget(self.forecast_thumb2, 5, 1, 7, 3)

        self.forecast_thumb3 = QLabel(self)
        self.weather_text.setStyleSheet("color: %s" % (Palettes["darkly"]["colors"]["fg"]))
        self.layout.addWidget(self.forecast_thumb3, 5, 2, 7, 3)

        # ------------------------------Timer------------------------------
        
        self.forecast_updater()
        timer = QTimer(self)
        timer.timeout.connect(self.forecast_updater)
        timer.start(86400000)
        
    def forecast_updater(self):
        self.weather_text.setText("Forecast")
        # if internet_connection:
            # response, _, _ = GET_WEATHER_ICON()
            # for idx, (text, url) in enumerate(response):
            #     with urllib.request.urlopen(url) as u:
            #         raw_data = u.read()            
                
            #     # now create the ImageTk PhotoImage:
            #     self.img[idx] = config_pic(io.BytesIO(raw_data), (self.width / 3) - (5 * self.padding), self.height - (5 * self.padding), self.padding)
            #     # imagelab1 = Label(
            #     #     self,
            #     #     image = self.img[idx],
            #     # )
            #     # imagelab1.place(relx = (0.167 + 0.33 * idx), rely = 0.4, anchor = CENTER)
    
            #     # imagelab2 = Label(
            #     #     self,
            #     #     text = text,
            #     #     font = ("Helvetica’", 16),
            #     # )
            #     # imagelab2.place(relx = (0.167 + 0.33 * idx), rely = 0.85, anchor = CENTER)
                    
    def resizeEvent(self, event):
        self.width = int(self.controller.width() * 2 / 5)
        self.height = int(self.controller.height() / 3)
        self.min_dim = min(int(self.width / 2), self.height)

        self.forecast_updater()

        font_size = int(self.min_dim * (35 / 500))
        if font_size <= 0:
            font_size = 1
        font = QFont('Arial', font_size)
        self.weather_text.setFont(font)

        master_geom = (
            widget_padding,
            widget_padding,
            self.min_dim * 2 - (2 * widget_padding),
            self.min_dim - (2 * widget_padding),
        )

        self.master_label.setGeometry(*master_geom)
        self.weather_text.setGeometry(*master_geom)
        self.master_label.setStyleSheet("border : 2px solid %s" % Palettes["darkly"]["colors"]["fg"]) 

        self.master_label.setAlignment(Qt.AlignCenter)
        self.weather_text.setAlignment(Qt.AlignHCenter)

class CustomSmallImg(QWidget):
    def __init__(self, parent, controller, *args, **kwargs):
        super(QWidget, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller
        self.width = int(self.controller.width() / 5)
        self.height = int(self.controller.height() / 3)
        self.min_dim = min(self.width, self.height)

        # ------------------------------Define Widgets------------------------------

        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        self.master_label = QLabel(self)
        self.layout.addWidget(self.master_label, 0, 0, 3, 3)
        
        self.moon_label = QLabel(self)
        self.layout.addWidget(self.moon_label, 1, 1)

        # ------------------------------Timer------------------------------

        self.getImage()
        timer = QTimer(self)
        timer.timeout.connect(self.getImage)
        timer.start(86400000)

    def getImage(self):
        if internet_connection:
            GET_MOON_IMAGE()

        im = config_pic("moon/" + [i for i in os.listdir("moon/")][0], self.min_dim - (4 * widget_padding), self.min_dim - (4 * widget_padding), 0)
        temp = im.convert('RGBA')
        new_img = QImage(
            temp.tobytes('raw', "RGBA"),
            temp.size[0],
            temp.size[1],
            QImage.Format.Format_RGBA8888,
        )
        self.moon_pixmap = QPixmap.fromImage(new_img)
        self.hex_bg = '#%02x%02x%02x' % tuple(int(i) for i in np.nanmedian(np.nanmedian(im, 0), 0))

    def resizeEvent(self, event):
        self.width = int(self.controller.width() / 5)
        self.height = int(self.controller.height() / 3)
        self.min_dim = min(self.width, self.height)
        
        self.master_label.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.moon_label.setGeometry(widget_padding, widget_padding, self.min_dim - (4 * widget_padding), self.min_dim - (4 * widget_padding))

        self.master_label.setStyleSheet("background-color: black; border: 2px solid %s" % (Palettes["darkly"]["colors"]["fg"]))
        # self.master_label.setStyleSheet("background-color: %s; border: 2px solid %s" % (Palettes["darkly"]["colors"]["bg"], Palettes["darkly"]["colors"]["fg"]))
        self.master_label.setAlignment(Qt.AlignCenter)
        self.moon_label.setAlignment(Qt.AlignCenter)
        
        self.getImage()
        self.moon_pixmap.scaled(self.min_dim - (4 * widget_padding), self.min_dim - (4 * widget_padding), Qt.KeepAspectRatio, Qt.FastTransformation)
        self.moon_label.setPixmap(self.moon_pixmap)
        
class CustomClock(QWidget):
    def __init__(self, parent, controller, *args, **kwargs): 
        super(QWidget, self).__init__(parent, *args, **kwargs)
        self.parent = parent
        self.controller = controller
        self.width = int(self.controller.width() / 5)
        self.height = int(self.controller.height() / 3)
        self.min_dim = min(self.width, self.height)

        # ------------------------------Define Widgets------------------------------
        
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.master_label = QLabel(self)
        self.layout.addWidget(self.master_label, 0, 0, 3, 1)
        
        self.time_label = QLabel(self)
        self.time_label.setStyleSheet("color: %s" % (Palettes["darkly"]["colors"]["info"]))
        self.layout.addWidget(self.time_label, 1, 0)

        self.sunrise_label = QLabel(self)
        self.sunrise_label.move(self.sunrise_label.x(), self.sunrise_label.y() + 60)
        self.sunrise_label.setStyleSheet("color: %s" % (Palettes["darkly"]["colors"]["light"]))
        self.layout.addWidget(self.sunrise_label, 0, 0)

        self.sunset_label = QLabel(self)
        self.sunset_label.move(self.sunset_label.x(), self.sunset_label.y() - 70)
        self.sunset_label.setStyleSheet("color: %s" % (Palettes["darkly"]["colors"]["light"]))
        self.layout.addWidget(self.sunset_label, 2, 0)
        
        # ------------------------------Timer------------------------------

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.updateTime()
        timer2 = QTimer(self)
        timer2.timeout.connect(self.updateTime)
        timer2.start(86400000)

    def showTime(self):
        self.time_label.setText(datetime.now().strftime('%I:%M:%S %p'))

    def updateTime(self):
        self.sunrise_label.setText("Sunrise: %s" % datetime.now().strftime('%I:%M:%S %p'))
        self.sunset_label.setText("Sunset: %s" % datetime.now().strftime('%I:%M:%S %p'))

    def resizeEvent(self, event):
        self.width = int(self.controller.width() / 5)
        self.height = int(self.controller.height() / 3)
        self.min_dim = min(self.width, self.height)
        
        font_size = int(self.min_dim * (60 / 500))
        if font_size <= 0:
            font_size = 1
        font = QFont('Arial', font_size)
        self.time_label.setFont(font)

        font_size = int(self.min_dim * (32 / 500))
        if font_size <= 0:
            font_size = 1
        font = QFont('Arial', font_size)
        self.sunrise_label.setFont(font)

        font_size = int(self.min_dim * (32 / 500))
        if font_size <= 0:
            font_size = 1
        font = QFont('Arial', font_size)
        self.sunset_label.setFont(font)

        master_geom = (
            widget_padding,
            widget_padding,
            self.min_dim - (2 * widget_padding),
            self.min_dim - (2 * widget_padding),
        )

        self.master_label.setGeometry(*master_geom)
        self.time_label.setGeometry(*master_geom)
        self.sunrise_label.setGeometry(*master_geom)
        self.sunset_label.setGeometry(*master_geom)
        
        self.master_label.setStyleSheet("background-color: %s; border: 2px solid %s" % (Palettes["darkly"]["colors"]["bg"], Palettes["darkly"]["colors"]["fg"]))
        self.master_label.setAlignment(Qt.AlignCenter)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.sunrise_label.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        self.sunset_label.setAlignment(Qt.AlignHCenter)

class PhotoButton(QWidget):
    def __init__(self, parent, controller, *args, **kwargs):
        super(QWidget, self).__init__(parent, *args, **kwargs)
        
        self.parent = parent
        self.controller = controller
        self.width = self.controller.width()
        self.height = self.controller.height()
        self.min_dim = min(self.width, self.height)

        # ------------------------------Define Widgets------------------------------
        
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        self.pushButton = QToolButton(self)
        self.layout.addWidget(self.pushButton, 0, 0)
        self.pushButton.clicked.connect(self.on_click)
        
        # ------------------------------Timer------------------------------

        self.getImage()
        timer = QTimer(self)
        timer.timeout.connect(self.on_click)
        timer.start(86400000)

    def getImage(self):
        if internet_connection:
            GET_MOON_IMAGE()

        im = config_pic("moon/" + [i for i in os.listdir("moon/")][0], self.width - (11 * widget_padding), self.height - (11 * widget_padding), 0)
        temp = im.convert('RGBA')
        new_img = QImage(
            temp.tobytes('raw', "RGBA"),
            temp.size[0],
            temp.size[1],
            QImage.Format.Format_RGBA8888,
        )
        self.pushButton.setIcon(QIcon(QPixmap.fromImage(new_img)))
        hex_bg = '#%02x%02x%02x' % tuple(int(i) for i in np.nanmedian(np.nanmedian(im, 0), 0))
        self.pushButton.setStyleSheet("background-color: %s; border: 2px solid %s" % (hex_bg, Palettes["darkly"]["colors"]["fg"]))

    def resizeEvent(self, event):
        self.width = self.controller.width()
        self.height = self.controller.height()
        self.min_dim = min(self.width, self.height)
        
        self.pushButton.setIconSize(QSize(self.width - (11 * widget_padding), self.height - (11 * widget_padding)))

    @pyqtSlot()
    def on_click(self):
        self.getImage()
        print("button pressed\n")