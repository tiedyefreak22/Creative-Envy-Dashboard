import sys
from sys import platform
import aiomultiprocess
import array
import astral, astral.sun
import asyncio
import csv
import dns.resolver
import http.server
import imageio
import io
import itertools
import json
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import multiprocessing as mp
import numpy as np
import os
import pandas as pd
import pytz
import queue
import random
import re
import requests
import socketserver
import ssl
import threading
import time as t
import urllib.request
#from decouple import config
#import pyicloud_get
#import rawpy
from contextlib import closing
from csv import writer
from datetime import date, datetime, timedelta, timezone
from dotenv import load_dotenv
from glob import glob
from io import BytesIO
from IPython.display import display
from math import floor, ceil
from matplotlib.backends.backend_qtagg import \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure
from more_itertools import time_limited
from pathlib import Path
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QTime, pyqtSlot, QSize
from PyQt5.QtGui import QPixmap, QImage, QColor, QFont, QIcon
from scipy.interpolate import CubicSpline, UnivariateSpline, InterpolatedUnivariateSpline, interp1d, splrep, PchipInterpolator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from send2trash import send2trash
from statistics import variance, mean
from threading import Thread, Event
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

global screen_width
global screen_height

def resolve(domain):
    resolveList = []
    resolver = dns.resolver.Resolver(); #create a new instance named Resolver
    answer = resolver.query(domain, "A");
    return answer    

def check_internet_connection():
    domainName = "google.com"
    queryResult = resolve(domainName);
    try:
        urllib.request.urlopen("http://" + str(queryResult[0]), timeout = 3)
        print("Internet connection verified.")
        return True
    except urllib.error.URLError:
        print("Internet connection failed.")
        return False

pyicloud = 0
hive_IDs = {"New Left Hive": '6b5cb8b012cb45038eacc24770a2fff7',
            "Utah OW Nuc Left": '13a71f80590a4184a2956058441c3be3',
            "Utah OW Nuc Right": 'dca02aae55b74ca1b1a6ac35042d2254',
           }

Palettes = {"darkly": {
        "type": "dark",
        "colors": {
            "primary": "#375a7f",
            "secondary": "#444444",
            "success": "#00bc8c",
            "info": "#3498db",
            "warning": "#f39c12",
            "danger": "#e74c3c",
            "light": "#ADB5BD",
            "dark": "#303030",
            "bg": "#222222",
            "fg": "#ffffff",
            "selectbg": "#555555",
            "selectfg": "#ffffff",
            "border": "#222222",
            "inputfg": "#ffffff",
            "inputbg": "#2f2f2f",
        },
    },
}

internet_connection = check_internet_connection()
widget_padding = 10