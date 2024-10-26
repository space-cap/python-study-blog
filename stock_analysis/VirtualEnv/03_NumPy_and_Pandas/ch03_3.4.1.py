from datetime import datetime 
from pandas_datareader import data as pdr
import yfinance as yf

start_date = datetime(2021,1,1) 
end_date = datetime(2021,12,31)

# yf.download을 사용하여 데이터를 불러오기
data = yf.download("AAPL", start="2022-01-01", end="2022-12-31")
print(data)
