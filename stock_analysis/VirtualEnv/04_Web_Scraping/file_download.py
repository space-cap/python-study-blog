import requests

# POST 요청을 보낼 URL
url = 'https://kind.krx.co.kr/corpgeneral/corpList.do'

# POST 요청에 필요한 데이터 (예시로 비워둡니다)
payload = {
    # 필요한 데이터 입력
    # 'param_name': 'param_value',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage&searchType13',
    'Origin': 'https://kind.krx.co.kr'
}

# POST 요청 보내기
response = requests.post(url, data=payload)

# 응답 확인
if response.status_code == 200:
    # 파일 이름 설정 (필요시)
    filename = 'downloaded_file.xls'  # 저장할 파일 이름

    # 파일로 저장
    with open(filename, 'wb') as f:
        f.write(response.content)
    
    print(f"파일이 성공적으로 다운로드되었습니다: {filename}")
else:
    print(f"요청 실패: {response.status_code}")
