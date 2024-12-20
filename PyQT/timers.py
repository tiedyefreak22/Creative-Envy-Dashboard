import sys
from PIL import Image
Image.CUBIC = Image.BICUBIC
from functions_and_classes import *
import pyicloud_get
import settings
import time
from scipy.stats import zscore
from math import ceil

# class Timers(Tk):
#     def __init__(self, *args, **kwargs):
#         #Tk.__init__(self, *args, **kwargs)
#         self.daily_updater()
#         self.hourly_updater()
#         self.five_min_updater()

#     def daily_updater(self):
#         GET_MOON_IMAGE()
#         if settings.pyicloud:
#             PYICLOUD_GET.cycle_files()
#             PYICLOUD_GET.download()
#         self.after(86400000, self.daily_updater)
    
#     def hourly_updater(self):
#         GET_FORECAST()
#         self.after(3600000, self.hourly_updater)
    
#     def five_min_updater(self):
#         for hive_name, hive_ID in settings.hive_IDs.items():
#             BROODMINDER_GET(hive_name, hive_ID)
#         AMBIENT_GET()
#         self.after(300000, self.five_min_updater)