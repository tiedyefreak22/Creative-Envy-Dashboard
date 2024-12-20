from functions_and_classes import *

pyicloud = 0
hive_IDs = {"New Left Hive": '6b5cb8b012cb45038eacc24770a2fff7',
            "Utah OW Nuc Left": '13a71f80590a4184a2956058441c3be3',
            "Utah OW Nuc Right": 'dca02aae55b74ca1b1a6ac35042d2254',
           }

Palettes = {"darkly": {
        "type": "dark",
        "colors": {
            "primary": "#375a7f",
            "secondary": "#444444",
            "success": "#00bc8c",
            "info": "#3498db",
            "warning": "#f39c12",
            "danger": "#e74c3c",
            "light": "#ADB5BD",
            "dark": "#303030",
            "bg": "#222222",
            "fg": "#ffffff",
            "selectbg": "#555555",
            "selectfg": "#ffffff",
            "border": "#222222",
            "inputfg": "#ffffff",
            "inputbg": "#2f2f2f",
        },
    },
}

internet_connection = check_internet_connection()