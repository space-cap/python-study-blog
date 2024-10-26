import pandas as pd

# pip install pandas==2.0.3
s = pd.Series([0.0,3.6,2.0,5.8,4.2,8.0]) # 리스트로 시리즈 생성
print(s)

#3.2.2 시리즈의 인덱스 변경
s.index = pd.Index([0.0,1.2,1.8,3.0,3.6,4.8]) # 인덱스 변경
s.index.name = 'my_idx' # 인덱스명 설정
print(s)
