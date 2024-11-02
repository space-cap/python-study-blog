import yfinance as yf
import pymysql
import pandas as pd
import urllib3
import certifi
import requests
import os
import dart_fss
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine

# .env 파일 불러오기
load_dotenv()

# 환경 변수 가져오기
db_password = os.getenv('DB_PASSWORD')
db_user = os.getenv('DB_USER')
dart_api_key = os.getenv('DART_FSS_KEY')

# 1. SQLAlchemy를 사용하여 MariaDB 데이터베이스 연결
user = db_user              # MariaDB 사용자 이름
password = db_password      # MariaDB 비밀번호
host = 'localhost'          # MariaDB 호스트 (예: 'localhost')
port = 3306                 # 포트 번호 (기본값: 3306)
database = 'investar'       # 데이터베이스 이름

# MariaDB 연결 설정
conn = pymysql.connect(
    host='localhost',
    user=db_user,
    password=db_password,
    database='investar',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

# SQLAlchemy 연결 문자열을 생성
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# 2. company_info 테이블에서 모든 데이터를 읽기
query = "SELECT code, market FROM company_info LIMIT 2"
company_info = pd.read_sql_query(query, engine)

# 데이터가 제대로 읽혀졌는지 확인
# print(company_info)

start_date = datetime(2020,1,1) 
end_date = datetime(2024,12,31)

# MariaDB에 데이터 저장
def save_to_db(df, connection):
    with connection.cursor() as cursor:
        # 테이블이 없는 경우 생성
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_price_yahoo (
            ticker VARCHAR(10),
            date DATE,
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            adj_close FLOAT,
            volume BIGINT,
            PRIMARY KEY (ticker, date)
        )
        """)

        # 날짜 형식 변경하기
        df['date'] = df['date'].dt.date  # 날짜에서 시간 정보를 제거하여 순수한 날짜 형식으로 변경
        # df['Date'] = df['Date'].astype(str) # 날짜를 문자열로 변환

        # 데이터프레임의 각 행을 MariaDB에 저장
        for _, row in df.iterrows():
            sql = """
            REPLACE INTO daily_price_yahoo (ticker, date, open, high, low, close, adj_close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                row['ticker'], row['date'], row['open'], row['high'],
                row['low'], row['close'], row['adj_close'], row['volume']
            ))
        connection.commit()
        print("Data saved to database successfully.")  



# 4. 모든 code에 대해 데이터를 처리
for index, row in company_info.iterrows():
    code = row['code']
    market = row['market']

    if market == 'Y':
        code_suffix = '.KS'
    elif market == 'K':
        code_suffix = '.KQ'
    else:
        continue  # 다음 코드로 넘어감

    # 종목 코드 변환
    ticker = code + code_suffix
    print(f"Processing Ticker: {ticker}")

    try:
        # yfinance를 사용하여 일별 시세 데이터 가져오기
        df = yf.download(ticker, start_date, end_date, progress=False)
    except Exception as e:
        print(f"Failed to download data for ticker '{ticker}' due to: {e}")
    else:
        # 데이터프레임 열 이름을 DB에 맞게 변환
        # df.reset_index(inplace=True)
        df = df.reset_index()  # 인덱스를 초기화하여 'Date' 컬럼을 열로 변환
        df['Ticker'] = ticker  # ticker 컬럼 추가
        df = df[['Ticker', 'Date', 'Adj Close', 'Close', 'High', 'Low', 'Open', 'Volume']]
        df.columns = ['ticker', 'date', 'adj_close', 'close', 'high', 'low', 'open', 'volume']  # 컬럼 이름 변경
        
        # 데이터 저장 함수 호출
        save_to_db(df, conn)

# 데이터베이스 연결 닫기
conn.close()



