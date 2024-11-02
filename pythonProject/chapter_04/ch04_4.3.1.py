import pandas as pd
import numpy as np
import tensorflow as tf
from pykrx import stock
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from datetime import datetime, timedelta

# 삼성전자 종목 코드
ticker = '005930'

# 날짜 범위 설정
days = 365
today = datetime.today()
start_date = (today - timedelta(days=days)).strftime('%Y%m%d')
end_date = today.strftime('%Y%m%d')

# OHLCV 데이터
ohlcv = stock.get_market_ohlcv_by_date(start_date, end_date, ticker)
# 펀더멘털 데이터
fundamental = stock.get_market_fundamental_by_date(start_date, end_date, ticker)

# OHLCV와 펀더멘털 데이터 병합
#data = pd.concat([ohlcv, fundamental[['BPS', 'PER', 'PBR', 'EPS', 'DIV', 'DPS']]], axis=1)
#data.dropna(inplace=True)
data = pd.concat([ohlcv, fundamental], axis=1)

# 데이터 전처리 및 분할
train_data = data[['종가','PER']]
print(train_data)

# 정규화
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

# 시퀀스 데이터 생성
def create_sequences(data, seq_length):
    x = []
    y = []
    for i in range(len(data) - seq_length-1):
        x.append(data[i:(i+seq_length),:])
        y.append(data[i+seq_length, 0])

    return np.array(x), np.array(y)


seq_length = 30
x, y = create_sequences(scaled_data, seq_length)

print(x)

# LSTM 모델 구축 및 학습
model = Sequential()
input_shape = (x.shape[1], x.shape[2])
model.add(LSTM(units=100, return_sequences=True, input_shape=input_shape))
model.add(Dropout(0.2))
model.add(LSTM(units=100, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(100))
model.add(Dense(1))

# 모델 컴파일 및 학습
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x, y, epochs=100, batch_size=16)

# 일주일간 주가 예측
n_day = 7
predictions = []

for _ in range(n_day):
    last_seq = scaled_data[-seq_length:]
    last_seq = last_seq.reshape(1, seq_length, 2)
    prediction = model.predict(last_seq)
    predictions.append(prediction[0, 0])

    new_seq = np.array([[prediction[0, 0], last_seq[0, -1, 1]]])  # 종가 예측값과 PER의 마지막 값을 사용
    scaled_data = np.concatenate((scaled_data, new_seq), axis=0)















