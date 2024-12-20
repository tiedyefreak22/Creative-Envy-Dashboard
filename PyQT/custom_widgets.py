import sys
#from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtWidgets import *
# from PyQt5.QtGui import * 
# from PyQt5.QtCore import *
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

widget_padding = 10

class GraphWidget(QtWidgets.QWidget):
    def __init__(self, parent, controller, text, lf_values, dpi = 100, *args, **kwargs):
        super().__init__()
        self.parent = parent
        self.controller = controller
        self.width = int(self.controller.frameGeometry().width() / 5)
        self.height = int(self.controller.frameGeometry().height() / 3)
        self.text = text
        self.lf_values = lf_values
        self.dpi = dpi
        self.min_dim = min(self.width, self.height)

        # ------------------------------Graphs------------------------------

        self.figsize = ((self.min_dim  - (2 * widget_padding)) / self.dpi, (self.min_dim  - (2 * widget_padding)) / self.dpi)

        self.layout = QtWidgets.QGridLayout(self)
        self.setLayout(self.layout)

        canvas1 = FigureCanvas(Figure(figsize=self.figsize, facecolor=Palettes["darkly"]["colors"]["bg"]))
        self.layout.addWidget(canvas1, 0, 0, 7, 2)
        self.ax1 = canvas1.figure.subplots()
        self.ax1.set_axis_off()
        circ = patches.Circle(tuple([(i * self.dpi / 2) for i in self.figsize]), radius=self.figsize[0] * self.dpi / 2, transform=self.ax1.transData, facecolor='none')
        self._line1, = self.ax1.plot(self.lf_values, color=Palettes["darkly"]["colors"]["primary"], clip_on=False)
        canvas1.draw()
        
        # Now we can save it to a numpy array.
        data = np.frombuffer(canvas1.buffer_rgba(), dtype=np.uint8)
        data = data.reshape(canvas1.get_width_height()[::-1] + (4,))
        
        im = self.ax1.imshow(data)
        im.set_clip_path(circ)
        self.ax1.set_axis_off()

        self.ax2 = canvas1.figure.subplots()
        data = [self.lf_values.values[-1], max(self.lf_values.values) - self.lf_values.values[-1]]
        if not sum(data) == 0:
            self._wedges, _ = self.ax2.pie(data, wedgeprops=dict(width=0.15), startangle=-90 + ((data[1] / (2 * sum(data))) * 360), radius=1.5, colors=[Palettes["darkly"]["colors"]["info"], Palettes["darkly"]["colors"]["secondary"]])
        else:
            self._wedges, _ = self.ax2.pie([1, 1], wedgeprops=dict(width=0.15), startangle=0, radius=1.5, colors=[Palettes["darkly"]["colors"]["info"], Palettes["darkly"]["colors"]["secondary"]])
        
        # ------------------------------Labels------------------------------

        self.master_label = QLabel(self)
        self.master_label.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.master_label.setAlignment(Qt.AlignCenter)
        self.master_label.setStyleSheet("background-color: %s; border: 2px solid %s" % (Palettes["darkly"]["colors"]["bg"], Palettes["darkly"]["colors"]["fg"]))
        self.layout.addWidget(self.master_label, 0, 0, 7, 2)
        
        offset = 0.32
        self.main_graph_label = QLabel(str(round(lf_values.values[-1], 1)), self)
        self.main_graph_label.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.main_graph_label.setAlignment(Qt.AlignCenter)
        #self.main_graph_label.move(self.main_graph_label.x(), self.main_graph_label.y() - 10)
        color_effect_main_graph_label = QGraphicsColorizeEffect()
        color_effect_main_graph_label.setColor(QColor(Palettes["darkly"]["colors"]["info"]))
        self.main_graph_label.setGraphicsEffect(color_effect_main_graph_label)
        self.main_graph_label.setFont(QFont('Arial', int(min(self.width, self.height) * (70 / 500))))
        self.layout.addWidget(self.main_graph_label, 3, 0, 1, 2)

        self.graph_label_left = QLabel(str(round(min(lf_values.values), 1)), self)
        self.graph_label_left.setGeometry(
            int(((self.frameGeometry().width() - self.min_dim) / 2) + self.min_dim * offset),
            int(((self.frameGeometry().height() - self.min_dim) / 2) + self.min_dim * offset),
            int(self.min_dim - 2 * (self.min_dim * offset)),
            int(self.min_dim - 2 * (self.min_dim * offset)),
        )
        self.graph_label_left.setAlignment(Qt.AlignCenter)
        self.graph_label_left.move(self.graph_label_left.x(), self.graph_label_left.y() - 10)
        color_effect_graph_label_left = QGraphicsColorizeEffect()
        color_effect_graph_label_left.setColor(QColor(Palettes["darkly"]["colors"]["light"]))
        self.graph_label_left.setGraphicsEffect(color_effect_graph_label_left)
        self.graph_label_left.setFont(QFont('Arial', int(min(self.frameGeometry().width(), self.frameGeometry().height()) * (25 / 500))))
        self.layout.addWidget(self.graph_label_left, 4, 0, 1, 1)

        self.graph_label_right = QLabel(str(round(max(lf_values.values), 1)), self)
        self.graph_label_right.setGeometry(
            int(((self.frameGeometry().width() - self.min_dim) / 2) + self.min_dim * offset),
            int(((self.frameGeometry().height() - self.min_dim) / 2) + self.min_dim * offset),
            int(self.min_dim - 2 * (self.min_dim * offset)),
            int(self.min_dim - 2 * (self.min_dim * offset)),
        )
        self.graph_label_right.setAlignment(Qt.AlignCenter)
        self.graph_label_right.move(self.graph_label_right.x(), self.graph_label_right.y() - 10)
        color_effect_graph_label_right = QGraphicsColorizeEffect()
        color_effect_graph_label_right.setColor(QColor(Palettes["darkly"]["colors"]["light"]))
        self.graph_label_right.setGraphicsEffect(color_effect_graph_label_right)
        self.graph_label_right.setFont(QFont('Arial', int(min(self.frameGeometry().width(), self.frameGeometry().height()) * (25 / 500))))
        self.layout.addWidget(self.graph_label_right, 4, 1, 1, 1)

        self.graph_text = QLabel(text, self)
        self.graph_text.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.graph_text.setAlignment(Qt.AlignHCenter)
        self.graph_text.move(self.graph_text.x(), self.graph_text.y() - 10)
        color_effect_graph_text = QGraphicsColorizeEffect()
        color_effect_graph_text.setColor(QColor(Palettes["darkly"]["colors"]["fg"]))
        self.graph_text.setGraphicsEffect(color_effect_graph_text)
        self.graph_text.setFont(QFont('Arial', int(min(self.width, self.height) * (35 / 500))))
        self.layout.addWidget(self.graph_text, 5, 0, 7, 2)

        # ------------------------------Timer------------------------------
        
        self._timer = canvas1.new_timer(300000)
        self._timer.add_callback(self._update_canvas)
        self._timer.start()

    def _update_canvas(self):
        self._line.set_data(self.lf_values, color=Palettes["darkly"]["colors"]["primary"], clip_on=False)
        self._line.figure.canvas.draw()

        data = [self.lf_values.values[-1], max(self.lf_values.values) - self.lf_values.values[-1]]
        if not sum(data) == 0:
            self._wedges.set_data(data, wedgeprops=dict(width=0.15), startangle=-90 + ((data[1] / (2 * sum(data))) * 360), radius=1.5, colors=[Palettes["darkly"]["colors"]["info"], Palettes["darkly"]["colors"]["secondary"]])
        else:
            self._wedges.set_data([1, 1], wedgeprops=dict(width=0.15), startangle=0, radius=1.5, colors=[Palettes["darkly"]["colors"]["info"], Palettes["darkly"]["colors"]["secondary"]])
        self._wedges.figure.canvas.draw()

    def resizeEvent(self, event):
        self.width = int(self.controller.frameGeometry().width() / 5)
        self.height = int(self.controller.frameGeometry().height() / 3)
        self.min_dim = min(self.width, self.height)

        font = self.main_graph_label.font()
        font_size = int(self.min_dim * (70 / 500))
        if font_size <= 0:
            font_size = 1
        font.setPointSize(font_size)
        self.main_graph_label.setFont(font)

        font = self.graph_label_left.font()
        font_size = int(self.min_dim * (25 / 500))
        if font_size <= 0:
            font_size = 1
        font.setPointSize(font_size)
        self.graph_label_left.setFont(font)

        font = self.graph_label_right.font()
        font_size = int(self.min_dim * (25 / 500))
        if font_size <= 0:
            font_size = 1
        font.setPointSize(font_size)
        self.graph_label_right.setFont(font)
        
        font = self.graph_text.font()
        font_size = int(self.min_dim * (35 / 500))
        if font_size <= 0:
            font_size = 1
        font.setPointSize(font_size)
        self.graph_text.setFont(font)

        offset = 0.32
        self.master_label.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.main_graph_label.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.graph_label_left.setGeometry(
            int(((self.width - self.min_dim) / 2) + self.min_dim * offset),
            int(((self.height - self.min_dim) / 2) + self.min_dim * offset),
            int(self.min_dim - 2 * (self.min_dim * offset)),
            int(self.min_dim - 2 * (self.min_dim * offset)),
        )
        self.graph_label_right.setGeometry(
            int(((self.width - self.min_dim) / 2) + self.min_dim * offset),
            int(((self.height - self.min_dim) / 2) + self.min_dim * offset),
            int(self.min_dim - 2 * (self.min_dim * offset)),
            int(self.min_dim - 2 * (self.min_dim * offset)),
        )
        self.graph_text.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.master_label.setStyleSheet("border : 2px solid %s" % Palettes["darkly"]["colors"]["fg"]) 

        self.master_label.setAlignment(Qt.AlignCenter)
        self.main_graph_label.setAlignment(Qt.AlignCenter)
        self.graph_label_left.setAlignment(Qt.AlignCenter)
        self.graph_label_right.setAlignment(Qt.AlignCenter)
        self.graph_text.setAlignment(Qt.AlignHCenter)

