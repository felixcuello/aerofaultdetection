# Add the parent directory of the lib directory to the module search path
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from lib.csv import CSV

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if len(sys.argv) < 3:
    print("Usage: python {} <[anemo|veleta|barometro|a|c|d|i|v> <input_csv_file>".format(sys.argv[0]))
    sys.exit()

selected_y_cols = sys.argv[1]
input_csv_file = sys.argv[2]

csv = CSV(input_csv_file)
data = csv.to_df()

data = data.fillna(0)
data = data.replace('None', 0)

x_col = 'datetime'

if selected_y_cols == "anemo":
    y_cols = [
        'ANEMOMETRO 1;wind_speed;Avg (m/s)',
        'ANEMOMETRO 2;wind_speed;Avg (m/s)',
        'ANEMOMETRO 3;wind_speed;Avg (m/s)',
        'ANEMOMETRO 4;wind_speed;Avg (m/s)',
        'ANEMOMETRO 5;wind_speed;Avg (m/s)',
        'ANEMOMETRO 6;wind_speed;Avg (m/s)',
        'ANEMOMETRO 7;wind_speed;Avg (m/s)'
    ] # default
elif selected_y_cols == "veleta":
    y_cols = [
        'VELETA 1;wind_direction;Avg (°)',
        'VELETA 2;wind_direction;Avg (°)',
        'VELETA 3;wind_direction;Avg (°)',
        'VELETA 4;wind_direction;Avg (°)'
    ] # list of column names to be compared
elif selected_y_cols == "baromettro":
    y_cols = [
        'BAROMETRO;air_pressure;Avg (hPa)'
    ]
elif selected_y_cols == "a":
    y_cols = [
        'A1;channel;Avg (V)',
        'A2;channel;Avg (V)',
        'A3;channel;Avg (V)'
    ]
elif selected_y_cols == "c":
    y_cols = [
        'C1;channel;Avg (I)',
        'C2;channel;Avg (I)',
        'C3;channel;Avg (I)',
        'C4;channel;Avg (I)',
        'C5;channel;Avg (I)',
        'C6;channel;Avg (I)',
        'C7;channel;Avg (I)',
        'C8;channel;Avg (I)'
    ]
elif selected_y_cols == "d":
    y_cols = [
        'D1;channel;Avg ()',
        'D2;channel;Avg ()',
        'D3;channel;Avg ()',
        'D4;channel;Avg ()'
    ]
elif selected_y_cols == "i":
    y_cols = [
        'I;channel;Avg (mA)'
    ]
elif selected_y_cols == "v":
    y_cols = [
        'V;channel;Avg (V)'
    ]

melted_data = pd.melt(data, id_vars=[x_col], value_vars=y_cols)
sns.lineplot(x=x_col, y='value', hue='variable', data=melted_data)
plt.show()
