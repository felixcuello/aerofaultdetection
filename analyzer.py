# -----------------------------------------------------------------------------
#
#  Analyzer
#
#  This script is used to analyze the data from the CSV file and detect the
#  anomalies. The anomalies are dump to STDOUT and also a plot image is generated
#  and saved to the disk (anomalies.png).
#
#  The analyzer works as follows:
#
#  1. Use K-means to find the "potential" outliers
#  2. Determine if it's an outlier by calculating an RMSE between the data and the
#     average.
#
# -----------------------------------------------------------------------------
import re
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
 
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 🟥 REMOVE THIS IF YOU NEED TO DEBUG THE CODE 🟥
import warnings
warnings.filterwarnings("ignore")


def main():
# --[Parse the input arguments]------------------------------------------------
    if len(sys.argv) < 3:
        print("\nUsage: python <input file> <column to be analyzed>".format(sys.argv[0]))
        sys.exit()


# --[Read the input CSV file]--------------------------------------------------
# low_memory=False is used to avoid the warning: DtypeWarning: Columns (1,2,3) have mixed types
#                  It takes more memory but it's more accurate
    log_info("Reading the input CSV file...")
    input_csv_file = sys.argv[1]
    input_column = sys.argv[2]
    df = pd.read_csv(input_csv_file, low_memory=False)

    # Calculate the number of columns matchig the input_column
    number_of_devices = 0
    for column in df.columns:
        regex_input_column = re.escape(input_column)
        regex_input_column = regex_input_column.replace('\{', r'{')
        regex_input_column = regex_input_column.replace('\}', r'}')
        regex_input_column = re.compile(regex_input_column.format(r'\d+'))

        if(regex_input_column.match(column)):
            number_of_devices += 1

    log_info("Found {} columns matching the columns to be analyzed".format(number_of_devices))

# --[Get only the anemometer readings]-----------------------------------------
    device_columns = []
    for i in range(1, number_of_devices):
        column = input_column.format(i)
        device_columns.append(column)


# --[STEP 1: Use K-means to find the "potential" outliers]---------------------
#
# The first step is to use k-means with k=1 to determine which is the device
# with the potential anomaly. However, this could not be accurate since the
# model always determine an anomaly (i.e. a device lecture that moves slightly
# from the rest of de devices' lectures is informed).
#
# This is due to how the k-means work, so later on we have to determine if the
# anomaly is a false positive or real.
#

# Set all the anomalies to -1 (no anomaly)
    device_data = df[device_columns]
    device_data['anomaly'] = -1

