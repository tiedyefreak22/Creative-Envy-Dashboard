from settings import *

def BROODMINDER_GET(hive_name, hive_ID):
    debugging = False
    
    #Login to Broodminder, Get Beehive data, and format
    print("Getting Broodminder data.")
    directory = "Broodminder/"        
    options = Options()
    options.add_experimental_option("prefs", {
      "download.default_directory": r"C:\Users\khard\OneDrive\Documents\GitHub\Creative-Envy-Dashboard\Broodminder",
      "download.prompt_for_download": False,
      "download.directory_upgrade": True,
      "safebrowsing.enabled": True,
      "profile.default_content_setting_values.automatic_downloads": 1,
    })

    if debugging:
        chrome_options.add_experimental_option("detach", True)
    else:
        options.add_argument('--headless=new')

    s = None

    if platform == "linux" or platform == "linux2":
        pass 
    elif platform == "darwin":
        s = Service(str('./chromedriver'))
    elif platform == "win32":
        s = Service(str('./chromedriver.exe'))
        
    driver = webdriver.Chrome(service = s, options = options)

    ssl._create_default_https_context = ssl._create_unverified_context

    username = os.getenv("BROODMINDER_USERNAME")
    password = os.getenv("BROODMINDER_PASSWORD")

    session = requests.session()
    URL = 'https://mybroodminder.com/login'
    driver.get(URL)
    t.sleep(5)

    # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-default/div/app-login/div/mat-tab-group/div/mat-tab-body[1]/div/div/mat-card/form/div/button")))
        
    # find username/email field and send the username itself to the input field
    driver.find_element(by = By.NAME, value = "email").send_keys(username)

    # find password input field and insert password as well
    driver.find_element(by = By.NAME, value = "password").send_keys(password)

    # click login button
    driver.find_element(by = By.XPATH, value = "/html/body/app-root/app-default/div/app-login/div/mat-tab-group/div/mat-tab-body[1]/div/div/mat-card/form/div/button").click()

    t.sleep(3)

    # left hive dashboard
    URL = f'https://mybroodminder.com/app/dashboard/hives?hiveIds={hive_ID}&weaIds=37a0763f69e04c2c823013928e067d68'
    driver.get(URL)
    t.sleep(5)

    # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-core/mat-sidenav-container/mat-sidenav-content/div/div/app-hives-dashboard/div[1]/div/app-date-range-picker-2/div/mat-icon")))
    
    # select longest date range
    driver.find_element(by = By.XPATH, value = "/html/body/app-root/app-core/mat-sidenav-container/mat-sidenav-content/div/div/app-hives-dashboard/div[1]/div/app-date-range-picker-2/div/mat-icon").click()
    t.sleep(1)
    driver.find_element(by = By.XPATH, value = "/html/body/div[3]/div[2]/div/div/div/a/div/div[1]/button[9]/span[2]").click()
    t.sleep(1)

    # click three dots
    driver.find_element(by = By.XPATH, value = "/html/body/app-root/app-core/mat-sidenav-container/mat-sidenav-content/div/div/app-hives-dashboard/div[2]/div[2]/mat-icon").click()
    t.sleep(1)
    
    # click "Download Options"
    driver.find_element(by = By.XPATH, value = "/html/body/div[3]/div[2]/div/div/div/button[4]").click()
    t.sleep(1)

    # click "Hourly Readings CSV"
    driver.find_element(by = By.XPATH, value = "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/div/div[2]/div[2]/mat-checkbox/div/div/input").click()
    t.sleep(1)

    # click "Hourly Weather CSV"
    driver.find_element(by = By.XPATH, value = "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/div/div[2]/div[3]/mat-checkbox/div/div/input").click()
    t.sleep(1)

    # click "Download"
    driver.find_element(by = By.XPATH, value = "/html/body/div[3]/div[2]/div/mat-dialog-container/div/div/div/div[2]/div[4]/button/span[2]").click()
    t.sleep(3)

    if not debugging:
        # close the browser window
        driver.quit()
    
    READ_HIVE(hive_name)
    READ_BEE_WEATHER()
    print("Finished getting Broodminder data.")

