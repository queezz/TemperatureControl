import time
from PyQt5 import QtCore
from readsettings import select_settings
import os
os.environ['BLINKA_FT232H'] = '1' #Setting Environmental Variable

import time
try:
    import board
    import digitalio
except:
    print("no board module for ft232h")

config = select_settings(verbose=False)
CHHEATER = config["FT232H"]["Hearer Output"]["Pin"]



class HeaterContol(QtCore.QObject):
    def __init__(self, app):
        super().__init__()
        self.app = app
        # range 0~1
        self.duty = 0
        self.abort = False

    # MARK: setter
    def setOnLight(self, value: float):
        self.duty = value

    # MARK: - Methods
    @QtCore.pyqtSlot()
    def work(self):
        self.__setThread()
        #GPIO Setting : C0 will be output port.
        pin = self.pin_config(CHHEATER, "out")

        while not self.abort:
            while self.duty == 1:
                pin.value = True
                time.sleep(0.01)
            while self.duty == 0:
                pin.value = False
                time.sleep(0.01)
            pin.value = True
            time.sleep(0.01 * self.duty)
            pin.value = False
            time.sleep(0.01 * (1-self.duty))
            self.app.processEvents()

    def __setThread(self):
        self.threadName = QtCore.QThread.currentThread().objectName()
        self.threadId = int(QtCore.QThread.currentThreadId())

    @QtCore.pyqtSlot()
    def setAbort(self):
        self.abort = True

def pin_config(pin_name, direction):
    if pin_name == "c0":
        pin = digitalio.DigitalInOut(board.C0)
    elif pin_name == "c1":
        pin = digitalio.DigitalInOut(board.C1)
    elif pin_name == "c2":
        pin = digitalio.DigitalInOut(board.C2)
    elif pin_name == "c3":
        pin = digitalio.DigitalInOut(board.C3)
    elif pin_name == "c4":
        pin = digitalio.DigitalInOut(board.C4)
    elif pin_name == "c5":
        pin = digitalio.DigitalInOut(board.C5)
    elif pin_name == "c6":
        pin = digitalio.DigitalInOut(board.C6)
    elif pin_name == "c7":
        pin = digitalio.DigitalInOut(board.C7)
    elif pin_name == "d4":
        pin = digitalio.DigitalInOut(board.D4)
    elif pin_name == "d5":
        pin = digitalio.DigitalInOut(board.D5)
    elif pin_name == "d6":
        pin = digitalio.DigitalInOut(board.D6)
    elif pin_name == "d7":
        pin = digitalio.DigitalInOut(board.D7)
    else:
        print("pin name is not correct")
    if direction == "out":
        pin.direction = digitalio.Direction.OUTPUT
    elif direction == "in":
        pin.direction = digitalio.Direction.INPUT
    else:
        print("direction is not correct")
    return pin
        

if __name__ == "__main__":
    pass
