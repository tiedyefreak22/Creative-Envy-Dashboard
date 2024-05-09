import sys
if "Tkinter" not in sys.modules:
    from tkinter import *
from PIL import Image, ImageTk
Image.CUBIC = Image.BICUBIC
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from BEE_WEATHER_DATA import BROODMINDER_GET, AMBIENT_GET, READ_HIVE, PROCESS_HIVE, READ_BEE_WEATHER, PROCESS_BEE_WEATHER, PROCESS_AMBIENT, GRAPH_DATA, GET_MOON_IMAGE, GET_FORECAST, PROCESS_FORECAST, PROCESS_FORECAST_MIN_MAX, check_internet_connection, GET_WEATHER_ICON
import PYICLOUD_GET
import settings
import time

class Timers(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

    def daily_updater(self):
        # try:
        GET_MOON_IMAGE()
        if settings.pyicloud:
            PYICLOUD_GET.cycle_files()
            PYICLOUD_GET.download()
        # except:
        #     print("***FAIL*** daily_updater")
        self.after(86400000, self.daily_updater)
    
    def hourly_updater(self):
        # try:
        GET_FORECAST()
        # except:
        #     print("***FAIL*** hourly_updater")
        self.after(3600000, self.hourly_updater)
    
    def five_min_updater(self):
        # try:
        for hive_name, hive_ID in settings.hive_IDs.items():
            BROODMINDER_GET(hive_name, hive_ID)
        AMBIENT_GET()
        # except:
        #     print("***FAIL*** five_min_updater")
        self.after(300000, self.five_min_updater)