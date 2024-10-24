from fastapi import FastAPI, Request
import requests
import re  # 정규식을 위한 모듈

app = FastAPI()

# URL을 추출하는 함수
def extract_url(text):
    url_pattern = r'(https?://[^\s]+)'  # http 또는 https로 시작하는 URL 패턴
    urls = re.findall(url_pattern, text)
    return urls[0] if urls else None

@app.post("/reply")
async def reply_message(request: Request):
    data = await request.json()  # JSON 데이터를 수신 및 파싱
    
    room = data.get("room")
    msg = data.get("msg")
    sender = data.get("sender")

    # 수신한 데이터 출력 (로그 기록용)
    print(f"방: {room}, 발신자: {sender}, 메시지: {msg}")

    # 메시지에서 URL 추출
    url = extract_url(msg)
    
    if url:
        try:
            response = requests.get(url)
            data = response.text
        except requests.exceptions.RequestException as e:
            data = f"URL 요청 중 오류 발생: {str(e)}"
    else:
        data = "유효한 URL을 찾지 못했습니다."
    
    # 필요한 경우, 응답 메시지를 반환
    return {"response": f"{sender}에게 답장합니다: {data}"}
