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
from BEE_WEATHER_DATA import *
sys.path.append("PYICLOUD_GET")
from Custom_Widgets import *
import PYICLOUD_GET
import pandas as pd
from IPython.display import display

class Pane1(Frame): # Weather Dashboard; child to Notebook
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
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
                    "ambient_temp",
                    "solar",
                    "wind_spd",
                    "chooks", 
                    "hive1_wt", # Need to figure out what this needs to be (minimum wt, avg wt, or something else entirely like air qual)
                    "ambient_humid",
                    "UV",
                    "Precip",
                    "hive1_temp", # Need to figure out what this needs to be (minimum temp, avg temp, or something else entirely like air qual)
                    "hive1_humid", # Need to figure out what this needs to be (minimum temp, avg temp, or something else entirely like air qual)
                    ]
        
        self.LF = CustomClockWidget(
            self,
            parent,
            str(self.controller.shared_data["LF_geometry"][0].get() - 2 * self.controller.shared_data["padding"].get()),
            str(self.controller.shared_data["LF_geometry"][1].get() - 2 * self.controller.shared_data["padding"].get()),
            int(self.controller.shared_data["padding"].get()),
            lf_labels[0],
        ).grid(
            row = 0,
            column = 0,
            padx = int(self.controller.shared_data["padding"].get()),
            pady = int(self.controller.shared_data["padding"].get()),
        )
        
        self.LF = CustomSmallImg(
            self,
            parent,
            str(self.controller.shared_data["LF_geometry"][0].get() - 2 * self.controller.shared_data["padding"].get()),
            str(self.controller.shared_data["LF_geometry"][1].get() - 2 * self.controller.shared_data["padding"].get()),
            int(self.controller.shared_data["padding"].get()),
            lf_labels[1],
        ).grid(
            row = 0,
            column = 1,
            padx = int(self.controller.shared_data["padding"].get()),
            pady = int(self.controller.shared_data["padding"].get()),
        )

        self.LF = WeatherWidget(
            self,
            parent,
            str((self.controller.shared_data["LF_geometry"][0].get() * 2) - 2 * self.controller.shared_data["padding"].get()),
            str(self.controller.shared_data["LF_geometry"][1].get() - 2 * self.controller.shared_data["padding"].get()),
            int(self.controller.shared_data["padding"].get()),
            lf_labels[2],
        ).grid(
            row = 0,
            column = 2,
            columnspan = 2,
            sticky="nsew",
            padx = int(self.controller.shared_data["padding"].get()),
            pady = int(self.controller.shared_data["padding"].get()),
        )

        self.LF = EmptyLF(
            self,
            parent,
            str(self.controller.shared_data["LF_geometry"][0].get() - 2 * self.controller.shared_data["padding"].get()),
            str(self.controller.shared_data["LF_geometry"][1].get() - 2 * self.controller.shared_data["padding"].get()),
            int(self.controller.shared_data["padding"].get()),
            lf_labels[4],
        ).grid(
            row = 0,
            column = 4,
            padx = int(self.controller.shared_data["padding"].get()),
            pady = int(self.controller.shared_data["padding"].get()),
        )
        
        # Loop to create Meters
        i = 5
        while i < 15:
            self.meter = CustomMeter(
                self,
                parent,
                str(self.controller.shared_data["LF_geometry"][0].get() - 2 * self.controller.shared_data["padding"].get()),
                str(self.controller.shared_data["LF_geometry"][1].get() - 2 * self.controller.shared_data["padding"].get()),
                int(self.controller.shared_data["padding"].get()),
                lf_labels[i],
                self.controller.shared_data[lf_values[i]][0].get(),
                self.controller.shared_data[lf_values[i]][1].get(),
                self.controller.shared_data[lf_values[i]][2].get(),
            ).grid(
                row = floor((i - 5) / 5) + 1,
                column = (i - 5) % 5,
                padx = int(self.controller.shared_data["padding"].get()),
                pady = int(self.controller.shared_data["padding"].get()),
            )
            i = i + 1