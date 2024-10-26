from datetime import datetime 
import pandas_datareader as pdr
import yfinance as yf

print('pandas_datareader version: ' + pdr.__version__)

start_date = datetime(2021,1,1) 
end_date = datetime(2021,12,31)

# yf.download을 사용하여 데이터를 불러오기
sec = yf.download("005930.KS", start="2022-01-01", end="2022-12-31")
#print(sec)
sec_dpc = (sec['Close']-sec['Close'].shift(1)) / sec['Close'].shift(1) * 100
sec_dpc.iloc[0] = 0 # 일간 변동률의 첫 번째 값인 NaN을 0으로 변경한다.
sec_dpc_cp = ((100+sec_dpc)/100).cumprod()*100-100 # 일간 변동률 누적곱 계산

msft = yf.download("AAPL", start="2022-01-01", end="2022-12-31")
#print(msft)
msft_dpc = (msft['Close'] / msft['Close'].shift(1) -1) * 100
msft_dpc.iloc[0] = 0
msft_dpc_cp = ((100+msft_dpc)/100).cumprod()*100-100

import matplotlib.pyplot as plt
plt.plot(sec.index, sec_dpc_cp, 'b', label='Samsung Electronics')
plt.plot(msft.index, msft_dpc_cp, 'r--', label='Microsoft')
plt.ylabel('Change %') 
plt.grid(True)
plt.legend(loc='best')
plt.show()

