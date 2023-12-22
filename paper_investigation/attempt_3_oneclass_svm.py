# --[libraries]----------------------------------------------------------------
import time
import sys
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM


# --[Read the input CSV file]--------------------------------------------------
if len(sys.argv) < 2:
    print("\nUsage: python {} <input_csv_file>".format(sys.argv[0]))
    sys.exit()
input_csv_file = sys.argv[1]
df = pd.read_csv(input_csv_file)


# --[Get only the anemometer readings]-----------------------------------------
anemometer_columns = []
for i in range(1,8):
    column = 'ANEMOMETRO {};wind_speed;Avg (m/s)'.format(i)
    anemometer_columns.append(column)
anemometer_data = df[anemometer_columns]


# --[use minimum of other anemometers as a feature]----------------------------
# Create a new feature that represents the difference between each anemometer's reading 
# and the minimum of the other readings
for column in anemometer_columns:
    other_columns = [col for col in anemometer_columns if col != column]
    df[column+'_diff_min'] = (2 * df[column]) - df[other_columns].min(axis=1)

# --[data scaling]-------------------------------------------------------------
start_time = time.time()
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[anemometer_columns + [column+'_diff_min' for column in anemometer_columns]])
print("[INFO] Normalization time: {:.2f} seconds".format(time.time() - start_time))


# --[train the model]----------------------------------------------------------
start_time = time.time()
model = OneClassSVM(nu=0.25)  # The nu parameter is similar to the contamination parameter in the Isolation Forest model. Adjust this as needed.
model.fit(scaled_data)
print("[INFO] Training time: {:.2f} seconds".format(time.time() - start_time))


# --[predict anomalies]--------------------------------------------------------
start_time = time.time()
df['anomaly'] = model.predict(scaled_data)
print("[INFO] Prediction time: {:.2f} seconds".format(time.time() - start_time))


# --[plot the results]---------------------------------------------------------
plt.figure(figsize=(10,6))
plt.plot(df['datetime'], df['ANEMOMETRO 1;wind_speed;Avg (m/s)'], color='blue', label = 'anemo1')
plt.plot(df['datetime'], df['anomaly'], color='red', label = 'anomaly')
plt.legend()
plt.show()

