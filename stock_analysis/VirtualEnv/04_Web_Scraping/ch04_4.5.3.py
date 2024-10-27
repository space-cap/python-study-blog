import requests
import pandas as pd
import time
import mplfinance as mpf
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt

# 맨 뒤 페이지 숫자 구하기

url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
bs = BeautifulSoup(html, 'lxml')
pgrr = bs.find('td', class_='pgRR')
print(pgrr.a['href'])

s = str(pgrr.a['href']).split('=')
print(s)

last_page = s[-1]

print(last_page)


last_page = 2 # 테스트를 위해서 2로 수정

# 4.4.4 전체 페이지 읽어오기
df_list = []  # 빈 리스트 생성
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'  
for page in range(1, int(last_page) + 1):
    url = '{}&page={}'.format(sise_url, page)  
    html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
    
    # 페이지에서 데이터 읽어오기
    page_df = pd.read_html(html, header=0)[0]
    df_list.append(page_df)  # 데이터프레임을 리스트에 추가
    time.sleep(2)  # 2초 동안 멈춤

# 리스트에 있는 데이터프레임을 하나로 합치기
df = pd.concat(df_list, ignore_index=True)

# print(df)

# NaN 값 제거
df = df.dropna()  # NaN이 포함된 행을 제거합니다. # 값이 빠진 행을 제거한다.

# 차트 출력을 위해 데이터프레임 가공하기
df = df.iloc[0:30] # 최근 데이터 30행만 슬라이싱한다.

# 한글 칼럼명을 영문 칼럼명으로 변경한다.
df = df.rename(columns={'날짜':'Date', '시가':'Open', '고가':'High', '저가':'Low', '종가':'Close', '거래량':'Volume'})
df = df.sort_values(by='Date')
df.index = pd.to_datetime(df.Date) # Date 칼럼을 DatetimeIndex 형으로 변경한 후 인덱스로 설정한다.
df = df[['Open', 'High', 'Low', 'Close', 'Volume']] # Open, High, Low, Close, Volume 칼럼만 갖도록 데이터프레임 구조를 변경한다.

mpf.plot(df, title='Celltrion candle chart', type='candle')

mpf.plot(df, title='Celltrion ohlc chart', type='ohlc')

kwargs = dict(title='Celltrion customized chart', type='candle',
    mav=(2, 4, 6), volume=True, ylabel='ohlc candles')
mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
s  = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(df, **kwargs, style=s)



