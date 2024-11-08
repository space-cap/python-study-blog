import ccxt
import os
import pprint
from dotenv import load_dotenv

# 티커 조회
# https://wikidocs.net/179299
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

tickers = exchange.fetch_tickers()
# pprint.pprint(tickers)

# 티커 목록에서 원화 마켓만 필터링
symbols = tickers.keys()
krw_symbols = [x for x in symbols if x.endswith('KRW')]
print(krw_symbols)            # 리스트 출력
print(len(krw_symbols))     # 리스트에 원소 개수 출력


