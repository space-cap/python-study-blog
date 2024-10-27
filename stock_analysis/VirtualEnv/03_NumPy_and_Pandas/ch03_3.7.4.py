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

# 데이터를 병합하여 인덱스가 일치하도록 DataFrame 생성
df = pd.concat([dow['Close'], kospi['Close']], axis=1, keys=['X', 'Y'])
df = df.fillna(method='bfill')
df = df.fillna(method='ffill')

# print(df.head())  # 데이터 확인

# 선형 회귀 수행
regr = stats.linregress(df.X, df.Y)
regr_line = f'Y = {regr.slope:2f}  X + {regr.intercept:2f}'

(Py3810_32) C:\workdir\github-space-cap\python-study-blog\stock_analysis\VirtualEnv\03_NumPy_and_Pandas>python ch03_3.7.4.py
[*********************100%***********************]  1 of 1 completed
[*********************100%***********************]  1 of 1 completed
Traceback (most recent call last):
  File "ch03_3.7.4.py", line 25, in <module>
    regr = stats.linregress(df.X, df.Y)
  File "C:\workdir\github-space-cap\python-study-blog\stock_analysis\VirtualEnv\Py3810_32\lib\site-packages\scipy\stats\_stats_mstats_common.py", line 166, in linregress
    ssxm, ssxym, _, ssym = np.cov(x, y, bias=1).flat
ValueError: too many values to unpack (expected 4)