# Iterate over the data and find the anomalies for each anemometer
    log_info("Finding the anomalies (K-means)...")
    number_of_rows = len(device_data.index)
    for index, row in device_data.iterrows():
        if index % 1000 == 0: # Log every 1000 rows
            log_info("Processed {} / {} rows".format(index, number_of_rows))
        data = row[0:7].array.reshape(-1, 1) # Ignore anomaly & reshape

        # Standardize the data (mandatory)
        scaler = StandardScaler()
        standardized_data = scaler.fit_transform(data)

        # Apply kmeans (with k=1) to find the outliers
        k=1
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(standardized_data)

        # Find the outliers
        cluster_centers = kmeans.cluster_centers_
        distances = np.abs(standardized_data - cluster_centers[kmeans.labels_])
        outlier_indexes = np.where(np.argmax(distances) == np.arange(len(data)))[0]

        # Bear in mind that every row will have an outlier due to how k-means work.
        # So we need to check leter if the outlier is really an outlier or not.
        device_data.loc[index, 'datetime'] = df.loc[index, 'datetime']
        device_data.loc[index, 'anomaly'] = outlier_indexes[0]

    # Save the anomalies to an image
    image_name = 'anomaly_candidates.png'
    log_info("Saving candidate anomalies to '{}'...".format(image_name))
    plt.figure(figsize=(10,6))
    plt.title('Anomaly Candidates')

    colors = ['blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'cyan', 'magenta', 'black']
    np.random.shuffle(colors)
    for i in range(1, number_of_devices):
        column = input_column.format(i)
        plt.plot(device_data['datetime'], device_data[column], color=colors[i], label = column)

    plt.plot(device_data['datetime'], device_data['anomaly'], color='red', label = 'device number')
    plt.legend()
    plt.savefig(image_name)


# --[STEP 2: Determine if it's an outlier by calculating an RMSE]---------------
#
# For the step two we have introduced an ecuation similar to the RMSE to determine
# if the outliers calculated in STEP #1 are real outliers or false positives.
#
# --[Get only the anemometer readings]-----------------------------------------
    # device_readings = []
    # for i in range(1, number_of_devices):
    #     column = 'ANEMOMETRO {};wind_speed;Avg (m/s)'.format(i)
    #     device_readings.append(column)
    # device_data = df[device_readings]


# --# [Calculate the RMSE for each row]------------------------------------------
    # df['average'] = df[device_readings].mean(axis=1)
    # def calculate_rmse(row):
    #     rmse = 0
    #     for col in device_readings:
    #         rmse += (row[col] - row['average']) ** 2
    #     return np.sqrt(rmse / len(device_readings))
    # df['rmse'] = df.apply(calculate_rmse, axis=1)

# --# [Add a column to indicate if the row is an anomaly]-------------------------
    # df['is_anomaly'] = np.where(df['rmse'] >= 2, 1, 0) # 2 is an arbitrary threshold


# --# [Split the data into training and test sets]--------------------------------
    # start_time = time.time()
    # X = df[device_readings]
    # y = df['is_anomaly']
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=111)
    # print("[INFO] Splitting time: {:.2f} seconds".format(time.time() - start_time))


# --# [Train the model]----------------------------------------------------------
    # start_time = time.time()
    # model = RandomForestClassifier(n_estimators=100, random_state=42)
    # model.fit(X_train, y_train)
    # print("[INFO] Training time: {:.2f} seconds".format(time.time() - start_time))


# --# [Predict the anomalies in the test set]------------------------------------
    # start_time = time.time()
    # y_pred = model.predict(X_test)
    # print("[INFO] Prediction time: {:.2f} seconds".format(time.time() - start_time))


# --# [Get the model accuracy]---------------------------------------------------
    # accuracy = (y_pred == y_test).mean()
    # print(f'Accuracy: {accuracy}')


# --# [predict anomalies]--------------------------------------------------------
    # df['anomaly_pred'] = model.predict(X)


# --# [plot the anemometer readings]---------------------------------------------
    # plt.figure(figsize=(10,6))
    # plt.plot(df['datetime'], df['ANEMOMETRO 1;wind_speed;Avg (m/s)'], color='green', label='ANEMO 1')
    # plt.plot(df['datetime'], df['ANEMOMETRO 2;wind_speed;Avg (m/s)'], color='gold', label='ANEMO 2')
    # plt.plot(df['datetime'], df['ANEMOMETRO 3;wind_speed;Avg (m/s)'], color='azure', label='ANEMO 3')
    # plt.plot(df['datetime'], df['ANEMOMETRO 4;wind_speed;Avg (m/s)'], color='magenta', label='ANEMO 4')
    # plt.plot(df['datetime'], df['ANEMOMETRO 5;wind_speed;Avg (m/s)'], color='cadetblue', label='ANEMO 5')
    # plt.plot(df['datetime'], df['ANEMOMETRO 6;wind_speed;Avg (m/s)'], color='lime', label='ANEMO 6')
    # plt.plot(df['datetime'], df['ANEMOMETRO 7;wind_speed;Avg (m/s)'], color='cyan', label='ANEMO 7')
    # plt.plot(df['datetime'], df['ANEMOMETRO 8;wind_speed;Avg (m/s)'], color='lavender', label='ANEMO 8')



# --# [plot and point out the anomalies]-----------------------------------------
    # anomalies = df[df['is_anomaly'] == 1]
    # plt.plot(df['datetime'], df['is_anomaly'], color='red', label = 'is_anomaly')
    # plt.legend()
    # plt.show()


def log_info(string):
    print("[INFO] {}".format(string))

if __name__ == '__main__':
    main()
