import datetime
import backtrader as bt
import yfinance as yf
import pandas as pd
import numpy as np
from tensorflow import Sequential
from tensorflow import Dense, LSTM, Dropout


# yfinance를 사용하여 데이터 다운로드
df = yf.download("005930.KS", start="2023-01-01", end="2024-11-05")
df = df.reset_index()  # 인덱스를 초기화하여 'Date' 열을 열로 변환
df['Date'] = pd.to_datetime(df['Date'],format='%Y-%m-%d %H:%M:%S')

df = df[['Date', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']]
df.columns = ['date', 'adj_close', 'close', 'high', 'low', 'open', 'volume']  # 컬럼 이름 변경

# print(df)

def MinMaxScaler(data):
    """최솟값과 최댓값을 이용하여 0 ~ 1 값으로 변환"""
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    # 0으로 나누기 에러가 발생하지 않도록 매우 작은 값(1e-7)을 더해서 나눔
    return numerator / (denominator + 1e-7)

dfx = df[['open','high','low','volume', 'close']]
# print(dfx)
dfx = MinMaxScaler(dfx)
dfy = dfx[['close']]

x = dfx.values.tolist()
y = dfy.values.tolist()

# 데이터셋 준비하기
window_size = 10 
data_size = 5

data_x = []
data_y = []
for i in range(len(y) - window_size):
    _x = x[i : i + window_size] # 다음 날 종가(i+windows_size)는 포함되지 않음
    _y = y[i + window_size]     # 다음 날 종가
    data_x.append(_x)
    data_y.append(_y)
print(_x, "->", _y)

# 훈련용 데이터셋과 테스트용 데이터셋 분리
train_size = int(len(data_y) * 0.7)
train_x = np.array(data_x[0 : train_size])
train_y = np.array(data_y[0 : train_size])

test_size = len(data_y) - train_size
test_x = np.array(data_x[train_size : len(data_x)])
test_y = np.array(data_y[train_size : len(data_y)])

# 모델 생성
model = Sequential()
model.add(LSTM(units=10, activation='relu', return_sequences=True, input_shape=(window_size, data_size)))
model.add(Dropout(0.1))
model.add(LSTM(units=10, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(units=1))
model.summary()

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(train_x, train_y, epochs=60, batch_size=30)
pred_y = model.predict(test_x)
