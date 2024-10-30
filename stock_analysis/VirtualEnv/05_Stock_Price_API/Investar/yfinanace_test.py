import yfinance as yf
import pymysql
import pandas as pd
import urllib3
from datetime import datetime
import os
from dotenv import load_dotenv

os.environ['REQUESTS_CA_BUNDLE'] = 'D:\workdir\github-space-cap\python-study-blog\stock_analysis\VirtualEnv\05_Stock_Price_API\Investar'


# SSL 경고 비활성화
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# .env 파일 불러오기
load_dotenv()

# 환경 변수 가져오기
db_password = os.getenv('DB_PASSWORD')
db_user = os.getenv('DB_USER')


# MariaDB 연결 설정
db_connection = pymysql.connect(
    host='localhost',
    user=db_user,
    password=db_password,
    database='investar',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

start_date = datetime(2024,1,1) 
end_date = datetime(2024,12,31)

# 삼성전자 종목코드 (Yahoo Finance에서는 '005930.KS')
ticker = '005930.KS'

try:
    # yfinance를 사용하여 삼성전자 일별 시세 데이터 가져오기
    df = yf.download(ticker, start_date, end_date, progress=False)
except Exception as e:
    print(f"Failed to download data for ticker '{ticker}' due to: {e}")
else:
    # 데이터프레임 열 이름을 DB에 맞게 변환
    df.reset_index(inplace=True)
    df = df.rename(columns={
        'Date': 'date',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Adj Close': 'adj_close',
        'Volume': 'volume'
    })
    df['ticker'] = ticker  # ticker 컬럼 추가

    # MariaDB에 데이터 저장
    def save_to_db(df, connection):
        with connection.cursor() as cursor:
            # 테이블이 없는 경우 생성
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_price (
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

            # 데이터프레임의 각 행을 MariaDB에 저장
            for _, row in df.iterrows():
                sql = """
                REPLACE INTO daily_price (ticker, date, open, high, low, close, adj_close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    row['ticker'], row['date'], row['open'], row['high'],
                    row['low'], row['close'], row['adj_close'], row['volume']
                ))
            connection.commit()
            print("Data saved to database successfully.")

    # 데이터 저장 함수 호출
    save_to_db(df, db_connection)

# 데이터베이스 연결 닫기
db_connection.close()
