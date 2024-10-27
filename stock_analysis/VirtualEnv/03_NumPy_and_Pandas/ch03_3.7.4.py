import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
from scipy import stats
from datetime import datetime
import matplotlib.pylab as plt

# KOSPI와 다우존스 지수화 비교
# 날짜 설정
start_date = datetime(2000,1,4) 
end_date = datetime(2024,12,31)

# yf.download을 사용하여 데이터를 불러오기
dow = yf.download("^DJI", start_date, end_date)
kospi = yf.download("^KS11", start_date, end_date)

# 데이터를 병합하여 인덱스가 일치하도록 DataFrame 생성
df = pd.concat([dow['Close'], kospi['Close']], axis=1, keys=['X', 'Y'])
df = df.fillna(method='bfill')
df = df.fillna(method='ffill')

# print(df.head())  # 데이터 확인

# NaN 값 제거
df = df.dropna()

# 열 이름 변경
df.columns = ['X', 'Y']

# 데이터 유형 및 결측치 확인
print(df[['X', 'Y']].info())  # 결측치가 없고 float64 타입인지 확인

# 선형 회귀 수행
regr = stats.linregress(df['X'], df['Y'])
regr_line = f'Y = {regr.slope:.2f} X + {regr.intercept:.2f}'

# 그래프 생성
plt.figure(figsize=(7, 7))
plt.plot(df['X'], df['Y'], '.')
plt.plot(df['X'], regr.slope * df['X'] + regr.intercept, 'r')
plt.legend(['DOW x KOSPI', regr_line])
plt.title(f'DOW x KOSPI (R = {regr.rvalue:.2f})')
plt.xlabel('Dow Jones Industrial Average')
plt.ylabel('KOSPI')
plt.show()

