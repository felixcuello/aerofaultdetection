# --[libraries]----------------------------------------------------------------
import sys
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
for i in range(1,8):
    column = 'ANEMOMETRO {};wind_speed;Avg (m/s)'.format(i)
    anemometer_columns.append(column)
anemometer_data = df[anemometer_columns]


# --[Calculate the RMSE for each row]------------------------------------------
df['average'] = df[anemometer_columns].mean(axis=1)
def calculate_rmse(row):
    rmse = 0
    for col in anemometer_columns:
        rmse += (row[col] - row['average']) ** 2
    return np.sqrt(rmse / len(anemometer_columns))
df['rmse'] = df.apply(calculate_rmse, axis=1)


# --[Add a column to indicate if the row is an anomaly]-------------------------
df['is_anomaly'] = np.where(df['rmse'] >= 3, 1, 0) # 2 is an arbitrary threshold


# --[Split the data into training and test sets]--------------------------------
X = df[['average', 'rmse']]
y = df['is_anomaly']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


# --[Train the model]----------------------------------------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)


# --[Predict the anomalies in the test set]------------------------------------
y_pred = model.predict(X_test)


# --[Get the model accuracy]---------------------------------------------------
accuracy = (y_pred == y_test).mean()
print(f'Accuracy: {accuracy}')


# --[predict anomalies]--------------------------------------------------------
df['anomaly_pred'] = model.predict(X)


# --[plot the anemometer readings]---------------------------------------------
plt.figure(figsize=(10,6))
plt.plot(df['datetime'], df['ANEMOMETRO 1;wind_speed;Avg (m/s)'], color='green', label='ANEMO 1')
plt.plot(df['datetime'], df['ANEMOMETRO 2;wind_speed;Avg (m/s)'], color='gold', label='ANEMO 2')
plt.plot(df['datetime'], df['ANEMOMETRO 3;wind_speed;Avg (m/s)'], color='azure', label='ANEMO 3')
plt.plot(df['datetime'], df['ANEMOMETRO 4;wind_speed;Avg (m/s)'], color='magenta', label='ANEMO 4')
plt.plot(df['datetime'], df['ANEMOMETRO 5;wind_speed;Avg (m/s)'], color='cadetblue', label='ANEMO 5')
plt.plot(df['datetime'], df['ANEMOMETRO 6;wind_speed;Avg (m/s)'], color='lime', label='ANEMO 6')
plt.plot(df['datetime'], df['ANEMOMETRO 7;wind_speed;Avg (m/s)'], color='cyan', label='ANEMO 7')
plt.plot(df['datetime'], df['ANEMOMETRO 8;wind_speed;Avg (m/s)'], color='lavender', label='ANEMO 8')



# --[plot and point out the anomalies]-----------------------------------------
anomalies = df[df['is_anomaly'] == 1]
plt.plot(df['datetime'], df['is_anomaly'], color='red', label = 'is_anomaly')
plt.legend()
plt.show()
