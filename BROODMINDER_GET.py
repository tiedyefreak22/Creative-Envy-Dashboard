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
    
    directory = "./Broodminder"
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

if __name__ == '__main__':
    BROODMINDER_GET()