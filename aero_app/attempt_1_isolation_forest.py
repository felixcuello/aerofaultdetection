import sys
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

if len(sys.argv) < 2:
    print("\nUsage: python {} <input_csv_file>".format(sys.argv[0]))
    sys.exit()


# --[Read the input CSV file]--------------------------------------------------
input_csv_file = sys.argv[1]
df = pd.read_csv(input_csv_file)


# --[Get only the anemometer readings]-----------------------------------------
anemometer_columns = []
for i in range(1,8):
    column = 'ANEMOMETRO {};wind_speed;Avg (m/s)'.format(i)
    anemometer_columns.append(column)

anemometer_data = df[anemometer_columns]


# --[Train the model]----------------------------------------------------------
#model = IsolationForest(
#        contamination=0.1 # Parameter used to help estimate the number of outliers in the dataset. Adjust this as needed.
#        )
model = IsolationForest()
model.fit(anemometer_data)



# --[Predict the anomalies]-----------------------------------------------------
df['anomaly'] = model.predict(anemometer_data)



# Visualize the results
plt.figure(figsize=(10,6))
plt.plot(df['datetime'], df['ANEMOMETRO 1;wind_speed;Avg (m/s)'], color='blue', label = 'anemo1')
plt.plot(df['datetime'], df['anomaly'], color='red', label = 'anomaly')
plt.legend()
plt.show()

