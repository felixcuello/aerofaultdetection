# --[libraries]----------------------------------------------------------------
import sys
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


# --[get the CSV fle from the command line]------------------------------------
if len(sys.argv) < 2:
    print("\nUsage: python {} <input_csv_file>".format(sys.argv[0]))
    sys.exit()
input_csv_file = sys.argv[1]
df = pd.read_csv(input_csv_file)


# --[Get only the anemometer readings]-----------------------------------------
anemometer_columns = []
for i in range(1,5):
    column = 'VELETA {};wind_direction;Avg (°)'.format(i)
    anemometer_columns.append(column)
anemometer_data = df[anemometer_columns]


# --[Calculate the RMSE for each row]------------------------------------------
df['average'] = df[anemometer_columns].mean(axis=1)
def calculate_rmse(row):
    rmse = 0
    for col in anemometer_columns:
        print("{} << row[{}]".format(row[col], col))
        print("{} << row['average']".format(row['average']))
        print("{} << rmse".format(rmse))
        print("rmse += ({} - {}) ** 2".format(row[col], row['average']))
        row[col].replace('None', 0)
        a = float(row[col]) - float(row['average'])
        print(">>>>>>>>> a={}".format(a))
        rmse += (a*a)
        print(">>>>>>>>> result rmse={}".format(rmse))

    return np.sqrt(rmse / len(anemometer_columns))
df['rmse'] = df.apply(calculate_rmse, axis=1)
import ipdb; ipdb.set_trace()

# --[Add a column to indicate if the row is an anomaly]-------------------------
df['is_anomaly'] = np.where(df['rmse'] >= 2, 1, 0) # 2 is an arbitrary threshold


# --[Split the data into training and test sets]--------------------------------
start_time = time.time()
X = df[anemometer_columns]
y = df['is_anomaly']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=111)
print("[INFO] Splitting time: {:.2f} seconds".format(time.time() - start_time))


# --[Train the model]----------------------------------------------------------
start_time = time.time()
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("[INFO] Training time: {:.2f} seconds".format(time.time() - start_time))


# --[Predict the anomalies in the test set]------------------------------------
start_time = time.time()
y_pred = model.predict(X_test)
print("[INFO] Prediction time: {:.2f} seconds".format(time.time() - start_time))


# --[Get the model accuracy]---------------------------------------------------
accuracy = (y_pred == y_test).mean()
print(f'Accuracy: {accuracy}')


# --[predict anomalies]--------------------------------------------------------
df['anomaly_pred'] = model.predict(X)


# --[plot the anemometer readings]---------------------------------------------
plt.figure(figsize=(10,6))
plt.plot(df['datetime'], df['VELETA 1;wind_speed;Avg (m/s)'], color='green', label='ANEMO 1')
plt.plot(df['datetime'], df['VELETA 2;wind_speed;Avg (m/s)'], color='gold', label='ANEMO 2')
plt.plot(df['datetime'], df['VELETA 3;wind_speed;Avg (m/s)'], color='azure', label='ANEMO 3')
plt.plot(df['datetime'], df['VELETA 4;wind_speed;Avg (m/s)'], color='magenta', label='ANEMO 4')



# --[plot and point out the anomalies]-----------------------------------------
anomalies = df[df['is_anomaly'] == 1]
plt.plot(df['datetime'], df['is_anomaly'], color='red', label = 'is_anomaly')
plt.legend()
plt.show()
