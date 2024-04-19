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

class Pane2(Frame): # Bee Dashboard
     def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        shared_list = list(self.controller.shared_data.keys())

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
        i = 0        
        while i < 15:
            self.meter = CustomMeter(
                self,
                parent,
                str(self.controller.shared_data["LF_geometry"][0].get() - 2 * self.controller.shared_data["padding"].get()),
                str(self.controller.shared_data["LF_geometry"][1].get() - 2 * self.controller.shared_data["padding"].get()),
                int(self.controller.shared_data["padding"].get()), lf_labels[i],
                25
            ).grid(
                row = floor(i/5),
                column = i % 5,
                padx = int(self.controller.shared_data["padding"].get()),
                pady = int(self.controller.shared_data["padding"].get()))
            i = i + 1