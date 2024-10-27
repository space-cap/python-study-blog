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
df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'  
for page in range(1, int(last_page)+1):
    url = '{}&page={}'.format(sise_url, page)  
    html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
    df = df.append(pd.read_html(html, header=0)[0])
    time.sleep(2)  # 2초 동안 멈춤

print(df)


