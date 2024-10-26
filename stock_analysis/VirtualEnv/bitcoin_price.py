from blockchain import exchangerates
tk = exchangerates.get_ticker()
print('1 bitcoin =', tk['KRW'].p15min, 'KRW')
