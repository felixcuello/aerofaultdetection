import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential, Model

tf.random.set_seed(123) # TF Seed

columns = [
        'ANEMOMETRO 1;wind_speed;Avg (m/s)',
        'ANEMOMETRO 2;wind_speed;Avg (m/s)',
        'ANEMOMETRO 3;wind_speed;Avg (m/s)',
        'ANEMOMETRO 4;wind_speed;Avg (m/s)',
        'ANEMOMETRO 5;wind_speed;Avg (m/s)',
        'ANEMOMETRO 6;wind_speed;Avg (m/s)',
        'ANEMOMETRO 7;wind_speed;Avg (m/s)'
        ]

rows_without_problems = np.r_[
        1:2281,
        4617:7584,
        8968:10512
]

data = pd.read_csv('./data/D214102-2023.csv')
df = data[columns]
df = df.iloc[rows_without_problems]

train_data, test_data = train_test_split(df, test_size=0.2, shuffle=False)


# Step 3: Normalize the data
scaler = MinMaxScaler()
train_data_scaled = scaler.fit_transform(train_data)
test_data_scaled = scaler.transform(test_data)


# Step 4: Design the autoencoder architecture
input_dim = train_data_scaled.shape[1]
hidden_dim = 4  # You can adjust the number of nodes in the hidden layer as needed

autoencoder = Sequential()
autoencoder.add(Dense(hidden_dim, activation='relu', input_dim=input_dim))
autoencoder.add(Dense(input_dim, activation='linear'))


# Step 5: Train the autoencoder
autoencoder.compile(optimizer='adam', loss='mean_squared_error')
autoencoder.fit(train_data_scaled, train_data_scaled, epochs=100, batch_size=32, verbose=0)


# Step 6: Evaluate reconstruction error
train_data_pred = autoencoder.predict(train_data_scaled)
train_mse = np.mean(np.power(train_data_scaled - train_data_pred, 2), axis=1)


# Step 7: Define a threshold
threshold = np.mean(train_mse) + 3 * np.std(train_mse)  # Adjust the multiplier as needed


# Step 8: Detect anomalies
test_data_pred = autoencoder.predict(test_data_scaled)
test_mse = np.mean(np.power(test_data_scaled - test_data_pred, 2), axis=1)





import ipdb; ipdb.set_trace()

