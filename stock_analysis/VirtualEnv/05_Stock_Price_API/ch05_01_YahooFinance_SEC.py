import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import matplotlib.pylab as plt
import time
from scipy import stats
from datetime import datetime

start_date = datetime(2017,1,1) 
end_date = datetime(2019,12,31)

# yf.download을 사용하여 데이터를 불러오기
df = yf.download("005930.KS", start_date, end_date)

# 실제 열 이름 확인
print("Columns in DataFrame:", df.columns)

# MultiIndex의 첫 번째 레벨만 남기고 컬럼 이름을 간단하게 변경
df.columns = df.columns.get_level_values(0)

print("Columns in DataFrame:", df.columns)

# 그래프 설정
plt.figure(figsize=(9, 6))

# 종가와 수정 종가 라인 차트
plt.subplot(2, 1, 1) 
plt.title('Samsung Electronics (Yahoo Finance)')
if 'Close' in df.columns:
    plt.plot(df.index, df['Close'], 'c', label='Close')
if 'Adj Close' in df.columns:
    plt.plot(df.index, df['Adj Close'], 'b--', label='Adj Close')
plt.legend(loc='best')

# 거래량 바 차트
plt.subplot(2, 1, 2)
if 'Volume' in df.columns:
    plt.bar(df.index, df['Volume'], color='g', label='Volume')
plt.legend(loc='best')

plt.show()


