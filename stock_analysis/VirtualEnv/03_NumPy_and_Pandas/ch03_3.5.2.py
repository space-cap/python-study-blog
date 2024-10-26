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
plt.subplot(211)
kospi['Close'].plot(label='KOSPI', title='KOSPI MDD', grid=True, legend=True)
plt.subplot(212)
drawdown.plot(c='blue', label='KOSPI DD', grid=True, legend=True)
max_dd.plot(c='red', label='KOSPI MDD', grid=True, legend=True)
plt.show()

