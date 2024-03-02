from PIL import Image
Image.CUBIC = Image.BICUBIC
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
import os, time, sys, queue, datetime
from csv import writer
from datetime import datetime, timedelta
from threading import Thread, Event
from tkinter import filedialog, Canvas, Label, LabelFrame, Frame, PhotoImage, Button, Entry, Scrollbar, StringVar, IntVar, DoubleVar#, ttk 
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
# import nest_asyncio
# nest_asyncio.apply()
sys.path.append("BROODMINDER_GET")
from BROODMINDER_GET import BROODMINDER_GET
sys.path.append("PYICLOUD_GET")
import PYICLOUD_GET

# root window (parent to all), controller to Frames
class Windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.shared_data = {
            "window_geometry":    [IntVar(self, 1280),  IntVar(self, 800)],
            "padding":     IntVar(self, 5),
            "num_rows":    IntVar(self, 3),
            "num_cols":    IntVar(self, 5),
        }
        self.shared_data.update({"notebook_geometry": [IntVar(self, int(self.shared_data["window_geometry"][0].get()) - (int(self.shared_data["padding"].get()) * 3)), # width
                                                       IntVar(self, int(self.shared_data["window_geometry"][1].get()) - (int(self.shared_data["padding"].get()) * 9)), # height
                                                      ]})
        self.shared_data.update({"LF_geometry": [IntVar(self, (int(self.shared_data["notebook_geometry"][0].get()) - (int(self.shared_data["padding"].get()) * int(self.shared_data["num_cols"].get()) * 2 - 1)) / int(self.shared_data["num_cols"].get())), # width
                                                 IntVar(self, (int(self.shared_data["notebook_geometry"][1].get()) - (int(self.shared_data["padding"].get()) * int(self.shared_data["num_rows"].get()) * 2)) / int(self.shared_data["num_rows"].get()) - 30), # height
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
        tab_names = ["Dash", "Alarm", "Photos"]
        for i, F in enumerate([Pane1, Pane2, Pane3]):
            frame = F(main_notebook, self)
            #main_notebook.add(frame, text= 'Tab %s' % (i + 1)) # "self." adds to this instance, ...(self) adds to parent instance
            main_notebook.add(frame, text=tab_names[i]) # "self." adds to this instance, ...(self) adds to parent instance
        main_notebook.grid(
            row=0,
            column=0,
            #sticky="nsew",
            padx=(int(self.shared_data["padding"].get()), int(self.shared_data["padding"].get())),
            pady=(int(self.shared_data["padding"].get()), int(self.shared_data["padding"].get())),
        )
        
        def on_tab_change(event):
            index = main_notebook.index(main_notebook.select())
        main_notebook.bind("<<NotebookTabChanged>>", on_tab_change)

class Pane1(tk.Frame): # child to Notebook
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
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
                lfs[-1].grid(row = floor(i/5), column = i % 5, columnspan = 2, sticky="nsew", padx=int(self.controller.shared_data["padding"].get()), pady=int(self.controller.shared_data["padding"].get()))
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
            meters[-1].grid(row = floor((i-4)/5) + 1, column = (i - 4) % 5, sticky="nsew", padx=int(self.controller.shared_data["padding"].get()), pady=int(self.controller.shared_data["padding"].get()), ipadx=int(self.controller.shared_data["padding"].get()), ipady=int(self.controller.shared_data["padding"].get())) # for some reason ipad works better on meter than LF
            i = i + 1

class Pane2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Pane2 Objects
        canvas1 = tk.Canvas(
            self,
            width=str(self.controller.shared_data["notebook_geometry"][0].get()),
            height=str(self.controller.shared_data["notebook_geometry"][1].get()),
        ).grid(row=0, column=0)

class Pane3(tk.Frame): # Picture Frame (need to install pyicloud)
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Pane3 Objects
        canvas1 = tk.Canvas(
            self,
            width=str(self.controller.shared_data["notebook_geometry"][0].get()),
            height=str(self.controller.shared_data["notebook_geometry"][1].get()),
        )
        canvas1.create_rectangle(0, 0, int(self.controller.shared_data["notebook_geometry"][0].get()), int(self.controller.shared_data["notebook_geometry"][1].get()), fill="#444444")
        canvas1.create_rectangle(20, 20, int(self.controller.shared_data["notebook_geometry"][0].get()) - 20, int(self.controller.shared_data["notebook_geometry"][1].get()) - 50, fill="black")
        canvas1.grid(row=0, column=0)

def main():
    windows = Windows()
    windows.mainloop()
    
if __name__ == '__main__': # runs main if in python script
    t1 = threading.Thread(target=main,args=())
    t2 = threading.Thread(target=PYICLOUD_GET.cycle_files,args=())
    t2 = threading.Thread(target=PYICLOUD_GET.download,args=())
    t1.start()
    t2.start()
    t1.join()
    t2.join()