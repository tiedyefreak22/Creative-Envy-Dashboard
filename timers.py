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
        self.daily_updater()
        self.hourly_updater()
        self.five_min_updater()

    def daily_updater(self):
        GET_MOON_IMAGE()
        if settings.pyicloud:
            PYICLOUD_GET.cycle_files()
            PYICLOUD_GET.download()
        self.after(86400000, self.daily_updater)
    
    def hourly_updater(self):
        GET_FORECAST()
        self.after(3600000, self.hourly_updater)
    
    def five_min_updater(self):
        for hive_name, hive_ID in settings.hive_IDs.items():
            BROODMINDER_GET(hive_name, hive_ID)
        AMBIENT_GET()
        self.after(300000, self.five_min_updater)

class Singleton(type):
    _instances = {}
    # redefine (override) what it means to "call" a class
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # No existing instance; build one now.
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        elif hasattr(cls, '__allow_reinitialization') and cls.__allow_reinitialization:
            # if the class allows reinitialization, then do it
            instance = cls._instances[cls]
            instance.__init__(*args, **kwargs)  # call the init again
        else:
            raise Exception("Singleton cannot be instantiated more than once")
        return instance

class Ambient(metaclass = Singleton):
    # __allow_reinitialization = True
    def __init__(self, value):
        self._value = value

    @property
    def ambient(self):
        return self._value

    @ambient.setter
    def ambient(self, value):
        self._value = value

class BeeWeather(metaclass = Singleton):
    # __allow_reinitialization = True
    def __init__(self, value):
        self._value = value

    @property
    def beeweather(self):
        return self._value

    @beeweather.setter
    def beeweather(self, value):
        self._value = value

class Hive(Tk):
    def __init__(self, hive_name, hive_ID):
        Tk.__init__(self)
        self.hive_name = hive_name
        self.hive_ID = hive_ID
        self._hive_df = None
        self._honey = None
        self._bees = None
        self._weight = None
        self._upper_temp = None
        self._lower_temp = None
        self._humid = None
        #self.five_min_updater()

    @property
    def hive(self):
        return self._hive_df

    @hive.setter
    def hive(self, hive_df):
        self._hive_df = hive_df
        # self._honey = None
        # self._bees = None
        self._weight = list(gen_dict_extract("Weight", hive_df))
        self._upper_temp = hive_df["Upper Brood"]["Temperature"]
        self._lower_temp = hive_df["Lower Brood"]["Temperature"]
        self._humid = list(gen_dict_extract("Humidity", hive_df))

    def set(self):
        self.hive = PROCESS_HIVE(self.hive_name)
        
    def five_min_updater(self):
        BROODMINDER_GET(self._hive_name, self._hive_ID)
        self.after(300000, self.five_min_updater)
    
    # def get_honey(self):
    #     return(list(gen_dict_extract("Weight", PROCESS_HIVE(self._hive_name))))

    # def get_bees(self):
    #     return(list(gen_dict_extract("Weight", PROCESS_HIVE(self._hive_name))))

    def get_weight(self):
        return(self._weight)

    def get_upper_temp(self):
        return(self._upper_temp)

    def get_lower_temp(self):
        return(self._lower_temp)

    def get_humidity(self):
        return(self._humid)