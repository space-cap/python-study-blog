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