def READ_HIVE(hive_name: str):
    print("Reading Broodminder data.")
    directory = "Broodminder/"
    
    # Check for new download data
    Hive = pd.DataFrame()
    filename = ""
    for test_str in os.listdir(directory):
        regex = str(hive_name) + r"_combined_readings_20[a-zA-Z0-9\-\_\.]*.csv"
        matches = re.finditer(regex, test_str, re.MULTILINE)
        for matchNum, match in enumerate(matches, start = 1):
            filename = directory + match.group()

    # Load master file
    if filename:
        Hive = pd.read_csv(filename)
        Hive.drop('App', axis = 1, inplace = True)
        Hive.drop('Record_Type', axis = 1, inplace = True)
        Hive.drop('Radar', axis = 1, inplace = True)
        Hive.drop('UTC_TimeStamp', axis = 1, inplace = True)
        Hive.drop('Local_TimeStamp', axis = 1, inplace = True)
        Hive.drop('Metric', axis = 1, inplace = True)
        Hive.drop('Audio', axis = 1, inplace = True)

        Hive_master = pd.DataFrame()
        if os.path.exists(str(directory + str(hive_name) + " Master.csv")):
            Hive_master = pd.read_csv(str(directory + str(hive_name) + " Master.csv"))
            Hive_master = pd.concat([Hive, Hive_master]).astype(str).drop_duplicates(subset = ['Unix_Time'], keep = 'last').sort_values(by = ['Unix_Time']).reset_index(drop = True)
        else:
            Hive_master = Hive.sort_values(by = ['Unix_Time']).reset_index(drop = True)

        Hive_master.to_csv(directory + hive_name + " Master.csv", mode = 'w', index = False, header = True)
        os.remove(filename)
    elif os.path.exists(str(directory + str(hive_name) + " Master.csv")):
        Hive_master = pd.read_csv(str(directory + str(hive_name) + " Master.csv")).sort_values(by = ['Unix_Time'])
        
    return Hive_master
    print("Finished reading Broodminder data.")

def READ_BEE_WEATHER():
    print("Reading Broodminder weather data.")
    directory = "Broodminder/"
    
    # Check for new download data
    Bee_Weather = pd.DataFrame()
    filename = ""
    for test_str in os.listdir(directory):
        regex = r"KevBec Apiary_weather_20[a-zA-Z0-9\-\_\.]*.csv"
        matches = re.finditer(regex, test_str, re.MULTILINE)
        for matchNum, match in enumerate(matches, start = 1):
            filename = directory + match.group()
    
    # Load master file
    if filename:
        Bee_Weather = pd.read_csv(filename)
        Bee_Weather.drop(['DownloadTimeStamp', 'UTC_TimeStamp', 'Local_TimeStamp', 'Metric'], axis = 1, inplace = True)
        
        if os.path.exists(directory + "KevBec Apiary_weather Master.csv"):
            Bee_Weather_master = pd.read_csv(directory + "KevBec Apiary_weather Master.csv")        
            Bee_Weather_master = pd.concat([Bee_Weather, Bee_Weather_master]).astype(str).drop_duplicates(subset = ['Unix_Time'], keep = 'last').reset_index(drop = True)
        else:
            Bee_Weather_master = Bee_Weather
            
        Bee_Weather.to_csv(directory + "KevBec Apiary_weather Master.csv", mode = 'w', index = False, header = True)
        os.remove(filename)
    elif os.path.exists(directory + "KevBec Apiary_weather Master.csv"):
         Bee_Weather_master = pd.read_csv(directory + "KevBec Apiary_weather Master.csv")
    return Bee_Weather_master
    print("Finished reading Broodminder weather data.")

def PROCESS_HIVE(hive_name: str):
    print("Processing Broodminder data.")
    directory = "Broodminder/"
    metrics = ["Weight", "Humidity", "Temperature"]
    Hive = READ_HIVE(hive_name)
    Unique_Dev_Names = Hive.Hive_Position.unique()
    Unique_Devs = Hive.Device.unique()
    Devices = {}

    for i, Device in enumerate(Unique_Devs):
        Devices.update({Unique_Dev_Names[i]: Hive[Hive['Device'] == Device]})
    
    Week_Devices = {}
    for i in range(len(Devices)):
        Week_Devices[list(Devices.keys())[i]] = Devices[list(Devices.keys())[i]]

    for i, key in enumerate(list(Week_Devices.keys())):
        for j, cat in enumerate(Week_Devices[str(key)]):
            if Week_Devices[str(key)][str(cat)].isnull().all():
                Week_Devices[str(key)] = Week_Devices[str(key)].drop(columns = [str(cat)])
    for i, key in enumerate(list(Week_Devices.keys())):
        Week_Devices[str(key)] = Week_Devices[str(key)].sort_values(by = ["Unix_Time"])
        Week_Devices[str(key)]["Unix_Time"] = [int(i) for i in Week_Devices[str(key)]["Unix_Time"]]
        Week_Devices[str(key)] = Week_Devices[str(key)].loc[Week_Devices[str(key)][Week_Devices[str(key)]["Unix_Time"] >= min(Week_Devices[str(key)]["Unix_Time"])].index[0]:].set_index("Unix_Time")
    
    return Week_Devices
    print("Finished processing Broodminder data.")

