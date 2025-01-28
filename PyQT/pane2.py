from custom_widgets import *

Image.CUBIC = Image.BICUBIC

class Pane2(QWidget):
    def __init__(self, parent, controller, screen_width, screen_height):
        self.parent = parent
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

        lf_labels = [
                    "Hive 1 Wt.",
                    "Hive 2 Wt.",
                    "Hive 3 Wt.",
                    "Hive 4 Wt.",
                    "Hive 5 Wt.",
                    "Hive 1 Temp.",
                    "Hive 2 Temp.",
                    "Hive 3 Temp.",
                    "Hive 4 Temp.",
                    "Hive 5 Temp.",
                    "Hive 1 Humid.",
                    "Hive 2 Humid.",
                    "Hive 3 Humid.",
                    "Hive 4 Humid.",
                    "Hive 5 Humid.",
                    ]
        lf_values = [
                    Hive_Processed[0].get_weight(num_days = 7),
                    Hive_Processed[1].get_weight(num_days = 7),
                    Hive_Processed[0].get_weight(num_days = 7),
                    Hive_Processed[0].get_weight(num_days = 7),
                    Hive_Processed[0].get_weight(num_days = 7),
                    Hive_Processed[0].get_upper_temp(num_days = 7),
                    Hive_Processed[1].get_upper_temp(num_days = 7),
                    Hive_Processed[2].get_upper_temp(num_days = 7),
                    Hive_Processed[0].get_upper_temp(num_days = 7),
                    Hive_Processed[0].get_upper_temp(num_days = 7),
                    Hive_Processed[0].get_humidity(num_days = 7),
                    Hive_Processed[1].get_humidity(num_days = 7),
                    Hive_Processed[2].get_humidity(num_days = 7),
                    Hive_Processed[0].get_humidity(num_days = 7),
                    Hive_Processed[0].get_humidity(num_days = 7),
                    ]
        i = 0
        while i < 15:
            grid.addWidget(GraphWidget(self, controller, lf_labels[i], lf_values[i]), floor((i - 5) / 5) + 1, (i - 5) % 5)
            i = i + 1
        
        self.setLayout(grid)