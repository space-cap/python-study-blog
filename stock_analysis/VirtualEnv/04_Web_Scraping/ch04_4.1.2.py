import pandas as pd
krx_list = pd.read_html('상장법인목록.xls')
krx_list[0].종목코드 = krx_list[0].종목코드.map('{:06d}'.format)
#print(krx_list[0])


# KRX 기업 리스트 페이지 URL
url = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage&searchType13'

# URL에서 HTML 테이블 읽어오기
dfs = pd.read_html(url)

# 발견된 테이블 수 확인
print(f"발견된 테이블 수: {len(dfs)}")

# 첫 번째 테이블이 존재하는 경우 표시
if dfs:
    df = dfs[0]  # 첫 번째 테이블 선택
    print(df.head())  # DataFrame의 첫 몇 행 출력
    print(df.columns)  # DataFrame의 열 이름 출력
else:
    print("테이블을 찾을 수 없습니다.")
    
#df = dfs[0]
#df[0].종목코드 = df[0].종목코드.map('{:06d}'.format)
#df = df.sort_values(by='종목코드')
#print(df)
