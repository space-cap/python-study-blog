import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from datetime import datetime

# 8.2.5 로그 메시지 출력

# .env 파일 불러오기
load_dotenv()

# 환경 변수 가져오기
SLACK_BOT_TOKEN = os.getenv('SLACK_BOT_TOKEN_tradingview')

# Slack Bot Token 설정
client = WebClient(token=SLACK_BOT_TOKEN)

def dbgout(message):
    """인자로 받은 문자열을 파이썬 셸과 슬랙으로 동시에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
    #slack.chat.post_message('#etf-algo-trading', strbuf)
    try:
        response = client.chat_postMessage(
            channel="#tradingview",  # 메시지를 보낼 채널
            text=strbuf,
        )
        print(response)
    except SlackApiError as e:
        print(f"Error: {e.response['error']}")

def printlog(message, *args):
    """인자로 받은 문자열을 파이썬 셸에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message, *args)


dbgout('this is test log.')

