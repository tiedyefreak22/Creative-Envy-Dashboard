import ssl
import requests
import time as t
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import pandas as pd
from glob import glob
import numpy as np
from scipy.interpolate import CubicSpline, UnivariateSpline, InterpolatedUnivariateSpline, interp1d, splrep
import re
from math import floor
import matplotlib.pyplot as plt

def BROODMINDER_GET(hive_name):
    #Login to Broodminder, Get Beehive data, and format
    directory = "Broodminder/"        
    options = Options()
    options.add_experimental_option("prefs", {
      "download.default_directory": r"C:\Users\khard\OneDrive\Documents\GitHub\Creative-Envy-Dashboard\Broodminder",
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "safebrowsing.enabled": True,
      "profile.default_content_setting_values.automatic_downloads": 1,
    })
    options.add_argument('--headless=new')
    
    s = Service(str('./chromedriver.exe'))
    driver = webdriver.Chrome(service=s, options=options)

    ssl._create_default_https_context = ssl._create_unverified_context

    username = 'olivine8910@gmail.com'
    password = 'nujtab-7bebfo-baTweh'

    session = requests.session()
    URL = 'https://mybroodminder.com/login'
    driver.get(URL)
    t.sleep(5)

    # find username/email field and send the username itself to the input field
    driver.find_element(by=By.NAME, value="email").send_keys(username)

    # find password input field and insert password as well
    driver.find_element(by=By.NAME, value="password").send_keys(password)

    # click login button
    driver.find_element(by=By.XPATH, value="/html/body/app-root/app-default/div/app-login/div/mat-tab-group/div/mat-tab-body[1]/div/div/mat-card/form/div/button").click()

    t.sleep(3)

    # download left hive data
    URL = 'https://mybroodminder.com/app/dashboard/hives?hiveIds=6b5cb8b012cb45038eacc24770a2fff7&weaIds=37a0763f69e04c2c823013928e067d68'
    driver.get(URL)
    t.sleep(3)
    driver.find_element(by=By.XPATH, value="/html/body/app-root/app-core/mat-sidenav-container/mat-sidenav-content/div/div/app-hives-dashboard/div[2]/div[2]/mat-icon").click()
    t.sleep(1)
    driver.find_element(by=By.XPATH, value="/html/body/div[3]/div[2]/div/div/div/button[4]/span").click()
    t.sleep(1)
    driver.find_element(by=By.XPATH, value="/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/div/div[2]/div[2]/mat-checkbox/div/div/input").click()
    t.sleep(1)
    driver.find_element(by=By.XPATH, value="/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/div/div[2]/div[3]/mat-checkbox/div/div/input").click()
    t.sleep(1)
    driver.find_element(by=By.XPATH, value="/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/div/div[2]/div[4]/button/span[2]").click()
    t.sleep(3)

    # close the browser window
    driver.quit()
    
    READ_HIVE(hive_name)
    READ_BEE_WEATHER()

