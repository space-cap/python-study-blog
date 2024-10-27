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

regr = stats.linregress(df.X, df.Y)
regr_line = f'Y = {regr.slope:2f}  X + {regr.intercept:2f}'

plt.figure(figsize=(7, 7))
plt.plot(df.X, df.Y, '.') 
plt.plot(df.X, regr.slope * df.X + regr.intercept, 'r')
plt.legend(['DOW x KOSPI', regr_line])
plt.title(f'DOW x KOSPI (R = {regr.rvalue:2f})')
plt.xlabel('Dow Jones Industrial Average')
plt.ylabel('KOSPI')
plt.show()

(Py3810_32) C:\workdir\github-space-cap\python-study-blog\stock_analysis\VirtualEnv\03_NumPy_and_Pandas>python ch03_3.7.4.py
[*********************100%***********************]  1 of 1 completed
[*********************100%***********************]  1 of 1 completed
Traceback (most recent call last):
  File "ch03_3.7.4.py", line 23, in <module>
    regr = stats.linregress(df.X, df.Y)
  File "C:\workdir\github-space-cap\python-study-blog\stock_analysis\VirtualEnv\Py3810_32\lib\site-packages\pandas\core\generic.py", line 5989, in __getattr__
    return object.__getattribute__(self, name)
AttributeError: 'DataFrame' object has no attribute 'X'
