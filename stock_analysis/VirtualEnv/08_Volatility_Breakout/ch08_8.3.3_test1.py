import win32com.client
import pandas as pd
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from datetime import datetime

# 8.3.3 주식 잔고 조회

# 크레온 플러스 공통 OBJECT
cpTradeUtil = win32com.client.Dispatch('CpTrade.CpTdUtil') # 주문 관련 도구
cpBalance = win32com.client.Dispatch('CpTrade.CpTd6033') # 계좌 정보
cpCodeMgr = win32com.client.Dispatch('CpUtil.CpStockCode') # 종목코드

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
        # print(response)
    except SlackApiError as e:
        print(f"Error: {e.response['error']}")

def printlog(message, *args):
    """인자로 받은 문자열을 파이썬 셸에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message, *args)

def get_stock_balance(code):
    """인자로 받은 종목의 종목명과 수량을 반환한다."""
    cpTradeUtil.TradeInit()
    acc = cpTradeUtil.AccountNumber[0]      # 계좌번호
    accFlag = cpTradeUtil.GoodsList(acc, 1) # -1:전체, 1:주식, 2:선물/옵션
    cpBalance.SetInputValue(0, acc)         # 계좌번호
    cpBalance.SetInputValue(1, accFlag[0])  # 상품구분 - 주식 상품 중 첫번째
    cpBalance.SetInputValue(2, 50)          # 요청 건수(최대 50)
    cpBalance.BlockRequest()     
    
    if code == 'ALL':
        dbgout('계좌명: ' + str(cpBalance.GetHeaderValue(0)))
        dbgout('결제잔고수량 : ' + str(cpBalance.GetHeaderValue(1)))
        dbgout('평가금액: ' + str(cpBalance.GetHeaderValue(3)))
        dbgout('평가손익: ' + str(cpBalance.GetHeaderValue(4)))
        dbgout('종목수: ' + str(cpBalance.GetHeaderValue(7)))
    
    stocks = []
    for i in range(cpBalance.GetHeaderValue(7)):
        stock_code = cpBalance.GetDataValue(12, i)  # 종목코드
        stock_name = cpBalance.GetDataValue(0, i)   # 종목명
        stock_qty = cpBalance.GetDataValue(15, i)   # 수량
        if code == 'ALL':
            dbgout(str(i+1) + ' ' + stock_code + '(' + stock_name + ')' 
                + ':' + str(stock_qty))
            stocks.append({'code': stock_code, 'name': stock_name, 
                'qty': stock_qty})
        if stock_code == code:  
            return stock_name, stock_qty
    
    if code == 'ALL':
        return stocks
    else:
        stock_name = cpCodeMgr.CodeToName(code)
        return stock_name, 0

result = get_stock_balance('A305080')
print(result)

result2 = get_stock_balance('ALL')
print(result2)


