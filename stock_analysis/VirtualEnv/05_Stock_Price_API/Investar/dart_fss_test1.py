import dart_fss
import os
from dotenv import load_dotenv

# .env 파일 불러오기
load_dotenv()

# 환경 변수 가져오기
dart_api_key = os.getenv('DART_FSS_KEY')

# OpenDart API 키 설정
dart_fss.set_api_key(dart_api_key)

# 상장된 종목 리스트 가져오기
corp_list = dart_fss.get_corp_list()

# 예시: 삼성전자 정보 가져오기
samsung = corp_list.find_by_corp_name('삼성전자', exactly=True)
print(samsung.to_dict())
