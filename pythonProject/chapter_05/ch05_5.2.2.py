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

ohlcv_data = [[], [], [], [], [], []]

# 모든 내부 리스트가 비어 있는지 확인
if all(not data for data in ohlcv_data):
    print("모든 데이터가 비어 있습니다.")
else:
    print("일부 데이터가 있습니다.")





