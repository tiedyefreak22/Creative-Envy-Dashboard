from BEE_WEATHER_DATA import BROODMINDER_GET, AMBIENT_GET, READ_HIVE, PROCESS_HIVE, READ_BEE_WEATHER, PROCESS_BEE_WEATHER, PROCESS_AMBIENT, GRAPH_DATA, GET_MOON_IMAGE, GET_FORECAST, PROCESS_FORECAST, PROCESS_FORECAST_MIN_MAX, check_internet_connection, GET_WEATHER_ICON

def init():
    global hive_IDs
    
    hive_IDs = {"New Left Hive": '6b5cb8b012cb45038eacc24770a2fff7',
                #"Utah OW Left Nuc": '',
                #"Utah OW Right Nuc": '',
               }