class EmptyLF(QWidget):
    def __init__(self, parent, controller, width = None, height = None, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.controller = controller
        if (width is None) or (height is None):
            min_dim = min(int(self.controller.frameGeometry().width() / 5), int(self.controller.frameGeometry().height() / 3))
            self.width = min_dim
            self.height = min_dim
        else:
            self.width = width
            self.height = height
        self.layout = QVBoxLayout()

        self.empty_label = QLabel()
        self.empty_label.setGeometry(widget_padding, widget_padding, self.width - (2 * widget_padding), self.height - (2 * widget_padding))
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("background-color: %s; border: 2px solid %s" % (Palettes["darkly"]["colors"]["bg"], Palettes["darkly"]["colors"]["fg"]))
        self.layout.addWidget(self.empty_label)

        self.setLayout(self.layout)

class WeatherWidget(QWidget):
    def __init__(self, parent, controller, dpi=100, *args, **kwargs):
        self.parent = parent
        self.controller = controller
        super(QWidget, self).__init__(parent, *args, **kwargs)
        self.width = int(self.controller.frameGeometry().width() * 2 / 5)
        self.height = int(self.controller.frameGeometry().height() / 3)
        self.dpi = dpi
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        min_dim = min(int(self.width / 2), self.height)
        self.weather_label = QLabel(self)
        self.weather_label.setGeometry(widget_padding, widget_padding, min_dim * 2 - (2 * widget_padding), min_dim - (2 * widget_padding))
        self.weather_label.setAlignment(Qt.AlignCenter)
        self.weather_label.setStyleSheet("border : 2px solid %s" % Palettes["darkly"]["colors"]["fg"])
        self.layout.addWidget(self.weather_label, 0, 0, 1, 1)

        self.forecast_updater()
        timer = QTimer(self)
        timer.timeout.connect(self.forecast_updater)
        timer.start(86400000)
        
    def forecast_updater(self):
        if internet_connection:
            response, _, _ = GET_WEATHER_ICON()
            for idx, (text, url) in enumerate(response):
                with urllib.request.urlopen(url) as u:
                    raw_data = u.read()            
                
                # now create the ImageTk PhotoImage:
                self.img[idx] = config_pic(io.BytesIO(raw_data), (self.width / 3) - (5 * self.padding), self.height - (5 * self.padding), self.padding)
                # imagelab1 = Label(
                #     self,
                #     image = self.img[idx],
                # )
                # imagelab1.place(relx = (0.167 + 0.33 * idx), rely = 0.4, anchor = CENTER)
    
                # imagelab2 = Label(
                #     self,
                #     text = text,
                #     font = ("Helvetica’", 16),
                # )
                # imagelab2.place(relx = (0.167 + 0.33 * idx), rely = 0.85, anchor = CENTER)
                    
    def resizeEvent(self, event):
        self.width = int(self.controller.frameGeometry().width() * 2 / 5)
        self.height = int(self.controller.frameGeometry().height() / 3)
        
        min_dim = min(int(self.width / 2), self.height)
        self.weather_label.setGeometry(widget_padding, widget_padding, min_dim * 2 - (2 * widget_padding), min_dim - (2 * widget_padding))
        self.weather_label.setStyleSheet("border : 2px solid %s" % Palettes["darkly"]["colors"]["fg"]) 
        self.weather_label.setAlignment(Qt.AlignCenter)

class CustomSmallImg(QWidget):
    def __init__(self, parent, controller, dpi = 100, *args, **kwargs):
        super(QWidget, self).__init__(parent, *args, **kwargs)
        
        self.parent = parent
        self.controller = controller
        self.width = int(self.controller.frameGeometry().width() / 5)
        self.height = int(self.controller.frameGeometry().height() / 3)
        self.dpi = dpi

        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        self.min_dim = min(self.width, self.height)
        self.master_label = QLabel(self)
        self.master_label.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.master_label.setAlignment(Qt.AlignCenter)
        self.master_label.setStyleSheet("background-color: %s; border: 2px solid %s" % (Palettes["darkly"]["colors"]["bg"], Palettes["darkly"]["colors"]["fg"]))
        self.layout.addWidget(self.master_label, 0, 0, 3, 3)
        
        self.moon_label = QLabel(self)
        self.moon_label.setGeometry(widget_padding, widget_padding, self.min_dim - (4 * widget_padding), self.min_dim - (4 * widget_padding))
        self.moon_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.moon_label, 1, 1, 1, 1)

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

    def resizeEvent(self, event):
        self.width = int(self.controller.frameGeometry().width() / 5)
        self.height = int(self.controller.frameGeometry().height() / 3)
        
        self.min_dim = min(self.width, self.height)
        self.master_label.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.moon_label.setGeometry(widget_padding, widget_padding, self.min_dim - (4 * widget_padding), self.min_dim - (4 * widget_padding))

        self.master_label.setStyleSheet("background-color: %s; border: 2px solid %s" % (Palettes["darkly"]["colors"]["bg"], Palettes["darkly"]["colors"]["fg"]))
        self.master_label.setAlignment(Qt.AlignCenter)
        self.moon_label.setAlignment(Qt.AlignCenter)
        
        self.getImage()
        self.moon_pixmap.scaled(self.min_dim - (4 * widget_padding), self.min_dim - (4 * widget_padding), Qt.KeepAspectRatio, Qt.FastTransformation)
        self.moon_label.setPixmap(self.moon_pixmap)
        
