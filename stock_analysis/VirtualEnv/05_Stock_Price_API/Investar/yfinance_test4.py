import yfinance as yf
import pymysql
import pandas as pd
import urllib3
import certifi
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

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


