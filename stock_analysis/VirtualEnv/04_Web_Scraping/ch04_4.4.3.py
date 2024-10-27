import requests
import pandas as pd
import time
from bs4 import BeautifulSoup

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

print(df)

# 차트 출력을 위해 데이터프레임 가공하기
df = df.dropna() # 값이 빠진 행을 제거한다.
df = df.iloc[0:30]
df = df.sort_values(by='날짜')










