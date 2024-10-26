import pandas as pd
krx_list = pd.read_html('상장법인목록.xls')
print(krx_list[0])
