from ni import Thermocouple
from gui import MainWidget
from timekeeper import TimeKeeper
from heater_control import HeaterControl
import pandas as pd
import numpy as np
import time
import threading


class TemperatureControl():

    def __init__(self):

        self.app = MainWidget()
        self.tc = Thermocouple()
        self.heater = HeaterControl()
        self.timer = TimeKeeper()

        thread1 = threading.Thread(target=self.app.main,daemon=True)
        thread2 = threading.Thread(target=self.tc.measure_temperature,daemon=True)
        thread3 = threading.Thread(target=self.heater.start_control_ft232h,daemon=True)
        
        self.__sumE = 0
        self.__exE = 0
        self.sample_rate = 10

        self.columns = ["date", "time", "T", "PresetT"]
        self.data = pd.DataFrame(columns = self.columns)


        thread1.start()
        thread2.start()
        thread3.start()

        self.main()

        

    
    def main(self):

        while self.tc.measuring_flag == False:
            time.sleep(0.01)

        self.timer.start()

        while True:
            self.temperature_setpoint = self.app.var_tar_temp
            if self.app.end_measurement:
                self.tc.measurement_flag = False
                self.heater.measurement_flag = False
                break

            self.temperature = self.tc.temperature[0]
            self.app.update_cur_temp(round(self.temperature,4))

            self.update_dataframe()

            self.feedback_control()

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

        if e > 100: # TODO Adjustment
            self.heater.duty = 1
        elif e >= 0:
            output = Kp * e + Ki * integral + Kd * derivative
            output = output * 0.0002 # デューティ比の仕様に応じてここも変える, PWMの発信源を別スレッドで作る(Class)
            self.heater.duty = output
        else:
            self.heater.duty = 0

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

    import os.path
    data_folder = "../../data/temp/"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    data_name = data_folder + timenow.strftime("%Y_%m%d_%H%M")+ '.csv'
    app.data.to_csv(data_name,index=False)


