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
from functions_and_classes import *
from custom_widgets import *
from pyicloud_get import *
import pandas as pd
from IPython.display import display
from timers import *
from settings import *

class Pane2(QWidget):
    def __init__(self, parent, controller, screen_width, screen_height):
        self.parent = parent
        super(QWidget, self).__init__(parent)
        grid = QGridLayout(self)

        Hive_Processed = []
        for hive_creds in settings.hive_IDs.items():
            hive = Hive(*list(hive_creds))
            hive.set()
            Hive_Processed.append(hive)
        forecast_data = PROCESS_FORECAST()
        ambient = Ambient()
        ambient.set()

        lf_labels = [
                    "Hive 1 Wt.",
                    "Hive 2 Wt.",
                    "Hive 3 Wt.",
                    "Hive 4 Wt.",
                    "Hive 5 Wt.",
                    "Hive 1 Temp.",
                    "Hive 2 Temp.",
                    "Hive 3 Temp.",
                    "Hive 4 Temp.",
                    "Hive 5 Temp.",
                    "Hive 1 Humid.",
                    "Hive 2 Humid.",
                    "Hive 3 Humid.",
                    "Hive 4 Humid.",
                    "Hive 5 Humid.",
                    ]
        lf_values = [
                    Hive_Processed[0].get_weight(num_days = 7),
                    Hive_Processed[1].get_weight(num_days = 7),
                    Hive_Processed[0].get_weight(num_days = 7),
                    Hive_Processed[0].get_weight(num_days = 7),
                    Hive_Processed[0].get_weight(num_days = 7),
                    Hive_Processed[0].get_upper_temp(num_days = 7),
                    Hive_Processed[1].get_upper_temp(num_days = 7),
                    Hive_Processed[2].get_upper_temp(num_days = 7),
                    Hive_Processed[0].get_upper_temp(num_days = 7),
                    Hive_Processed[0].get_upper_temp(num_days = 7),
                    Hive_Processed[0].get_humidity(num_days = 7),
                    Hive_Processed[1].get_humidity(num_days = 7),
                    Hive_Processed[2].get_humidity(num_days = 7),
                    Hive_Processed[0].get_humidity(num_days = 7),
                    Hive_Processed[0].get_humidity(num_days = 7),
                    ]
        grid.addWidget(EmptyLF(self, controller, width = screen_width, height = screen_height), 0, 0, 3, 5)
        i = 0
        while i < 15:
            grid.addWidget(GraphWidget(self, controller, lf_labels[i], lf_values[i]), floor((i - 5) / 5) + 1, (i - 5) % 5)
            i = i + 1
        
        self.setLayout(grid)