def PROCESS_BEE_WEATHER():
    print("Processing Broodminder weather data.")
    directory = "Broodminder/"
    Bee_Weather = READ_BEE_WEATHER()
    metrics = [i for i in list(Bee_Weather.keys()) if not "Unix_Time" in i]
    
    for i, metric in enumerate(metrics):
        Bee_Weather = Bee_Weather.sort_values(by = ["Unix_Time"])
    Week_Devices = pd.DataFrame()
    for i in range(len(Bee_Weather.keys())):
        Week_Devices[list(Bee_Weather.keys())[i]] = Bee_Weather[list(Bee_Weather.keys())[i]]

    for j, cat in enumerate(Week_Devices):
        if Week_Devices[str(cat)].isnull().all():
            Week_Devices = Week_Devices.drop(columns = [str(cat)])
    Week_Devices = Week_Devices.sort_values(by = ["Unix_Time"])
    int_Unix = [int(i) for i in Week_Devices["Unix_Time"]]
    #Week_Devices = Week_Devices.loc[Week_Devices[Week_Devices["Unix_Time"] >= max(int_Unix) - 604800].index[0]:].set_index("Unix_Time")
    
    return Week_Devices.set_index("Unix_Time")
    print("Finished processing Broodminder weather data.")

def AMBIENT_GET():
    # Get Ambient data via URL and format
    print("Getting Ambient data.")
    # csv file name
    filename = "Ambient/Ambient_Data.csv"
    
    # Define weather station data
    AMBIENT_API_KEY = os.getenv("AMBIENT_API_KEY")
    AMBIENT_APPLICATION_KEY = os.getenv("AMBIENT_APPLICATION_KEY")
    AMBIENT_MAC = os.getenv("AMBIENT_MAC")
    
    # Read in current csv values
    rows = pd.read_csv(filename, sep = ',', on_bad_lines = 'skip')
    
    AMBIENT_START_DATE = datetime.fromtimestamp(int(rows['dateutc'][len(rows['dateutc']) - 1]))
    
    # Determine number of days since beginning of record
    dateDelta = datetime.today() - AMBIENT_START_DATE
    
    # Iterate through each day of data
    for i in range(int(dateDelta.days + 1)):
        # Fetch data from Ambient
        AMBIENT_DATE = AMBIENT_START_DATE + timedelta(days=i)
        AMBIENT_DATE = str(AMBIENT_DATE)
        AMBIENT_DATE = AMBIENT_DATE[:AMBIENT_DATE.rindex(" ")]
        print(AMBIENT_DATE)
        query_params = {'applicationKey': AMBIENT_APPLICATION_KEY, 'macAddress': AMBIENT_MAC, 'apiKey': AMBIENT_API_KEY, 'endDate': AMBIENT_DATE}
        AMBIENT_ENDPOINT = f'https://rt.ambientweather.net/v1/devices/{AMBIENT_MAC}?apiKey={AMBIENT_API_KEY}&applicationKey={AMBIENT_APPLICATION_KEY}&endDate={AMBIENT_DATE}'
        data = pd.DataFrame()

        response = requests.get(AMBIENT_ENDPOINT)
        if response.status_code == 200:
            data = pd.DataFrame(response.json())
        else:
            # Handle errors
            print(f'Error: {response.status_code} - {response.text}')

        # Wait for 1 second to comply with Ambient server limits
        t.sleep(1)
        
        # Sort and append new data
        if data.empty:
            pass
        else:
            data = data[['dateutc', 'winddir', 'windspeedmph', 'windgustmph', 'maxdailygust',
                         'tempf', 'humidity', 'hourlyrainin', 'eventrainin', 'dailyrainin',
                         'weeklyrainin', 'monthlyrainin', 'yearlyrainin', 'totalrainin', 'uv',
                         'solarradiation', 'feelsLike', 'dewPoint', 'lastRain']]
            data['dateutc'] = (data['dateutc'].astype(np.int64) / 1000.0)
            sorted_df = data.sort_values('dateutc', axis = 0, ascending = True, kind = 'mergesort')
            sorted_df.to_csv(filename, mode = 'a', index = False, header = False)
    
    # Re-read file and drop any duplicates
    rows = pd.read_csv(filename, sep = ',', on_bad_lines = 'skip')
    rows = rows.drop_duplicates(subset = ['dateutc'], keep = 'last').reset_index(drop = True)
    rows.to_csv(filename, mode = 'w', index = False, header = True)
    print("Finished getting Ambient data.")

