import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import MeanShift
from sklearn.preprocessing import StandardScaler

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
anemometer_data['anomaly'] = 0

# --[Train the model]----------------------------------------------------------
for index, row in anemometer_data.iterrows():
    data = row.array.reshape(-1, 1)

    # It's mandatory to standardize the data
    scaler = StandardScaler()
    standardized_data = scaler.fit_transform(data)

    # Apply Meanshift
    k=2
    clustering = MeanShift(bandwidth=2).fit(standardized_data)
    clustering.labels_
    x = clustering.predict(standardized_data)
    import ipdb; ipdb.set_trace()
    
    

    # Find the outliers
    cluster_centers = kmeans.cluster_centers_
    distances = np.abs(standardized_data - cluster_centers[kmeans.labels_])
    outlier_indexes = np.where(np.argmax(distances) == np.arange(len(data)))[0]

    anemometer_data.loc[index, 'datetime'] = df.loc[index, 'datetime']
    anemometer_data.loc[index, 'anomaly'] = outlier_indexes[0]


# --[Predict the anomalies]-----------------------------------------------------
## Visualize the results
plt.figure(figsize=(10,6))
plt.plot(anemometer_data['datetime'], anemometer_data['ANEMOMETRO 1;wind_speed;Avg (m/s)'], color='blue', label = 'anemo1')
plt.plot(anemometer_data['datetime'], anemometer_data['anomaly'], color='red', label = 'anomaly')
plt.legend()
plt.show()

