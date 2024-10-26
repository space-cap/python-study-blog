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

plt.figure(figsize=(9, 7))

# 첫 번째 subplot
ax1 = plt.subplot(211)
kospi['Close'].plot(ax=ax1, label='KOSPI', title='KOSPI MDD', grid=True, legend=True)

# 두 번째 subplot 생성 전에 명시적으로 제거
ax1.remove()

# 새로운 subplot 추가
ax2 = plt.subplot(212)
drawdown.plot(ax=ax2, c='blue', label='KOSPI DD', grid=True, legend=True)
max_dd.plot(ax=ax2, c='red', label='KOSPI MDD', grid=True, legend=True)

plt.show()