def PROCESS_AMBIENT():
    print("Processing Ambient data.")
    filename = "Ambient/Ambient_Data.csv"
    Ambient = pd.read_csv(filename)
    metrics = [i for i in list(Ambient.keys()) if not "dateutc" in i]

    for i, metric in enumerate(metrics):
        Ambient = Ambient.sort_values(by = ["dateutc"])
        
    Week_Devices = pd.DataFrame()
    for i in range(len(Ambient.keys())):
        Week_Devices[list(Ambient.keys())[i]] = Ambient[list(Ambient.keys())[i]]

    for j, cat in enumerate(Week_Devices):
        if Week_Devices[str(cat)].isnull().all():
            Week_Devices = Week_Devices.drop(columns = [str(cat)])
    Week_Devices = Week_Devices.sort_values(by = ["dateutc"])
    int_Unix = [int(i) for i in Week_Devices["dateutc"]]
    #Week_Devices = Week_Devices.loc[Week_Devices[Week_Devices["dateutc"] >= max(int_Unix) - 604800].index[0]:].set_index("dateutc")

    return Week_Devices.set_index("dateutc")
    print("Finished processing Ambient data.")

def GRAPH_DATA(Data: pd.DataFrame):
    metrics = [key for key in Data.keys() if key not in ["dateutc", "Device", "Hive_Position", "lastRain", "Unix_Time", "Sample", "w1", "w2", "w3", "w4", "Weight_Scale_Factor"]]
    metric_num = len(metrics)

    ncols = 4
    nrows = metric_num // ncols + (metric_num % ncols > 0)
    plt.figure(figsize = (15, 4 * nrows))
    plt.subplots_adjust(hspace = 0.2)

    for i, match in enumerate(metrics):
        try:
            ax = plt.subplot(nrows, ncols, i + 1)
            Data[str(match)].plot(ax = ax)
            ax.set_title(str(match))
        except:
            pass
    plt.show()

def GET_FORECAST():
    print("Getting Forecast data.")
    api_key = os.getenv("FORECAST_API_KEY")
    lat = 40.907220
    lon = -111.894300
    query_params = {'lat': lat, 'lon': lon, 'appid': api_key, 'units': 'imperial'}

    
    api_endpoint = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}'
    query_params = {'lat': lat, 'lon': lon, 'appid': api_key, 'units': 'imperial'}
    
    response = requests.get(api_endpoint, params = query_params)
    
    if response.status_code == 200:
        data = response.json()
        json_object = json.dumps(data, indent = 4)
 
        # Writing to sample.json
        with open("Forecast/forecast.json", "w") as outfile:
            outfile.write(json_object)
    else:
        # Handle errors
        print(f'Error: {response.status_code} - {response.text}')
    print("Finished getting Forecast data.")

def GET_MOON_IMAGE(size = 216):
    print("Getting moon phase image.")
    total_images = 8760
    moon_domain = "https://svs.gsfc.nasa.gov"
    
    # https://svs.gsfc.nasa.gov/vis/a000000/a005100/a005187/frames/216x216_1x1_30p/moon.8597.jpg
    moon_path = "/vis/a000000/a005100/a005187"
    image = None
    pixmap = None
    now = datetime.utcnow()
    janone = datetime(now.year, 1, 1, 0, 0, 0)
    moon_image_number = round((now - janone).total_seconds() / 3600)

    if size > 2160:
        url = moon_domain + moon_path + "/frames/5760x3240_16x9_30p/" + f"plain/moon.{moon_image_number:04d}.tif" # can't have space before "04d"
    elif size > 216:
        url = moon_domain + moon_path + "/frames/3840x2160_16x9_30p/" + f"plain/moon.{moon_image_number:04d}.tif"
    else:
        url = moon_domain + moon_path + "/frames/216x216_1x1_30p/" + f"moon.{moon_image_number:04d}.jpg"
    response = requests.get(url, verify = False)
    img = Image.open(BytesIO(response.content))

    for file in os.listdir("moon/"):
        os.remove("moon/" + file)
    img.save(f"moon/moon.{moon_image_number:04d}.tiff")

    print("Finished getting moon phase image.")

