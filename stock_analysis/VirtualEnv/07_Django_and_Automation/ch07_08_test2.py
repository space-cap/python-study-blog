import datetime
import backtrader as bt
import yfinance as yf

# Download data using yfinance
df = yf.download("036570.KS", start="2024-01-01", end="2024-11-05")
df = df.reset_index()  # 인덱스를 초기화하여 'Date' 컬럼을 열로 변환
df['Date'] = df['Date'].dt.date  # 날짜에서 시간 정보를 제거하여 순수한 날짜 형식으로 변경

# print(df)

# Convert data to Backtrader feed
data_feed = bt.feeds.PandasData(dataname=df)

# Define the strategy
class RSIStrategy(bt.Strategy):
    params = (('rsi_period', 14), ('rsi_overbought', 70), ('rsi_oversold', 30))

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.params.rsi_period)

    def next(self):
        if self.position.size == 0:  # If not in position
            if self.rsi < self.params.rsi_oversold:  # Buy signal
                self.buy()
            elif self.rsi > self.params.rsi_overbought:  # Sell signal
                self.sell()
        elif self.position.size > 0:  # If holding a position
            if self.rsi > self.params.rsi_overbought:  # Exit if RSI indicates overbought
                self.sell()
        elif self.position.size < 0:  # If short
            if self.rsi < self.params.rsi_oversold:  # Exit if RSI indicates oversold
                self.buy()

# Set up Backtrader
cerebro = bt.Cerebro()
cerebro.addstrategy(RSIStrategy)
cerebro.adddata(data_feed)
cerebro.broker.set_cash(10000000)  # Set initial portfolio value
cerebro.run()
cerebro.plot()

