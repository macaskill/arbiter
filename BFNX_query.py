import asyncio
import requests
import time

async def get_last_price(pair):
    '''
    a coroutine to get the last traded price for the given pair
    :param pair: pair in standard form
    :return: float in the base currency of the pairing (i.e. BTCUSD returns a float in US Dollars)
    '''
    bfnx_url = "https://api.bitfinex.com/v1/trades/"
    response = requests.get(bfnx_url + pair)
    data = response.json()
    lt = data[0]
    lt_price = lt['price']
    return pair, lt_price

async def main(pairs, lasts):
    '''
    creates a group of coroutines and waits for them to finish
    :param pairs: a list of the POIs
    :return:
    '''
    coroutines = [get_last_price(pair) for pair in pairs]
    completed, pending = await asyncio.wait(coroutines)
    for item in completed:
        #print(item.result())
        lasts[item.result()[0]] = float(item.result()[1])

if __name__ =='__main__':
    now = time.time()
    pairs = ['ETHUSD', 'LTCUSD', 'ETHBTC', 'XRPUSD',
             'BTCUSD', 'IOTUSD', 'IOTETH', 'XMRUSD']
    lasts = {}
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(pairs, lasts))
    finally:
        event_loop.close()
    print(lasts)
    print(time.time() - now, " seconds to complete")