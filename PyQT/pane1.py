import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLayout, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PIL import Image
Image.CUBIC = Image.BICUBIC
import os, time, sys, queue, datetime
from csv import writer
from datetime import datetime, timedelta
from threading import Thread, Event
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import multiprocessing as mp
import http.server
import socketserver
from contextlib import closing
from more_itertools import time_limited
from math import floor
import aiomultiprocess
import asyncio
import threading
import numpy as np
#import rawpy
import imageio
import time
import random
import urllib.request
import io
from pathlib import Path
import pandas as pd
from IPython.display import display
from functions_and_classes import *
from custom_widgets import *
from pyicloud_get import *
from timers import *
from settings import *

class Pane1(QWidget):
    def __init__(self, parent, controller, screen_width, screen_height):
        self.parent = parent
        self.controller = controller
        super(QWidget, self).__init__(parent)
        grid = QGridLayout(self)

        Hive_Processed = []
        for hive_creds in hive_IDs.items():
            hive = Hive(*list(hive_creds))
            hive.set()
            Hive_Processed.append(hive)
        forecast_data = PROCESS_FORECAST()
        ambient = Ambient()
        ambient.set()
        
        # Pane1 Objects
        # Loop to create LabelFrames
        lf_labels = [
                    "Time/Sunrise/Sunset",
                    "Moon Phase",
                    "Wx Forecast",
                    "",
                    "Honey Wt./Bee Count",
                    "Temp",
                    "Solar Rad.",
                    "Wind Spd./Dir.",
                    "Chook Temp", 
                    "Bee Wt.",
                    "Humidity",
                    "UV Index",
                    "Precip.",
                    "Bee Temp.",
                    "Bee Humid.",
                    ]
        
        lf_values = [
                    "",
                    "",
                    "",
                    "",
                    "",
                    ambient.get_tempf(num_days = 7),
                    ambient.get_solarradiation(num_days = 7),
                    ambient.get_windspeedmph(num_days = 7),
                    pd.Series([1]), 
                    Hive_Processed[0].get_weight(num_days = 7),
                    ambient.get_humidity(num_days = 7),
                    ambient.get_uv(num_days = 7),
                    ambient.get_hourlyrainin(num_days = 7),
                    Hive_Processed[0].get_upper_temp(num_days = 7),
                    Hive_Processed[0].get_humidity(num_days = 7),
                    ]

        grid.addWidget(EmptyLF(self, controller, width = screen_width, height = screen_height), 0, 0, 3, 5)
        i = 0
        
        while i < 15:
            while i < 5:
                if i == 0:
                    grid.addWidget(CustomClock(self, controller), floor((i - 5) / 5) + 1, (i - 5) % 5, 1, 1)
                    i = i + 1
                if i == 1:
                    grid.addWidget(CustomSmallImg(self, controller), floor((i - 5) / 5) + 1, (i - 5) % 5, 1, 1)
                    i = i + 1
                if i == 2:
                    grid.addWidget(WeatherWidget(self, controller), floor((i - 5) / 5) + 1, (i - 5) % 5, 1, 2)
                    i = i + 2
                else:
                    grid.addWidget(EmptyLF(self, controller), floor((i - 5) / 5) + 1, (i - 5) % 5, 1, 1)
                    i = i + 1
            grid.addWidget(GraphWidget(self, controller, lf_labels[i], lf_values[i]), floor((i - 5) / 5) + 1, (i - 5) % 5)
            i = i + 1
        
        self.setLayout(grid)