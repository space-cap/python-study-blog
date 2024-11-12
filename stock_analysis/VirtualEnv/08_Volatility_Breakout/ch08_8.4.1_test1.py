from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


# ch08_02_DynamicPageScraping_NaverETF.py
# 네이버 금융에서 ETF 종목을 가져오는 함수

# 옵션값 설정
opt = webdriver.ChromeOptions()
opt.add_argument('headless')

# 웹드라이버를 통해 네이버 금융 ETF 페이지에 접속
drv = webdriver.Chrome(executable_path='D:\\chromedriver\\chromedriver-130\\chromedriver.exe', chrome_options=opt)
drv.implicitly_wait(3)
drv.get('https://finance.naver.com/sise/etf.nhn')

# 뷰티풀 수프로 테이블을 스크래핑
bs = BeautifulSoup(drv.page_source, 'lxml')
drv.quit()
table = bs.find_all("table", class_="type_1 type_etf")
df = pd.read_html(str(table), header=0)[0]

print(df)



