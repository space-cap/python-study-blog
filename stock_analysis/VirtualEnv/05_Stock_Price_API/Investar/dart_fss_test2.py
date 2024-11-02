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
stock_code = '168360'

# 기업 리스트 가져오기
corp_list = dart.get_corp_list()

# 삼성전자 종목 코드로 기업 검색 (종목 코드: '005930')
samsung = corp_list.find_by_stock_code(stock_code)

# 기업 분류 정보 확인
corp_classification = samsung.info['corp_cls']

if corp_classification == 'Y':
    print("KOSPI에 상장되어 있습니다.")
elif corp_classification == 'K':
    print("KOSDAQ에 상장되어 있습니다.")
else:
    print("다른 시장에 상장되어 있습니다.")
