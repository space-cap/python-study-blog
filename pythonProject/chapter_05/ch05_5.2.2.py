import ccxt
import pandas as pd
import numpy as np
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from datetime import datetime, timedelta


import os
from dotenv import load_dotenv

# .env 파일 불러오기
load_dotenv()

# 환경 변수 가져오기
# 업비트 API 키 설정
api_key = os.getenv('UPBIT_API_KEY')
api_secret = os.getenv('UPBIT_SECRET')

# 업비트 거래소 객체 생성
upbit = ccxt.upbit({
    'apiKey': api_key,
    'secret': api_secret,
})

# ccxt 라이브러리로 업비트 마켓 정보 가져오기
tickers = upbit.fetch_tickers()

# 티커 목록에서 원화 마켓만 필터링
symbols = tickers.keys()
krw_symbols = [x for x in symbols if x.endswith('KRW')]

# print(krw_symbols)

# 현재 날짜와 1년 전 날짜 계산
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

selected_cryptos = []

selected_cryptos = []
            
# 각 코인에 대해 OHLCV 데이터 가져오기 및 조건 검토
for market in krw_symbols:
    ohlcv = upbit.fetch_ohlcv(market, timeframe='1d', since=int(start_date.timestamp() * 1000))

    # 모든 내부 리스트가 비어 있는지 확인
    if all(not data for data in ohlcv):
        print(f"{market} 모든 데이터가 비어 있습니다.")
        continue
    # else:
    #     print(f"{market} 일부 데이터가 있습니다.")

    # OHLCV 데이터를 DataFrame으로 변환
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    # 이동평균선 계산
    df['ma7'] = df['close'].rolling(window=7).mean()
    df['ma30'] = df['close'].rolling(window=30).mean()
    df['ma90'] = df['close'].rolling(window=90).mean()

    print('종목:', market)





