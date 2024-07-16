import sys
if "Tkinter" not in sys.modules:
    from tkinter import *
from PIL import Image, ImageTk
Image.CUBIC = Image.BICUBIC
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from BEE_WEATHER_DATA import *
import PYICLOUD_GET
import settings
import time

def gen_dict_extract(key, var):
    if hasattr(var, 'items'):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result
            elif isinstance(v, pd.DataFrame):
                for result in gen_dict_extract(key, v):
                    yield result

class Timers(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        daily_updater()
        hourly_updater()
        five_min_updater()

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

class Hive(Tk):
    def __init__(self, hive_name, hive_ID):
        Tk.__init__(self)
        self.hive_name = hive_name
        self.hive_ID = hive_ID
        self.honey = None
        self.bees = None
        self.weight = None
        self.upper_temp = None
        self.lower_temp = None
        self.humid = None
        self.five_min_updater()

    def five_min_updater(self):
        BROODMINDER_GET(self.hive_name, self.hive_ID)
        self.after(300000, self.five_min_updater)

    # def get_honey(self):
    #     return(list(gen_dict_extract("Weight", PROCESS_HIVE(self.hive_name))))

    # def get_bees(self):
    #     return(list(gen_dict_extract("Weight", PROCESS_HIVE(self.hive_name))))

    def get_weight(self):
        return(list(gen_dict_extract("Weight", PROCESS_HIVE(self.hive_name))))

    # def get_upper_temp(self):
    #     return(list(gen_dict_extract("Weight", PROCESS_HIVE(self.hive_name))))

    # def get_lower_temp(self):
    #     return(list(gen_dict_extract("Weight", PROCESS_HIVE(self.hive_name))))

    def get_humidity(self):
        return(list(gen_dict_extract("Humidity", PROCESS_HIVE(self.hive_name))))