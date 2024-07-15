from BEE_WEATHER_DATA import *

def init():
    global pyicloud
    global hive_IDs

    pyicloud = 0
    hive_IDs = {"New Left Hive": '6b5cb8b012cb45038eacc24770a2fff7',
                "Utah OW Nuc Left": '13a71f80590a4184a2956058441c3be3',
                "Utah OW Nuc Right": 'dca02aae55b74ca1b1a6ac35042d2254',
               }