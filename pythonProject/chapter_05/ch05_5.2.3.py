import requests

# 업비트 API 엔드포인트 URL
url = 'https://api.upbit.com/v1/ticker'
# 원하는 암호화폐의 마켓 코드 (예: 비트코인)
market = 'KRW-BTC'

# API 요청 보내기
response = requests.get(url, params={'markets': market})
data = response.json()

# API 응답에서 원하는 데이터 추출
if data:
    btc_price = data[0]['trade_price']  # 비트코인의 현재 거래 가격
    print(f'비트코인 가격 (KRW): {btc_price}')
else:
    print('데이터를 가져오지 못했습니다.')


    