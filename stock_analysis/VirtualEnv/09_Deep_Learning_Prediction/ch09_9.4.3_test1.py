import datetime
import backtrader as bt
import yfinance as yf
import pandas as pd
import numpy as np

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


