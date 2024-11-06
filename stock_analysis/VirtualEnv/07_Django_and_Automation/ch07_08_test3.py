import datetime
import backtrader as bt
import yfinance as yf
import pandas as pd

# yfinance를 사용하여 데이터 다운로드
df = yf.download("036570.KS", start="2024-01-01", end="2024-11-05")
df = df.reset_index()  # 인덱스를 초기화하여 'Date' 열을 열로 변환
df['Date'] = df['Date'].dt.date  # 날짜에서 시간 정보를 제거하여 순수한 날짜 형식으로 변경
# 'Date' 열을 datetime 객체로 변환
df['Date'] = pd.to_datetime(df['Date'])

df = df[['Date', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']]
df.columns = ['date', 'adj_close', 'close', 'high', 'low', 'open', 'volume']  # 컬럼 이름 변경

print(df)

# 데이터를 Backtrader 피드로 변환
data_feed = bt.feeds.PandasData(dataname=df)

# 전략 정의
class RSIStrategy(bt.Strategy):
    params = (('rsi_period', 14), ('rsi_overbought', 70), ('rsi_oversold', 30))

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.params.rsi_period)

    def next(self):
        if self.position.size == 0:  # 포지션이 없을 때
            if self.rsi < self.params.rsi_oversold:  # 매수 신호
                self.buy()
            elif self.rsi > self.params.rsi_overbought:  # 매도 신호
                self.sell()
        elif self.position.size > 0:  # 포지션이 있을 때
            if self.rsi > self.params.rsi_overbought:  # RSI가 과매수 상태이면 매도
                self.sell()
        elif self.position.size < 0:  # 공매도 포지션일 때
            if self.rsi < self.params.rsi_oversold:  # RSI가 과매도 상태이면 매수
                self.buy()

# Backtrader 설정
cerebro = bt.Cerebro()
cerebro.addstrategy(RSIStrategy)
cerebro.adddata(data_feed)
cerebro.broker.set_cash(10000000)  # 초기 자산 설정
cerebro.run()
cerebro.plot()
