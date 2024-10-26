import pandas as pd
krx_list = pd.read_html('상장법인목록.xls')
krx_list[0].종목코드 = krx_list[0].종목코드.map('{:06d}'.format)

print(krx_list[0])
