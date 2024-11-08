import ccxt
import os
import pprint
import pandas as pd
from dotenv import load_dotenv

# 시세 캔들 조회
# https://wikidocs.net/179304
# https://github.com/sharebook-kr/book-cryptocurrency-trading-with-python-ccxt/blob/main/Chapter_05/05_2_2.py
# https://github.com/sharebook-kr/pyupbit/blob/main/docs/upbit.md

# .env 파일 불러오기
load_dotenv()

# 환경 변수 가져오기
# 업비트 API 키 설정
api_key = os.getenv('UPBIT_API_KEY')
api_secret = os.getenv('UPBIT_SECRET')

# 업비트 거래소 객체 생성
exchange = ccxt.upbit({
    'apiKey': api_key,
    'secret': api_secret,
})



