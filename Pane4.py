import sys
if "Tkinter" not in sys.modules:
    from tkinter import *
from PIL import Image, ImageTk
Image.CUBIC = Image.BICUBIC
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
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
import rawpy
import imageio
import time
import random
import urllib.request
import io
from pathlib import Path
sys.path.append("BEE_WEATHER_DATA")
from BEE_WEATHER_DATA import BROODMINDER_GET, AMBIENT_GET, READ_HIVE, PROCESS_HIVE, READ_BEE_WEATHER, PROCESS_BEE_WEATHER, PROCESS_AMBIENT, GRAPH_DATA, GET_MOON_IMAGE, GET_FORECAST, PROCESS_FORECAST, PROCESS_FORECAST_MIN_MAX, check_internet_connection, GET_WEATHER_ICON
sys.path.append("PYICLOUD_GET")
from Custom_Widgets import CustomMeter, EmptyLF, CustomClockWidget, CustomSmallImg, WeatherWidget
import PYICLOUD_GET
import pandas as pd
from IPython.display import display

class Pane4(Frame): # Alarm Control
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        # Pane4 Objects
        canvas1 = Canvas(
            self,
            width = str(self.controller.shared_data["window_geometry"][0].get()),
            height = str(self.controller.shared_data["window_geometry"][1].get()),
        ).grid(
            row = 0,
            column = 0,
            padx = (int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
            pady = (int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
            ipadx = int(self.controller.shared_data["padding"].get()),
            ipady = int(self.controller.shared_data["padding"].get()),
        )