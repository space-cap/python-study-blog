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

# 4. 표준화 함수: 데이터의 평균을 빼고 표준편차로 나눠서 표준화
def standardize_series(series):
    return (series - series.mean()) / series.std()

# 3 & 5. 데이터 시각화
def plot_standardized_prices_and_volatility(prices, volatility):
    standardized_prices = standardize_series(prices)
    standardized_volatility = standardize_series(volatility)

    plt.figure(figsize=(14, 7))
    plt.plot(standardized_prices, label='Standardized Close Price', color='green')
    plt.plot(standardized_volatility, label='Standardized 30-day Historical Volatility', color='blue')
    plt.title('Standardized Bitcoin Close Price and 30-Day Historical Volatility')
    plt.xlabel('Date')
    plt.ylabel('Standardized Value')
    plt.legend()
    plt.show()

# 데이터 가져오기
btc_close = fetch_ohlcv()

# 역사적 변동성 계산
btc_volatility = calculate_historical_volatility(btc_close)

# 시각화: 표준화된 종가와 변동성 비교
plot_standardized_prices_and_volatility(btc_close, btc_volatility)
