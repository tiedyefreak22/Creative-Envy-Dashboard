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
from pathlib import Path
sys.path.append("BEE_WEATHER_DATA")
from BEE_WEATHER_DATA import BROODMINDER_GET, AMBIENT_GET, READ_HIVE, PROCESS_HIVE, READ_BEE_WEATHER, PROCESS_BEE_WEATHER, PROCESS_AMBIENT, GRAPH_DATA, GET_MOON_IMAGE, GET_FORECAST, PROCESS_FORECAST, PROCESS_FORECAST_MIN_MAX, check_internet_connection
sys.path.append("PYICLOUD_GET")
import PYICLOUD_GET
import pandas as pd
from IPython.display import display
        
internet = check_internet_connection()

# root window (parent to all), controller to Frames
class Windows(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        hive_names = "New Left Hive"
        Hive_Processed = PROCESS_HIVE(hive_names)
        forecast_data = PROCESS_FORECAST()
        ambient_data = PROCESS_AMBIENT()
        file = [i for i in os.listdir("moon/")]
        self.shared_data = {
            "window_geometry":    [IntVar(self, 1280),  IntVar(self, 800)],
            "padding":      IntVar(self, 5),
            "num_rows":     IntVar(self, 3),
            "num_cols":     IntVar(self, 5),
            "hive_name":    StringVar(self, hive_names),
            "sun":          [StringVar(self, 1), StringVar(self, 1)],
            #"moon":         moon_img,
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
            "ambient_temp": [IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "solar":        [DoubleVar(self, 1), DoubleVar(self, 1), DoubleVar(self, 1)],
            "wind_spd":     [IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "wind_dir":     [IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "ambient_humid":[IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "UV":           [IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "Precip":       [DoubleVar(self, 1), DoubleVar(self, 1), DoubleVar(self, 1)],
            "lightning":    StringVar(self, 1),
            "air_qual":     [IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "chooks":       [IntVar(self, 1), IntVar(self, 1), IntVar(self, 1)],
            "hive1_wt":     [DoubleVar(self, list(Hive_Processed[list(Hive_Processed.keys())[0]]["Weight"].items())[-1][1]), DoubleVar(self, min([i[1] for i in list(Hive_Processed[list(Hive_Processed.keys())[0]]["Weight"].items())])), DoubleVar(self, max([i[1] for i in list(Hive_Processed[list(Hive_Processed.keys())[0]]["Weight"].items())]))],
            "hive2_wt":     [DoubleVar(self, 1), DoubleVar(self, 1), DoubleVar(self, 2)],
            "hive3_wt":     [DoubleVar(self, 1), DoubleVar(self, 1), DoubleVar(self, 2)],
            "hive4_wt":     [DoubleVar(self, 1), DoubleVar(self, 1), DoubleVar(self, 2)],
            "hive5_wt":     [DoubleVar(self, 1), DoubleVar(self, 1), DoubleVar(self, 2)],
            "hive1_temp":   [DoubleVar(self, list(Hive_Processed[list(Hive_Processed.keys())[2]]["Temperature"].items())[-1][1]), DoubleVar(self, min([i[1] for i in list(Hive_Processed[list(Hive_Processed.keys())[2]]["Temperature"].items())])), DoubleVar(self, max([i[1] for i in list(Hive_Processed[list(Hive_Processed.keys())[2]]["Temperature"].items())]))],
            "hive2_temp":   [DoubleVar(self, 1), DoubleVar(self, 1), DoubleVar(self, 2)],
            "hive3_temp":   [DoubleVar(self, 1), DoubleVar(self, 1), DoubleVar(self, 2)],
            "hive4_temp":   [DoubleVar(self, 1), DoubleVar(self, 1), DoubleVar(self, 2)],
            "hive5_temp":   [DoubleVar(self, 1), DoubleVar(self, 1), DoubleVar(self, 2)],
            "hive1_humid":  [DoubleVar(self, list(Hive_Processed[list(Hive_Processed.keys())[1]]["Humidity"].items())[-1][1]), DoubleVar(self, min([i[1] for i in list(Hive_Processed[list(Hive_Processed.keys())[1]]["Humidity"].items())])), DoubleVar(self, max([i[1] for i in list(Hive_Processed[list(Hive_Processed.keys())[1]]["Humidity"].items())]))],
            "hive2_humid":  [IntVar(self, 1), IntVar(self, 1), IntVar(self, 2)],
            "hive3_humid":  [IntVar(self, 1), IntVar(self, 1), IntVar(self, 2)],
            "hive4_humid":  [IntVar(self, 1), IntVar(self, 1), IntVar(self, 2)],
            "hive5_humid":  [IntVar(self, 1), IntVar(self, 1), IntVar(self, 2)],
            "min_max_temp": [DoubleVar(self, PROCESS_FORECAST_MIN_MAX(forecast_data)[0]), DoubleVar(self, PROCESS_FORECAST_MIN_MAX(forecast_data)[1])],
            "min_max_humid":[DoubleVar(self, PROCESS_FORECAST_MIN_MAX(forecast_data)[2]), DoubleVar(self, PROCESS_FORECAST_MIN_MAX(forecast_data)[3])],
        }
        # self.shared_data.update({"notebook_geometry": [IntVar(self, int(self.shared_data["window_geometry"][0].get()) - (int(self.shared_data["padding"].get()) * 5)), # width
        #                                                IntVar(self, int(self.shared_data["window_geometry"][1].get()) - (int(self.shared_data["padding"].get()) * 11)), # height
        #                                               ]})
        # self.shared_data.update({"LF_geometry": [IntVar(self, (int(self.shared_data["notebook_geometry"][0].get()) - (int(self.shared_data["padding"].get()) * int(self.shared_data["num_cols"].get()) * 2)) / int(self.shared_data["num_cols"].get())), # width
        #                                          IntVar(self, ((int(self.shared_data["window_geometry"][1].get()) - (int(self.shared_data["padding"].get()) * int(self.shared_data["num_rows"].get()) * 2)) / int(self.shared_data["num_rows"].get())) - 30), # height (notebook tabs appear to be 30 pix)
        #                                         ]})
        self.shared_data.update({"LF_geometry": [IntVar(self, int((int(self.shared_data["window_geometry"][0].get()) - 2 * int(self.shared_data["padding"].get())) / int(self.shared_data["num_cols"].get()))),
                                                 IntVar(self, int((int(self.shared_data["window_geometry"][1].get()) - 2 * int(self.shared_data["padding"].get())) / int(self.shared_data["num_rows"].get())) - 30), 
                                                ]}) # height (notebook tabs appear to be 30 pix)
        
        self.wm_title("Creative Envy Dashboard")
        ttk.Style("darkly")
        self.geometry(str(self.shared_data["window_geometry"][0].get()) + "x" + str(self.shared_data["window_geometry"][1].get()))
        self.resizable(False, False)
        self.container = Frame(self)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
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
            main_notebook.add(frame, text=tab_names[i]) # "self." adds to this instance, ...(self) adds to parent instance
        main_notebook.grid(
            row=0,
            column=0,
            padx=int(self.shared_data["padding"].get()),
            pady=int(self.shared_data["padding"].get()),
            ipadx=int(self.shared_data["padding"].get()),
            ipady=int(self.shared_data["padding"].get()),
        )
        main_notebook.grid_rowconfigure(0, weight=1)
        main_notebook.grid_columnconfigure(0, weight=1)
        
        def on_tab_change(event):
            index = main_notebook.index(main_notebook.select())
        main_notebook.bind("<<NotebookTabChanged>>", on_tab_change)

class CustomMeter(ttk.LabelFrame):
    def __init__(self, parent, controller, width, height, padding, text, amt_used):
        ttk.LabelFrame.__init__(
            self,
            parent,
            relief="solid",
            borderwidth=1,
            width=str(width),
            height=str(height),
            #padding=padding,
            text=text,
        )
        meter = ttk.Meter(
            self,
            metersize=min(int(width), int(height)) - 2 * int(padding),
            amountused=amt_used,
            metertype="semi",
            subtext=text,
            showtext=True,
            interactive=False,
        )
        meter.pack(anchor=CENTER)
    
    def get(self):
        return self.entry.get()

# class CustomSmallImg(): #Moon image, but generalized to a small space img, possibly used for weather icon too
    
# class CustomClockWidget(): #Clock, sunrise, sunset

class Pane1(Frame): # Weather Dashboard; child to Notebook
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        # Pane1 Objects
        # Loop to create LabelFrames
        lfs = []
        lf_labels = "Time/Sunrise/Sunset", "Moon Phase", "Wx Forecast", "", "Honey Wt./Bee Count", "Temp", "Solar Rad.", "Wind Spd./Dir.", "Chook Temp", "Bee Wt.", "Humidity", "UV Index", "Precip.", "Bee Temp.", "Bee Humid.",
        i = 0
        while i < 4:
            if i == 2:
                lfs.append(ttk.LabelFrame(
                    self,
                    relief="solid",
                    borderwidth=1,
                    width=str(int(self.controller.shared_data["LF_geometry"][0].get()) - int(self.controller.shared_data["padding"].get())),
                    height=str(self.controller.shared_data["LF_geometry"][1].get()),
                    #padding=int(self.controller.shared_data["padding"].get()),
                    text=lf_labels[i],
                ))
                lfs[-1].grid(
                    row = floor(i/5),
                    column = i % 5, columnspan = 2,
                    sticky="nsew",
                    # padx=(int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
                    # pady=(int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
                    # ipadx=int(self.controller.shared_data["padding"].get()),
                    # ipady=int(self.controller.shared_data["padding"].get()),
                )
                i = i + 2
            else:
                lfs.append(ttk.LabelFrame(
                    self,
                    relief="solid",
                    borderwidth=1,
                    width=str(self.controller.shared_data["LF_geometry"][0].get()),
                    height=str(self.controller.shared_data["LF_geometry"][1].get()),
                    #padding=int(self.controller.shared_data["padding"].get()),
                    text=lf_labels[i],
                ))
                lfs[-1].grid(row = floor(i/5), column = i % 5, sticky="nsew")#, padx=int(self.controller.shared_data["padding"].get()), pady=int(self.controller.shared_data["padding"].get()))
                i = i + 1
        
        # Loop to create Meters
        i = 4
        while i < 15:
            self.meter = CustomMeter(self, parent, str(self.controller.shared_data["LF_geometry"][0].get()), str(self.controller.shared_data["LF_geometry"][1].get()), int(self.controller.shared_data["padding"].get()), lf_labels[i], 25)
            self.meter.grid(row = floor((i-5)/5) + 1, column = (i - 5) % 5, sticky="nsew")#, padx=int(self.controller.shared_data["padding"].get()), pady=int(self.controller.shared_data["padding"].get()))
            i = i + 1
        meters = []
        
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

            constraining_dim = min(self.controller.shared_data["LF_geometry"][0].get() - 4 * self.controller.shared_data["padding"].get(),
                                   self.controller.shared_data["LF_geometry"][1].get() - 4 * self.controller.shared_data["padding"].get())
            minor_constraint = min(constraining_dim/original_w, constraining_dim/original_h)
            width = int(original_w * minor_constraint)
            height = int(original_h * minor_constraint)
            PIL_image_small = PIL_image.resize((width,height), Image.Resampling.LANCZOS)

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
            lfs[1],
            image = img,
            width=self.controller.shared_data["LF_geometry"][0].get() - 4 * self.controller.shared_data["padding"].get(),
            height=self.controller.shared_data["LF_geometry"][1].get() - 4 * self.controller.shared_data["padding"].get(),
        )
        change_pic()
        in_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        #-------------------------------------------------------------------------------------------------------------------------------------------------

        def periodic_updater():
            if internet:
                try:
                    BROODMINDER_GET(str(self.controller.shared_data["hive_name"].get()))
                    AMBIENT_GET()
                except:
                    pass
            
            # run itself again
            self.after(600000, periodic_updater)
        
        # run first time at once
        #periodic_updater()
        
        def change_clock():
            current_time = datetime.now().strftime('%I:%M:%S %p')
            clock_frame.config(text = current_time)
            clock_frame.text = current_time
            
        def change_forecast():
            GET_FORECAST()
        
        clock_frame = Label(
            lfs[0],
            text = datetime.now().strftime('%I:%M:%S %p'),
            font=("Helvetica’", 28),
        )
        change_clock()
        clock_frame.pack(side="top", ipady=30)

        sunrise_frame = Label(
            lfs[0],
            text = datetime.now().strftime("Sunrise: %I:%M:%S %p"),
            font=("Helvetica’", 16),
        )
        sunrise_frame.pack(side="bottom")
        sunset_frame = Label(
            lfs[0],
            text = datetime.now().strftime("Sunset: %I:%M:%S %p"),
            font=("Helvetica’", 16),
        )
        sunset_frame.pack(side="bottom", ipady=20)
        lfs[0].pack_propagate(0)
        
        def clock_updater():
            change_clock()
            # run itself again
            self.after(1000, clock_updater)

        clock_updater()
        
        def daily_updater():
            if internet:
                try:
                    change_pic()
                    change_forecast()
                except:
                    pass
            # run itself again
            self.after(86400000, daily_updater)
        
        # run first time at once
        daily_updater()

class Pane2(Frame): # Bee Dashboard
     def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        shared_list = list(self.controller.shared_data.keys())

        lf_labels = "Hive 1 Wt.", "Hive 2 Wt.", "Hive 3 Wt.", "Hive 4 Wt.", "Hive 5 Wt.", "Hive 1 Temp.", "Hive 2 Temp.", "Hive 3 Temp.", "Hive 4 Temp.", "Hive 5 Temp.", "Hive 1 Humid.", "Hive 2 Humid.", "Hive 3 Humid.", "Hive 4 Humid.", "Hive 5 Humid.",
        i = 0        
        while i < 15:
            self.meter = CustomMeter(self, parent, str(self.controller.shared_data["LF_geometry"][0].get()), str(self.controller.shared_data["LF_geometry"][1].get()), int(self.controller.shared_data["padding"].get()), lf_labels[i], 25)
            self.meter.grid(row = floor(i/5), column = i % 5, sticky="nsew")#, padx=int(self.controller.shared_data["padding"].get()), pady=int(self.controller.shared_data["padding"].get()))
            i = i + 1

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
                    PYICLOUD_GET.cycle_files()
                    PYICLOUD_GET.download()
                except:
                    pass
            # run itself again
            self.after(86400000, daily_updater)
        
        # run first time at once
        #daily_updater()
        
class Pane4(Frame): # Alarm Control
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        # Pane4 Objects
        canvas1 = Canvas(
            self,
            width=str(self.controller.shared_data["window_geometry"][0].get()),
            height=str(self.controller.shared_data["window_geometry"][1].get()),
        ).grid(
            row=0,
            column=0,
            padx=(int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
            pady=(int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
            ipadx=int(self.controller.shared_data["padding"].get()),
            ipady=int(self.controller.shared_data["padding"].get()),
        )

def main():
    windows = Windows()    
    windows.mainloop()
    
if __name__ == '__main__': # runs main if in python script
    t1 = threading.Thread(target=main,args=())
    # t2 = threading.Thread(target=PYICLOUD_GET.cycle_files,args=())
    # t3 = threading.Thread(target=PYICLOUD_GET.download,args=())
    # t4 = threading.Thread(target=BROODMINDER_GET,args=str("New Left Hive"))#str(self.controller.shared_data["hive_name"].get()))
    # t5 = threading.Thread(target=AMBIENT_GET,args=())
    t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    # t5.start()
    t1.join()
    # t2.join()
    # t3.join()
    # t4.join()
    # t5.join()
    # windows.mainloop()