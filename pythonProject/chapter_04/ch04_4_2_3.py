import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 1. 비트코인의 1년간 일별 종가 데이터를 받아오는 함수
def fetch_ohlcv(symbol='BTC/USDT', timeframe='1d', days=365):
    exchange = ccxt.binance()
    since = exchange.parse8601((datetime.now() - timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%S'))
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df['close']

# 2. 1년간의 종가 데이터를 사용하여 30일간의 역사적 변동성을 계산
def calculate_historical_volatility(prices, window=30):
    log_returns = np.log(prices / prices.shift(1))
    rolling_std = log_returns.rolling(window).std()
    annualized_volatility = rolling_std * np.sqrt(365)
    return annualized_volatility

# 3. 데이터 시각화
def plot_volatility(volatility):
    plt.figure(figsize=(12, 6))
    plt.plot(volatility, color='blue', label='30-day Historical Volatility')
    plt.title('Bitcoin 30-Day Historical Volatility')
    plt.xlabel('Date')
    plt.ylabel('Volatility')
    plt.legend()
    plt.show()

# 데이터 가져오기
btc_close = fetch_ohlcv()

# 역사적 변동성 계산
btc_volatility = calculate_historical_volatility(btc_close)

# 시각화
plot_volatility(btc_volatility)
