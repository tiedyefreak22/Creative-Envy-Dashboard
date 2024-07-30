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
from settings import *
from BEE_WEATHER_DATA import *
sys.path.append("PYICLOUD_GET")
from Custom_Widgets import *
from Pane1 import *
from Pane2 import *
from Pane3 import *
from Pane4 import *
import PYICLOUD_GET
import pandas as pd
from IPython.display import display
from timers import *
import warnings
warnings.filterwarnings("ignore")
    
# root window (parent to all), controller to Frames
class Windows(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        Hive_Processed = []
        for hive_creds in settings.hive_IDs.items():
            hive = Hive(*list(hive_creds))
            hive.set()
            Hive_Processed.append(hive)
        forecast_data = PROCESS_FORECAST()
        ambient = Ambient()
        ambient.set()
        ambient_data = ambient.get_ambient(interp = 0, num_days = 7)
        file = [i for i in os.listdir("moon/")]
        self.shared_data = {
            "window_geometry":    [IntVar(self, 1280),  IntVar(self, 800)],
            "padding":      IntVar(self, 5),
            "num_rows":     IntVar(self, 3),
            "num_cols":     IntVar(self, 5),
            "hive_names":   StringVar(self, settings.hive_IDs.keys()),
            "sun":          [StringVar(self, 1), StringVar(self, 1)],
            "honey1":       [DoubleVar(self, 1), DoubleVar(self, 1), DoubleVar(self, 1)],
            "honey2":       [DoubleVar(self, 1), DoubleVar(self, 1), DoubleVar(self, 1)],
            "honey3":       [DoubleVar(self, 1), DoubleVar(self, 1), DoubleVar(self, 1)],
            "honey4":       [DoubleVar(self, 1), DoubleVar(self, 1), DoubleVar(self, 1)],
            "honey5":       [DoubleVar(self, 1), DoubleVar(self, 1), DoubleVar(self, 1)],
            "bees1":        [IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "bees2":        [IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "bees3":        [IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "bees4":        [IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "bees5":        [IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "ambient_temp": [DoubleVar(self, ambient.get_tempf(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(ambient.get_tempf(num_days = 7))),
                             DoubleVar(self, max(ambient.get_tempf(num_days = 7)))],
            "solar":        [DoubleVar(self, ambient.get_solarradiation(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(ambient.get_solarradiation(num_days = 7))),
                             DoubleVar(self, max(ambient.get_solarradiation(num_days = 7)))],
            "wind_spd":     [DoubleVar(self, ambient.get_windspeedmph(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(ambient.get_windspeedmph(num_days = 7))),
                             DoubleVar(self, max(ambient.get_windspeedmph(num_days = 7)))],
            "wind_dir":     [DoubleVar(self, ambient.get_winddir(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(ambient.get_winddir(num_days = 7))),
                             DoubleVar(self, max(ambient.get_winddir(num_days = 7)))],
            "ambient_humid":[DoubleVar(self, ambient.get_humidity(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(ambient.get_humidity(num_days = 7))),
                             DoubleVar(self, max(ambient.get_humidity(num_days = 7)))],
            "UV":           [DoubleVar(self, ambient.get_uv(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(ambient.get_uv(num_days = 7))),
                             DoubleVar(self, max(ambient.get_uv(num_days = 7)))],
            "Precip":       [DoubleVar(self, ambient.get_hourlyrainin(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(ambient.get_hourlyrainin(num_days = 7))),
                             DoubleVar(self, max(ambient.get_hourlyrainin(num_days = 7)))],
            "air_qual":     [IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "chooks":       [IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "hive1_wt":     [DoubleVar(self, Hive_Processed[0].get_weight(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(Hive_Processed[0].get_weight(num_days = 7))),
                             DoubleVar(self, max(Hive_Processed[0].get_weight(num_days = 7)))],
            "hive2_wt":     [DoubleVar(self, Hive_Processed[1].get_weight(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(Hive_Processed[1].get_weight(num_days = 7))),
                             DoubleVar(self, max(Hive_Processed[1].get_weight(num_days = 7)))],
            "hive3_wt":     [DoubleVar(self, Hive_Processed[0].get_weight(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(Hive_Processed[0].get_weight(num_days = 7))),
                             DoubleVar(self, max(Hive_Processed[0].get_weight(num_days = 7)))],
            "hive4_wt":     [DoubleVar(self, Hive_Processed[0].get_weight(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(Hive_Processed[0].get_weight(num_days = 7))),
                             DoubleVar(self, max(Hive_Processed[0].get_weight(num_days = 7)))],
            "hive5_wt":     [DoubleVar(self, Hive_Processed[0].get_weight(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(Hive_Processed[0].get_weight(num_days = 7))),
                             DoubleVar(self, max(Hive_Processed[0].get_weight(num_days = 7)))],
            "hive1_temp":   [DoubleVar(self, Hive_Processed[0].get_upper_temp(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(Hive_Processed[0].get_upper_temp(num_days = 7))),
                             DoubleVar(self, max(Hive_Processed[0].get_upper_temp(num_days = 7)))],
            "hive2_temp":   [DoubleVar(self, Hive_Processed[1].get_upper_temp(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(Hive_Processed[1].get_upper_temp(num_days = 7))),
                             DoubleVar(self, max(Hive_Processed[1].get_upper_temp(num_days = 7)))],
            "hive3_temp":   [DoubleVar(self, Hive_Processed[2].get_upper_temp(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(Hive_Processed[2].get_upper_temp(num_days = 7))),
                             DoubleVar(self, max(Hive_Processed[2].get_upper_temp(num_days = 7)))],
            "hive4_temp":   [DoubleVar(self, Hive_Processed[0].get_upper_temp(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(Hive_Processed[0].get_upper_temp(num_days = 7))),
                             DoubleVar(self, max(Hive_Processed[0].get_upper_temp(num_days = 7)))],
            "hive5_temp":   [DoubleVar(self, Hive_Processed[0].get_upper_temp(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(Hive_Processed[0].get_upper_temp(num_days = 7))),
                             DoubleVar(self, max(Hive_Processed[0].get_upper_temp(num_days = 7)))],
            "hive1_humid":  [DoubleVar(self, Hive_Processed[0].get_humidity(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(Hive_Processed[0].get_humidity(num_days = 7))),
                             DoubleVar(self, max(Hive_Processed[0].get_humidity(num_days = 7)))],
            "hive2_humid":  [DoubleVar(self, Hive_Processed[1].get_humidity(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(Hive_Processed[1].get_humidity(num_days = 7))),
                             DoubleVar(self, max(Hive_Processed[1].get_humidity(num_days = 7)))],
            "hive3_humid":  [DoubleVar(self, Hive_Processed[2].get_humidity(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(Hive_Processed[2].get_humidity(num_days = 7))),
                             DoubleVar(self, max(Hive_Processed[2].get_humidity(num_days = 7)))],
            "hive4_humid":  [DoubleVar(self, Hive_Processed[0].get_humidity(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(Hive_Processed[0].get_humidity(num_days = 7))),
                             DoubleVar(self, max(Hive_Processed[0].get_humidity(num_days = 7)))],
            "hive5_humid":  [DoubleVar(self, Hive_Processed[0].get_humidity(num_days = 7).iloc[-1]),
                             DoubleVar(self, min(Hive_Processed[0].get_humidity(num_days = 7))),
                             DoubleVar(self, max(Hive_Processed[0].get_humidity(num_days = 7)))],
            "min_max_temp": [DoubleVar(self, PROCESS_FORECAST_MIN_MAX(forecast_data)[0]), DoubleVar(self, PROCESS_FORECAST_MIN_MAX(forecast_data)[1])],
            "min_max_humid":[DoubleVar(self, PROCESS_FORECAST_MIN_MAX(forecast_data)[2]), DoubleVar(self, PROCESS_FORECAST_MIN_MAX(forecast_data)[3])],
        }
        self.shared_data.update({"LF_geometry": [IntVar(self, int((int(self.shared_data["window_geometry"][0].get()) - 2 * int(self.shared_data["padding"].get())) / int(self.shared_data["num_cols"].get()))),
                                                 IntVar(self, int((int(self.shared_data["window_geometry"][1].get()) - 2 * int(self.shared_data["padding"].get())) / int(self.shared_data["num_rows"].get())) - 30),
                                                ]}) # height (notebook tabs appear to be 30 pix)
        self.wm_title("Creative Envy Dashboard")
        ttk.Style("darkly")
        self.geometry(str(self.shared_data["window_geometry"][0].get()) + "x" + str(self.shared_data["window_geometry"][1].get()))
        self.resizable(False, False)
        self.container = Frame(self)
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)
        main_notebook = ttk.Notebook(
            self,
            height = str(int(self.shared_data["window_geometry"][1].get()) - 2 * int(self.shared_data["padding"].get())),
            width = str(int(self.shared_data["window_geometry"][0].get()) - 2 * int(self.shared_data["padding"].get())),
            ) # "self" as passed argument means Windows is parent
        tab_names = [
                    "Weather",
                    "Bees",
                    "Photos",
                    # "Alarm",
                    ]
        for i, F in enumerate([
                              Pane1,
                              Pane2,
                              Pane3,
                              # Pane4,
                              ]):
            frame = F(main_notebook, self)
            main_notebook.add(frame, text = tab_names[i]) # "self." adds to this instance, ...(self) adds to parent instance
        main_notebook.grid(
            row = 0,
            column = 0,
            padx = int(self.shared_data["padding"].get()),
            pady = int(self.shared_data["padding"].get()),
            ipadx = int(self.shared_data["padding"].get()),
            ipady = int(self.shared_data["padding"].get()),
        )
        main_notebook.grid_rowconfigure(0, weight = 1)
        main_notebook.grid_columnconfigure(0, weight = 1)
        
        def on_tab_change(event):
            index = main_notebook.index(main_notebook.select())
        main_notebook.bind("<<NotebookTabChanged>>", on_tab_change)

        #self.after(60000, self.refresh)

    def refresh(self):
        self.destroy()
        self.__init__()
    
def main():
    windows = Windows()
    windows.mainloop()
    
def timers():
    timers = Timers()
    
if __name__ == '__main__': # runs main if in python script
    t1 = threading.Thread(target = main,args = ())
    t2 = threading.Thread(target = timers,args = ())
    t1.start()
    t2.start()
    t1.join()
    t2.join()