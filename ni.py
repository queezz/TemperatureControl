# Description: This program is for NI-DAQ (NI-9211) communication.
import matplotlib.pyplot as plt
import time
import pandas as pd
import datetime
from PyQt5 import QtCore


try:
    import nidaqmx
except:
    print("no nidaqmx module for ni.py")


### Write down fundamental program to communicate with NI-DAQ (NI-9211)
class Thermocouple(QtCore.QObject):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.init_ni()
        self.abort = False

    def init_ni(self):
        """Types of Thermocouple"""
        B = 10047
        E = 10055
        J = 10072
        K = 10073
        N = 10077
        R = 10082
        S = 10085
        T = 10086

        self.tc_type = K

        self.temperature = 20

        self.measuring_flag = False

    @QtCore.pyqtSlot()
    def work(self):
        self.__setThread()
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_thrmcpl_chan("cDAQ1Mod1/ai0",thermocouple_type = nidaqmx.constants.ThermocoupleType(self.tc_type))
            task.timing.cfg_samp_clk_timing(rate=1000)
            while not self.abort:
                self.temperature = task.read(number_of_samples_per_channel=1)[0]
                self.measuring_flag = True
                # print(self.abort)
                self.app.processEvents()

    def __setThread(self):
        self.threadName = QtCore.QThread.currentThread().objectName()
        self.threadId = int(QtCore.QThread.currentThreadId())

    @QtCore.pyqtSlot()
    def setAbort(self):
        self.abort = True

        
if __name__ == '__main__':
    Thermocouple()