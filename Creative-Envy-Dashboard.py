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
from BEE_WEATHER_DATA import BROODMINDER_GET, AMBIENT_GET
sys.path.append("PYICLOUD_GET")
import PYICLOUD_GET

# root window (parent to all), controller to Frames
class Windows(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.shared_data = {
            "window_geometry":    [IntVar(self, 1280),  IntVar(self, 800)],
            "padding":     IntVar(self, 5),
            "num_rows":    IntVar(self, 3),
            "num_cols":    IntVar(self, 5),
        }
        self.shared_data.update({"notebook_geometry": [IntVar(self, int(self.shared_data["window_geometry"][0].get()) - (int(self.shared_data["padding"].get()) * 5)), # width
                                                       IntVar(self, int(self.shared_data["window_geometry"][1].get()) - (int(self.shared_data["padding"].get()) * 11)), # height
                                                      ]})
        self.shared_data.update({"LF_geometry": [IntVar(self, (int(self.shared_data["notebook_geometry"][0].get()) - (int(self.shared_data["padding"].get()) * int(self.shared_data["num_cols"].get()) * 2)) / int(self.shared_data["num_cols"].get())), # width
                                                 IntVar(self, ((int(self.shared_data["notebook_geometry"][1].get()) - (int(self.shared_data["padding"].get()) * int(self.shared_data["num_rows"].get()) * 2)) / int(self.shared_data["num_rows"].get())) - 30), # height (notebook tabs appear to be 30 pix)
                                                ]})
        self.wm_title("Creative Envy Dashboard")
        ttk.Style("darkly")
        self.geometry(str(self.shared_data["window_geometry"][0].get()) + "x" + str(self.shared_data["window_geometry"][1].get()))
        self.resizable(False, False)
        self.container = Frame(self)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        main_notebook = ttk.Notebook(
            self,
            height = str(self.shared_data["notebook_geometry"][1].get()),
            width = str(self.shared_data["notebook_geometry"][0].get()),
        ) # "self" as passed argument means Windows is parent
        tab_names = ["Weather", "Bees", "Photos",  "Alarm"]
        for i, F in enumerate([Pane1, Pane2, Pane3, Pane4]):
            frame = F(main_notebook, self)
            main_notebook.add(frame, text=tab_names[i]) # "self." adds to this instance, ...(self) adds to parent instance
        main_notebook.grid(
            row=0,
            column=0,
            padx=(int(self.shared_data["padding"].get()), int(self.shared_data["padding"].get())),
            pady=(int(self.shared_data["padding"].get()), int(self.shared_data["padding"].get())),
            ipadx=int(self.shared_data["padding"].get()),
            ipady=int(self.shared_data["padding"].get()),
        )
        
        def on_tab_change(event):
            index = main_notebook.index(main_notebook.select())
        main_notebook.bind("<<NotebookTabChanged>>", on_tab_change)

class Pane1(Frame): # Weather Dashboard; child to Notebook
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        # Pane1 Objects
        # Loop to create LabelFrames
        lfs = []
        lf_labels = "Time/Sunrise/Sunset", "Moon Phase", "Wx Forecast", "", "Honey Wt./Bee Count", "Temp", "Solar Rad.", "Wind Spd./Dir.", "Chook Temp", "Bee Wt.", "Humidity", "UV Index", "Precip.", "Bee Temp.", "Bee Humid.",
        i = 0
        while i < 15:
            lfs.append(ttk.LabelFrame(
                self,
                relief="solid",
                borderwidth=1,
                width=str(self.controller.shared_data["LF_geometry"][0].get()),
                height=str(self.controller.shared_data["LF_geometry"][1].get()),
                padding=int(self.controller.shared_data["padding"].get()),
                text=lf_labels[i],
            ))
            if i == 2:
                lfs[-1].grid(
                    row = floor(i/5),
                    column = i % 5, columnspan = 2,
                    sticky="nsew",
                    padx=(int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
                    pady=(int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
                    ipadx=int(self.controller.shared_data["padding"].get()),
                    ipady=int(self.controller.shared_data["padding"].get()),
                )
                i = i + 2
            else:
                lfs[-1].grid(row = floor(i/5), column = i % 5, sticky="nsew", padx=int(self.controller.shared_data["padding"].get()), pady=int(self.controller.shared_data["padding"].get()))
                i = i + 1
        
        # Loop to create Meters
        i = 4
        meters = []
        while i < len(lfs):
            meters.append(ttk.Meter(
                lfs[i],
                metersize=min(int(self.controller.shared_data["LF_geometry"][0].get()), int(self.controller.shared_data["LF_geometry"][1].get())),
                amountused=25,
                metertype="semi",
                subtext=lf_labels[i + 1],
                showtext=True,
                interactive=False,
            ))
            meters[-1].grid(
                row = floor((i-4)/5) + 1,
                column = (i - 4) % 5,
                sticky="nsew",
                padx=(int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
                pady=(int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
                ipadx=int(self.controller.shared_data["padding"].get()),
                ipady=int(self.controller.shared_data["padding"].get()),
            ) # for some reason ipad works better on meter than LF
            i = i + 1

class Pane2(Frame): # Bee Dashboard
     def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        # Pane1 Objects
        # Loop to create LabelFrames
        lfs = []
        lf_labels = "Time/Sunrise/Sunset", "Moon Phase", "Wx Forecast", "", "Honey Wt./Bee Count", "Temp", "Solar Rad.", "Wind Spd./Dir.", "Chook Temp", "Bee Wt.", "Humidity", "UV Index", "Precip.", "Bee Temp.", "Bee Humid.",
        i = 0
        while i < 15:
            lfs.append(ttk.LabelFrame(
                self,
                relief="solid",
                borderwidth=1,
                width=str(self.controller.shared_data["LF_geometry"][0].get()),
                height=str(self.controller.shared_data["LF_geometry"][1].get()),
                padding=int(self.controller.shared_data["padding"].get()),
                text=lf_labels[i],
            ))
            if i == 2:
                lfs[-1].grid(
                    row = floor(i/5),
                    column = i % 5, columnspan = 2,
                    sticky="nsew",
                    padx=(int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
                    pady=(int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
                    ipadx=int(self.controller.shared_data["padding"].get()),
                    ipady=int(self.controller.shared_data["padding"].get()),
                )
                i = i + 2
            else:
                lfs[-1].grid(row = floor(i/5), column = i % 5, sticky="nsew", padx=int(self.controller.shared_data["padding"].get()), pady=int(self.controller.shared_data["padding"].get()))
                i = i + 1
        
        # Loop to create Meters
        i = 4
        meters = []
        while i < len(lfs):
            meters.append(ttk.Meter(
                lfs[i],
                metersize=min(int(self.controller.shared_data["LF_geometry"][0].get()), int(self.controller.shared_data["LF_geometry"][1].get())),
                amountused=25,
                metertype="semi",
                subtext=lf_labels[i + 1],
                showtext=True,
                interactive=False,
            ))
            meters[-1].grid(
                row = floor((i-4)/5) + 1,
                column = (i - 4) % 5,
                sticky="nsew",
                padx=(int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
                pady=(int(self.controller.shared_data["padding"].get()), int(self.controller.shared_data["padding"].get())),
                ipadx=int(self.controller.shared_data["padding"].get()),
                ipady=int(self.controller.shared_data["padding"].get()),
            ) # for some reason ipad works better on meter than LF
            i = i + 1

class Pane3(Frame): # Picture Frame
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        directory = "PhotosB/"
        file_paths = []
        ext = ('.png', '.jpg', '.jpeg', '.HEIC', '.tiff', '.tif')
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
            width=self.controller.shared_data["notebook_geometry"][0].get() - 2 * self.controller.shared_data["padding"].get(),
            height=self.controller.shared_data["notebook_geometry"][1].get() - 2 * self.controller.shared_data["padding"].get(),
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
            rand_pic = file_paths[random.randint(0,len(file_paths) - 1)]
            PIL_image = Image.open(rand_pic)
            original_w = np.shape(PIL_image)[1]
            original_h = np.shape(PIL_image)[0]
            aspect = original_h/original_w

            constraining_dim = min(self.controller.shared_data["notebook_geometry"][0].get(), self.controller.shared_data["notebook_geometry"][1].get())
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
        in_frame = Button(make_frame, command = change_pic)
        change_pic()
        in_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        
class Pane4(Frame): # Alarm Control
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        
        # Pane4 Objects
        canvas1 = Canvas(
            self,
            width=str(self.controller.shared_data["notebook_geometry"][0].get()),
            height=str(self.controller.shared_data["notebook_geometry"][1].get()),
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
    t2 = threading.Thread(target=PYICLOUD_GET.cycle_files,args=())
    t3 = threading.Thread(target=PYICLOUD_GET.download,args=())
    t4 = threading.Thread(target=BROODMINDER_GET,args=())
    t5 = threading.Thread(target=AMBIENT_GET,args=())
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()