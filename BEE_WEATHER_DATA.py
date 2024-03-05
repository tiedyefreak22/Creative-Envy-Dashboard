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
from scipy.interpolate import CubicSpline, UnivariateSpline

def BROODMINDER_GET():
    #Login to Broodminder, Get Beehive data, and format
    # path arg is path to chromedriver.exe
    #s = Service('/Users/kevinhardin/PythonScripts/chromedriver')
    #s = Service(str(path))
    
    directory = "Broodminder/"
    try:
        files = os.listdir(directory)
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except OSError:
        print("Error")
        
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
    #driver.find_element(by=By.XPATH, value="/html/body/app-root/app-default/div/app-login/div/mat-tab-group/div/mat-tab-body[1]/div/div/mat-card/form/div/button/span").click()
    driver.find_element(by=By.XPATH, value="/html/body/app-root/app-default/div/app-login/div/mat-tab-group/div/mat-tab-body[1]/div/div/mat-card/form/div/button").click()

    t.sleep(3)

    # download left hive data
    # URL = 'https://mybroodminder.com/app/hive/4c146db0cb534e1d8d56f8e4c7b49c0d?start=1648872000&range=9'
    URL = 'https://mybroodminder.com/app/dashboard/hives?hiveIds=6b5cb8b012cb45038eacc24770a2fff7&weaIds=37a0763f69e04c2c823013928e067d68'
    driver.get(URL)
    t.sleep(3)
    driver.find_element(by=By.XPATH, value="/html/body/app-root/app-core/mat-sidenav-container/mat-sidenav-content/div/div/app-hives-dashboard/div[2]/div[2]/mat-icon").click()
    t.sleep(1)
    # driver.find_element(by=By.XPATH, value="/html/body/app-root/app-core/mat-sidenav-container/mat-sidenav-content/div/div/app-hives-dashboard/div[2]/div[2]/mat-icon").click()
    # t.sleep(1)
    driver.find_element(by=By.XPATH, value="/html/body/div[3]/div[2]/div/div/div/button[4]/span").click()
    t.sleep(1)
    driver.find_element(by=By.XPATH, value="/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/div/div[2]/div[2]/mat-checkbox/div/div/input").click()
    t.sleep(1)
    driver.find_element(by=By.XPATH, value="/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/div/div[2]/div[3]/mat-checkbox/div/div/input").click()
    t.sleep(1)
    driver.find_element(by=By.XPATH, value="/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/div/div[2]/div[4]/button/span[2]").click()
    t.sleep(3)
    
    # # download weather data for both
    # driver.find_element(by=By.XPATH, value="/html/body/app-root/app-core/mat-sidenav-container/mat-sidenav-content/div/div/app-hive-landing/div[3]/button[2]/span").click()
    # t.sleep(1)

    # # download right hive data
    # URL = "https://mybroodminder.com/app/hive/74ab0c07e39e429a929c9a5a6ac86392?start=1648872000&&range=9"
    # driver.get(URL)
    # t.sleep(5)
    # driver.find_element(by=By.XPATH, value="/html/body/app-root/app-core/mat-sidenav-container/mat-sidenav-content/div/div/app-hive-landing/div[3]/button[1]/span").click()
    # t.sleep(1)

    # close the browser window
    driver.quit()

def READ_HIVE(hive_name):
    directory = "Broodminder/"
    
    # Check for new download data
    Hive = pd.DataFrame()
    res = [f for f in glob(directory + "*.csv") if hive_name in f and "Master" not in f]
    filename = ""
    for f in res:
        filename = f
        Hive = pd.read_csv(f)
        Hive.drop('App', axis=1, inplace=True)
        Hive.drop('Record_Type', axis=1, inplace=True)
        Hive.drop('Radar', axis=1, inplace=True)
        Hive.drop('UTC_TimeStamp', axis=1, inplace=True)
        Hive.drop('Local_TimeStamp', axis=1, inplace=True)
        Hive.drop('Metric', axis=1, inplace=True)
        Hive.drop('Audio', axis=1, inplace=True)
        #Hive.to_csv(directory + hive_name + " Master.csv", mode='w', index=False, header=True)

    # Load master file
    Hive_master = pd.read_csv(directory + hive_name + " Master.csv")
    if not res == []:
        new_Hive_master = pd.concat([Hive, Hive_master]).astype(str).drop_duplicates(subset=['Unix_Time'], keep='last').reset_index(drop=True)
        new_Hive_master.to_csv(directory + hive_name + " Master.csv", mode='w', index=False, header=True)
        #os.remove(filename)
    Hive_master = pd.read_csv(directory + hive_name + " Master.csv")
    return Hive_master

def READ_BEE_WEATHER():
    directory = "Broodminder/"
    
    # Check for new download data
    Bee_Weather = pd.DataFrame()
    res = [f for f in glob(directory + "*.csv") if "KevBec Apiary_weather" in f and "Master" not in f]
    filename = ""
    for f in res:
        filename = f
        Bee_Weather = pd.read_csv(f)
        Bee_Weather.drop('DownloadTimeStamp', axis=1, inplace=True)
        Bee_Weather.drop('UTC_TimeStamp', axis=1, inplace=True)
        Bee_Weather.drop('Local_TimeStamp', axis=1, inplace=True)
        Bee_Weather.drop('Metric', axis=1, inplace=True)
        #Bee_Weather.to_csv(directory + "KevBec Apiary_weather" + " Master.csv", mode='w', index=False, header=True)

    # Load master file
    Bee_Weather_master = pd.read_csv(directory + "KevBec Apiary_weather" + " Master.csv")
    if not res == []:
        new_Bee_Weather_master = pd.concat([Bee_Weather, Bee_Weather_master]).astype(str).drop_duplicates(subset=['Unix_Time'], keep='last').reset_index(drop=True)
        new_Bee_Weather_master.to_csv(directory + "KevBec Apiary_weather" + " Master.csv", mode='w', index=False, header=True)
        #os.remove(filename)
    Bee_Weather_master = pd.read_csv(directory + "KevBec Apiary_weather" + " Master.csv")
    return Bee_Weather_master

