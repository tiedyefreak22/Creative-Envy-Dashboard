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
        elif hasattr(cls, '_allow_reinitialization') and cls._allow_reinitialization:
            # if the class allows reinitialization, then do it
            instance = cls._instances[cls]
            instance.__init__(*args, **kwargs)  # call the init again
        else:
            raise Exception("Singleton cannot be instantiated more than once")
        return instance

class Ambient(metaclass = Singleton):
    _allow_reinitialization = True
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
        self._winddir = ambient_df["winddir"]
        self._windspeedmph = ambient_df["windspeedmph"]
        self._windgustmph = ambient_df["windgustmph"]
        self._maxdailygust = ambient_df["maxdailygust"]
        self._tempf = ambient_df["tempf"]
        self._humidity = ambient_df["humidity"]
        self._hourlyrainin = ambient_df["hourlyrainin"]
        self._eventrainin = ambient_df["eventrainin"]
        self._dailyrainin = ambient_df["dailyrainin"]
        self._weeklyrainin = ambient_df["weeklyrainin"]
        self._monthlyrainin = ambient_df["monthlyrainin"]
        self._yearlyrainin = ambient_df["yearlyrainin"]
        self._totalrainin = ambient_df["totalrainin"]
        self._uv = ambient_df["uv"]
        self._solarradiation = ambient_df["solarradiation"]
        self._feelsLike = ambient_df["feelsLike"]
        self._dewPoint = ambient_df["dewPoint"]
        self._lastRain = ambient_df["lastRain"]

    def get_ambient(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._ambient_df.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._ambient_df
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._ambient_df.resample('5min').interpolate("linear")
            else:
                return self._ambient_df
        
    def set(self):
        df = PROCESS_AMBIENT()
        df.index = pd.to_datetime(df.index, unit = 's')
        self.ambient = df

    def get_winddir(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._winddir.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._winddir
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._winddir.resample('5min').interpolate("linear")
            else:
                return self._winddir

    def get_windspeedmph(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._windspeedmph.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._windspeedmph
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._windspeedmph.resample('5min').interpolate("linear")
            else:
                return self._windspeedmph

    def get_windgustmph(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._windgustmph.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._windgustmph
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._windgustmph.resample('5min').interpolate("linear")
            else:
                return self._windgustmph

    def get_maxdailygust(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._maxdailygust.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._maxdailygust
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._maxdailygust.resample('5min').interpolate("linear")
            else:
                return self._maxdailygust

    def get_tempf(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._tempf.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._tempf
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._tempf.resample('5min').interpolate("linear")
            else:
                return self._tempf

    def get_humidity(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._humidity.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._humidity
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._humidity.resample('5min').interpolate("linear")
            else:
                return self._humidity

    def get_hourlyrainin(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._hourlyrainin.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._hourlyrainin
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._hourlyrainin.resample('5min').interpolate("linear")
            else:
                return self._hourlyrainin

    def get_eventrainin(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._eventrainin.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._eventrainin
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._eventrainin.resample('5min').interpolate("linear")
            else:
                return self._eventrainin

    def get_dailyrainin(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._dailyrainin.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._dailyrainin
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._dailyrainin.resample('5min').interpolate("linear")
            else:
                return self._dailyrainin

    def get_weeklyrainin(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._weeklyrainin.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._weeklyrainin
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._weeklyrainin.resample('5min').interpolate("linear")
            else:
                return self._weeklyrainin

    def get_monthlyrainin(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._monthlyrainin.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._monthlyrainin
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._monthlyrainin.resample('5min').interpolate("linear")
            else:
                return self._monthlyrainin

    def get_yearlyrainin(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._yearlyrainin.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._yearlyrainin
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._yearlyrainin.resample('5min').interpolate("linear")
            else:
                return self._yearlyrainin

    def get_totalrainin(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._totalrainin.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._totalrainin
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._totalrainin.resample('5min').interpolate("linear")
            else:
                return self._totalrainin

    def get_uv(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._uv.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._uv
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._uv.resample('5min').interpolate("linear")
            else:
                return self._uv

    def get_solarradiation(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._solarradiation.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._solarradiation
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._solarradiation.resample('5min').interpolate("linear")
            else:
                return self._solarradiation

    def get_feelsLike(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._feelsLike.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._feelsLike
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._feelsLike.resample('5min').interpolate("linear")
            else:
                return self._feelsLike

    def get_dewPoint(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._dewPoint.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._dewPoint
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._dewPoint.resample('5min').interpolate("linear")
            else:
                return self._dewPoint

    def get_lastRain(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._lastRain.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._lastRain
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._lastRain.resample('5min').interpolate("linear")
            else:
                return self._lastRain

class BeeWeather(metaclass = Singleton):
    _allow_reinitialization = True
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

    def get_beeweather(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._beeweather_df.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._beeweather_df
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._beeweather_df.resample('5min').interpolate("linear")
            else:
                return self._beeweather_df

    def set(self):
        df = PROCESS_BEE_WEATHER()
        df.index = pd.to_datetime(df.index, unit = 's')
        self.beeweather = df

    def get_temp(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._temp.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._temp
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._temp.resample('5min').interpolate("linear")
            else:
                return self._temp

    def get_rain_in(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._rain_in.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._rain_in
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._rain_in.resample('5min').interpolate("linear")
            else:
                return self._rain_in

    def get_humidity(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._humidity.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._humidity
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._humidity.resample('5min').interpolate("linear")
            else:
                return self._humidity

    def get_cloud_cover(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._cloud_cover.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._cloud_cover
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._cloud_cover.resample('5min').interpolate("linear")
            else:
                return self._cloud_cover

    def get_windspeed10m_mph(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._windspeed10m_mph.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._windspeed10m_mph
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._windspeed10m_mph.resample('5min').interpolate("linear")
            else:
                return self._windspeed10m_mph

    def get_pressure(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._pressure.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._pressure
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._pressure.resample('5min').interpolate("linear")
            else:
                return self._pressure

    def get_winddir(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._winddir.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._winddir
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._winddir.resample('5min').interpolate("linear")
            else:
                return self._winddir

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
        
        self._weight = pd.DataFrame(list(gen_dict_extract("Weight", hive_df))).T
        self._weight.index = pd.to_datetime(self._weight.index, unit = 's')
        
        self._upper_temp = hive_df["Upper Brood"]["Temperature"]
        self._upper_temp.index = pd.to_datetime(self._upper_temp.index, unit = 's')
        
        self._lower_temp = hive_df["Lower Brood"]["Temperature"]
        self._lower_temp.index = pd.to_datetime(self._lower_temp.index, unit = 's')
        
        self._humid = pd.concat([s.dropna().reset_index(drop=True) for i, s in pd.DataFrame(list(gen_dict_extract("Humidity", hive_df))).T.iterrows()], axis = 1).T.rename(columns = {0: "Humidity"})        
        self._humid.index.names = ['Unix_Time']
        self._humid.index = pd.to_datetime(self._humid.index, unit = 's')

    def get_hive(self):
        return self._hive_df
    
    def set(self):
        self.hive = PROCESS_HIVE(self.hive_name)
        
    def five_min_updater(self):
        BROODMINDER_GET(self._hive_name, self._hive_ID)
        self.after(300000, self.five_min_updater)
    
    # def get_honey(self, interp = 0):
    #     return(list(gen_dict_extract("Weight", PROCESS_HIVE(self._hive_name))))

    # def get_bees(self, interp = 0):
    #     return(list(gen_dict_extract("Weight", PROCESS_HIVE(self._hive_name))))

    def get_weight(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._weight.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]["Weight"]
            else:
                df = self._weight
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]["Weight"]
        else:
            if interp:
                return self._weight.resample('5min').interpolate("linear")["Weight"]
            else:
                return self._weight["Weight"]

    def get_upper_temp(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._upper_temp.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._upper_temp
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._upper_temp.resample('5min').interpolate("linear")
            else:
                return self._upper_temp

    def get_lower_temp(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._lower_temp.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
            else:
                df = self._lower_temp
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]
        else:
            if interp:
                return self._lower_temp.resample('5min').interpolate("linear")
            else:
                return self._lower_temp
    

    def get_humidity(self, interp = 0, num_days = None):
        if num_days != None:
            if interp:
                df = self._humid.resample('5min').interpolate("linear")
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]["Humidity"]
            else:
                df = self._humid
                return df[df.index >= (max(df.index) - timedelta(days = num_days))]["Humidity"]
        else:
            if interp:
                return self._humid.resample('5min').interpolate("linear")["Humidity"]
            else:
                return self._humid["Humidity"]
