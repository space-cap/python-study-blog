import ccxt
import os
from dotenv import load_dotenv


# 다음은 업비트 API를 사용하여 계정 정보를 가져오는 코드입니다.

# .env 파일 불러오기
load_dotenv()

# 환경 변수 가져오기
# 업비트 API 키 설정
api_key = os.getenv('UPBIT_API_KEY')
api_secret = os.getenv('UPBIT_SECRET')

# 업비트 거래소 객체 생성
exchange = ccxt.upbit({
    'apiKey': api_key,
    'secret': api_secret,
})

try:
    # 계정 정보 가져오기
    account_info = exchange.fetch_balance()
    
    # 보유한 자산 출력
    for asset in account_info['total']:
        if account_info['total'][asset] > 0:
            print(f'자산: {asset}, 잔고: {account_info["total"][asset]}')
except Exception as e:
    print(f'에러 발생: {str(e)}')


