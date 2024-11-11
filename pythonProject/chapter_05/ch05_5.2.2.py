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

    # 정배열 조건 확인
    last_row = df.iloc[-1]
    if last_row['ma7'] > last_row['ma30'] > last_row['ma90']:

        # 볼린저 밴드 계산
        df['stddev'] = df['close'].rolling(window=20).std()

        # 볼린저 밴드 계산 (데이터가 충분한지 확인)
        if df['ma30'].notna().all() and df['stddev'].notna().all():
            df['upper_band'] = df['ma30'] + (df['stddev'] * 2)
            df['lower_band'] = df['ma30'] - (df['stddev'] * 2)
        else:
            print(f"{market}에 대해 충분한 데이터가 없어 볼린저 밴드를 계산할 수 없습니다.")
            continue  # 다음 코인으로 넘어감

        # 볼린저 밴드 조건 확인
        if last_row['close'] < last_row['upper_band']:
            selected_cryptos.append(market)

    print('종목:', market)

# 결과 출력
if selected_cryptos:
    print("조건에 맞는 암호화폐 리스트:")
    for crypto in selected_cryptos:
        print(crypto)
else:
    print("조건에 맞는 암호화폐가 없습니다.")



