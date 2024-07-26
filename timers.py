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
    def __init__(self):
        self._ambient_df = None
        self._winddir = None
        self._windspeedmph = None
        self._windgustmph = None
        self._maxdailygust = None
        self._tempf = None
        self._humidity = None
        self._hourlyrainin = None
        self._eventrainin = None
        self._dailyrainin = None
        self._weeklyrainin = None
        self._monthlyrainin = None
        self._yearlyrainin = None
        self._totalrainin = None
        self._uv = None
        self._solarradiation = None
        self._feelsLike = None
        self._dewPoint = None
        self._lastRain = None

    @property
    def ambient(self):
        return self._ambient_df

    @ambient.setter
    def ambient(self, ambient_df):
        self._ambient_df = ambient_df
        self._winddir = list(ambient_df[list(ambient_df.keys())]["winddir"].items())[-1][1]
        self._windspeedmph = list(ambient_df[list(ambient_df.keys())]["windspeedmph"].items())[-1][1]
        self._windgustmph = list(ambient_df[list(ambient_df.keys())]["windgustmph"].items())[-1][1]
        self._maxdailygust = list(ambient_df[list(ambient_df.keys())]["maxdailygust"].items())[-1][1]
        self._tempf = list(ambient_df[list(ambient_df.keys())]["tempf"].items())[-1][1]
        self._humidity = list(ambient_df[list(ambient_df.keys())]["humidity"].items())[-1][1]
        self._hourlyrainin = list(ambient_df[list(ambient_df.keys())]["hourlyrainin"].items())[-1][1]
        self._eventrainin = list(ambient_df[list(ambient_df.keys())]["eventrainin"].items())[-1][1]
        self._dailyrainin = list(ambient_df[list(ambient_df.keys())]["dailyrainin"].items())[-1][1]
        self._weeklyrainin = list(ambient_df[list(ambient_df.keys())]["weeklyrainin"].items())[-1][1]
        self._monthlyrainin = list(ambient_df[list(ambient_df.keys())]["monthlyrainin"].items())[-1][1]
        self._yearlyrainin = list(ambient_df[list(ambient_df.keys())]["yearlyrainin"].items())[-1][1]
        self._totalrainin = list(ambient_df[list(ambient_df.keys())]["totalrainin"].items())[-1][1]
        self._uv = list(ambient_df[list(ambient_df.keys())]["uv"].items())[-1][1]
        self._solarradiation = list(ambient_df[list(ambient_df.keys())]["solarradiation"].items())[-1][1]
        self._feelsLike = list(ambient_df[list(ambient_df.keys())]["feelslike"].items())[-1][1]
        self._dewPoint = list(ambient_df[list(ambient_df.keys())]["dewpoint"].items())[-1][1]
        self._lastRain = list(ambient_df[list(ambient_df.keys())]["lastrain"].items())[-1][1]

    def set(self):
        self.ambient = PROCESS_AMBIENT()

    def get_winddir(self):
        return(self._winddir)

    def get_windspeedmph(self):
        return(self._windspeedmph)

    def get_windgustmph(self):
        return(self._windgustmph)

    def get_maxdailygust(self):
        return(self._maxdailygust)

    def get_tempf(self):
        return(self._tempf)

    def get_humidity(self):
        return(self._humidity)

    def get_hourlyrainin(self):
        return(self._hourlyrainin)

    def get_eventrainin(self):
        return(self._eventrainin)

    def get_dailyrainin(self):
        return(self._dailyrainin)

    def get_weeklyrainin(self):
        return(self._weeklyrainin)

    def get_monthlyrainin(self):
        return(self._monthlyrainin)

    def get_yearlyrainin(self):
        return(self._yearlyrainin)

    def get_totalrainin(self):
        return(self._totalrainin)

    def get_uv(self):
        return(self._uv)

    def get_solarradiation(self):
        return(self._solarradiation)

    def get_feelsLike(self):
        return(self._feelsLike)

    def get_dewPoint(self):
        return(self._dewPoint)

    def get_lastRain(self):
        return(self._lastRain)

class BeeWeather(metaclass = Singleton):
    # __allow_reinitialization = True
    def __init__(self):
        self._beeweather_df = None
        self._temp = None
        self._rain_in = None # inches
        self._humidity = None # relative
        self._cloud_cover = None
        self._windspeed10m_mph = None
        self._pressure = None # millibars
        self._winddir = None # degrees

    @property
    def beeweather(self):
        return self._beeweather_df

    @beeweather.setter
    def beeweather(self, beeweather_df):
        self._beeweather_df = beeweather_df
        self._temp = beeweather_df["Temperature"]
        self._rain_in = beeweather_df["Precipitation_inches"] # inches
        self._humidity = beeweather_df["Relative_Humidity"] # relative
        self._cloud_cover = beeweather_df["Cloud_Cover"]
        self._windspeed10m_mph = beeweather_df["WindSpeed10mAbove_mph"]
        self._pressure = beeweather_df["SurfacePressure_millibars"] # millibars
        self._winddir = beeweather_df[" WindDirection_degrees"] # degrees

    def set(self):
        self.beeweather = PROCESS_BEE_WEATHER()

    def get_temp(self):
        return(self._temp)

    def get_rain_in(self):
        return(self._rain_in)

    def get_humidity(self):
        return(self._humidity)

    def get_cloud_cover(self):
        return(self._cloud_cover)

    def get_windspeed10m_mph(self):
        return(self._windspeed10m_mph)

    def get_pressure(self):
        return(self._pressure)

    def get_winddir(self):
        return(self._winddir)

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