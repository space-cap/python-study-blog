from datetime import datetime 
import pandas_datareader as pdr
import yfinance as yf

print('pandas_datareader version: ' + pdr.__version__)

start_date = datetime(2021,1,1) 
end_date = datetime(2021,12,31)

# yf.download을 사용하여 데이터를 불러오기
sec = yf.download("005930.KS", start="2022-01-01", end="2022-12-31")
print(sec)


data = yf.download("AAPL", start="2022-01-01", end="2022-12-31")
print(data)