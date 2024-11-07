import win32com.client

# 8.3.1 현재가 조회

# 크레온 플러스 공통 OBJECT
cpStock = win32com.client.Dispatch('DsCbo1.StockMst')

def get_current_price(code):
    """인자로 받은 종목의 현재가, 매도호가, 매수호가를 반환한다."""
    cpStock.SetInputValue(0, code)  # 종목코드에 대한 가격 정보
    cpStock.BlockRequest()
    
    item = {}
    item['cur_price'] = cpStock.GetHeaderValue(11)   # 현재가
    item['ask'] =  cpStock.GetHeaderValue(16)        # 매도호가
    item['bid'] =  cpStock.GetHeaderValue(17)        # 매수호가    
    
    return item['cur_price'], item['ask'], item['bid']

result = get_current_price('A305080')
print(result)
