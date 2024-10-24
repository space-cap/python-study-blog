from fastapi import FastAPI, Request
import requests
import re
from bs4 import BeautifulSoup  # BeautifulSoup 추가
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

app = FastAPI()

# Google Gemini API 키 가져오기
GOOGLE_API_KEY = "{여러분의 API 키}"

# URL을 추출하는 함수
def extract_url(text):
    url_pattern = r'(https?://[^\s]+)'  # http 또는 https로 시작하는 URL 패턴
    urls = re.findall(url_pattern, text)
    return urls[0] if urls else None

# HTML에서 텍스트를 추출하는 함수
def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')  # HTML 파싱
    return soup.get_text(separator='\n', strip=True)  # 텍스트 추출 및 정리

# 리스트를 텍스트로 변환하는 함수
def list_to_text(subtitle_list):
    # 리스트 내의 각 자막의 'text' 항목을 하나의 문자열로 변환하고 개행 처리
    return "\n".join([item['text'] for item in subtitle_list])

# LangChain을 사용해 요약하기 위한 함수
def summarize_text(text):
    # Gemini 모델과 LangChain 세팅
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)
    
    # 요약을 위한 프롬프트 템플릿 생성
    summary_prompt = PromptTemplate.from_template("아래의 내용을 요약해줘. 요약된 내용은 3개의 <p>를 사용해서 요약해줘.: {text}")
    
    # LangChain에서 요약 실행
    summary_chain = LLMChain(llm=llm, prompt=summary_prompt)
    summary = summary_chain.run(text=text)
    
    return summary

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
            if 'youtube.com' in url :
                id_yt = url.split("?v=")[1]

                url_subtitle = "https://youtube-v2.p.rapidapi.com/video/subtitles"

                querystring = {"video_id":id_yt}

                headers = {
                    "x-rapidapi-key": "{여러분의 api 키}",
                    "x-rapidapi-host": "youtube-v2.p.rapidapi.com"
                }

                response = requests.get(url_subtitle, headers=headers, params=querystring)

                response_text = list_to_text(response.json()["subtitles"])

            else:
                response = requests.get(url)
                response_text = response.text
            
            # HTML에서 텍스트 추출
            extracted_text = extract_text_from_html(response_text)
            print(extracted_text)
            
            # URL로 얻은 텍스트를 요약
            summary = summarize_text(extracted_text)

            summary2 = extract_text_from_html(summary)
        except requests.exceptions.RequestException as e:
            summary = f"URL 요청 중 오류 발생: {str(e)}"
    else:
        summary = "유효한 URL을 찾지 못했습니다."
    
    # 요약 결과 반환
    return {"response": f"{sender}에게 답장합니다: {summary2}"}
