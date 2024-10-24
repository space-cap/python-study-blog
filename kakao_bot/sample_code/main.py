#main: 메아리봇(그냥 하는 말 따라하는 봇), main.py라는 파일을 만들어서 붙여넣기
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/reply")
async def reply_message(request: Request):
    data = await request.json()  # JSON 데이터를 수신 및 파싱
    
    room = data.get("room")
    msg = data.get("msg")
    sender = data.get("sender")

    # 수신한 데이터 출력 (로그 기록용)
    print(f"방: {room}, 발신자: {sender}, 메시지: {msg}")
    
    # 필요한 경우, 응답 메시지를 반환
    return {"response": f"{sender}에게 답장합니다: {msg}"}
