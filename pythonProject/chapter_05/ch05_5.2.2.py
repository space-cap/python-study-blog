import ccxt
import pandas as pd
import numpy as np
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from datetime import datetime, timedelta


# ccxt 라이브러리로 업비트 마켓 정보 가져오기
upbit = ccxt.upbit()
markets = upbit.load_markets()

# 원화 마켓 코인 필터링
krw_markets = [market for market in markets if market.startswith("KRW-")]

print(krw_markets)


# 현재 날짜와 1년 전 날짜 계산
end_date = datetime.now()
start_date = end_date - timedelta(days=365)



