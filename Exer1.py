import sys
import time

from bitmex import BitMEX

from configparser import ConfigParser

myconfig = ConfigParser()

if not myconfig.read('trading.conf'):
    print('There is not configurations file')
    raise SystemExit

MODE         = myconfig.get('DEFAULT', 'Mode')
API_KEY      = myconfig.get(MODE, 'API_KEY')
API_SECRET   = myconfig.get(MODE, 'API_SECRET')
BASE_URL     = myconfig.get(MODE, 'BASE_URL')

bitmex = BitMEX(apiKey=API_KEY, apiSecret=API_SECRET, base_url=BASE_URL)

content = bitmex.orderbook(1)
print(content)

ask_price = content[0]['price']

content = bitmex.place_order(10, ask_price-100)
print(content)

time.sleep(5)


content = bitmex.cancel(id)
print(content)





