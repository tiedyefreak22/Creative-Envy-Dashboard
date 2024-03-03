import ssl
import requests
import time as t
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

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

def BROODMINDER_PANDAS():
    NewLeftHive = pd.DataFrame()
    NewHiveWeather = pd.DataFrame()
    NewRightHive = pd.DataFrame()
    OldLeftHive = pd.DataFrame()
    OldHiveWeather = pd.DataFrame()
    OldRightHive = pd.DataFrame()

    filename = "Left Hive_combined_readings_20[a-zA-Z0-9\-\_\.]*.csv"
    for f in glob('/Users/kevinhardin/Downloads/'+filename):
        NewLeftHive = pd.read_csv(f)
        NewLeftHive.drop('App', axis=1, inplace=True)
        NewLeftHive.drop('Record_Type', axis=1, inplace=True)
        NewLeftHive.drop('DownloadTimeStamp', axis=1, inplace=True)
        NewLeftHive.drop('UTC_TimeStamp', axis=1, inplace=True)
        NewLeftHive.drop('Local_TimeStamp', axis=1, inplace=True)
        NewLeftHive.drop('Metric', axis=1, inplace=True)
        NewLeftHive.drop(' WeightLRaw', axis=1, inplace=True)
        NewLeftHive.drop(' WeightRRaw', axis=1, inplace=True)
        NewLeftHive = NewLeftHive[['Unix_Time','Device','Hive_Position','Sample','Battery','Temperature','Humidity','Scaled_Weight',' Weight_Scale_Factor',' Weight',' WeightL',' WeightR']]
        send2trash(f)

    filename = "Left Hive_weather_20[a-zA-Z0-9\-\_\.]*.csv"
    for f in glob('/Users/kevinhardin/Downloads/'+filename):
        NewHiveWeather = pd.read_csv(f)
        NewHiveWeather.drop('DownloadTimeStamp', axis=1, inplace=True)
        NewHiveWeather.drop('UTC_TimeStamp', axis=1, inplace=True)
        NewHiveWeather.drop('Local_TimeStamp', axis=1, inplace=True)
        NewHiveWeather.drop('Metric', axis=1, inplace=True)
        send2trash(f)

    filename = "Right Hive_combined_readings_20[a-zA-Z0-9\-\_\.]*.csv"
    for f in glob('/Users/kevinhardin/Downloads/'+filename):
        NewRightHive = pd.read_csv(f)
        NewRightHive.drop('App', axis=1, inplace=True)
        NewRightHive.drop('Record_Type', axis=1, inplace=True)
        NewRightHive.drop('DownloadTimeStamp', axis=1, inplace=True)
        NewRightHive.drop('UTC_TimeStamp', axis=1, inplace=True)
        NewRightHive.drop('Local_TimeStamp', axis=1, inplace=True)
        NewRightHive.drop('Metric', axis=1, inplace=True)
        NewRightHive.drop(' WeightLRaw', axis=1, inplace=True)
        NewRightHive.drop(' WeightRRaw', axis=1, inplace=True)
        NewRightHive = NewRightHive[['Unix_Time','Device','Hive_Position','Sample','Battery','Temperature','Humidity','Scaled_Weight',' Weight_Scale_Factor',' Weight',' WeightL',' WeightR']]
        send2trash(f)

    for f in glob(filename1):
        OldLeftHive = pd.read_csv(f)
        fields = OldLeftHive.columns
        new_entries = pd.concat([OldLeftHive,NewLeftHive]).astype(str).drop_duplicates(subset=['Unix_Time'], keep='last').reset_index(drop=True)
        new_entries.to_csv(filename1, mode='w', index=False, header=True)

    for f in glob(filename2):
        OldHiveWeather = pd.read_csv(f)
        fields = OldHiveWeather.columns
        new_entries = pd.concat([OldHiveWeather,NewHiveWeather]).astype(str).drop_duplicates(subset=['Unix_Time'], keep='last').reset_index(drop=True)
        new_entries.to_csv(filename2, mode='w', index=False, header=True)

    for f in glob(filename3):
        OldRightHive = pd.read_csv(f)
        fields = OldRightHive.columns
        new_entries = pd.concat([OldRightHive,NewRightHive]).astype(str).drop_duplicates(subset=['Unix_Time'], keep='last').reset_index(drop=True)
        new_entries.to_csv(filename3, mode='w', index=False, header=True)

    LeftHive = pd.read_csv(filename1)
    HiveWeather = pd.read_csv(filename2)
    RightHive = pd.read_csv(filename3)

    # LeftHive resampled and interpolated to five minutes
    LeftHive['Unix_Time'] = LeftHive['Unix_Time'].astype('int64')
    LeftHive['Unix_Time'] = pd.to_datetime(LeftHive['Unix_Time'], unit='s', origin='unix')
    
    # RightHive resampled and interpolated to five minutes
    RightHive['Unix_Time'] = RightHive['Unix_Time'].astype('int64')
    RightHive['Unix_Time'] = pd.to_datetime(RightHive['Unix_Time'], unit='s', origin='unix')
    
    # HiveWeather resampled and interpolated to five minutes
    HiveWeather['Unix_Time'] = HiveWeather['Unix_Time'].astype('int64')
    HiveWeather['Unix_Time'] = pd.to_datetime(HiveWeather['Unix_Time'], unit='s', origin='unix')
    
    RightUpper = RightHive[RightHive['Device'] == '56:0B:D1']
    RightLower = RightHive[RightHive['Device'] == '47:13:0C']
    RightScale = RightHive[RightHive['Device'] == '49:02:8D']
    LeftUpper = LeftHive[LeftHive['Device'] == '56:0B:D0']
    LeftLower = LeftHive[LeftHive['Device'] == '47:13:E4']
    LeftScale = LeftHive[LeftHive['Device'] == '49:02:8C']

    # Should downsampling be "mean" instead of asfreq?  Need to specify and align start date/time? 1652133991

