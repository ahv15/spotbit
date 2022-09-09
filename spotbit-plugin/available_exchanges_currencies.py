import ccxt as ccxt
from bs4 import BeautifulSoup
import requests
r = requests.get("https://github.com/ccxt/ccxt/tree/master/python/ccxt")
soup = BeautifulSoup(r.content, 'html5lib')
links = soup.findAll('a', attrs={'class': 'js-navigation-open Link--primary'})
objects = {}
for i in range(6, len(links)):
    try:
        objects[links[i].text[0:-3]
                ] = eval("ccxt." + links[i].text[0:-3] + "()")
    except:
        print(links[i].text[0:-3] + " is not available.")
        continue
exchanges = objects.keys()
currencies = ['USD', 'EUR', 'CAD', 'GBP', 'AUD', 'SEK', 'BRL', 'CZK', 'INR']
possibilities = {}


def get_supported_pair_for(currency, exchange):
    result = ''
    exchange.load_markets()
    market_ids_found = []
    for market in exchange.markets_by_id.keys():
        if ((market[:len('BTC')].upper() == 'BTC' or market[:len('XBT')].upper() == 'XBT' or market[:len('XXBTZCAD')].upper() == 'XXBTZCAD') and market[-len(currency):].upper() == currency.upper() and (len(market) == (3 + len(currency)) or (len(market) == (4 + len(currency)) and (market[3] == '/' or market[3] == '-' or market[3] == '_')))):
            market_ids_found.append(market)
    if market_ids_found:
        market_id = market_ids_found[0]
        market = exchange.markets_by_id[exchange.market_id(market_id)]
        if market:
            result = market['symbol']
    return result


for exchange in exchanges:
    if objects[exchange].has['fetchOHLCV']:
        try:
            ticker = get_supported_pair_for('USD', objects[exchange])
        except:
            print(exchange + " is not available.")
            continue
        for currency in currencies:
            ticker = get_supported_pair_for(currency, objects[exchange])
            if ticker == '' or ticker == 'BTC/USDT':  # incorrect id to ticker mapping USD to USDT
                continue
            if (currency in possibilities.keys()):
                possibilities[currency].append([exchange, ticker])
            else:
                possibilities[currency] = [[exchange, ticker]]

for curr in possibilities.keys():
    for exchange in possibilities[curr]:
        print(f"{curr}: exchange: {exchange[0]}")
