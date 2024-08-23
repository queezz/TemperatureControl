"""
Device Super Class

This is the basic structure of a thread with hardware Input/Outputs.
Last time I tried (AK) to put more methods in this superclass, 
some PyQt connections and slots didn't work.
Need to understand the slots and signals better, and put more 
of the reused stuff here.

All this generalisation is good, but it requires time and some learning,
which is a waste of time at the moment. So maybe for later edits:
TODO: make data dummies? 
TODO: can we add main loop here?
TODO: add PID here?

"""
from PyQt5 import QtCore

TEST = False
PRINTTHREADINFO = False
STEP = 3 # Defines number of points before sending to main thread


# MARK: Worker
class Sensor(QtCore.QObject):
    """
    send_message usage:
    self.send_message.emit(f"Your Message Here to pass to main.py")
    """
    TEST = TEST
    STEP = STEP
    PRINTTHREADINFO = PRINTTHREADINFO

    send_step_data = QtCore.pyqtSignal(list)
    signal_done = QtCore.pyqtSignal(str)
    send_message = QtCore.pyqtSignal(str)

    def __init__(self, sensor_name, app, startTime, config):
        super().__init__()

        self.__id = id
        self.__app = app
        self.sensor_name = sensor_name
        self.__startTime = startTime
        self.config = config

    def print_checks(self):
        attrs = vars(self)

        if PRINTTHREADINFO:
            print("Thread Checks:")
            print(", ".join(f"{i}" for i in attrs.items()))
            print("ID:", self.__id)
            print("End Thread Checks")

    def set_thread_name(self):
        """Set Thread name and ID, signal them to the log browser"""
        threadName = QtCore.QThread.currentThread().objectName()
        print(threadName)
        return

    def getStartTime(self):
        return self.__startTime

    def setSampling(self, sampling):
        """Set sampling time"""
        self.sampling = sampling
        # print(f"Updated sampling to {sampling}")


if __name__ == "__main__":
    pass
