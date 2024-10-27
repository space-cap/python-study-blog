import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import matplotlib.pylab as plt
import time
from scipy import stats
from datetime import datetime

start_date = datetime(2017,1,1) 
end_date = datetime(2017,1,31)

# yf.download을 사용하여 데이터를 불러오기
df = yf.download("005930.KS", start_date, end_date)

# 실제 열 이름 확인
print("Columns in DataFrame:", df.columns)

# 예시: 첫 번째 레벨 이름을 특정 열로 바꾸기
df.columns = df.columns.set_levels(['Adj Close', 'Open', 'High', 'Low', 'Close', 'Volume'], level=1)



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


(Py3810_32) C:\workdir\github-space-cap\python-study-blog\stock_analysis\VirtualEnv\05_Stock_Price_API>python ch05_01_YahooFinance_SEC.py
[*********************100%***********************]  1 of 1 completed
Columns in DataFrame: MultiIndex([('Adj Close', '005930.KS'),
            (    'Close', '005930.KS'),
            (     'High', '005930.KS'),
            (      'Low', '005930.KS'),
            (     'Open', '005930.KS'),
            (   'Volume', '005930.KS')],
           names=['Price', 'Ticker'])
Columns in DataFrame: MultiIndex([('Adj Close', 'Adj Close'),
            (    'Close', 'Adj Close'),
            (     'High', 'Adj Close'),
            (      'Low', 'Adj Close'),
            (     'Open', 'Adj Close'),
            (   'Volume', 'Adj Close')],
           names=['Price', 'Ticker'])
Traceback (most recent call last):
  File "ch05_01_YahooFinance_SEC.py", line 40, in <module>
    plt.bar(df.index, df['Volume'], color='g', label='Volume')
  File "C:\workdir\github-space-cap\python-study-blog\stock_analysis\VirtualEnv\Py3810_32\lib\site-packages\matplotlib\pyplot.py", line 2439, in bar
    return gca().bar(
  File "C:\workdir\github-space-cap\python-study-blog\stock_analysis\VirtualEnv\Py3810_32\lib\site-packages\matplotlib\__init__.py", line 1474, in inner
    return func(ax, *map(sanitize_sequence, args), **kwargs)
  File "C:\workdir\github-space-cap\python-study-blog\stock_analysis\VirtualEnv\Py3810_32\lib\site-packages\matplotlib\axes\_axes.py", line 2472, in bar
    r = mpatches.Rectangle(
  File "C:\workdir\github-space-cap\python-study-blog\stock_analysis\VirtualEnv\Py3810_32\lib\site-packages\matplotlib\_api\deprecation.py", line 454, in wrapper
    return func(*args, **kwargs)
  File "C:\workdir\github-space-cap\python-study-blog\stock_analysis\VirtualEnv\Py3810_32\lib\site-packages\matplotlib\patches.py", line 714, in __init__
    super().__init__(**kwargs)
  File "C:\workdir\github-space-cap\python-study-blog\stock_analysis\VirtualEnv\Py3810_32\lib\site-packages\matplotlib\_api\deprecation.py", line 454, in wrapper
    return func(*args, **kwargs)
  File "C:\workdir\github-space-cap\python-study-blog\stock_analysis\VirtualEnv\Py3810_32\lib\site-packages\matplotlib\patches.py", line 93, in __init__
    self.set_linewidth(linewidth)
  File "C:\workdir\github-space-cap\python-study-blog\stock_analysis\VirtualEnv\Py3810_32\lib\site-packages\matplotlib\patches.py", line 394, in set_linewidth
    self._linewidth = float(w)
TypeError: only size-1 arrays can be converted to Python scalars

(Py3810_32) C:\workdir\github-space-cap\python-study-blog\stock_analysis\VirtualEnv\05_Stock_Price_API>


