class CustomClock(QWidget):
    def __init__(self, parent, controller, dpi = 100, *args, **kwargs): 
        super(QWidget, self).__init__(parent, *args, **kwargs)
        
        self.parent = parent
        self.controller = controller
        self.width = int(self.controller.frameGeometry().width() / 5)
        self.height = int(self.controller.frameGeometry().height() / 3)
        self.dpi = dpi
        
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.min_dim = min(self.width, self.height)
        self.master_label = QLabel(self)
        self.master_label.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.master_label.setAlignment(Qt.AlignCenter)
        self.master_label.setStyleSheet("background-color: %s; border: 2px solid %s" % (Palettes["darkly"]["colors"]["bg"], Palettes["darkly"]["colors"]["fg"]))
        self.layout.addWidget(self.master_label, 0, 0, 3, 1)
        
        self.time_label = QLabel(self)
        self.time_label.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.time_label.setAlignment(Qt.AlignCenter)
        color_effect_time_label = QGraphicsColorizeEffect()
        color_effect_time_label.setColor(QColor(Palettes["darkly"]["colors"]["info"]))
        self.time_label.setGraphicsEffect(color_effect_time_label)
        self.time_label.setFont(QFont('Arial', int(min(self.width, self.height) * (60 / 500))))
        self.layout.addWidget(self.time_label, 1, 0, 1, 1)

        self.sunrise_label = QLabel("Sunrise: %s" % datetime.now().strftime('%I:%M:%S %p'), self)
        self.sunrise_label.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.sunrise_label.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        self.sunrise_label.move(self.sunrise_label.x(), self.sunrise_label.y() + 60)
        color_effect_sunrise_label = QGraphicsColorizeEffect()
        color_effect_sunrise_label.setColor(QColor(Palettes["darkly"]["colors"]["light"]))
        self.sunrise_label.setGraphicsEffect(color_effect_sunrise_label)
        self.sunrise_label.setFont(QFont('Arial', int(min(self.width, self.height) * (32 / 500))))
        self.layout.addWidget(self.sunrise_label, 0, 0, 1, 1)

        self.sunset_label = QLabel("Sunset: %s" % datetime.now().strftime('%I:%M:%S %p'), self)
        self.sunset_label.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.sunset_label.setAlignment(Qt.AlignHCenter)
        self.sunset_label.move(self.sunset_label.x(), self.sunset_label.y() - 70)
        color_effect_sunset_label = QGraphicsColorizeEffect()
        color_effect_sunset_label.setColor(QColor(Palettes["darkly"]["colors"]["light"]))
        self.sunset_label.setGraphicsEffect(color_effect_sunset_label)
        self.sunset_label.setFont(QFont('Arial', int(min(self.width, self.height) * (32 / 500))))
        self.layout.addWidget(self.sunset_label, 2, 0, 1, 1)

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

    def showTime(self):
        current_time = QTime.currentTime()
        label_time = datetime.now().strftime('%I:%M:%S %p')
        self.time_label.setText(label_time)

    def resizeEvent(self, event):
        self.width = int(self.controller.frameGeometry().width() / 5)
        self.height = int(self.controller.frameGeometry().height() / 3)

        self.min_dim = min(self.width, self.height)
        font = self.time_label.font()
        font_size = int(self.min_dim * (60 / 500))
        if font_size <= 0:
            font_size = 1
        font.setPointSize(font_size)
        self.time_label.setFont(font)

        font = self.sunrise_label.font()
        font_size = int(self.min_dim * (32 / 500))
        if font_size <= 0:
            font_size = 1
        font.setPointSize(font_size)
        self.sunrise_label.setFont(font)

        font = self.sunset_label.font()
        font_size = int(self.min_dim * (32 / 500))
        if font_size <= 0:
            font_size = 1
        font.setPointSize(font_size)
        self.sunset_label.setFont(font)

        self.master_label.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.time_label.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.sunrise_label.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        self.sunset_label.setGeometry(widget_padding, widget_padding, self.min_dim - (2 * widget_padding), self.min_dim - (2 * widget_padding))
        
        self.master_label.setStyleSheet("background-color: %s; border: 2px solid %s" % (Palettes["darkly"]["colors"]["bg"], Palettes["darkly"]["colors"]["fg"]))
        self.master_label.setAlignment(Qt.AlignCenter)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.sunrise_label.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        self.sunset_label.setAlignment(Qt.AlignHCenter)