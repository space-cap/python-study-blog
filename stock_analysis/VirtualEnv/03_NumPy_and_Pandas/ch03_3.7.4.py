import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
from scipy import stats
from datetime import datetime
import matplotlib.pylab as plt

# KOSPI와 다우존스 지수화 비교
# 날짜 설정
start_date = datetime(2024,1,1) 
end_date = datetime(2024,12,31)

# yf.download을 사용하여 데이터를 불러오기
dow = yf.download("^DJI", start_date, end_date)
kospi = yf.download("^KS11", start_date, end_date)

# 인덱스를 맞춘 후 DataFrame 생성
df = pd.concat([dow['Close'], kospi['Close']], axis=1, keys=['DOW', 'KOSPI'])
df = df.fillna(method='bfill')
df = df.fillna(method='ffill')

# NaN 값을 제거한 후 선형 회귀 수행
df = df.dropna()
regr = stats.linregress(df['DOW'], df['KOSPI'])
regr_line = f'Y = {regr.slope:2f} X + {regr.intercept:2f}'

# 그래프 생성
plt.figure(figsize=(7, 7))
plt.plot(df['DOW'], df['KOSPI'], '.') 
plt.plot(df['DOW'], regr.slope * df['DOW'] + regr.intercept, 'r')
plt.legend(['DOW x KOSPI', regr_line])
plt.title(f'DOW x KOSPI (R = {regr.rvalue:2f})')
plt.xlabel('Dow Jones Industrial Average')
plt.ylabel('KOSPI')
plt.show()
