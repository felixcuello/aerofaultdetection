import sys
import time
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
start_time = time.time()
model = IsolationForest()
model.fit(anemometer_data)
print("[INFO] Training time: {} seconds".format(time.time() - start_time)) 



# --[Predict the anomalies]-----------------------------------------------------
start_time = time.time()
df['anomaly'] = model.predict(anemometer_data)
print("[INFO] Prediction time: {} seconds".format(time.time() - start_time))


# Visualize the results
plt.figure(figsize=(10,6))
plt.plot(df['datetime'], df['ANEMOMETRO 1;wind_speed;Avg (m/s)'], color='blue', label = 'anemo1')
plt.plot(df['datetime'], df['anomaly'], color='red', label = 'anomaly')
plt.legend()
plt.show()

