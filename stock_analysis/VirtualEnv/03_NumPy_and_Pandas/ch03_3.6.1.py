import pandas_datareader as pdr
import yfinance as yf
import pandas as pd
from datetime import datetime

start_date = datetime(2024,1,1) 
end_date = datetime(2024,12,31)

# yf.download을 사용하여 데이터를 불러오기
dow = yf.download("^DJI", start_date, end_date)
kospi = yf.download("^KS11", start_date, end_date)

# 인덱스를 맞춘 후 DataFrame 생성
df = pd.concat([dow['Close'], kospi['Close']], axis=1, keys=['DOW', 'KOSPI'])
#print(df)

import matplotlib.pyplot as plt
plt.figure(figsize=(9, 5))
plt.plot(dow.index, dow.close, 'r--', label='Dow Jones Industrial')
plt.plot(kospi.index, kospi.close, 'b', label='KOSPI')
plt.grid(True)
plt.legend(loc='best')
plt.show()
