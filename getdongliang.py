#!/usr/bin/env python3
import ccxt
from datetime import datetime
from datetime import timedelta
import pandas as pd

huobi_exchange = ccxt.huobipro()
huobi_exchange.load_markets()

now = datetime.now()
if int(now.strftime("%H%M%S"))<=200000:
    now = now + timedelta(days=-1)
else:
    pass

aDay = timedelta(days=-7)
lastweek = now + aDay
print(now.strftime('%Y-%m-%d'))
print(lastweek.strftime('%Y-%m-%d'))
today_time = now.strftime('%Y-%m-%d')+' 19:00:00+00:00'
lastweek_time = lastweek.strftime('%Y-%m-%d')+' 19:00:00+00:00'

symbol = ['BTC/USDT','BSV/USDT','HT/USDT']
dongliang_list = []

for symbol in symbol:
    if huobi_exchange.has['fetchOHLCV']:
        kline_data = pd.DataFrame(huobi_exchange.fetch_ohlcv(symbol,timeframe='1h'))
        kline_data.columns = ['Datetime','open','High','Low','close','vol']
        kline_data = kline_data[['Datetime', 'close']]
        kline_data['Datetime'] = kline_data['Datetime'].apply(huobi_exchange.iso8601)
        kline_data['Datetime'] = pd.to_datetime(kline_data['Datetime'])+pd.Timedelta(hours=8)
        thisweekclose = kline_data[kline_data['Datetime'] == today_time]['close'].values
        lastweekclose = kline_data[kline_data['Datetime'] == lastweek_time]['close'].values
        dongliang = thisweekclose/lastweekclose
        dongliang_list.append(dongliang)

        print(now.strftime('%Y-%m-%d'),symbol,thisweekclose)
        print(lastweek.strftime('%Y-%m-%d'),symbol,lastweekclose)
        print(symbol,'动量',dongliang)


dongliang_btc = dongliang_list[0]
dongliang_bsv = dongliang_list[1]
dongliang_ht = dongliang_list[2]

# print(dongliang_btc)
# print(dongliang_bsv)

# print(dongliang_ht)

print('BTC-BSV 轮动组')
if dongliang_btc > dongliang_bsv:
    print('操作BTC')
else:
    print('操作BSV')

if dongliang_btc < 0.99 and dongliang_bsv < 0.99:
    print('空仓追涨')
else:
    print('持仓止损')

print('BTC-HT 轮动组')
if dongliang_btc > dongliang_ht:
    print('操作BTC')
else:
    print('操作HT')

if dongliang_btc < 0.99 and dongliang_ht < 0.99:
    print('空仓追涨')
else:
    print('持仓止损')