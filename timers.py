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
from scipy.stats import zscore
from math import ceil

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

def nanzscore(df):
    return [(i - np.nanmean(df))/np.nanstd(df) for i in df]

def ret_prop(df, interp, remove_outliers, num_days):
    if remove_outliers:
        threshold_z = 2
        chunk = 50
        if isinstance(df, pd.Series):
            for idx in range(len(df.values)):
                if (idx >= ceil(chunk / 2)) and (idx <= len(df.values) - ceil(chunk / 2)):
                    z = nanzscore(df.values[idx - ceil(chunk / 2):idx + ceil(chunk / 2)])
                    if abs(z[ceil(chunk / 2) - 1]) > threshold_z:
                        df.iloc[idx - 1] = np.nan
                else:
                    pass
        else:
            pass
    if interp:
        df = df.resample('10s').interpolate(method = "time", limit_direction='both')
    if num_days:
        df = df[df.index >= (max(df.index) - timedelta(days = num_days))]
    return df

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

    def get_ambient(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._ambient_df, interp, remove_outliers, num_days)
        
    def set(self):
        df = PROCESS_AMBIENT()
        df.index = pd.to_datetime(df.index, unit = 's')
        self.ambient = df

    def get_winddir(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._winddir, interp, remove_outliers, num_days)

    def get_windspeedmph(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._windspeedmph, interp, remove_outliers, num_days)

    def get_windgustmph(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._windgustmph, interp, remove_outliers, num_days)

    def get_maxdailygust(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._maxdailygust, interp, remove_outliers, num_days)

    def get_tempf(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._tempf, interp, remove_outliers, num_days)

    def get_humidity(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._humidity, interp, remove_outliers, num_days)

    def get_hourlyrainin(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._hourlyrainin, interp, remove_outliers, num_days)

    def get_eventrainin(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._eventrainin, interp, remove_outliers, num_days)

    def get_dailyrainin(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._dailyrainin, interp, remove_outliers, num_days)

    def get_weeklyrainin(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._weeklyrainin, interp, remove_outliers, num_days)

    def get_monthlyrainin(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._monthlyrainin, interp, remove_outliers, num_days)

    def get_yearlyrainin(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._yearlyrainin, interp, remove_outliers, num_days)

    def get_totalrainin(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._totalrainin, interp, remove_outliers, num_days)

    def get_uv(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._uv, interp, remove_outliers, num_days)

    def get_solarradiation(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._solarradiation, interp, remove_outliers, num_days)

    def get_feelsLike(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._feelsLike, interp, remove_outliers, num_days)

    def get_dewPoint(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._dewPoint, interp, remove_outliers, num_days)

    def get_lastRain(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._lastRain, interp, remove_outliers, num_days)


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

    def get_beeweather(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._beeweather_df, interp, remove_outliers, num_days)

    def set(self):
        df = PROCESS_BEE_WEATHER()
        df.index = pd.to_datetime(df.index, unit = 's')
        self.beeweather = df
    
    def get_temp(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._temp, interp, remove_outliers, num_days)

    def get_rain_in(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._rain_in, interp, remove_outliers, num_days)

    def get_humidity(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._humidity, interp, remove_outliers, num_days)

    def get_cloud_cover(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._cloud_cover, interp, remove_outliers, num_days)

    def get_windspeed10m_mph(self, interp = 0, remove_outliers = 0, num_days = None):
         return ret_prop(self._windspeed10m_mph, interp, remove_outliers, num_days)

    def get_pressure(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._pressure, interp, remove_outliers, num_days)

    def get_winddir(self, interp = 0, remove_outliers = 0, num_days = None):
        return ret_prop(self._winddir, interp, remove_outliers, num_days)

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

    def get_weight(self, interp = 0, remove_outliers = 0, num_days = None):
        if not self._weight.empty:
            return ret_prop(self._weight["Weight"], interp, remove_outliers, num_days)

    def get_upper_temp(self, interp = 0, remove_outliers = 0, num_days = None):
        if not self._upper_temp.empty:
            return ret_prop(self._upper_temp, interp, remove_outliers, num_days)

    def get_lower_temp(self, interp = 0, remove_outliers = 0, num_days = None):
        if not self._lower_temp.empty:
            return ret_prop(self._lower_temp, interp, remove_outliers, num_days)

    def get_humidity(self, interp = 0, remove_outliers = 0, num_days = None):
        if not self._humid.empty:
            return ret_prop(self._humid["Humidity"], interp, remove_outliers, num_days)