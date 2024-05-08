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
import settings
sys.path.append("BEE_WEATHER_DATA")
from BEE_WEATHER_DATA import BROODMINDER_GET, AMBIENT_GET, READ_HIVE, PROCESS_HIVE, READ_BEE_WEATHER, PROCESS_BEE_WEATHER, PROCESS_AMBIENT, GRAPH_DATA, GET_MOON_IMAGE, GET_FORECAST, PROCESS_FORECAST, PROCESS_FORECAST_MIN_MAX, check_internet_connection, GET_WEATHER_ICON, config_pic
sys.path.append("PYICLOUD_GET")
import PYICLOUD_GET
import pandas as pd
from IPython.display import display

class CustomMeter(ttk.LabelFrame):
    def __init__(self, parent, controller, width, height, padding, text, amt_used, amt_min, amt_max):
        self.width = int(width)
        self.height = int(height)
        self.padding = int(padding)
        ttk.LabelFrame.__init__(
            self,
            parent,
            relief = "solid",
            borderwidth = 1,
            width = self.width,
            height = self.height,
            text = text,
        )
        meter = ttk.Meter(
            self,
            metersize = min(int(self.width), int(self.height)) - 4 * int(self.padding),
            amountused = amt_used,
            amounttotal = int(amt_min if amt_used == amt_min else amt_used / ((amt_used - amt_min) / (amt_max - amt_min))) if int(amt_min if amt_used == amt_min else amt_used / ((amt_used - amt_min) / (amt_max - amt_min))) != 0 else 100,
            metertype = "semi",
            subtext = text,
            textleft = amt_min,
            textright = amt_max,
            showtext = True,
            interactive = False,
        )
        meter.place(relx = 0.5, rely = 0.5, anchor = CENTER)
    
    def get(self):
        return self.entry.get()

class EmptyLF(ttk.LabelFrame):
    def __init__(self, parent, controller, width, height, padding, text):#, amt_used):
        self.width = int(width)
        self.height = int(height)
        self.padding = int(padding)
        ttk.LabelFrame.__init__(
            self,
            parent,
            relief = "solid",
            borderwidth = 1,
            width = self.width,
            height = self.height,
            text = text,
        )
    def get(self):
        return self.entry.get()

class WeatherWidget(ttk.LabelFrame):
    def __init__(self, parent, controller, width, height, padding, text):#, amt_used):
        self.width = int(width)
        self.height = int(height)
        self.padding = int(padding)
        self.img = dict()
        ttk.LabelFrame.__init__(
            self,
            parent,
            relief = "solid",
            borderwidth = 1,
            width = self.width,
            height = self.height,
            text = text,
        )

        def forecast_updater():
            if settings.internet_avail:
                GET_FORECAST()
            response, _, _ = GET_WEATHER_ICON()
            for idx, (text, url) in enumerate(response):
                with urllib.request.urlopen(url) as u:
                    raw_data = u.read()            
                
                # now create the ImageTk PhotoImage:
                self.img[idx] = config_pic(io.BytesIO(raw_data), (self.width / 3) - (5 * self.padding), self.height - (5 * self.padding), self.padding)
                imagelab1 = Label(
                    self,
                    image = self.img[idx],
                )
                imagelab1.place(relx = (0.167 + 0.33 * idx), rely = 0.4, anchor = CENTER)
    
                imagelab2 = Label(
                    self,
                    text = text,
                    font = ("Helvetica’", 16),
                )
                imagelab2.place(relx = (0.167 + 0.33 * idx), rely = 0.85, anchor = CENTER)
            self.after(86400, forecast_updater)
        forecast_updater()
    
    def get(self):
        return self.entry.get()
        
class CustomSmallImg(ttk.LabelFrame): #Moon image, but generalized to a small space img, possibly used for weather icon too
    def __init__(self, parent, controller, width, height, padding, text):#, amt_used):
        self.width = int(width)
        self.height = int(height)
        self.padding = int(padding)
        ttk.LabelFrame.__init__(
            self,
            parent,
            relief = "solid",
            borderwidth = 1,
            width = self.width,
            height = self.height,
            text = text,
        )

        def moon_updater():
            if settings.internet_avail:
                GET_MOON_IMAGE()
            img = config_pic("moon/" + [i for i in os.listdir("moon/")][0], self.width, self.height, self.padding)
            in_frame = Label(
                self,
            )
            in_frame.config(image = img)
            in_frame.image = img
            # change_pic(in_frame)
            in_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)
            self.after(86400, moon_updater)
        moon_updater()
    
    def get(self):
        return self.entry.get()


class CustomClockWidget(ttk.LabelFrame):
    def __init__(self, parent, controller, width, height, padding, text):
        self.width = int(width)
        self.height = int(height)
        self.padding = int(padding)
        ttk.LabelFrame.__init__(
            self,
            parent,
            relief = "solid",
            borderwidth = 1,
            width = self.width,
            height = self.height,
            text = text,
        )
        
        def clock_updater():
            change_clock()
            # run itself again
            self.after(1000, clock_updater)
        
        def change_clock():
            current_time = datetime.now().strftime('%I:%M:%S %p')
            clock_frame.config(text = current_time)
            clock_frame.text = current_time
            
        clock_frame = Label(
            self,
            text = datetime.now().strftime('%I:%M:%S %p'),
            font = ("Helvetica’", 28),
        )
        clock_frame.place(relx = 0.5, rely = 0.35, anchor = CENTER)

        _, sunrise, sunset = GET_WEATHER_ICON()
        sunrise_frame = Label(
            self,
            text = datetime.fromtimestamp(sunrise).strftime("Sunrise: %I:%M:%S %p"),
            font = ("Helvetica’", 16),
        )
        sunrise_frame.place(relx=0.5, rely=0.8, anchor=S)
        
        sunset_frame = Label(
            self,
            text = datetime.fromtimestamp(sunset).strftime("Sunset: %I:%M:%S %p"),
            font = ("Helvetica’", 16),
        )
        sunset_frame.place(relx = 0.5, rely = 0.8, anchor = N)
        self.pack_propagate(0)
        clock_updater()
        
    def get(self):
        return self.entry.get()