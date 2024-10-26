import pandas_datareader as pdr
import yfinance as yf
import pandas as pd
from datetime import datetime

# KOSPI와 다우존스 지수화 비교

start_date = datetime(2024,1,1) 
end_date = datetime(2024,12,31)

# yf.download을 사용하여 데이터를 불러오기
dow = yf.download("^DJI", start_date, end_date)
kospi = yf.download("^KS11", start_date, end_date)

d = (dow.Close / dow.Close.loc['2024-01-01']) * 100
k = (kospi.Close / kospi.Close.loc['2024-01-01']) * 100

import matplotlib.pyplot as plt
plt.figure(figsize=(9, 5))
plt.plot(dow.index, d, 'r--', label='Dow Jones Industrial')
plt.plot(kospi.index, k, 'b', label='KOSPI')
plt.grid(True)
plt.legend(loc='best')
plt.show()
