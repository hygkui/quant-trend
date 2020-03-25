import pandas as pd
import ccxt
import time
import requests

exchange = ccxt.okex3()
# exchange = ccxt.binance()
# exchange = ccxt.huobipro()
c_time = int(time.time()//60 * 60 * 1000)  # 60*60*1000
limit = 8
since_time = c_time - limit * 24 * 60 * 60 * 1000  # 500 min before
rate = 0.999
maxWaveRate = 0.15
dataSet = {}
url = 'https://v1.hitokoto.cn/?c=f&encode=text'


def cal_symbol(symbol):
    if symbol in dataSet:
        return dataSet[symbol]['wave'], dataSet[symbol]['price']

    data = exchange.fetch_ohlcv(
        symbol=symbol, timeframe='1d', limit=limit, since=since_time)
    columns = {0: 'open_time', 1: 'open', 2: 'high',
               3: 'low', 4: 'close', 5: 'volume'}
    df = pd.DataFrame(data)
    df = df.rename(columns=columns)
    # df['open_time'] = pd.to_datetime(
    #     df['open_time'], unit='ms') + pd.Timedelta(hours=8)
    ds = df['close']
    lastWeekPrice = ds[0]
    price = ds[7]
    wave = price / lastWeekPrice
    dataSet[symbol] = {'wave': wave, 'price': price}
    return wave, price


def check_pair(p1, p2):
    wave1, price1 = cal_symbol(p1)
    wave2, price2 = cal_symbol(p2)

    print('\r\n轮动组：%s %.3f, %s %.3f' % (p1, wave1, p2, wave2))

    if wave1 > wave2 and wave1 > rate:
        print('全买入%s, 止损价格: %.4f' % (p1, price1 * (1 - maxWaveRate)))
    elif wave2 > wave1 and wave2 > rate:
        print('全买入%s, 止损价格: %.4f' % (p2, price2 * (1 - maxWaveRate)))
    else:
        if (wave1 > wave2):
            print('全空仓，追涨%s 价格: %.4f' % (p1, price1 * (1 + maxWaveRate)))
        else:
            print('全空仓，追涨%s 价格: %.4f' % (p2, price2 * (1 + maxWaveRate)))

    time.sleep(2)


current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

print('\r\n动量计算时间', current_time)
check_pair('BTC/USDT', 'ETH/USDT')
check_pair('BTC/USDT', 'BCH/USDT')
check_pair('BTC/USDT', 'EOS/USDT')
check_pair('ETH/USDT', 'EOS/USDT')
check_pair('BSV/USDT', 'BCH/USDT')

print('')
print(requests.get(url).text)
print('')

exit()
