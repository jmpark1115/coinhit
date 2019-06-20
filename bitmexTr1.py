from bitmex import BitMEX

import logging
import time
import os, sys

from configparser import ConfigParser
import math

myconfig = ConfigParser()
myconfig.read('trading.conf')

MODE         = myconfig.get('DEFAULT', 'Mode')
API_KEY      = myconfig.get(MODE, 'API_KEY')
API_SECRET   = myconfig.get(MODE, 'API_SECRET')
BASE_URL     = myconfig.get(MODE, 'BASE_URL')
checkprice   = float(myconfig.get('DEFAULT', 'Buy'))
checkprice_2 = float(myconfig.get('DEFAULT', 'Sell'))
dry_run      = True if myconfig.get('DEFAULT', 'dry_run') == 'yes' else False


bitmex = BitMEX(apiKey=API_KEY, apiSecret=API_SECRET, base_url=BASE_URL)

logger = logging.getLogger()


def setup_logger():
    # Prints logger info to terminal
    logger.setLevel(logging.DEBUG)  # Change this to DEBUG if you want a lot more info
    ch = logging.StreamHandler()

    fh = logging.FileHandler('user.log', mode='a', encoding=None, delay=False)
    fh.setLevel(logging.INFO)
    # create formatter
    formatter = logging.Formatter("%(filename)s %(lineno)s %(message)s")
    formatter_fh = logging.Formatter("%(asctime)s %(filename)s %(lineno)s %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    fh.setFormatter(formatter_fh)

    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

def best_offer():

    ask_price = 0
    bid_price = 0

    try:
        orderbooks = bitmex.orderbook(depth = 1)
    except Exception as e:
        logger.error("orderbook error occured {}".format(e))
        return 0, 0

    try:
        ask_price = orderbooks[0]['price']
        ask_qty   = orderbooks[0]['size']
        bid_price = orderbooks[1]['price']
        bid_qty   = orderbooks[1]['size']

        logger.info("best offer Buy {}@{} - Sell{}@{}".format(bid_qty, bid_price, ask_qty, ask_price))
    except Exception as e:
        logger.error("orderbook error occurred {}" .format(e))

    return ask_price, bid_price

# e_orders = [{'orderID': xxx, 'entry_price': xxx, 'price':0, 'orderQty': 0, 'status' : 'None', 'child':'None'}]
# c_orders = {'orderID': yyy, 'price': 0, 'orderQty': 0, 'status': 'None'}

def monitoringTr(orders):

    for order in orders:
        print(order)

    ask_price, bid_price = best_offer()

    # step1 : 주문하기
    for order in orders:
        if order['orderID'] == 'None' and order['status'] == 'Ready':
            order['price'] = order['entry_price']
            if bid_price > order['entry_price']:
                resp = bitmex.place_order(quantity=order['orderQty'], price=order['price'])
                time.sleep(0.1)
                orderID = resp.get('orderID', 'None')
                if orderID != 'None':
                    order['orderID'] = orderID
                    order['status']  = resp['ordStatus']
                else:
                    order['status'] = 'Rejected'
                    print('place order cmd error')
            else:
                print('bid price is lower than entry_price')

    # step2 : 주문체결 된 것이 있으면 child 주문
    get_orders = bitmex.http_open_orders(isTerminated=True)
    time.sleep(0.1)
    # for ord in get_orders:
    #     logger.debug("Get_Orders %s %s %d %d %s"
    #                  % (ord['orderID'][:9], ord['side'], ord['orderQty'], ord['leavesQty'], ord['ordStatus']))
    for order in orders:
        for ord in get_orders:
            if ord['orderID'] == order['orderID']:
                order['status'] = ord['ordStatus']
                # check if parent order is contracted
                # Step2 : patent 중에 주문 체결이 되었으면 child 주문을 낸다
                if ord['ordStatus'] == 'Filled' and ord['leavesQty'] == 0:
                    if order['child'] == 'None':
                        c_order = dict()
                        c_order['price']    = order['entry_price'] + 2
                        c_order['orderQty'] = order['orderQty']

                        resp = bitmex.place_order(quantity=c_order['orderQty']*-1, price=c_order['price'])
                        time.sleep(0.1)
                        orderID = resp.get('orderID', 'None')
                        c_order['orderID'] = orderID
                        c_order['status']  = resp['ordStatus']
                        order['child']     = c_order

            if order['child'] != 'None' and ord['orderID'] == order['child']['orderID']:
                order['child']['status'] = ord['ordStatus']
                # step3 : child 중에 주문 체결이 되었으면 최초 상태로 전환한다
                if ord['ordStatus'] == 'Filled' and ord['leavesQty'] == 0:
                    order['orderID'] = 'None'
                    order['price']   = 'None'
                    order['status']  = 'Ready'
                    order['child']   = 'None'

def main_tradingTr():

    e_orders = [
        {'entry_price': 3805, 'orderID': 'None', 'orderQty': 100, 'status': 'Ready', 'child':'None'},
        {'entry_price': 3800, 'orderID': 'None', 'orderQty': 200, 'status': 'Ready', 'child':'None'},
    ]
    while True:
        sys.stdout.write("-----\n")
        sys.stdout.flush()
        monitoringTr(e_orders)
        time.sleep(5)

def main_setup():
    logger = setup_logger()

if __name__ == "__main__":

    main_setup()
    main_tradingTr()
