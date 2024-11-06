import yfinance as yf
import backtrader as bt
import pandas as pd


class MyStrategy(bt.Strategy):  # ①
    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close)  # ②
    def next(self):  # ③
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()

cerebro = bt.Cerebro()  # ④
cerebro.addstrategy(MyStrategy)

# data = bt.feeds.PandasData(dataname=yf.download('036570.KS', '2017-01-01', '2019-12-01', auto_adjust=True))
df = yf.download("036570.KS", start="2024-01-01", end="2024-11-05")
df = df.reset_index()  # 인덱스를 초기화하여 'Date' 열을 열로 변환
df.columns = ['date', 'adj_close', 'close', 'high', 'low', 'open', 'volume']  # 컬럼 이름 변경
df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d %H:%M:%S', dayfirst=True)
df.set_index('date', inplace=True)
data = bt.feeds.PandasData(dataname=df)

cerebro.adddata(data)
cerebro.broker.setcash(10000000)  # ⑥
cerebro.addsizer(bt.sizers.SizerFix, stake=30)  # ⑦

print(f'Initial Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.run()  # ⑧
print(f'Final Portfolio Value   : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.plot()  # ⑨


