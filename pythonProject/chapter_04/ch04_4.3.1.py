import pykrx
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

# 삼성전자의 오늘부터 1년 동안의 OHLCV와 펀더멘털 지표를 가져옵니다.
today = pd.Timestamp('2024-10-31')
ohlcv = pykrx.get_market_ohlcv_by_date('005930', start=today - pd.DateOffset(years=1), end=today)
fundamental = pykrx.get_market_fundamental_by_date('005930', start=today - pd.DateOffset(years=1), end=today)

# 종가와 PER를 이용하여 LSTM 모델을 만듭니다.
model = keras.models.Sequential([
    keras.layers.LSTM(50, activation='relu', input_shape=(ohlcv['종가'].shape[1], 1)),
    keras.layers.Dense(1)
])

# 모델을 컴파일합니다.
model.compile(optimizer='adam', loss='mean_squared_error')

# 모델을 학습합니다.
model.fit(ohlcv['종가'].values.reshape(-1, 1), ohlcv['종가'].shift(-1).values.reshape(-1, 1), epochs=100, batch_size=32)

# 내일부터 향후 일주일간 주가를 예측합니다.
predictions = model.predict(ohlcv['종가'].tail(7).values.reshape(-1, 1))

# 예측 결과를 시각화합니다.
plt.figure(figsize=(10, 5))
plt.plot(ohlcv['종가'].tail(7), label='실제 주가')
plt.plot(predictions, label='예측 주가')
plt.title('삼성전자 주가 예측')
plt.xlabel('날짜')
plt.ylabel('주가')
plt.legend()
plt.show()
