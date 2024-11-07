import sys
sys.path.append('/path/to/Investar')


from Investar import Analyzer


mk = Analyzer.MarketDB()
df = mk.get_daily_price('삼성전자', '2024-10-04', '2024-11-04')
print(df)

