import dart_fss as dart
import os
import pandas as pd
from dotenv import load_dotenv

# .env 파일 불러오기
load_dotenv()

# 환경 변수 가져오기
dart_api_key = os.getenv('DART_FSS_KEY')

# OpenDart API 키 설정
dart.set_api_key(dart_api_key)

# 삼성전자 종목 코드 (005930)
samsung_stock_code = '005930'

# 종목 정보 가져오기
stock_info = dart.get_stock_info(samsung_stock_code)

# 시장 구분 확인
if stock_info['market'] == 'KOSPI':
    print("삼성전자는 KOSPI에 상장되어 있습니다.")
elif stock_info['market'] == 'KOSDAQ':
    print("삼성전자는 KOSDAQ에 상장되어 있습니다.")
else:
    print("삼성전자는 KOSPI 또는 KOSDAQ에 상장되어 있지 않습니다.")