def PROCESS_FORECAST(interp = 0):
    print("Processing Forecast data.")
    response = pd.DataFrame()
    with open('Forecast/forecast.json', 'r') as openfile:
        # Reading from json file
        data = json.load(openfile)
        response = pd.DataFrame()
        for key in data:
            if key == "list":
                cur_dict = {}
                for key2 in data[key]:
                    for key3, value in key2.items():
                        if key3 == "main":
                            for key4, value2 in key2[key3].items():
                                cur_dict.update({key4: value2})
                        if key3 == "weather":
                            for key4, value2 in key2[key3][0].items():
                                cur_dict.update({key4: value2})
                        else:
                            cur_dict.update({key3: value})
                    response = pd.concat([response, pd.DataFrame(cur_dict, index = [key2["dt"]])], axis = 0, join = 'outer')
    response = response.drop(columns = ["dt"])
    return response
    print("Finished processing Forecast data.")

def PROCESS_FORECAST_MIN_MAX(response):
    print("Processing Forecast min/max data.")
    prior_midnight = int(datetime.timestamp(datetime.strptime(date.today().strftime('%Y-%m-%d') + " 00:00:00", '%Y-%m-%d %H:%M:%S')))
    future_midnight = int(datetime.timestamp(datetime.strptime((date.today() + timedelta(days = 1)).strftime('%Y-%m-%d') + " 00:00:00", '%Y-%m-%d %H:%M:%S')))
    todays_forecast = pd.DataFrame([response.loc[i] for i in response.index.values.tolist() if i <= future_midnight and i >= prior_midnight])
    if todays_forecast.empty:
        max_temp = 0.0
        min_temp = 0.0
        max_humid = 0.0
        min_humid = 0.0
        # max_wind = 0.0
        # min_wind = 0.0
    else:
        max_temp = max(todays_forecast["temp_max"])
        min_temp = min(todays_forecast["temp_min"])
        max_humid = max(todays_forecast["humidity"])
        min_humid = min(todays_forecast["humidity"])
        # max_wind = max(todays_forecast["wind"])
        # min_wind = min(todays_forecast["wind"])
    return min_temp, max_temp, min_humid, max_humid#, min_wind, max_wind
    print("Finished processing Forecast min/max data.")

def GET_WEATHER_ICON():
    print("Getting weather icon.")
    lat = 40.907220
    lon = -111.894300
    tz = pytz.timezone('America/Denver')
    tz_name = 'America/Denver'
    for_date = date.today()
    
    l = astral.LocationInfo('Custom Name', 'My Region', tz_name, lat, lon)
    s = astral.sun.sun(l.observer, date = for_date)

    sunrise = s['sunrise'].astimezone(tz)
    sunset = s['sunset'].astimezone(tz)
    
    response = PROCESS_FORECAST()
    icon_dict = {200: "11d",
                201: "11d",
                202: "11d",
                210: "11d",
                211: "11d",
                212: "11d",
                221: "11d",
                230: "11d",
                231: "11d",
                232: "11d",
                300: "09d",
                301: "09d",
                302: "09d",
                310: "09d",
                311: "09d",
                312: "09d",
                313: "09d",
                314: "09d",
                321: "09d",
                500: "10d",
                501: "10d",
                502: "10d",
                503: "10d",
                504: "10d",
                511: "13d",
                520: "09d",
                521: "09d",
                522: "09d",
                531: "09d",
                600: "13d",
                601: "13d",
                602: "13d",
                611: "13d",
                612: "13d",
                613: "13d",
                615: "13d",
                616: "13d",
                620: "13d",
                621: "13d",
                622: "13d",
                701: "50d",
                711: "50d",
                721: "50d",
                731: "50d",
                741: "50d",
                751: "50d",
                761: "50d",
                762: "50d",
                771: "50d",
                781: "50d",
                "800d": "01d",
                "800n": "01n",
                "801d": "02d",
                "801n": "02n",
                "802d": "03d",
                "802n": "03n",
                "803d": "04d",
                "803n": "04n",
                "804d": "04d",
                "804n": "04n",
                }

    temp = response.loc[response.index > int(t.time())]
    subresponse = temp if len(temp) >= 3 else response.iloc[-3:]
    
    icon_url = []
    for idx, id in subresponse["id"].items():
        if (floor(id/100) == 8) & (idx >= int(datetime.timestamp(sunrise))) & (idx <= int(datetime.timestamp(sunset))):
            icon_url.append("https://openweathermap.org/img/wn/%s@2x.png" % (icon_dict[str(id) + "d"]))
        elif (floor(id/100) == 8) & ((idx < int(datetime.timestamp(sunrise))) | (idx > int(datetime.timestamp(sunset)))):
            icon_url.append("https://openweathermap.org/img/wn/%s@2x.png" % (icon_dict[str(id) + "n"]))
        else:
            icon_url.append("https://openweathermap.org/img/wn/%s@2x.png" % (icon_dict[id]))
    
    return list(zip([datetime.fromtimestamp(i).strftime('%I:%M %p') for i in subresponse.index], icon_url)), datetime.timestamp(sunrise), datetime.timestamp(sunset)
    print("Finished getting weather icon.")

