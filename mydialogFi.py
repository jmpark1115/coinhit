'''
master와 worker를 이용해 bitmexTr1 을 구동
'''
import sys, time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("BitmexTr.ui")[0]

import config
from bitmexTr1 import *

def put_dialog_orders(q):
    config.e_orders.append(q)

def get_dialog_orders():
    return config.e_orders

class Monitor(QThread):

    update_signal = pyqtSignal()

    def run(self):
        main_setup()
        while True:
            monitoringTr(get_dialog_orders())
            self.update_signal.emit()
            time.sleep(5)

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.confirm_pushButton.clicked.connect(self.confirm_cmd)
        self.action_pushButton.clicked.connect(self.action_cmd)
        self.MyDialog()

    def MyDialog(self):
        self.monitor = Monitor()
        self.monitor.update_signal.connect(self.display_orders_list)
        self.monitor.start()

    def display_orders_list(self):
        orders = get_dialog_orders()
        message = ""
        for idx, order in enumerate(orders):
            message += "{}번 {} + " .format(idx, order['status'])
        self.message_label.setText('메시지 : ' + message)

    def confirm_cmd(self):
        print("confirm cmd")
        entry_price = float(self.entry_lineEdit.text())
        qty  = float(self.qty_lineEdit.text())
        print(entry_price)
        print(qty)
        if entry_price ==0 or qty == 0:
            print('invalid value')
            return

        order = {'entry_price':entry_price,
                 'orderID' : 'None',
                 'orderQty':qty,
                 'status': 'None',
                 'child' : 'None'}
        put_dialog_orders(order)
        self.message_label.setText('메시지 : ' + '주문을 확인합니다')

    def action_cmd(self):
        print("action cmd")
        orders = get_dialog_orders()
        for order in orders:
            print(order)
            if order['status'] == 'None':
                order['status'] = 'Ready'
        self.message_label.setText('메시지 : ' + '주문을 합니다')



app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()