def PROCESS_HIVE(hive_name):
    metrics = ["Weight", "Humidity", "Temperature"]
    Hive = READ_HIVE(hive_name)
    Unique_Dev_Names = Hive.Hive_Position.unique()
    Unique_Devs = Hive.Device.unique()
    Devices = {}
    Graph = 0
    for i, Device in enumerate(Unique_Devs):
        Devices.update({Unique_Dev_Names[i]: Hive[Hive['Device'] == Device]})
    
    if Graph:
        fig, ax = plt.subplots(1, 3, figsize=(30, 5))
    for j, metric in enumerate(metrics):
        for i, Device in enumerate(Unique_Devs):
            Devices[list(Devices.keys())[i]] = Devices[list(Devices.keys())[i]].sort_values(by=["Unix_Time"])
            # Resample and cubic-spline-interpolate to five minutes
            x = []
            y = []
            for k, value in enumerate(Devices[list(Devices.keys())[i]][str(metrics[j])]):
                if not np.isnan(value):
                    x.append(int(Devices[list(Devices.keys())[i]]["Unix_Time"].tolist()[k]))
                    y.append(value)
                    
            if not np.shape(x)[0] == 0:
                Temp_DF = pd.DataFrame()
                cs = UnivariateSpline(x, y)
                xs = np.arange(min(x), max(x), 300)
                Temp_DF["Unix_Time"] = xs
                Temp_DF[str('Interp_' + metrics[j])] = cs(xs)
                Devices[list(Devices.keys())[i]] = pd.concat([Temp_DF, Devices[list(Devices.keys())[i]]], axis=0, join='outer')
                Devices[list(Devices.keys())[i]] = Devices[list(Devices.keys())[i]].sort_values(by=["Unix_Time"])
                
                if Graph:
                    ax[j].plot(Devices[list(Devices.keys())[i]]["Unix_Time"], Devices[list(Devices.keys())[i]][str("Interp_" + metrics[j])], label=str(Unique_Dev_Names[i] + ' ' + metrics[j]))
                    ax[j].legend(loc='lower left', ncol=2)
    
    return Devices

def PROCESS_BEE_WEATHER():
    Bee_Weather = READ_BEE_WEATHER()
    metrics = [i for i in list(Bee_Weather.keys()) if not "Unix_Time" in i]
    Graph = 0
    rows = 2
    cols = 4
    
    if Graph:
        fig, ax = plt.subplots(rows, cols, figsize=(30, 10))
    for i, metric in enumerate(metrics):
        Bee_Weather = Bee_Weather.sort_values(by=["Unix_Time"])
        # Resample and cubic-spline-interpolate to five minutes
        x = []
        y = []
        for j, value in enumerate(Bee_Weather[str(metric)]):
            if not np.isnan(value):
                x.append(int(Bee_Weather["Unix_Time"].tolist()[j]))
                y.append(value)

        if not np.shape(x)[0] == 0:
            Temp_DF = pd.DataFrame()
            cs = UnivariateSpline(x, y)
            xs = np.arange(min(x), max(x), 300)
            Temp_DF["Unix_Time"] = xs
            Temp_DF[str('Interp_' + metric)] = cs(xs)
            Bee_Weather = pd.concat([Temp_DF, Bee_Weather], axis=0, join='outer')
            Bee_Weather = Bee_Weather.sort_values(by=["Unix_Time"])
            
            if Graph:
                ax[floor(i/cols), i % cols].plot(Bee_Weather["Unix_Time"], Bee_Weather[str("Interp_" + metrics[i])], label=str(metrics[i]))
                ax[floor(i/cols), i % cols].legend(loc='lower left', ncol=2)

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

    AMBIENT = pd.read_csv(filename)

    # AMBIENT resampled and interpolated to five minutes
    AMBIENT['dateutc'] = AMBIENT['dateutc'].astype('int64')
    AMBIENT['dateutc'] = pd.to_datetime(AMBIENT['dateutc'], unit='s', origin='unix')
    
    AMBIENT = AMBIENT.set_index('dateutc',drop = True)
    AMBIENT_upsampled = AMBIENT.resample('60s').mean()
    AMBIENT_interpolated = AMBIENT_upsampled[AMBIENT_upsampled.columns[0::]].interpolate(method='linear')
    AMBIENT_downsampled = AMBIENT_interpolated.resample('300s').mean()
    AMBIENT_downsampled.loc[(AMBIENT_downsampled.winddir > 180), 'winddir'] = AMBIENT_downsampled['winddir'] - 360

    #return(AMBIENT_downsampled)

# if __name__ == '__main__':
#     BROODMINDER_GET()
#     AMBIENT_GET()