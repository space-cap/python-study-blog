import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# .env 파일 불러오기
load_dotenv()

# 환경 변수 가져오기
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN')

# Slack Bot Token 설정
client = WebClient(token=SLACK_BOT_TOKEN)

try:
    response = client.chat_postMessage(
        channel="#submarine",  # 메시지를 보낼 채널
        text="Hello from your bot!"
    )
    print(response)
except SlackApiError as e:
    print(f"Error: {e.response['error']}")
