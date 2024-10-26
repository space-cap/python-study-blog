
# 연평균 성장률(CAGR) 구하기
def getCAGR(first, last, years):
    return (last/first)**(1/years) - 1

# 삼성전자 1998년 65,300원
# 2018년 2,669,000원까지 20년 동안 연평균 성장률은?
cagr = getCAGR(65300, 2669000, 20)

print("SEC CAGR : {:.2%}".format(cagr))
