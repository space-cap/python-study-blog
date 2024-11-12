from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import pandas as pd

# chromedriver 경로 설정
driver_path = "D:/chromedriver/chromedriver-130/chromedriver.exe"
service = Service(executable_path=driver_path)

# Selenium 옵션 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 브라우저 창을 띄우지 않음
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Selenium WebDriver 초기화
driver = webdriver.Chrome(service=service, options=options)

try:
    # 웹페이지 열기
    url = "https://finance.naver.com/sise/etf.nhn"
    driver.get(url)

    # 페이지가 로드될 시간을 줌
    time.sleep(3)

    # 페이지 소스 가져오기
    html = driver.page_source

    # BeautifulSoup을 이용해 HTML 파싱
    bs = BeautifulSoup(html, "lxml")
    table = bs.find_all("table", class_="type_1 type_etf")
    df = pd.read_html(str(table), header=0)[0]

    # print(df)

    # 불필요한 열과 행을 삭제하고 인덱스를 재설정해서 출력
    df = df.drop(columns=['Unnamed: 9'])
    df = df.dropna()
    df.index = range(1, len(df)+1)
    print(df)

finally:
    # 드라이버 종료
    driver.quit()
