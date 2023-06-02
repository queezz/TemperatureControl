from ni import Thermocouple
# from gui import MainWidget
from signal_output import Signal
from timekeeper import TimeKeeper
import pandas as pd
import numpy as np
import time
import threading
import serial
import msvcrt
import datetime

port = "COM4"
baudrate = 9600


class TemperatureControl():
    def __init__(self):
        self.tc = Thermocouple()
        # self.app = MainWidget()
        self.sig = Signal()
        self.timer = TimeKeeper()
        thread1 = threading.Thread(target=self.tc.measure_temperature)
        # thread2 = threading.Thread(target=self.app.mainloop)

        self.__sumE = 0
        self.__exE = 0
        self.sample_rate = 10


        self.columns = ["date", "time", "T", "PresetT"]
        self.data = pd.DataFrame(columns = self.columns)

        self.temperature_setpoint = int(input("Target Temperature is: "))
        print("Press 'q' to quit this program")

        thread1.start()
        # thread2.start()

        self.main()

    
    def main(self):
        while self.tc.measuring_flag == False:
            time.sleep(0.1)
        self.timer.start()
        while True:
            if msvcrt.kbhit() and msvcrt.getch() == b'q':
                self.sig.output_signal('0')
                self.sig.close_port()

                self.tc.measurement_flag = False

                break
            self.temperature = self.tc.temperature[0]
            print(self.temperature)

            self.update_dataframe()

            # self.feedback_control()
            self.output = 1

            self.sig.output_signal(self.output)

            time.sleep(1/self.sample_rate)
        self.timer.end()
        print(self.timer.timedelta)

        pass

    def feedback_control(self):
        e = self.temperature_setpoint - self.temperature
        integral = self.__sumE + e / self.sample_rate
        derivative = (e - self.__exE) * self.sample_rate

        # TODO Adjustment
        Kp = 3.5
        Ki = 0.06
        Kd = 0

        # TODO Adjustment
        if integral < -0.5:
            integral = 0

        if e >= 0:
            output = Kp * e + Ki * integral + Kd * derivative
            output = output * 0.0002 # デューティ比の仕様に応じてここも変える, PWMの発信源を別スレッドで作る(Class)
            self.output = 1
        else:
            # self.membrane_heater.setOnLight(0)
            self.output = 0
        self.__exE = e
        self.__sumE = integral
        pass
    def update_dataframe(self):
        timenow = self.timer.now()
        timedelta = self.timer.timedelta
        new_row = pd.DataFrame(
            np.atleast_2d([timenow,timedelta, self.temperature, self.temperature_setpoint]), columns=self.columns
        )
        self.data = pd.concat([self.data, new_row], ignore_index=True)
    pass



if __name__=="__main__":
    app = TemperatureControl()
    timenow = app.timer.now()
    data_folder = "../data/temp/"
    data_name = data_folder + timenow.strftime("%Y_%m%d_%H%M")+ '.csv'
    app.data.to_csv(data_name,index=False)