def READ_HIVE(hive_name: str):
    directory = "Broodminder/"
    
    # Check for new download data
    Hive = pd.DataFrame()
    filename = ""
    for test_str in os.listdir(directory):
        regex = str(hive_name) + r"_combined_readings_20[a-zA-Z0-9\-\_\.]*.csv"
        matches = re.finditer(regex, test_str, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            filename = directory + match.group()

    # Load master file
    if filename:
        Hive = pd.read_csv(filename)
        Hive.drop('App', axis=1, inplace=True)
        Hive.drop('Record_Type', axis=1, inplace=True)
        Hive.drop('Radar', axis=1, inplace=True)
        Hive.drop('UTC_TimeStamp', axis=1, inplace=True)
        Hive.drop('Local_TimeStamp', axis=1, inplace=True)
        Hive.drop('Metric', axis=1, inplace=True)
        Hive.drop('Audio', axis=1, inplace=True)
        
        if os.path.exists(str(directory + str(hive_name) + " Master.csv")):
            Hive_master = pd.read_csv(str(directory + str(hive_name) + " Master.csv"))
            Hive_master = pd.concat([Hive, Hive_master]).astype(str).drop_duplicates(subset=['Unix_Time'], keep='last').reset_index(drop=True)
        else:
            Hive_master = Hive

        Hive_master.to_csv(directory + hive_name + " Master.csv", mode='w', index=False, header=True)
        os.remove(filename)
    elif os.path.exists(str(directory + str(hive_name) + " Master.csv")):
        Hive_master = pd.read_csv(str(directory + str(hive_name) + " Master.csv"))
        
    return Hive_master

def READ_BEE_WEATHER():
    directory = "Broodminder/"
    
    # Check for new download data
    Bee_Weather = pd.DataFrame()
    filename = ""
    for test_str in os.listdir(directory):
        regex = r"KevBec Apiary_weather_20[a-zA-Z0-9\-\_\.]*.csv"
        matches = re.finditer(regex, test_str, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            filename = directory + match.group()
    
    # Load master file
    if filename:
        Bee_Weather = pd.read_csv(filename)
        Bee_Weather.drop('DownloadTimeStamp', axis=1, inplace=True)
        Bee_Weather.drop('UTC_TimeStamp', axis=1, inplace=True)
        Bee_Weather.drop('Local_TimeStamp', axis=1, inplace=True)
        Bee_Weather.drop('Metric', axis=1, inplace=True)
        
        if os.path.exists(directory + "KevBec Apiary_weather Master.csv"):
            Bee_Weather_master = pd.read_csv(directory + "KevBec Apiary_weather Master.csv")        
            Bee_Weather_master = pd.concat([Bee_Weather, Bee_Weather_master]).astype(str).drop_duplicates(subset=['Unix_Time'], keep='last').reset_index(drop=True)
        else:
            Bee_Weather_master = Bee_Weather
            
        Bee_Weather.to_csv(directory + "KevBec Apiary_weather Master.csv", mode='w', index=False, header=True)
        os.remove(filename)
    elif os.path.exists(directory + "KevBec Apiary_weather Master.csv"):
         Bee_Weather_master = pd.read_csv(directory + "KevBec Apiary_weather Master.csv")
    return Bee_Weather_master

def PROCESS_HIVE(hive_name: str, interp=0):
    directory = "Broodminder/"
    metrics = ["Weight", "Humidity", "Temperature"]
    Hive = READ_HIVE(hive_name)
    Unique_Dev_Names = Hive.Hive_Position.unique()
    Unique_Devs = Hive.Device.unique()
    Devices = {}
    span = 3600
    intervals = int(604800 / span)

    for i, Device in enumerate(Unique_Devs):
        Devices.update({Unique_Dev_Names[i]: Hive[Hive['Device'] == Device]})
    
    Week_Devices = {}
    for i in range(len(Devices)):
        Week_Devices[list(Devices.keys())[i]] = Devices[list(Devices.keys())[i]]

    for i, key in enumerate(list(Week_Devices.keys())):
        for j, cat in enumerate(Week_Devices[str(key)]):
            if Week_Devices[str(key)][str(cat)].isnull().all():
                Week_Devices[str(key)] = Week_Devices[str(key)].drop(columns=[str(cat)])
    for i, key in enumerate(list(Week_Devices.keys())):
        Week_Devices[str(key)] = Week_Devices[str(key)].sort_values(by=["Unix_Time"])
        int_Unix = [int(i) for i in Week_Devices[str(key)]["Unix_Time"]]
        Week_Devices[str(key)] = Week_Devices[str(key)].loc[Week_Devices[str(key)][Week_Devices[str(key)]["Unix_Time"] >= max(int_Unix) - 604800].index[0]:]
    if interp:
        Interps = dict.fromkeys(list(Week_Devices.keys()))
        for i, key in enumerate(list(Week_Devices.keys())):
            Temp_DF = pd.DataFrame()
            for j, cat in enumerate(list(Week_Devices[str(key)].keys())):
                Temp_Dict = {}
                if not str(cat) == "Device" and not str(cat) == "Hive_Position" and not str(cat) == "Unix_Time" and not str(cat) == "Sample":
                    x = [int(i) for i in Week_Devices[str(key)]["Unix_Time"].tolist()]
                    y = Week_Devices[str(key)][str(cat)]
                    if not np.shape(x)[0] == 0:
                        cs = UnivariateSpline(x, y, k=5)
                        xs = np.arange(min(x), max(x), span)
                        Temp_Dict = {"Unix_Time": xs, str('Interp_' + str(cat)): cs(xs)}
                Temp_DF = pd.concat([Temp_DF, pd.DataFrame(Temp_Dict)], axis=0, join='outer')
            Interps[str(key)] = Temp_DF
        return Interps
    else:
        return Week_Devices

def PROCESS_BEE_WEATHER(interp=0):
    directory = "Broodminder/"
    Bee_Weather = READ_BEE_WEATHER()
    metrics = [i for i in list(Bee_Weather.keys()) if not "Unix_Time" in i]
    metric_num = len(metrics)
    span = 3600
    intervals = int(604800 / span)
    Interps = pd.DataFrame()
    
    for i, metric in enumerate(metrics):
        Bee_Weather = Bee_Weather.sort_values(by=["Unix_Time"])
    Week_Devices = pd.DataFrame()
    for i in range(len(Bee_Weather.keys())):
        Week_Devices[list(Bee_Weather.keys())[i]] = Bee_Weather[list(Bee_Weather.keys())[i]]

    for j, cat in enumerate(Week_Devices):
        if Week_Devices[str(cat)].isnull().all():
            Week_Devices = Week_Devices.drop(columns=[str(cat)])
    Week_Devices = Week_Devices.sort_values(by=["Unix_Time"])
    int_Unix = [int(i) for i in Week_Devices["Unix_Time"]]
    Week_Devices = Week_Devices.loc[Week_Devices[Week_Devices["Unix_Time"] >= max(int_Unix) - 604800].index[0]:]
    if interp:
        Interps = dict.fromkeys(list(Week_Devices.keys()))
        Temp_DF = pd.DataFrame()
        for j, cat in enumerate(list(Week_Devices.keys())):
            Temp_Dict = {}
            if not str(cat) == "Device" and not str(cat) == "Hive_Position" and not str(cat) == "Unix_Time" and not str(cat) == "Sample":
                x = [int(i) for i in Week_Devices["Unix_Time"].tolist()]
                y = Week_Devices[str(cat)]
                if not np.shape(x)[0] == 0:
                    cs = UnivariateSpline(x, y, k=5)
                    xs = np.arange(min(x), max(x), span)
                    Temp_Dict = {"Unix_Time": xs, str('Interp_' + str(cat)): cs(xs)}
            Temp_DF = pd.concat([Temp_DF, pd.DataFrame(Temp_Dict)], axis=0, join='outer')
        Interps = Temp_DF
        return Interps
    else:
        return Week_Devices
            
            
#             #Resample and spline-interpolate to five minutes
#             x = []
#             y = []
#             for j, value in enumerate(Bee_Weather[str(metric)]):
#                 if not np.isnan(value):
#                     x.append(int(Bee_Weather["Unix_Time"].tolist()[j]))
#                     y.append(value)

#             if not np.shape(x)[0] == 0:
#                 Temp_DF = pd.DataFrame()
#                 cs = UnivariateSpline(x, y, k=5)
#                 xs = np.arange(min(x), max(x), 300)
#                 Temp_DF["Unix_Time"] = xs
#                 Temp_DF[str('Interp_' + metric)] = cs(xs)
#                 if i == 0:
#                     Interps = Temp_DF
#                 else:
#                     Interps = pd.concat([Temp_DF, Interps], axis=0, join='outer')
#                 Interps = Bee_Weather.sort_values(by=["Unix_Time"])
#             return Interps.iloc[-intervals:]
#         else:
#             return Bee_Weather.iloc[-intervals:]

def AMBIENT_GET():
    # Get Ambient data via URL and format
    from datetime import date
    from datetime import datetime
    from datetime import timedelta
    import urllib.request
    import ssl
    import re
    import array
    import time as t
    import csv
    from csv import writer
    import numpy as np
    import itertools
    import pandas as pd
    from glob import glob
    from send2trash import send2trash

    # csv file name
    filename = "Ambient/Ambient_Data.csv"

    ssl._create_default_https_context = ssl._create_unverified_context

    # Define weather station data
    AMBIENT_ENDPOINT = "https://api.ambientweather.net/v1"
    AMBIENT_API_KEY = "a6ed012c794e4d8283cb2475e187daaffb847bc9d13d4e13a90d5b4c2e11c98a"
    AMBIENT_APPLICATION_KEY = "d34a5337cdbe460a8624135e6661bdb4bd810a078dc84f47b07c0170bc867eec"
    AMBIENT_MAC = "00:0E:C6:30:1F:CC"

    # Initialize titles and rows list
    fields = []
    rows = []

    # Read in current csv values
    rows = pd.read_csv(filename)
    fields = rows.columns

    AMBIENT_START_DATE = datetime.fromtimestamp(int(rows['dateutc'][len(rows['dateutc'])-1]))

    # Determine number of days since beginning of record
    dateDelta = datetime.today() - AMBIENT_START_DATE

    newrows = []
    i = 0
    # Iterate through each day of data
    for i in range(dateDelta.days + 1):
        # Fetch data from Ambient
        AMBIENT_DATE = AMBIENT_START_DATE + timedelta(days=i)
        AMBIENT_DATE = str(AMBIENT_DATE)
        AMBIENT_DATE = AMBIENT_DATE[:AMBIENT_DATE.rindex(" ")]
        while True:
            try:
                request = urllib.request.urlopen('https://rt.ambientweather.net/v1/devices/{}?apiKey={}&applicationKey={}&endDate={}'.format(AMBIENT_MAC,AMBIENT_API_KEY,AMBIENT_APPLICATION_KEY,AMBIENT_DATE))
        # Wait for 1 second to comply with Ambient server limits
                t.sleep(1)
                break
            except:
                continue

        Data = (request.read()).decode('utf-8')

        # Get rid of brackets
        replaceData = Data.replace('[','')
        replaceData = replaceData.replace(']','')

        compiled = re.compile('("time":)[0-9]*,')
        replaceData = compiled.sub('',replaceData)
        compiled = re.compile('("batt)[0-9](":)[a-zA-Z0-9_\/]*,')
        replaceData = compiled.sub('',replaceData)
        compiled = re.compile('("passkey":")[a-zA-Z0-9_\/"]*,')
        replaceData = compiled.sub('',replaceData)
        compiled = re.compile('("loc":")[a-zA-Z0-9_\/]*(\.json",)')
        replaceData = compiled.sub('',replaceData)
        compiled = re.compile(',("date":")[a-zA-Z0-9_\/\:\.\-]*(")')
        replaceData = compiled.sub('',replaceData)
        compiled = re.compile('("temp1f":)[a-zA-Z0-9_\/\:\.\-]*(,)')
        replaceData = compiled.sub('',replaceData)
        compiled = re.compile('("battout":)[a-zA-Z0-9_\/]*,')
        replaceData = compiled.sub('',replaceData)

        # Chop data frames between curly braces
        dataCriteria = re.compile('\{[^\{\}]*\}')
        dataSets = re.findall(dataCriteria,replaceData)
        x = 0
        for x in dataSets:
            temp = x.replace('{','')
            temp = temp.replace('}','')
            temp = temp.replace('"dateutc":','')
            temp = temp.replace('"winddir":','')
            temp = temp.replace('"windspeedmph":','')
            temp = temp.replace('"windgustmph":','')
            temp = temp.replace('"maxdailygust":','')
            temp = temp.replace('"tempf":','')
            temp = temp.replace('"humidity":','')
            temp = temp.replace('"hourlyrainin":','')
            temp = temp.replace('"eventrainin":','')
            temp = temp.replace('"dailyrainin":','')
            temp = temp.replace('"weeklyrainin":','')
            temp = temp.replace('"monthlyrainin":','')
            temp = temp.replace('"yearlyrainin":','')
            temp = temp.replace('"totalrainin":','')
            temp = temp.replace('"uv":','')
            temp = temp.replace('"solarradiation":','')
            temp = temp.replace('"feelsLike":','')
            temp = temp.replace('"dewPoint":','')
            temp = temp.replace('"lastRain":','')
            temp = temp.replace('"','')
            temp = temp.split(',')
            newrows.append(temp)

        i = i + 1

    # Sort and append new data
    df_updated = pd.DataFrame(columns=fields, data=newrows)
    df_updated['dateutc'] = (df_updated['dateutc'].astype(np.int64) / 1000.0)
    sorted_df = df_updated.sort_values('dateutc', axis=0, ascending=True, kind='mergesort')

    new_entries = pd.concat([rows,sorted_df]).astype(str).drop_duplicates(subset=['dateutc'], keep='last').reset_index(drop=True)
    new_entries.to_csv(filename, mode='w', index=False, header=True)

def PROCESS_AMBIENT(interp=0):
    filename = "Ambient/Ambient_Data.csv"
    Ambient = pd.read_csv(filename)

    metrics = [i for i in list(Ambient.keys()) if not "dateutc" in i]
    metric_num = len(metrics)

    # Ambient["dateutc"] = [int(i) for i in Ambient["dateutc"]]
    # Ambient["winddir"] = [int(i) for i in Ambient["winddir"]]
    # Ambient["windspeedmph"] = [float(i) for i in Ambient["windspeedmph"]]
    # Ambient["windgustmph"] = [float(i) for i in Ambient["windgustmph"]]
    # Ambient["maxdailygust"] = [float(i) for i in Ambient["maxdailygust"]]
    # Ambient["tempf"] = [float(i) for i in Ambient["tempf"]]
    # Ambient["humidity"] = [int(i) for i in Ambient["humidity"]]
    # Ambient["hourlyrainin"] = [float(i) for i in Ambient["hourlyrainin"]]
    # Ambient["eventrainin"] = [float(i) for i in Ambient["eventrainin"]]
    # Ambient["dailyrainin"] = [float(i) for i in Ambient["dailyrainin"]]
    # Ambient["weeklyrainin"] = [float(i) for i in Ambient["weeklyrainin"]]
    # Ambient["monthlyrainin"] = [float(i) for i in Ambient["monthlyrainin"]]
    # Ambient["yearlyrainin"] = [float(i) for i in Ambient["yearlyrainin"]]
    # Ambient["totalrainin"] = [float(i) for i in Ambient["totalrainin"]]
    # Ambient["uv"] = [int(i) for i in Ambient["uv"]]
    # Ambient["solarradiation"] = [float(i) for i in Ambient["solarradiation"]]
    # Ambient["feelsLike"] = [float(i) for i in Ambient["feelsLike"]]
    # Ambient["dewPoint"] = [float(i) for i in Ambient["dewPoint"]]
    # Ambient["lastRain"] = [str(i) for i in Ambient["lastRain"]]
    span = 300
    intervals = int(604800 / span)
    Interps = pd.DataFrame()
    for i, metric in enumerate(metrics):
        Ambient = Ambient.sort_values(by=["dateutc"])
        
    Week_Devices = pd.DataFrame()
    for i in range(len(Ambient.keys())):
        Week_Devices[list(Ambient.keys())[i]] = Ambient[list(Ambient.keys())[i]]

    for j, cat in enumerate(Week_Devices):
        if Week_Devices[str(cat)].isnull().all():
            Week_Devices = Week_Devices.drop(columns=[str(cat)])
    Week_Devices = Week_Devices.sort_values(by=["Unix_Time"])
    int_Unix = [int(i) for i in Week_Devices["Unix_Time"]]
    Week_Devices = Week_Devices.loc[Week_Devices[Week_Devices["Unix_Time"] >= max(int_Unix) - 604800].index[0]:]
    if interp:
        Interps = dict.fromkeys(list(Week_Devices.keys()))
        Temp_DF = pd.DataFrame()
        for j, cat in enumerate(list(Week_Devices.keys())):
            Temp_Dict = {}
            if not str(cat) == "Device" and not str(cat) == "Hive_Position" and not str(cat) == "Unix_Time" and not str(cat) == "Sample":
                x = [int(i) for i in Week_Devices["Unix_Time"].tolist()]
                y = Week_Devices[str(cat)]
                if not np.shape(x)[0] == 0:
                    cs = UnivariateSpline(x, y, k=5)
                    xs = np.arange(min(x), max(x), span)
                    Temp_Dict = {"Unix_Time": xs, str('Interp_' + str(cat)): cs(xs)}
            Temp_DF = pd.concat([Temp_DF, pd.DataFrame(Temp_Dict)], axis=0, join='outer')
        Interps = Temp_DF
        return Interps
    else:
        return Week_Devices

def GRAPH_DATA(Data): #Pandas DF
    metrics = [i for i in list(Data.keys()) if not i == "dateutc" and not i == "lastRain" and not i == "Unix_Time" and not i == "Sample" and not i == "w1" and not i == "w2" and not i == "w3" and not i == "w4"]
    metric_num = len(metrics)

    ncols = 4
    nrows = metric_num // ncols + (metric_num % ncols > 0)
    plt.figure(figsize=(15, 4*nrows))
    plt.subplots_adjust(hspace=0.2)

    for i, match in enumerate(metrics):
        try:
            ax = plt.subplot(nrows, ncols, i + 1)
            Data[str(match)].plot(ax=ax)
            ax.set_title(str(match))
        except:
            pass
    plt.show()
    
# if __name__ == '__main__':
#     BROODMINDER_GET()
#     AMBIENT_GET()