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
from BEE_WEATHER_DATA import BROODMINDER_GET, AMBIENT_GET, READ_HIVE, PROCESS_HIVE, READ_BEE_WEATHER, PROCESS_BEE_WEATHER, PROCESS_AMBIENT, GRAPH_DATA, GET_MOON_IMAGE, GET_FORECAST, PROCESS_FORECAST, PROCESS_FORECAST_MIN_MAX, check_internet_connection, GET_WEATHER_ICON, config_pic
sys.path.append("PYICLOUD_GET")
from Custom_Widgets import CustomMeter, EmptyLF, CustomClockWidget, CustomSmallImg, WeatherWidget
import PYICLOUD_GET
import pandas as pd
from IPython.display import display

internet = check_internet_connection()

class Pane3(Frame): # Picture Frame
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        directory = "PhotosB/"
        file_paths = []
        ext = ('.png', '.jpg', '.jpeg', '.heic', '.tiff', '.tif')
        raw_ext = ('.raw', '.arw', '.dng')
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(tuple(ext)):
                    file_paths.append(os.path.join(root, file))
                elif file.lower().endswith(tuple(ext)):
                    try:
                        with rawpy.imread(np.fromfile("Test/DSC1160-medium.RAW", allow_pickle=True)) as raw:
                            print(f'raw type:                     {raw.raw_type}')                      # raw type (flat or stack, e.g., Foveon sensor)
                            print(f'number of colors:             {raw.num_colors}')                    # number of different color components, e.g., 3 for common RGB Bayer sensors with two green identical green sensors 
                            print(f'color description:            {raw.color_desc}')                    # describes the various color components
                            print(f'raw pattern:                  {raw.raw_pattern.tolist()}')          # decribes the pattern of the Bayer sensor
                            print(f'black levellos:                 {raw.black_level_per_channel}')       # black level correction
                            print(f'white level:                  {raw.white_level}')                   # camera white level
                            print(f'color matrix:                 {raw.color_matrix.tolist()}')         # camera specific color matrix, usually obtained from a list in rawpy (not from the raw file)
                            print(f'XYZ to RGB conversion matrix: {raw.rgb_xyz_matrix.tolist()}')       # camera specific XYZ to camara RGB conversion matrix
                            print(f'camera white balance:         {raw.camera_whitebalance}')           # the picture's white balance as determined by the camera
                            print(f'daylight white balance:       {raw.daylight_whitebalance}')         # the camera's daylight white balance
                        file_paths.append(os.path.join(root, file))
                    except:
                        pass
        # Pane3 Objects
        make_frame = LabelFrame(
            self,
            width=self.controller.shared_data["window_geometry"][0].get() - 2 * self.controller.shared_data["padding"].get(),
            height=self.controller.shared_data["window_geometry"][1].get() - 2 * self.controller.shared_data["padding"].get(),
        )
        make_frame.grid(
            row=0,
            column=0,
            padx=(int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
            pady=(int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
            ipadx=int(self.controller.shared_data["padding"].get()),
            ipady=int(self.controller.shared_data["padding"].get()),
        )
        
        def config_pic():
            while True:
                try:
                    rand_pic = file_paths[random.randint(0,len(file_paths) - 1)]
                    PIL_image = Image.open(rand_pic)
                    break
                except:
                    pass
            original_w = np.shape(PIL_image)[1]
            original_h = np.shape(PIL_image)[0]
            aspect = original_h/original_w
    
            constraining_dim = min(self.controller.shared_data["window_geometry"][0].get(), self.controller.shared_data["window_geometry"][1].get())
            minor_constraint = min(constraining_dim/original_w, constraining_dim/original_h)
            width = int(original_w * minor_constraint)
            height = int(original_h * minor_constraint)
            PIL_image_small = PIL_image.resize((width,height), Image.Resampling.LANCZOS)
    
            # now create the ImageTk PhotoImage:
            img = ImageTk.PhotoImage(image=PIL_image_small)
            return img
        
        def change_pic():
            img = config_pic()
            in_frame.configure(image = img)
            in_frame.image = img
    
        # create the PIL image object:
        img = config_pic()
        in_frame = Button(
            make_frame,
            command = change_pic,
            width=self.controller.shared_data["window_geometry"][0].get() - 2 * self.controller.shared_data["padding"].get(),
            height=self.controller.shared_data["window_geometry"][1].get() - 2 * self.controller.shared_data["padding"].get(),
        )
        change_pic()
        in_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
    
        def daily_updater():
            if internet:
                try:
                    pass
                    # PYICLOUD_GET.cycle_files()
                    # PYICLOUD_GET.download()
                except:
                    pass
            # run itself again
            self.after(86400000, daily_updater)
        
        # run first time at once
        daily_updater()