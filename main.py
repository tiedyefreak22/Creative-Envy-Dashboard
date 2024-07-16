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
        for hive_name in settings.hive_IDs.keys():
            Hive_Processed.append(PROCESS_HIVE(hive_name))
        forecast_data = PROCESS_FORECAST()
        ambient_data = PROCESS_AMBIENT()
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
            "ambient_temp": [DoubleVar(self, list(ambient_data[list(ambient_data.keys())]["tempf"].items())[-1][1]),
                             DoubleVar(self, min([i[1] for i in list(ambient_data[list(ambient_data.keys())]["tempf"].items())])),
                             DoubleVar(self, max([i[1] for i in list(ambient_data[list(ambient_data.keys())]["tempf"].items())]))],
            "solar":        [DoubleVar(self, list(ambient_data[list(ambient_data.keys())]["solarradiation"].items())[-1][1]),
                             DoubleVar(self, min([i[1] for i in list(ambient_data[list(ambient_data.keys())]["solarradiation"].items())])),
                             DoubleVar(self, max([i[1] for i in list(ambient_data[list(ambient_data.keys())]["solarradiation"].items())]))],
            "wind_spd":     [DoubleVar(self, list(ambient_data[list(ambient_data.keys())]["windspeedmph"].items())[-1][1]),
                             DoubleVar(self, min([i[1] for i in list(ambient_data[list(ambient_data.keys())]["windspeedmph"].items())])),
                             DoubleVar(self, max([i[1] for i in list(ambient_data[list(ambient_data.keys())]["windspeedmph"].items())]))],
            "wind_dir":     [DoubleVar(self, list(ambient_data[list(ambient_data.keys())]["winddir"].items())[-1][1]),
                             DoubleVar(self, min([i[1] for i in list(ambient_data[list(ambient_data.keys())]["winddir"].items())])),
                             DoubleVar(self, max([i[1] for i in list(ambient_data[list(ambient_data.keys())]["winddir"].items())]))],
            "ambient_humid":[DoubleVar(self, list(ambient_data[list(ambient_data.keys())]["humidity"].items())[-1][1]),
                             DoubleVar(self, min([i[1] for i in list(ambient_data[list(ambient_data.keys())]["humidity"].items())])),
                             DoubleVar(self, max([i[1] for i in list(ambient_data[list(ambient_data.keys())]["humidity"].items())]))],
            "UV":           [DoubleVar(self, list(ambient_data[list(ambient_data.keys())]["uv"].items())[-1][1]),
                             DoubleVar(self, min([i[1] for i in list(ambient_data[list(ambient_data.keys())]["uv"].items())])),
                             DoubleVar(self, max([i[1] for i in list(ambient_data[list(ambient_data.keys())]["uv"].items())]))],
            "Precip":       [DoubleVar(self, list(ambient_data[list(ambient_data.keys())]["hourlyrainin"].items())[-1][1]),
                             DoubleVar(self, min([i[1] for i in list(ambient_data[list(ambient_data.keys())]["hourlyrainin"].items())])),
                             DoubleVar(self, max([i[1] for i in list(ambient_data[list(ambient_data.keys())]["hourlyrainin"].items())]))],
            "lightning":    StringVar(self, 1),
            "air_qual":     [IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "chooks":       [IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "hive1_wt":     [DoubleVar(self, list(Hive_Processed[0]['Scale Under Hive']['Weight'].items())[-1][1]),
                             DoubleVar(self, min(Hive_Processed[0]['Scale Under Hive']['Weight'])),
                             DoubleVar(self, max(Hive_Processed[0]['Scale Under Hive']['Weight']))],
            "hive2_wt":     [DoubleVar(self, list(Hive_Processed[1]['Scale Under Hive']['Weight'].items())[-1][1]),
                             DoubleVar(self, min(Hive_Processed[1]['Scale Under Hive']['Weight'])),
                             DoubleVar(self, max(Hive_Processed[1]['Scale Under Hive']['Weight']))],
            # "hive3_wt":     [DoubleVar(self, list(Hive_Processed[2]['Scale Under Hive']['Weight'].items())[-1][1]),
            #                  DoubleVar(self, min(Hive_Processed[2]['Scale Under Hive']['Weight'])),
            #                  DoubleVar(self, max(Hive_Processed[2]['Scale Under Hive']['Weight']))],
            "hive3_wt":     [DoubleVar(self, list(Hive_Processed[0]['Scale Under Hive']['Weight'].items())[-1][1]),
                             DoubleVar(self, min(Hive_Processed[0]['Scale Under Hive']['Weight'])),
                             DoubleVar(self, max(Hive_Processed[0]['Scale Under Hive']['Weight']))],
            "hive4_wt":     [DoubleVar(self, list(Hive_Processed[0]['Scale Under Hive']['Weight'].items())[-1][1]),
                             DoubleVar(self, min(Hive_Processed[0]['Scale Under Hive']['Weight'])),
                             DoubleVar(self, max(Hive_Processed[0]['Scale Under Hive']['Weight']))],
            "hive5_wt":     [DoubleVar(self, list(Hive_Processed[0]['Scale Under Hive']['Weight'].items())[-1][1]),
                             DoubleVar(self, min(Hive_Processed[0]['Scale Under Hive']['Weight'])),
                             DoubleVar(self, max(Hive_Processed[0]['Scale Under Hive']['Weight']))],
            "hive1_temp":   [DoubleVar(self, list(Hive_Processed[0]['Lower Brood']['Temperature'].items())[-1][1]),
                             DoubleVar(self, min(Hive_Processed[0]['Lower Brood']['Temperature'])),
                             DoubleVar(self, max(Hive_Processed[0]['Lower Brood']['Temperature']))],
            # "hive2_temp":   [DoubleVar(self, list(Hive_Processed[1]['Lower Brood']['Temperature'].items())[-1][1]),
            #                  DoubleVar(self, min(Hive_Processed[1]['Lower Brood']['Temperature'])),
            #                  DoubleVar(self, max(Hive_Processed[1]['Lower Brood']['Temperature']))],
            # "hive3_temp":   [DoubleVar(self, list(Hive_Processed[2]['Lower Brood']['Temperature'].items())[-1][1]),
            #                  DoubleVar(self, min(Hive_Processed[2]['Lower Brood']['Temperature'])),
            #                  DoubleVar(self, max(Hive_Processed[2]['Lower Brood']['Temperature']))],
            "hive2_temp":   [DoubleVar(self, list(Hive_Processed[0]['Lower Brood']['Temperature'].items())[-1][1]),
                             DoubleVar(self, min(Hive_Processed[0]['Lower Brood']['Temperature'])),
                             DoubleVar(self, max(Hive_Processed[0]['Lower Brood']['Temperature']))],
            "hive3_temp":   [DoubleVar(self, list(Hive_Processed[0]['Lower Brood']['Temperature'].items())[-1][1]),
                             DoubleVar(self, min(Hive_Processed[0]['Lower Brood']['Temperature'])),
                             DoubleVar(self, max(Hive_Processed[0]['Lower Brood']['Temperature']))],
            "hive4_temp":   [DoubleVar(self, list(Hive_Processed[0]['Lower Brood']['Temperature'].items())[-1][1]),
                             DoubleVar(self, min(Hive_Processed[0]['Lower Brood']['Temperature'])),
                             DoubleVar(self, max(Hive_Processed[0]['Lower Brood']['Temperature']))],
            "hive5_temp":   [DoubleVar(self, list(Hive_Processed[0]['Lower Brood']['Temperature'].items())[-1][1]),
                             DoubleVar(self, min(Hive_Processed[0]['Lower Brood']['Temperature'])),
                             DoubleVar(self, max(Hive_Processed[0]['Lower Brood']['Temperature']))],
            "hive1_humid":  [DoubleVar(self, list(Hive_Processed[0]['Upper Brood']['Humidity'].items())[-1][1]),
                             DoubleVar(self, min(Hive_Processed[0]['Upper Brood']['Humidity'])),
                             DoubleVar(self, max(Hive_Processed[0]['Upper Brood']['Humidity']))],
            # "hive2_humid":  [DoubleVar(self, list(Hive_Processed[1]['Upper Brood']['Humidity'].items())[-1][1]),
            #                  DoubleVar(self, min(Hive_Processed[1]['Upper Brood']['Humidity'])),
            #                  DoubleVar(self, max(Hive_Processed[1]['Upper Brood']['Humidity']))],
            # "hive3_humid":  [DoubleVar(self, list(Hive_Processed[2]['Upper Brood']['Humidity'].items())[-1][1]),
            #                  DoubleVar(self, min(Hive_Processed[2]['Upper Brood']['Humidity'])),
            #                  DoubleVar(self, max(Hive_Processed[2]['Upper Brood']['Humidity']))],
            "hive2_humid":  [DoubleVar(self, list(Hive_Processed[0]['Upper Brood']['Humidity'].items())[-1][1]),
                             DoubleVar(self, min(Hive_Processed[0]['Upper Brood']['Humidity'])),
                             DoubleVar(self, max(Hive_Processed[0]['Upper Brood']['Humidity']))],
            "hive3_humid":  [DoubleVar(self, list(Hive_Processed[0]['Upper Brood']['Humidity'].items())[-1][1]),
                             DoubleVar(self, min(Hive_Processed[0]['Upper Brood']['Humidity'])),
                             DoubleVar(self, max(Hive_Processed[0]['Upper Brood']['Humidity']))],
            "hive4_humid":  [DoubleVar(self, list(Hive_Processed[0]['Upper Brood']['Humidity'].items())[-1][1]),
                             DoubleVar(self, min(Hive_Processed[0]['Upper Brood']['Humidity'])),
                             DoubleVar(self, max(Hive_Processed[0]['Upper Brood']['Humidity']))],
            "hive5_humid":  [DoubleVar(self, list(Hive_Processed[0]['Upper Brood']['Humidity'].items())[-1][1]),
                             DoubleVar(self, min(Hive_Processed[0]['Upper Brood']['Humidity'])),
                             DoubleVar(self, max(Hive_Processed[0]['Upper Brood']['Humidity']))],
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