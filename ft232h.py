"""
GPIO for Windows, FT232H by Adafruit
Solid state relay PWM control
"""

import time
import os
from PyQt5 import QtCore
from readsettings import select_settings

os.environ["BLINKA_FT232H"] = "1"  # Setting Environmental Variable


try:
    import board
    import digitalio
except ImportError:
    print("no board module for ft232h")

config = select_settings(verbose=False)
CHHEATER = config["FT232H"]["Heater Output"]["Pin"]
CHSYNC = config["FT232H"]["Sync Input"]["Pin"]
DUTYCYCLE = config["Duty Cycle"]


class HeaterContol(QtCore.QObject):
    """
    PWM for SSD of the membrane heater.
    The PID value comes from worker.py thread.
    """

    def __init__(self, app):
        super().__init__()
        self.app = app
        # range 0~1
        self.duty = 0
        self.abort = False
        self.pin = None

    # MARK: Duty setter
    def set_ssd_duty(self, value: float):
        """
        Set SSD duty cycle, 0 by default
        """
        self.duty = value

    # MARK: PWD loop
    @QtCore.pyqtSlot()
    def work(self):
        self.__setThread()
        # GPIO Setting : C0 will be output port.
        self.pin = pin_config(CHHEATER, "out")

        while not self.abort:
            if self.duty == 1:
                self.pin.value = True
                self.app.processEvents()
                time.sleep(DUTYCYCLE)
            if self.duty == 0:
                self.pin.value = False
                self.app.processEvents()
                time.sleep(DUTYCYCLE)
            if 0 < self.duty < 1:
                self.pin.value = True
                time.sleep(DUTYCYCLE * self.duty)
                self.pin.value = False
                time.sleep(DUTYCYCLE * (1 - self.duty))
                self.app.processEvents()
        self.pin.value = False

    def __setThread(self):
        self.threadName = QtCore.QThread.currentThread().objectName()
        self.threadId = int(QtCore.QThread.currentThreadId())

    @QtCore.pyqtSlot()
    def setAbort(self):
        self.abort = True


class QmsSigSync:

    def __init__(self):
        # super().__init__()
        # self.app = app
        self.abort = False
        self.init_board()

    def init_board(self):
        self.pin = pin_config(CHSYNC, "in")

    def get_sig(self):
        return self.pin.value


# MARK: Pin Config
def pin_config(pin_name, direction):
    """
    Select pin and set input/output mode.
    """
    pin_map = {
        "c0": board.C0,
        "c1": board.C1,
        "c2": board.C2,
        "c3": board.C3,
        "c4": board.C4,
        "c5": board.C5,
        "c6": board.C6,
        "c7": board.C7,
        "d4": board.D4,
        "d5": board.D5,
        "d6": board.D6,
        "d7": board.D7,
    }
    pin_board = pin_map.get(pin_name)
    if pin_board is None:
        print("Pin name is not correct")
        return None
    pin = digitalio.DigitalInOut(pin_board)

    if direction == "out":
        pin.direction = digitalio.Direction.OUTPUT
    elif direction == "in":
        pin.direction = digitalio.Direction.INPUT
    else:
        print("direction is not correct")
    return pin


if __name__ == "__main__":
    app = QmsSigSync()
    while True:
        print(app.get_sig())
