import datetime
import backtrader as bt
import yfinance as yf

# yfinance를 사용하여 데이터 다운로드
df = yf.download("036570.KS", start="2024-01-01", end="2024-11-05")
df = df.reset_index()  # 인덱스를 초기화하여 'Date' 열을 열로 변환
df['Date'] = df['Date'].dt.date  # 날짜에서 시간 정보를 제거하여 순수한 날짜 형식으로 변경

df = df[['Date', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']]
df.columns = ['date', 'adj_close', 'close', 'high', 'low', 'open', 'volume']  # 컬럼 이름 변경

print(df)

