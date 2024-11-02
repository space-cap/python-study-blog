import yfinance as yf
import pandas as pd
import os
from sqlalchemy import create_engine
from datetime import datetime
from dotenv import load_dotenv

# .env 파일 불러오기
load_dotenv()

# 환경 변수 가져오기
db_password = os.getenv('DB_PASSWORD')
db_user = os.getenv('DB_USER')

# 주식 데이터 가져오기
tickers = {
    'samsung': '005930.KS',
    'naver': '035420.KS'
}

# 시작 및 종료 날짜 설정
start_date = '2020-01-01'
end_date = '2024-10-31'

# 모든 데이터 프레임을 저장할 딕셔너리 생성
stock_data = {}

# 각 티커에 대해 데이터를 가져오기
for name, ticker in tickers.items():
    stock_data[name] = yf.download(ticker, start=start_date, end=end_date)

# MariaDB 연결 정보 설정
host = 'localhost'  # 예: 'localhost' 또는 '127.0.0.1'
user = db_user      # 사용자 이름
password = db_password  # 비밀번호
database = 'investar'  # 데이터베이스 이름

# SQLAlchemy 엔진 생성
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

# 각 데이터 프레임을 MariaDB에 저장
for name, data in stock_data.items():
    table_name = f'{name}_stock_data'
    data.to_sql(table_name, con=engine, if_exists='replace', index=True)

print("삼성전자와 네이버 주가 데이터가 성공적으로 MariaDB에 저장되었습니다!")
