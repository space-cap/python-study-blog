import yfinance as yf

# 삼성전자의 데이터를 불러오기
ticker = "005930.KS"
stock = yf.Ticker(ticker)

# 주식 정보 출력
print(stock.info)

# 과거 주가 데이터 가져오기
data = stock.history(period="1mo")
print(data)