#     # Sort based on device
#     LeftUpper = LeftHive[LeftHive['Device'] == '56:0B:D0']
#     LeftLower = LeftHive[LeftHive['Device'] == '47:13:E4']
#     LeftScale = LeftHive[LeftHive['Device'] == '49:02:8C']

    # LeftUpper resampled and interpolated to five minutes (no weight measurements)
    LeftUpper = LeftUpper.set_index('Unix_Time',drop=False,inplace=False)
    LeftUpper.drop('Device', axis=1, inplace=True)
    LeftUpper.drop('Hive_Position', axis=1, inplace=True)
    LeftUpper.drop('Sample', axis=1, inplace=True)
    LeftUpper.drop('Scaled_Weight', axis=1, inplace=True)
    LeftUpper.drop(' Weight_Scale_Factor', axis=1, inplace=True)
    LeftUpper.drop(' Weight', axis=1, inplace=True)
    LeftUpper.drop(' WeightL', axis=1, inplace=True)
    LeftUpper.drop(' WeightR', axis=1, inplace=True)
    LeftUpper_upsampled = LeftUpper.resample('1s').mean()
    LeftUpper_interpolated = LeftUpper_upsampled[LeftUpper_upsampled.columns[1::]].interpolate(method='linear')
    LeftUpper_downsampled = LeftUpper_interpolated.resample('300s').mean()
    # LeftUpper_downsampled.iloc[:, 0]

    # LeftLower resampled and interpolated to five minutes (no weight or humidity measurements)
    LeftLower = LeftLower.set_index('Unix_Time',drop = False)
    LeftLower.drop('Device', axis=1, inplace=True)
    LeftLower.drop('Hive_Position', axis=1, inplace=True)
    LeftLower.drop('Sample', axis=1, inplace=True)
    LeftLower.drop('Scaled_Weight', axis=1, inplace=True)
    LeftLower.drop(' Weight_Scale_Factor', axis=1, inplace=True)
    LeftLower.drop(' Weight', axis=1, inplace=True)
    LeftLower.drop(' WeightL', axis=1, inplace=True)
    LeftLower.drop(' WeightR', axis=1, inplace=True)
    LeftLower.drop('Humidity', axis=1, inplace=True)
    LeftLower_upsampled = LeftLower.resample('1s').mean()
    LeftLower_interpolated = LeftLower_upsampled[LeftLower_upsampled.columns[1::]].interpolate(method='linear')
    LeftLower_downsampled = LeftLower_interpolated.resample('300s').mean()

     # LeftScale resampled and interpolated to five minutes (no humidity measurements)
    LeftScale = LeftScale.set_index('Unix_Time',drop = False)
    LeftScale.drop('Device', axis=1, inplace=True)
    LeftScale.drop('Hive_Position', axis=1, inplace=True)
    LeftScale.drop('Sample', axis=1, inplace=True)
    LeftScale.drop('Humidity', axis=1, inplace=True)
    LeftScale_upsampled = LeftScale.resample('1s').mean()
    LeftScale_interpolated = LeftScale_upsampled[LeftScale_upsampled.columns[1::]].interpolate(method='linear')
    LeftScale_downsampled = LeftScale_interpolated.resample('300s').mean()
    LeftAvg = LeftScale_downsampled['Scaled_Weight'].resample('1d').mean()

