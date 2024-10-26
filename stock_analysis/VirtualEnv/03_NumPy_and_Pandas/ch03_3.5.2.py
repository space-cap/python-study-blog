import pandas_datareader as pdr
import yfinance as yf
from datetime import datetime

start_date = datetime(2024,1,1) 
end_date = datetime(2024,12,31)

# yf.download을 사용하여 데이터를 불러오기
kospi = yf.download("^KS11", start_date, end_date)
#print(kospi.head(10))

window = 252
peak = kospi['Adj Close'].rolling(window, min_periods=1).max()
drawdown = kospi['Adj Close']/peak - 1.0
max_dd = drawdown.rolling(window, min_periods=1).min()

import matplotlib.pyplot as plt

# Figure와 두 개의 subplot 생성
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7))

# 첫 번째 subplot: kospi의 종가를 표시
kospi['Close'].plot(ax=ax1, label='KOSPI', title='KOSPI MDD', grid=True, legend=True)

# 두 번째 subplot: drawdown과 max_dd를 표시
drawdown.plot(ax=ax2, c='blue', label='KOSPI DD', grid=True, legend=True)
max_dd.plot(ax=ax2, c='red', label='KOSPI MDD', grid=True, legend=True)

# 그래프 보여주기
plt.show()

