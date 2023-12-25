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
#  3. Print a little report with the anomalies found.
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

    # colors used for plots
    colors = ['blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'lavender', 'cyan', 'magenta', 'black']

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

# --[Get only the device readings]-----------------------------------------
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

# Iterate over the data and find the anomalies for each device
    log_info("STEP #1 - Finding the anomalies (K-means)...")
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

    for i in range(1, number_of_devices):
        column = input_column.format(i)
        plt.plot(device_data['datetime'],
                 device_data[column],
                 color=colors[i],
                 label = column,
                 linewidth=0.3,
                 alpha=0.75)

    # plot and point out anomalies
    plt.plot(device_data['datetime'],
             device_data['anomaly'],
             color='red',
             label = 'Device # with anomaly',
             linewidth=0.4,
             alpha=1)

    # add legend and save graphic
    plt.legend()
    plt.savefig(image_name, dpi=1200)


# --[STEP 2: Determine if it's an outlier by calculating an RMSE]---------------
#
# For the step two we have introduced an ecuation similar to the RMSE to determine
# if the outliers calculated in STEP #1 are real outliers or false positives.
#

    log_info("STEP #2 - Getting actual anomalies")
    # Get only the device readings
    device_readings = []
    for i in range(1, number_of_devices):
        column = input_column.format(i)
        device_readings.append(column)


    # Calculate the RMSE for each row
    df['average'] = df[device_readings].mean(axis=1)

    # This calculates the RMSE for a given row
    def calculate_rmse(row):
        rmse = 0
        for col in device_readings:
            rmse += (row[col] - row['average']) ** 2
        return np.sqrt(rmse / len(device_readings))

    df['rmse'] = df.apply(calculate_rmse, axis=1)

    # Add a column to indicate if the row is an anomaly
    #
    # Note:
    #   We have found (empirically) that a threshold of 2 is a good value to
    #   determine if a row is an anomaly or not. However, this value could be
    #   changed if needed.
    #
    anomaly_threshold = 2
    df['is_anomaly'] = np.where(df['rmse'] >= anomaly_threshold, 1, 0) # 2 is an arbitrary threshold

    # Save the anomalies to an image
    image_name = 'anomalies_detected.png'
    log_info("Saving devices with errors to '{}'...".format(image_name))
    plt.figure(figsize=(10,6))

    for i in range(1, number_of_devices):
        column = input_column.format(i)
        plt.plot(df['datetime'],
                 df[column],
                 color=colors[i],
                 label = column,
                 linewidth=0.3,
                 alpha=0.75)

    # [plot and point out the anomalies]---------------------------------------
    anomalies = df[df['is_anomaly'] == 1]
    plt.plot(df['datetime'],
             df['is_anomaly'],
             color='red',
             label = 'Anomaly Detected',
             linewidth=0.4,
             alpha=1)

    # add legend and save graphic
    plt.legend()
    plt.savefig(image_name, dpi=1200)


# --[STEP 3: Print a little report with the anomalies found]-------------------
#
# This report tries to aglutinate all the information found in the two previous
# steps and print them out to STDOUT.
#

    devices_anomalies = {}
    for i in range(0, number_of_devices):
        devices_anomalies[i] = 0

    log_info("STEP #3 - Printing the report...")
    for i in range(0, number_of_rows):
        if df.loc[i, 'is_anomaly'] == 1:
            devices_anomalies[device_data.loc[i, 'anomaly']] += 1

    for i in range(0, number_of_devices):
        column = input_column.format(i)
        log_info("Device {} ({}): {} anomalies found".format(i, column, devices_anomalies[i]))

# Helper method to calculate the RMSE
def log_info(string):
    print("[INFO] {}".format(string))

if __name__ == '__main__':
    main()
