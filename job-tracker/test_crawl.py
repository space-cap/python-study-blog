import requests
import json

# 크롤링 API 테스트
url = "http://127.0.0.1:8000/api/jobs/crawl"
data = {
    "url": "https://www.saramin.co.kr/zf_user/search/recruit?searchType=search&searchword=개발자"
}

response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response:", response.json())