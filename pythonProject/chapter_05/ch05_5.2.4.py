import requests
import pandas as pd

# 업비트 API 엔드포인트 URL
url = 'https://api.upbit.com/v1/candles/minutes/30'
# 원하는 암호화폐의 마켓 코드 (예: 비트코인)
market = 'KRW-BTC'
# 데이터 조회 기간 설정 (최근 200분 데이터)
querystring = {'market': market, 'count': '200'}
response = requests.request('GET', url, params=querystring)
data = response.json()

# API 응답을 DataFrame으로 변환
df = pd.DataFrame(data)

# DataFrame을 시간 역순으로 정렬
df = df.iloc[::-1]

# 이동평균 계산 (단기 이동평균과 장기 이동평균)
short_window = 10
long_window = 50
df['Short_MA'] = df['trade_price'].rolling(window=short_window).mean()
df['Long_MA'] = df['trade_price'].rolling(window=long_window).mean()

# 매매 신호 계산
df['Signal'] = 0  # 0: 매매 없음, 1: 매수 신호, -1: 매도 신호

for i in range(long_window, len(df)):
    if df['Short_MA'][i] > df['Long_MA'][i] and df['Short_MA'][i - 1] <= df['Long_MA'][i - 1]:
        df['Signal'][i] = 1  # 단기 이동평균이 장기 이동평균을 상향 돌파하면 매수 신호
    elif df['Short_MA'][i] < df['Long_MA'][i] and df['Short_MA'][i - 1] >= df['Long_MA'][i - 1]:
        df['Signal'][i] = -1  # 단기 이동평균이 장기 이동평균을 하향 돌파하면 매도 신호

# 매매 신호 및 이동평균 데이터 출력
print(df[['candle_date_time_utc', 'trade_price', 'Short_MA', 'Long_MA', 'Signal']])

# 매매 신호를 기반으로 실제 매매를 추가로 구현해야 합니다.

'''
이 코드는 30분봉 데이터를 사용하여 이동평균 크로스오버 전략을 시뮬레이션하는 간단한 예제입니다. 
특정 전략에 따라 매매를 수행하는 부분은 아직 구현되어 있지 않으므로, 
이 부분을 해당 전략에 맞게 확장하고 실제 매매로 연결해야 합니다.
'''
