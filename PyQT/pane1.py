from custom_widgets import *

Image.CUBIC = Image.BICUBIC

class Pane1(QWidget):
    def __init__(self, parent, controller, screen_width, screen_height):
        self.parent = parent
        self.controller = controller
        super(QWidget, self).__init__(parent)
        grid = QGridLayout(self)

        Hive_Processed = []
        for hive_creds in hive_IDs.items():
            hive = Hive(*list(hive_creds))
            hive.set()
            Hive_Processed.append(hive)
        forecast_data = PROCESS_FORECAST()
        ambient = Ambient()
        ambient.set()
        
        # Pane1 Objects
        # Loop to create LabelFrames
        lf_labels = [
                    "Time/Sunrise/Sunset",
                    "Moon Phase",
                    "Wx Forecast",
                    "",
                    "Honey Wt./Bee Count",
                    "Temp",
                    "Solar Rad.",
                    "Wind Spd./Dir.",
                    "Chook Temp", 
                    "Bee Wt.",
                    "Humidity",
                    "UV Index",
                    "Precip.",
                    "Bee Temp.",
                    "Bee Humid.",
                    ]
        
        lf_values = [
                    "",
                    "",
                    "",
                    "",
                    "",
                    ambient.get_tempf(num_days = 7),
                    ambient.get_solarradiation(num_days = 7),
                    ambient.get_windspeedmph(num_days = 7),
                    pd.Series([1]), 
                    Hive_Processed[0].get_weight(num_days = 7),
                    ambient.get_humidity(num_days = 7),
                    ambient.get_uv(num_days = 7),
                    ambient.get_hourlyrainin(num_days = 7),
                    Hive_Processed[0].get_upper_temp(num_days = 7),
                    Hive_Processed[0].get_humidity(num_days = 7),
                    ]
        
        grid.addWidget(CustomClock(self, controller), 0, 0)
        grid.addWidget(CustomSmallImg(self, controller), 0, 1)
        grid.addWidget(WeatherWidget(self, controller), 0, 2, 1, 2)
        grid.addWidget(EmptyLF(self, controller), 0, 4)

        i = 5
        while i < 15:
            grid.addWidget(GraphWidget(self, controller, lf_labels[i], lf_values[i]), floor((i - 5) / 5) + 1, (i - 5) % 5)
            i = i + 1
        
        self.setLayout(grid)