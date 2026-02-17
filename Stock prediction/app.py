import os
import warnings

# Keep TensorFlow startup logs quieter and disable oneDNN optimization notice.
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
warnings.filterwarnings(
    "ignore",
    message=r".*tf\.reset_default_graph is deprecated.*",
)

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

tf.get_logger().setLevel("ERROR")

st.set_page_config(page_title="Stock Price Prediction")

st.title("📈 Stock Price Prediction using LSTM")

stock = st.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, TCS.NS)", "AAPL")

if st.button("Predict"):

    # Fetch Data
    df = yf.download(stock, start="2015-01-01", end="2024-12-31")

    if df.empty:
        st.error("Invalid stock symbol")
    else:
        st.subheader("Stock Data")
        st.write(df.tail())

        # Use only Closing price
        data = df[['Close']].values

        # Scale data
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data = scaler.fit_transform(data)

        # Prepare training data
        x_train = []
        y_train = []

        for i in range(60, len(scaled_data)):
            x_train.append(scaled_data[i-60:i, 0])
            y_train.append(scaled_data[i, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # Build LSTM Model
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
        model.add(LSTM(units=50))
        model.add(Dense(1))

        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(x_train, y_train, epochs=1, batch_size=32)

        # Prepare Test Data (Last 60 days)
        test_data = scaled_data[-60:]
        x_test = []
        x_test.append(test_data[:,0])
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1],1))

        predicted_price = model.predict(x_test)
        predicted_price = scaler.inverse_transform(predicted_price)

        st.subheader("📊 Predicted Next Closing Price")
        st.write(f"Predicted Price: ${predicted_price[0][0]:.2f}")

        # Plot
        st.subheader("📈 Stock Closing Price History")
        fig, ax = plt.subplots()
        ax.plot(df['Close'])
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        st.pyplot(fig)
