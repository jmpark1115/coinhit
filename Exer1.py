import sys
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

quotes = bitmex.orderbook(depth=1)
