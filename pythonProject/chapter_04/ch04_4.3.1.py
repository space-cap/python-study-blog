import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pykrx import stock
from datetime import datetime, timedelta
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler


# 1. 삼성전자의 1년간 OHLCV 및 펀더멘털 데이터 가져오기
def get_samsung_data(days=365):
    today = datetime.today()
    start_date = (today - timedelta(days=days)).strftime('%Y%m%d')
    end_date = today.strftime('%Y%m%d')

    # OHLCV 데이터
    ohlcv = stock.get_market_ohlcv_by_date(start_date, end_date, "005930")
    # 펀더멘털 데이터
    fundamental = stock.get_market_fundamental_by_date(start_date, end_date, "005930")

    # OHLCV와 펀더멘털 데이터 병합
    data = pd.concat([ohlcv, fundamental[['BPS', 'PER', 'PBR', 'EPS', 'DIV', 'DPS']]], axis=1)
    data.dropna(inplace=True)
    return data


# 2. 종가와 PER을 이용한 데이터 준비 및 LSTM 모델을 사용하여 주가 예측
def prepare_data(data, target='종가', feature='PER', window_size=30, forecast_horizon=7):
    data = data[[target, feature]]

    # 정규화
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    # LSTM 학습용 데이터 준비
    x_train, y_train = [], []
    for i in range(len(scaled_data) - window_size - forecast_horizon + 1):
        x_train.append(scaled_data[i:i + window_size])
        y_train.append(scaled_data[i + window_size:i + window_size + forecast_horizon, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    return x_train, y_train, scaler


def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50))
    model.add(Dense(7))
    model.compile(optimizer='adam', loss='mse')
    return model


# 데이터 가져오기
data = get_samsung_data()

# 데이터 준비 및 스케일링
window_size = 30
forecast_horizon = 7
x_train, y_train, scaler = prepare_data(data, window_size=window_size, forecast_horizon=forecast_horizon)

# LSTM 모델 구축 및 학습
model = build_lstm_model((x_train.shape[1], x_train.shape[2]))
model.fit(x_train, y_train, epochs=20, batch_size=16, verbose=1)


# 3. 예측 및 시각화
def forecast_next_week(model, data, scaler, window_size=30):
    last_sequence = data[-window_size:]
    last_sequence_scaled = scaler.transform(last_sequence)
    last_sequence_scaled = np.expand_dims(last_sequence_scaled, axis=0)

    forecast_scaled = model.predict(last_sequence_scaled)
    forecast = scaler.inverse_transform(
        np.concatenate([forecast_scaled, np.zeros((forecast_scaled.shape[0], 1))], axis=1))[:, 0]
    return forecast


# 내일부터 일주일간 예측
forecast = forecast_next_week(model, data[['종가', 'PER']].values, scaler, window_size)

# 시각화
plt.figure(figsize=(12, 6))
plt.plot(data.index[-100:], data['종가'].values[-100:], label="Actual Price")
plt.plot(pd.date_range(data.index[-1] + timedelta(days=1), periods=7, freq='B'), forecast, label="Predicted Price",
         linestyle='--', color='red')
plt.title("Samsung Electronics Stock Price Prediction (Next 7 Days)")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.show()
