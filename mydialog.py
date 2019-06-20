import sys, time
from PyQt5.QtWidgets import *
from PyQt5 import uic

import bitmexTr1

form_class = uic.loadUiType("BitmexTr.ui")[0]



class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.confirm_pushButton.clicked.connect(self.confirm_cmd)
        self.action_pushButton.clicked.connect(self.action_cmd)

    def confirm_cmd(self):
        print("confirm cmd")
        entry_price = float(self.entry_lineEdit.text())
        qty  = float(self.qty_lineEdit.text())
        print(entry_price)
        print(qty)
        self.message_label.setText('메시지 : ' + '주문을 확인합니다')

    def action_cmd(self):
        print("action cmd")
        print("state changed None -> Ready")
        self.message_label.setText('메시지 : ' + '주문을 합니다')

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec_()