#     RightUpper = RightHive[RightHive['Device'] == '56:0B:D1']
#     RightLower = RightHive[RightHive['Device'] == '47:13:0C']
#     RightScale = RightHive[RightHive['Device'] == '49:02:8D']

    # RightUpper resampled and interpolated to five minutes (no weight measurements)
    RightUpper = RightUpper.set_index('Unix_Time',drop = False)
    RightUpper.drop('Device', axis=1, inplace=True)
    RightUpper.drop('Hive_Position', axis=1, inplace=True)
    RightUpper.drop('Sample', axis=1, inplace=True)
    RightUpper.drop('Scaled_Weight', axis=1, inplace=True)
    RightUpper.drop(' Weight_Scale_Factor', axis=1, inplace=True)
    RightUpper.drop(' Weight', axis=1, inplace=True)
    RightUpper.drop(' WeightL', axis=1, inplace=True)
    RightUpper.drop(' WeightR', axis=1, inplace=True)
    RightUpper_upsampled = RightUpper.resample('1s').mean()
    RightUpper_interpolated = RightUpper_upsampled[RightUpper_upsampled.columns[1::]].interpolate(method='linear')
    RightUpper_downsampled = RightUpper_interpolated.resample('300s').mean()

    # RightLower resampled and interpolated to five minutes (no weight or humidity measurements)
    RightLower = RightLower.set_index('Unix_Time',drop = False)
    RightLower.drop('Device', axis=1, inplace=True)
    RightLower.drop('Hive_Position', axis=1, inplace=True)
    RightLower.drop('Sample', axis=1, inplace=True)
    RightLower.drop('Scaled_Weight', axis=1, inplace=True)
    RightLower.drop(' Weight_Scale_Factor', axis=1, inplace=True)
    RightLower.drop(' Weight', axis=1, inplace=True)
    RightLower.drop(' WeightL', axis=1, inplace=True)
    RightLower.drop(' WeightR', axis=1, inplace=True)
    RightLower.drop('Humidity', axis=1, inplace=True)
    RightLower_upsampled = RightLower.resample('1s').mean()
    RightLower_interpolated = RightLower_upsampled[RightLower_upsampled.columns[1::]].interpolate(method='linear')
    RightLower_downsampled = RightLower_interpolated.resample('300s').mean()

    # RightScale resampled and interpolated to five minutes (no humidity measurements)
    RightScale = RightScale.set_index('Unix_Time',drop = False)
    RightScale.drop('Device', axis=1, inplace=True)
    RightScale.drop('Hive_Position', axis=1, inplace=True)
    RightScale.drop('Sample', axis=1, inplace=True)
    RightScale.drop('Humidity', axis=1, inplace=True)
    RightScale_upsampled = RightScale.resample('1s').mean()
    RightScale_interpolated = RightScale_upsampled[RightScale_upsampled.columns[1::]].interpolate(method='linear')
    RightScale_downsampled = RightScale_interpolated.resample('300s').mean()
    RightAvg = RightScale_downsampled['Scaled_Weight'].resample('1d').mean()

    HiveWeather = HiveWeather.set_index('Unix_Time',drop = False)
    HiveWeather_upsampled = HiveWeather.resample('1s').mean()
    HiveWeather_interpolated = HiveWeather_upsampled[HiveWeather_upsampled.columns[1::]].interpolate(method='linear')
    HiveWeather_downsampled = HiveWeather_interpolated.resample('300s').mean()

    # return dataframes for CSV files
    #return(LeftUpper_downsampled,LeftLower_downsampled,LeftScale_downsampled,LeftAvg,RightUpper_downsampled,RightLower_downsampled,RightScale_downsampled,RightAvg,HiveWeather)

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