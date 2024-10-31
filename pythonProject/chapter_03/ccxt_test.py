import ccxt
import pandas as pd
from datetime import datetime, timedelta

# 사용하려는 거래소 선택 (예: Binance)
exchange = ccxt.binance()

# 비트코인/USDT 페어, 1년 전 시작 날짜 설정
symbol = "BTC/USDT"
timeframe = "1d"  # 일봉 데이터
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=365)

# 타임스탬프로 변환
since = exchange.parse8601(start_date.strftime('%Y-%m-%dT%H:%M:%SZ'))

# OHLCV 데이터를 가져와서 DataFrame으로 변환
ohlcv_data = []
while since < exchange.parse8601(end_date.strftime('%Y-%m-%dT%H:%M:%SZ')):
    # 한 번에 가져올 수 있는 제한된 데이터만큼 가져옴
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit=1000)
    if not ohlcv:
        break
    ohlcv_data += ohlcv
    since = ohlcv[-1][0] + 24 * 60 * 60 * 1000  # 마지막 데이터 이후로 1일 추가

# DataFrame으로 변환 및 컬럼명 추가
df = pd.DataFrame(ohlcv_data, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
df["Date"] = pd.to_datetime(df["Timestamp"], unit="ms")
df.set_index("Date", inplace=True)
df.drop("Timestamp", axis=1, inplace=True)

# 등락률 계산
df['Change'] = (df['Close'] - df['Open']) / df['Open']

print(df.head())

# CSV 파일로 저장
df.to_csv("bitcoin_ohlcv_data.csv", encoding="utf-8-sig")

print("데이터가 'bitcoin_ohlcv_data.csv' 파일로 저장되었습니다.")
