# --[libraries]----------------------------------------------------------------
import sys
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM


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


# --[Create a new column with the average of all anemometer readings]----------
df['average'] = df[anemometer_columns].mean(axis=1)
for column in anemometer_columns:
      df[column + '_diff'] = df[column] - df['average']


# --[Normalize the data]-------------------------------------------------------
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[anemometer_columns + [column+'_diff' for column in anemometer_columns]])


# --[Train the model]----------------------------------------------------------
model = OneClassSVM(nu=0.05)  # The nu parameter is similar to the contamination parameter in the Isolation Forest model. Adjust this as needed.
model.fit(scaled_data)


# --[Predict the anomalies]----------------------------------------------------
df['anomaly'] = model.predict(scaled_data)


# --[Plot the results]---------------------------------------------------------
plt.figure(figsize=(10,6))
plt.plot(df['datetime'], df['ANEMOMETRO 1;wind_speed;Avg (m/s)'], color='blue', label = 'anemo1')
plt.plot(df['datetime'], df['anomaly'], color='red', label = 'anomaly')
plt.legend()
plt.show()

