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
import PYICLOUD_GET
import pandas as pd
from IPython.display import display

internet = check_internet_connection()

class CustomMeter(ttk.LabelFrame):
    def __init__(self, parent, controller, width, height, padding, text, amt_used):
        self.width = int(width)
        self.height = int(height)
        self.padding = int(padding)
        ttk.LabelFrame.__init__(
            self,
            parent,
            relief="solid",
            borderwidth=1,
            width=self.width,
            height=self.height,
            #padding=self.padding,
            text=text,
        )
        meter = ttk.Meter(
            self,
            metersize=min(int(self.width), int(self.height)) - 4 * int(self.padding),
            amountused=amt_used,
            metertype="semi",
            subtext=text,
            showtext=True,
            interactive=False,
        )
        meter.place(relx=0.5, rely=0.5, anchor=CENTER)
    
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
            relief="solid",
            borderwidth=1,
            width=self.width,
            height=self.height,
            #padding=self.padding,
            text=text,
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
            relief="solid",
            borderwidth=1,
            width=self.width,
            height=self.height,
            #padding=self.padding,
            text=text,
        )
        response = GET_WEATHER_ICON()
        for idx, (text, url) in enumerate(response):
            with urllib.request.urlopen(url) as u:
                raw_data = u.read()            
            PIL_image = Image.open(io.BytesIO(raw_data))
            original_w = np.shape(PIL_image)[1]
            original_h = np.shape(PIL_image)[0]
            aspect = original_h/original_w

            constraining_dim = min((self.width / 3) - (5 * self.padding),
                                   self.height - (5 * self.padding))
            minor_constraint = min(constraining_dim/original_w, constraining_dim/original_h)
            img_width = int(original_w * minor_constraint)
            img_height = int(original_h * minor_constraint)
            PIL_image_small = PIL_image.resize((img_width, img_height), Image.Resampling.LANCZOS)

            # now create the ImageTk PhotoImage:
            self.img[idx] = ImageTk.PhotoImage(image=PIL_image_small)
            
            # self.image = ImageTk.PhotoImage(image)
            # img = WebImage(link).get()
            imagelab1 = Label(
                self,
                image=self.img[idx],
            )
            imagelab1.place(relx=(0.167 + 0.33 * idx), rely=0.4, anchor=CENTER)

            imagelab2 = Label(
                self,
                text=text,
                font=("Helvetica’", 16),
            )
            imagelab2.place(relx=(0.167 + 0.33 * idx), rely=0.85, anchor=CENTER)
    
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
            relief="solid",
            borderwidth=1,
            width=self.width,
            height=self.height,
            #padding=self.padding,
            text=text,
        )
        
        def config_pic():
            if internet:
                try:
                    GET_MOON_IMAGE(216, save=1)
                except:
                    pass

            file = [i for i in os.listdir("moon/")]
            PIL_image = Image.open("moon/" + file[0])
            original_w = np.shape(PIL_image)[1]
            original_h = np.shape(PIL_image)[0]
            aspect = original_h/original_w

            constraining_dim = min(self.width - 5 * self.padding,
                                   self.height - 5 * self.padding)
            minor_constraint = min(constraining_dim/original_w, constraining_dim/original_h)
            img_width = int(original_w * minor_constraint)
            img_height = int(original_h * minor_constraint)
            PIL_image_small = PIL_image.resize((img_width, img_height), Image.Resampling.LANCZOS)

            # now create the ImageTk PhotoImage:
            img = ImageTk.PhotoImage(image=PIL_image_small)
            return img

        def change_pic():
            img = config_pic()
            in_frame.config(image = img)
            in_frame.image = img

        # create the PIL image object:
        img = config_pic()
        in_frame = Label(
            self,
            image = img,
        )
        change_pic()
        in_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    def get(self):
        return self.entry.get()


class CustomClockWidget(ttk.LabelFrame):
    def __init__(self, parent, controller, width, height, padding, text):#, amt_used):
        self.width = int(width)
        self.height = int(height)
        self.padding = int(padding)
        ttk.LabelFrame.__init__(
            self,
            parent,
            relief="solid",
            borderwidth=1,
            width=self.width,
            height=self.height,
            #padding=self.padding,
            text=text,
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
            font=("Helvetica’", 28),
            # width = self.width - 2 * self.padding
        )
        clock_frame.place(relx=0.5, rely=0.35, anchor=CENTER)
    
        sunrise_frame = Label(
            self,
            text = datetime.now().strftime("Sunrise: %I:%M:%S %p"),
            font=("Helvetica’", 16),
            # width = self.width - 2 * self.padding
        )
        sunrise_frame.place(relx=0.5, rely=0.8, anchor=S)
        
        sunset_frame = Label(
            self,
            text = datetime.now().strftime("Sunset: %I:%M:%S %p"),
            font=("Helvetica’", 16),
            # width = self.width - 2 * self.padding
        )
        sunset_frame.place(relx=0.5, rely=0.8, anchor=N)
        self.pack_propagate(0)
        clock_updater()
        
    def get(self):
        return self.entry.get()