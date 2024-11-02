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
query = "SELECT code, market FROM company_info"
company_info = pd.read_sql_query(query, engine)

# 데이터가 제대로 읽혀졌는지 확인
print(company_info)