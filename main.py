import pandas as pd
import ccxt
import time
import numpy as np
# print(pd.__version__)
# print(np.__version__)
#file_path = "./test.csv"
# df = pd.read_csv(file_path)
# print(df.head())

exchange = ccxt.okex3()
#exchange = ccxt.binance()
#exchange = ccxt.huobipro()
c_time = int(time.time()//60 * 60 * 1000)  # 60*60*1000
limit = 8
since_time = c_time - limit * 24 * 60 * 60 * 1000  # 500 min before


def cal_symbol(symbol):
    data = exchange.fetch_ohlcv(
        symbol=symbol, timeframe='1d', limit=limit, since=since_time)

    df = pd.DataFrame(data)
    df = df.rename(columns={0: 'open_time', 1: 'open',
                            2: 'high', 3: 'low', 4: 'close', 5: 'volume'})
    df['open_time'] = pd.to_datetime(
        df['open_time'], unit='ms') + pd.Timedelta(hours=8)
    ds = df['close']
    last = ds[0]
    now = ds[7]
    print(symbol, now/last)


current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(current_time)
cal_symbol('BTC/USDT')
cal_symbol('ETH/USDT')
cal_symbol('BCH/USDT')
cal_symbol('BSV/USDT')
cal_symbol('EOS/USDT')
cal_symbol('XRP/USDT')
cal_symbol('LTC/USDT')
