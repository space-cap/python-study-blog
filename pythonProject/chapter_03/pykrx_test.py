import pandas as pd
from pykrx import stock
from datetime import datetime, timedelta

# 삼성전자 종목코드
ticker = "005930"

# 오늘 날짜를 기준으로 1년 전 데이터 가져오기
end_date = datetime.today()
start_date = end_date - timedelta(days=365)
start_date_str = start_date.strftime("%Y%m%d")
end_date_str = end_date.strftime("%Y%m%d")

# 1년간의 OHLCV 데이터 가져오기
ohlcv_df = stock.get_market_ohlcv_by_date(start_date_str, end_date_str, ticker)

# 칼럼명 변경
ohlcv_df.columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Range']

# 1년간의 펀더멘털 데이터 가져오기
fundamental_df = stock.get_market_fundamental_by_date(start_date_str, end_date_str, ticker)

# OHLCV와 펀더멘털 데이터 병합
merged_df = pd.merge(ohlcv_df, fundamental_df, left_index=True, right_index=True)

# 인덱스 이름을 'Date'로 변경
merged_df.index.rename("Date", inplace=True)

# 결과 확인
print(merged_df.head())

# CSV 파일로 저장
merged_df.to_csv("samsung_electronics_data.csv", encoding="utf-8-sig")

print("데이터가 'samsung_electronics_data.csv' 파일로 저장되었습니다.")
