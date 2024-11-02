import pandas as pd
import pandas_datareader as pdr
import yfinance as yf
import matplotlib.pylab as plt
import pymysql, calendar, time, json
import requests
import urllib3
from scipy import stats
from datetime import datetime
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
from threading import Timer

class DBUpdater:  
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', user='root',
            password='doolman', db='INVESTAR', charset='utf8')
        
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        db_url = 'mysql+pymysql://root:doolman@localhost/INVESTAR?charset=utf8'
        self.engine = create_engine(db_url)

        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS company_info (
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATE,
                PRIMARY KEY (code))
            """
            curs.execute(sql)
            sql = """
            CREATE TABLE IF NOT EXISTS daily_price (
                code VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                diff BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date))
            """
            curs.execute(sql)
        self.conn.commit()
        self.codes = dict()
    

    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()


    def read_krx_code(self):
        """KRX로부터 상장기업 목록 파일을 읽어와서 데이터프레임으로 반환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method='\
            'download&searchType=13'
        krx = pd.read_html(url, header=0)[0]
        krx = krx[['종목코드', '회사명']]
        krx = krx.rename(columns={'종목코드': 'code', '회사명': 'company'})
        krx.code = krx.code.map('{:06d}'.format)
        return krx


    def update_comp_info(self):
        """종목코드를 company_info 테이블에 업데이트 한 후 딕셔너리에 저장"""
        sql = "SELECT * FROM company_info"
        # df = pd.read_sql(sql, self.conn)
        df = pd.read_sql(sql, self.engine) # SQLAlchemy 엔진
        for idx in range(len(df)):
            self.codes[df['code'].values[idx]] = df['company'].values[idx]
                    
        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM company_info"
            curs.execute(sql)
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')
            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:
                krx = self.read_krx_code()
                for idx in range(len(krx)):
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]                
                    sql = f"REPLACE INTO company_info (code, company, last"\
                        f"_update) VALUES ('{code}', '{company}', '{today}')"
                    curs.execute(sql)
                    self.codes[code] = company
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] #{idx+1:04d} REPLACE INTO company_info "\
                        f"VALUES ({code}, {company}, {today})")
                self.conn.commit()
                print('')         


    def read_naver(self, code, company, pages_to_fetch):
        """네이버에서 주식 시세를 읽어서 데이터프레임으로 반환"""
        try:
            # https://remake.tistory.com/113
            # ssl 에러 메시지 숨김
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            # 세션을 사용하여 요청 시도 및 SSL 검증 무시
            session = requests.Session()
            session.verify = False
            url = f"http://finance.naver.com/item/sise_day.nhn?code={code}"
            
            response = session.get(url, headers={'User-agent': 'Mozilla/5.0'})
            html = response.text
            bs = BeautifulSoup(html, 'lxml')

            # last_page = int(str(pgrr.a['href']).split('=')[-1])
            # print(last_page)
            
            pgrr = bs.find('td', class_='pgRR')
            # print(pgrr.a['href'])
            s = str(pgrr.a['href']).split('=')
            # print(s)
            last_page = s[-1]
            # print("last_page: " , last_page)
            
            last_page = int(last_page)
            df_list = []
            pages = min(last_page, pages_to_fetch)
            
            pages = 1 # 임시로 1페이지만 읽기
            for page in range(1, pages+1):
                pg_url = f"{url}&page={page}"
                page_html = session.get(pg_url, headers={'User-agent': 'Mozilla/5.0'}).text
    
                # 페이지에서 데이터 읽어오기
                page_df = pd.read_html(page_html, header=0)[0]
                df_list.append(page_df)  # 데이터프레임을 리스트에 추가
                time.sleep(2)  # 2초 동안 멈춤

                tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                print(f'[{tmnow}] {company} ({code}) : {page:04d}/{pages:04d} pages are downloading...', end="\r")

            # 리스트에 있는 데이터프레임을 하나로 합치기
            df = pd.concat(df_list, ignore_index=True)

            # NaN 값 제거
            df = df.dropna()  # NaN이 포함된 행을 제거합니다. # 값이 빠진 행을 제거한다.

            # print(df)

            df = df.rename(columns={'날짜':'date','종가':'close','전일비':'diff'
                ,'시가':'open','고가':'high','저가':'low','거래량':'volume'})
            
            df['date'] = df['date'].replace('.', '-')

            # 숫자가 아닌 문자는 모두 제거하고 정수형으로 변환
            for col in ['close', 'diff', 'open', 'high', 'low', 'volume']:
                df[col] = df[col].astype(str).str.replace(r'[^0-9]', '', regex=True).astype(int)

            df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']]

        except Exception as e:
            print('Exception occurred:', str(e))
            return None

        return df


    def replace_into_db(self, df, num, code, company):
        """네이버에서 읽어온 주식 시세를 DB에 REPLACE"""
        with self.conn.cursor() as curs:
            for r in df.itertuples():
                sql = """
                    REPLACE INTO daily_price 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                # r의 각 필드를 정확하게 불러옵니다.
                curs.execute(sql, (code, r.date, r.open, r.high, r.low, r.close, r.diff, r.volume))
                
            self.conn.commit()

            print('[{}] #{:04d} {} ({}) : {} rows > REPLACE INTO daily_'\
                'price [OK]'.format(datetime.now().strftime('%Y-%m-%d'\
                ' %H:%M'), num+1, company, code, len(df)))


    def update_daily_price(self, pages_to_fetch):
        """KRX 상장법인의 주식 시세를 네이버로부터 읽어서 DB에 업데이트"""  
        for idx, code in enumerate(self.codes):
            try:
                # 네이버에서 주식 데이터를 읽어오기
                df = self.read_naver(code, self.codes[code], pages_to_fetch)
                if df is None:
                    print(f"[{self.codes[code]}] 데이터를 읽어오지 못했습니다.")
                    continue
                
                # DB에 데이터 업데이트
                self.replace_into_db(df, idx, code, self.codes[code])
            except Exception as e:
                print(f"오류 발생 - {self.codes[code]} ({code}): {e}")
                continue   


    def execute_daily(self):
        """실행 즉시 및 매일 오후 다섯시에 daily_price 테이블 업데이트"""
        # 회사 정보를 업데이트합니다.
        self.update_comp_info()

        try:
            # config.json 파일에서 pages_to_fetch 값을 읽어옵니다.
            with open('config.json', 'r') as in_file:
                config = json.load(in_file)
                pages_to_fetch = config.get('pages_to_fetch', 1)  # 기본값 100
        except (FileNotFoundError, json.JSONDecodeError):
            # 파일이 없거나 JSON 형식에 문제가 있을 경우, 기본값을 설정하고 파일을 생성합니다.
            pages_to_fetch = 1
            config = {'pages_to_fetch': pages_to_fetch}
            with open('config.json', 'w') as out_file:
                json.dump(config, out_file)
        
        # 주식 시세 업데이트
        self.update_daily_price(pages_to_fetch)

        # 다음 실행 시간 계산
        tmnow = datetime.now()
        lastday = calendar.monthrange(tmnow.year, tmnow.month)[1]

        # 매일 5시에 업데이트 스케줄 설정
        if tmnow.month == 12 and tmnow.day == lastday:
            tmnext = tmnow.replace(year=tmnow.year+1, month=1, day=1,
                hour=17, minute=0, second=0)
        elif tmnow.day == lastday:
            tmnext = tmnow.replace(month=tmnow.month+1, day=1, hour=17,
                minute=0, second=0)
        else:
            tmnext = tmnow.replace(day=tmnow.day+1, hour=17, minute=0,
                second=0)   

        # 다음 실행까지 대기 시간 설정
        tmdiff = tmnext - tmnow
        secs = tmdiff.total_seconds()  # 정확한 대기 시간을 계산합니다.
        t = Timer(secs, self.execute_daily)
        
        # 대기 메시지 출력
        print(f"Waiting for next update ({tmnext.strftime('%Y-%m-%d %H:%M')}) ...")
        t.start()



if __name__ == '__main__':
    dbu = DBUpdater()
    dbu.execute_daily()
    #dbu.read_naver('068270', '셀트리온', 1)

