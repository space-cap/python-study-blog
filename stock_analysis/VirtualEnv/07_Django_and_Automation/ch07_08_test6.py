import backtrader as bt
import yfinance as yf
import pandas as pd


class MyStrategy(bt.Strategy):
    
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
    
    def next(self):
        if self.order:
            return  # if an order is pending, don't do anything

        if not self.position:  # if not in the market
            if self.dataclose[0] > self.dataclose[-1]:  # if the current close is greater than the previous close
                self.buy()  # enter a long position
        else:
            if self.dataclose[0] < self.dataclose[-1]:  # if the current close is less than the previous close
                self.sell()  # exit the long position

cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)

# Add data feed to cerebro
df = yf.download("036570.KS", start="2024-01-01", end="2024-11-05")
print(df)

df = df.reset_index()  # 인덱스를 초기화하여 'Date' 열을 열로 변환
df.columns = ['date', 'adj_close', 'close', 'high', 'low', 'open', 'volume']  # 컬럼 이름 변경
print(df)

# df['date'] = pd.to_datetime([x[:-9] for x in df['date'].squeeze().tolist()], dayfirst=True)
df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d %H:%M:%S', dayfirst=True)
df.set_index('date', inplace=True)
print(df)




data = bt.feeds.PandasData(dataname=df)

# data = bt.feeds.PandasData(dataname= yf.download('TSLA','2018-01-01','2021-12-31'))

cerebro.adddata(data)

cerebro.run()
cerebro.plot()
