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
user = db_user       # MariaDB 사용자 이름
password = db_password   # MariaDB 비밀번호
host = 'localhost'           # MariaDB 호스트 (예: 'localhost')
port = 3306                  # 포트 번호 (기본값: 3306)
database = 'investar'   # 데이터베이스 이름

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
query = "SELECT code, company FROM company_info"
company_info = pd.read_sql_query(query, engine)

# 데이터가 제대로 읽혀졌는지 확인
print(company_info)

# 3. DART-FSS 라이브러리를 사용하여 KOSPI, KOSDAQ 구분
dart = dart_fss.auth.set_api_key(api_key=dart_api_key)  # DART API 키 설정
corp_list = dart_fss.corp.get_corp_list()

today = datetime.today().strftime('%Y-%m-%d')

# 4. 모든 code에 대해 데이터를 처리
with conn.cursor() as cursor:
    for index, row in company_info.iterrows():
        code = row['code']
        company = row['company']

        # 종목 코드로 기업 검색 (종목 코드: '005930')
        corp = corp_list.find_by_stock_code(code)

        # 기업 분류 정보 확인
        # market : str or list of str, optional
        # 'Y': 코스피, 'K': 코스닥, 'N': 코넥스, 'E': 기타
        corp_classification = corp.info['corp_cls']

        if corp_classification == 'Y':
            code_suffix = '.KS'
        elif corp_classification == 'K':
            code_suffix = '.KQ'
        else:
            print(f"Warning: {company}/{code}/{corp_classification} 의 시장 구분을 찾을 수 없습니다.")
            # continue  # 다음 코드로 넘어감

        # 종목 코드 변환
        ticker = code + code_suffix
        print(f"Processing Ticker: {ticker}")

        sql = f"REPLACE INTO company_info (code, company, last_update, market) "\
            f" VALUES ('{code}', '{company}', '{today}', '{corp_classification}')"
        cursor.execute(sql)

    conn.commit()
    print("Data saved to database successfully.")

# 데이터베이스 연결 닫기
conn.close()


