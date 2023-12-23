import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

if len(sys.argv) < 2:
    print("\nUsage: python {} <input_csv_file>".format(sys.argv[0]))
    sys.exit()

TIMES_OUTLIER_THRESHOLD = 15

# --[Read the input CSV file]--------------------------------------------------
input_csv_file = sys.argv[1]
df = pd.read_csv(input_csv_file)


# --[Get only the anemometer readings]-----------------------------------------
anemometer_columns = []
for i in range(1,8):
    column = 'ANEMOMETRO {};wind_speed;Avg (m/s)'.format(i)
    anemometer_columns.append(column)

anemometer_data = df[anemometer_columns]
anemometer_data['anomaly'] = 0

# --[Train the model]----------------------------------------------------------
last_outlier = -1
times_outlier = 0
for index, row in anemometer_data.iterrows():
    data = row[0:7].array.reshape(-1, 1) # Ignore anomaly & reshape

    # It's mandatory to standardize the data
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(data)

    # Apply kmeans
    k=1
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(standardized_data)

    # Find the outliers
    cluster_centers = kmeans.cluster_centers_
    distances = np.abs(standardized_data - cluster_centers[kmeans.labels_])
    outlier_indexes = np.where(np.argmax(distances) == np.arange(len(data)))[0]

    anemometer_data.loc[index, 'datetime'] = df.loc[index, 'datetime']
    anemometer_data.loc[index, 'anomaly'] = outlier_indexes[0]

    if outlier_indexes[0] != last_outlier:
        times_outlier += 1
    else:
        times_outlier = 0

    if times_outlier > TIMES_OUTLIER_THRESHOLD:
        print("Outlier {} detected at time: {}".format(outlier_indexes[0], df.loc[index, 'datetime']))

    times_outlier += 1
    last_outlier = outlier_indexes[0]


# --[Predict the anomalies]-----------------------------------------------------
## Visualize the results
plt.figure(figsize=(10,6))
plt.plot(anemometer_data['datetime'], anemometer_data['ANEMOMETRO 1;wind_speed;Avg (m/s)'], color='blue', label = 'anemo1')
plt.plot(anemometer_data['datetime'], anemometer_data['ANEMOMETRO 2;wind_speed;Avg (m/s)'], color='green', label = 'anemo2')
plt.plot(anemometer_data['datetime'], anemometer_data['anomaly'], color='red', label = 'anomaly')
plt.legend()
plt.show()