def RAND_PIC():
    directory = "PhotosB/"
    file_paths = []
    ext = ('.png', '.jpg', '.jpeg', '.heic', '.tiff', '.tif')
    raw_ext = ('.raw', '.arw', '.dng')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(tuple(ext)):
                file_paths.append(os.path.join(root, file))
            elif file.lower().endswith(tuple(raw_ext)):
                try:
                    with rawpy.imread(np.fromfile("Test/DSC1160-medium.RAW", allow_pickle=True)) as raw:
                        print(f'raw type:                     {raw.raw_type}')                      # raw type (flat or stack, e.g., Foveon sensor)
                        print(f'number of colors:             {raw.num_colors}')                    # number of different color components, e.g., 3 for common RGB Bayer sensors with two green identical green sensors 
                        print(f'color description:            {raw.color_desc}')                    # describes the various color components
                        print(f'raw pattern:                  {raw.raw_pattern.tolist()}')          # decribes the pattern of the Bayer sensor
                        print(f'black levellos:                 {raw.black_level_per_channel}')       # black level correction
                        print(f'white level:                  {raw.white_level}')                   # camera white level
                        print(f'color matrix:                 {raw.color_matrix.tolist()}')         # camera specific color matrix, usually obtained from a list in rawpy (not from the raw file)
                        print(f'XYZ to RGB conversion matrix: {raw.rgb_xyz_matrix.tolist()}')       # camera specific XYZ to camara RGB conversion matrix
                        print(f'camera white balance:         {raw.camera_whitebalance}')           # the picture's white balance as determined by the camera
                        print(f'daylight white balance:       {raw.daylight_whitebalance}')         # the camera's daylight white balance
                    file_paths.append(os.path.join(root, file))
                except:
                    pass
    while True:
        try:
            rand_pic = file_paths[random.randint(0, len(file_paths) - 1)]
            PIL_image = Image.open(rand_pic)
            break
        except:
            pass

def config_pic(file, widget_width, widget_height, padding):
    PIL_image = Image.open(file)
    original_w = np.shape(PIL_image)[1]
    original_h = np.shape(PIL_image)[0]
    aspect = original_h / original_w
    constraining_dim = min(widget_width - 5 * padding,
                           widget_height - 5 * padding)
    minor_constraint = min(constraining_dim / original_w, constraining_dim / original_h)
    img_width = int(original_w * minor_constraint)
    img_height = int(original_h * minor_constraint)
    PIL_image_small = PIL_image.resize((img_width, img_height), Image.Resampling.LANCZOS)

    # now create the ImageTk PhotoImage:
    #img = ImageQt(PIL_image_small)
    img = PIL_image_small
    return img

def kalman(z):
    # initial parameters
    n_iter = len(z)
    sz = (n_iter,)            # size of array
    Q = 0.05                  # process variance

    # allocate space for arrays
    xhat = np.zeros(sz)       # a posteri estimate of x
    P = np.zeros(sz)          # a posteri error estimate
    xhatminus = np.zeros(sz)  # a priori estimate of x
    Pminus = np.zeros(sz)     # a priori error estimate
    K = np.zeros(sz)          # gain or blending factor

    R = variance(z)           # estimate of measurement variance

    # initial estimates
    xhat[0] = mean(z[0:3])
    P[0] = 1.0

    for k in range(1, n_iter):
        # time update
        xhatminus[k] = xhat[k - 1]
        Pminus[k] = P[k - 1] + Q

        # measurement update
        K[k] = Pminus[k] / (Pminus[k] + R)
        xhat[k] = xhatminus[k] + K[k] * (z[k] - xhatminus[k])
        P[k] = (1 - K[k]) * Pminus[k]

    return xhat

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

class Hive():
    def __init__(self, hive_name, hive_ID):
        #Tk.__init__(self)
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