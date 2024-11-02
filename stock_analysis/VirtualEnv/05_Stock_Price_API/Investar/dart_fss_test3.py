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

# 기업 리스트 가져오기
corp_list = dart.api.filings.get_corp_code()
print(corp_list)
