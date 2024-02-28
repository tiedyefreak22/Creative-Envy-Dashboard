import ssl
import requests
import time as t
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def BROODMINDER_GET():
    #Login to Broodminder, Get Beehive data, and format
    # path arg is path to chromedriver.exe
    #s = Service('/Users/kevinhardin/PythonScripts/chromedriver')
    #s = Service(str(path))
    s = Service(str('./chromedriver'))
    driver = webdriver.Chrome(service=s)

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
    driver.find_element(by=By.XPATH, value="/html/body/app-root/app-default/div/app-login/div/mat-tab-group/div/mat-tab-body[1]/div/div/mat-card/form/div/button/span").click()
    t.sleep(5)

    # download left hive data
    URL = 'https://mybroodminder.com/app/hive/4c146db0cb534e1d8d56f8e4c7b49c0d?start=1648872000&range=9'
    driver.get(URL)
    t.sleep(5)
    driver.find_element(by=By.XPATH, value="/html/body/app-root/app-core/mat-sidenav-container/mat-sidenav-content/div/div/app-hive-landing/div[3]/button[1]/span").click()
    t.sleep(1)

    # download weather data for both
    driver.find_element(by=By.XPATH, value="/html/body/app-root/app-core/mat-sidenav-container/mat-sidenav-content/div/div/app-hive-landing/div[3]/button[2]/span").click()
    t.sleep(1)

    # download right hive data
    URL = "https://mybroodminder.com/app/hive/74ab0c07e39e429a929c9a5a6ac86392?start=1648872000&&range=9"
    driver.get(URL)
    t.sleep(5)
    driver.find_element(by=By.XPATH, value="/html/body/app-root/app-core/mat-sidenav-container/mat-sidenav-content/div/div/app-hive-landing/div[3]/button[1]/span").click()
    t.sleep(1)

    # close the browser window
    driver.quit()

# if __name__ == '__main__':
#     BROODMINDER_GET()
