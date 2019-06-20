import sys, time
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

form_class = uic.loadUiType("BitmexTr.ui")[0]

class Worker(QThread):
    update_signal = pyqtSignal(dict)

    def run(self):
        while True:
            now = datetime.now()
            data = {'time': '%s'%now}
            self.update_signal.emit(data)
            time.sleep(5)

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.worker = Worker()
        self.worker.update_signal.connect(self.update_display)
        self.worker.start()

    # @pyqtSlot(dict)
    def update_display(self, data):
        self.message_label.setText('메시지 : ' + data['time'] )

app = QApplication(sys.argv)
win = MyWindow()
win.show()
app.exec_()