import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from pykrx import stock
from datetime import datetime, timedelta



# 삼성전자 코드
code = '005930'

days=365
today = datetime.today()
start_date = (today - timedelta(days=days)).strftime('%Y%m%d')
end_date = today.strftime('%Y%m%d')

# OHLCV 데이터
df_ohlcv = stock.get_market_ohlcv_by_date(start_date, end_date, "005930")

# 펀더멘털 지표 가져오기 (pykrx에서는 펀더멘털 지표를 직접 제공하지 않으므로, 별도의 API나 데이터베이스에서 가져와야 합니다.)
# 예시:
# df_fundamentals = get_fundamentals_data(code)  # 가상의 함수
# 펀더멘털 데이터
df_fundamentals = stock.get_market_fundamental_by_date(start_date, end_date, "005930")

# 데이터 합치기
df = pd.concat([df_ohlcv, df_fundamentals], axis=1)

# 필요한 컬럼만 선택
df = df[['Close', 'PER']]

# 결측치 처리
df.fillna(method='ffill', inplace=True)

print(df.head())






