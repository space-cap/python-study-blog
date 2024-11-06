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

markdown_text = '''
This message is plain.
*This message is bold.*
`This message is code.`
_This message is italic._
~This message is strike.~
'''

attach_dict = {
    'color'      :'#ff0000',
    'author_name':'INVESTAR',
    "author_link":'https://github.com/INVESTAR',
    'title'      :'오늘의 증시 KOSPI',
    'title_link' :'http://finance.naver.com/sise/sise_index.nhn?code=KOSPI',
    'text'       :'2,326.13 △11.89 (+0.51%)',
    'image_url'  :'https://ssl.pstatic.net/imgstock/chart3/day/KOSPI.png'
}

attach_list = [attach_dict]

try:
    response = client.chat_postMessage(
        channel="#submarine",  # 메시지를 보낼 채널
        text=markdown_text,
        attachments=attach_list,
    )
    print(response)
except SlackApiError as e:
    print(f"Error: {e.response['error']}")
