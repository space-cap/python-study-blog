import ccxt
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# 사용할 거래소 설정 (예: Binance)
exchange = ccxt.binance()

# 1년 전 날짜 설정
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=365)

# 타임스탬프 변환
since = exchange.parse8601(start_date.strftime('%Y-%m-%dT%H:%M:%SZ'))

# 1. 비트코인 종가 데이터 가져오기
btc_symbol = "BTC/USDT"
btc_ohlcv = exchange.fetch_ohlcv(btc_symbol, '1d', since)
btc_df = pd.DataFrame(btc_ohlcv, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
btc_df["Date"] = pd.to_datetime(btc_df["Timestamp"], unit="ms")
btc_df.set_index("Date", inplace=True)
btc_close = btc_df["Close"]
print("비트코인 종가 데이터 (1년):")
print(btc_close)

# 2. 이더리움 종가 데이터 가져오기
eth_symbol = "ETH/USDT"
eth_ohlcv = exchange.fetch_ohlcv(eth_symbol, '1d', since)
eth_df = pd.DataFrame(eth_ohlcv, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
eth_df["Date"] = pd.to_datetime(eth_df["Timestamp"], unit="ms")
eth_df.set_index("Date", inplace=True)
eth_close = eth_df["Close"]
print("\n이더리움 종가 데이터 (1년):")
print(eth_close)

# 3. 비트코인과 이더리움 종가 데이터 병합 및 상관계수 계산
merged_df = pd.DataFrame({"BTC_Close": btc_close, "ETH_Close": eth_close})
correlation = merged_df.corr().iloc[0, 1]
print(f"\n비트코인과 이더리움 종가의 상관계수: {correlation}")

# 4. 두 종목의 가격을 표준화하여 시각화
scaler = StandardScaler()
standardized_prices = scaler.fit_transform(merged_df)
merged_df_std = pd.DataFrame(standardized_prices, index=merged_df.index, columns=["BTC_Standardized", "ETH_Standardized"])

# 시각화
plt.figure(figsize=(12, 6))
plt.plot(merged_df_std.index, merged_df_std["BTC_Standardized"], label="Bitcoin (Standardized)", color="blue")
plt.plot(merged_df_std.index, merged_df_std["ETH_Standardized"], label="Ethereum (Standardized)", color="orange")
plt.title("Standardized Prices of Bitcoin and Ethereum Over 1 Year")
plt.xlabel("Date")
plt.ylabel("Standardized Price")
plt.legend()
plt.grid(True)
plt.show()
