"""
NI9211 Acquisition Class
"""
import time, datetime
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from PyQt5 import QtCore

from .device import Sensor
from .ni_controller import Thermocouple
from .ft232h import HeaterContol
from simple_pid import PID

# MARK: -NI9211
class NI9211(Sensor):
    signal_abort_heater = QtCore.pyqtSignal()
    signal_abort_thermocouple = QtCore.pyqtSignal()
    signal_send_pid = QtCore.pyqtSignal(tuple)

    def __init__(self, sensor_name, app, startTime, config):
        super().__init__(sensor_name, app, startTime, config)
        self.__app = app
        self.sensor_name = sensor_name
        self.__startTime = startTime
        self.config = config
        self.__abort = False
        self.qmssig = 0
        self.pid = None

        self.temperature_setpoint = None
        self.columns = self.config["Temperature Columns"]
        self.data = None
        self.temperature_setpoint = 0
        self.sampling_time = self.config["Sampling Time"]
        self.smoothed_data = None
        self.datapoints_to_keep = 100 # for smoothing
        self.smoothing_window = 15


    def set_temp_worker(self, setpoint: int):
        """
        needs pigpio daemon
        """
        self.data = pd.DataFrame(columns=self.columns)
        self.smoothed_data = pd.DataFrame(columns=["T", "smoothed"])
        self.temperature_setpoint = setpoint

    @QtCore.pyqtSlot()
    def start(self):
        """
        Start data acquisition
        """
        self.acquisition_loop()

    def init_heater_control(self):
        self.membrane_heater = HeaterContol(self.__app)
        self.thread_heater = QtCore.QThread()
        self.thread_heater.setObjectName("heater current")
        self.membrane_heater.moveToThread(self.thread_heater)
        self.thread_heater.started.connect(self.membrane_heater.work)
        self.signal_abort_heater.connect(self.membrane_heater.setAbort)
        self.thread_heater.start()

        if self.membrane_heater.ISDUMMY:
            self.send_message.emit(
                f"<font size=4 color='blue'>{self.sensor_name}</font>"
                + f" <font color='red'>DUMMY</font> signal",
            )

    def init_thermocouple(self):
        """
        Select MAX6675 sensor on the SPI
        Need to start PIGPIO daemon
        """
        self.thermocouple = Thermocouple(self.__app)
        self.thread_thermocouple = QtCore.QThread()
        self.thread_thermocouple.setObjectName("thermocouple")
        self.thermocouple.moveToThread(self.thread_thermocouple)
        self.thread_thermocouple.started.connect(self.thermocouple.work)
        self.signal_abort_thermocouple.connect(self.thermocouple.setAbort)
        self.thread_thermocouple.start()

    def read_thermocouple(self):
        """
        Read NI-9211 sensor output
        """
        self.temperature = self.thermocouple.temperature
        self.cathodeBoxTemperature = self.thermocouple.cathodeBoxTemperature

    def clear_datasets(self):
        """
        Remove data from temporary dataframes
        """
        self.data = self.data.iloc[0:0]

    # MARK: update data
    def update_dataframe(self):
        """
        Append new reading to dataframe
        """
        now = datetime.datetime.now()
        dSec = (now - self.__startTime).total_seconds()
        # ["date", "time", "T", "PresetT"]
        new_row = pd.DataFrame(
            np.atleast_2d(
                [
                    now,
                    dSec,
                    self.temperature,
                    self.temperature_setpoint,
                    self.qmssig,
                    self.cathodeBoxTemperature,
                    *self.pid.components,
                ]
            ),
            columns=self.columns,
        )

        # This gives FutureWarning
        # self.data = pd.concat([self.data, new_row], ignore_index=True)
        # adjusting the dtypes to remove it:
        self.data = pd.concat(
            [self.data.astype(new_row.dtypes), new_row.astype(self.data.dtypes)]
        )

        # Smooth data (best to fix hardware issue, but let's use this for now).
        self.smoothed_data.loc[len(self.smoothed_data)] = [self.temperature,self.temperature]
        if len(self.smoothed_data) > self.smoothing_window:
            self.smoothed_data['smoothed'] = savgol_filter(self.smoothed_data['T'], self.smoothing_window,1)

        if len(self.smoothed_data) == self.datapoints_to_keep:
            self.smoothed_data = self.smoothed_data.drop(self.smoothed_data.index[0])
            self.smoothed_data = self.smoothed_data.reset_index(drop=True)
            

    def calculate_average(self):
        """
        Average signal
        """
        self.average = self.data["T"].mean()

    # MARK: PID
    def set_preset_temp(self, newTemp: int):
        self.temperature_setpoint = newTemp
        self.pid.setpoint = self.temperature_setpoint
        return

    def update_pid_coefficients(self, pid_coefficients):
        """update pid"""
        # self.pid.Ki = 1.0
        self.pid.tunings = pid_coefficients
        self.signal_send_pid.emit(self.pid.tunings)

    def prep_pid(self):
        """
        Set PID parameters
        """
        p, i, d = 1e-4, 1e-8, 5e-4
        self.pid = PID(p, i, d, setpoint=self.temperature_setpoint)
        self.pid.output_limits = (0, 1)
        self.pid.sample_time = self.sampling_time
        self.signal_send_pid.emit(self.pid.tunings)

    def update_ssr_duty(self):
        """
        update solid state relay duty
        This calculates the duty with simple-pid package
        and updates it
        """
        #output = max(0, self.pid(self.temperature))
        # Try average over STEP points to smooth derivative component
        output = max(0, self.pid(self.smoothed_data['smoothed'].iloc[-1]))
        self.membrane_heater.set_ssd_duty(output)
        return output

    def send_processed_data_to_main_thread(self):
        """
        Send processed data to main.py
        """
        self.send_step_data.emit([self.data, self.sensor_name])

    # MARK: acquisition loop
    @QtCore.pyqtSlot()
    def acquisition_loop(self):
        """
        Temperature acquisition and Feedback Control loop
        """
        self.init_thermocouple()
        self.init_heater_control()
        self.prep_pid()

        step = 0

        while not (self.__abort):
            time.sleep(self.sampling_time)
            self.read_thermocouple()
            self.update_dataframe()

            # Update PWM with PID as fast as possible
            self.update_ssr_duty()

            # This is needed to reduce the data flow to the main.py
            if step % (self.STEP - 1) == 0 and step != 0:
                self.calculate_average()
                # Update pid every STEP times to smooth signals
                #self.update_ssr_duty()
                self.send_processed_data_to_main_thread()
                self.clear_datasets()
                step = 0
            else:
                step += 1
            self.__app.processEvents()

        self.cleanup_to_abort()

    def cleanup_to_abort(self):
        """
        Shut down control, quit threads, reset data
        """
        self.membrane_heater.set_ssd_duty(0)
        self.calculate_average()
        self.send_processed_data_to_main_thread()
        self.signal_abort_heater.emit()
        self.signal_abort_thermocouple.emit()
        self.pid = None

        self.thread_thermocouple.quit()
        self.thread_heater.quit()
        self.thread_thermocouple.wait()
        self.thread_heater.wait()

        self.thread_heater = None
        self.thread_thermocouple = None
        self.signal_done.emit(self.sensor_name)

    @QtCore.pyqtSlot()
    def abort(self):
        """
        Sets the flag self.__abort to True to exit acquisition while loop
        """
        message = "Worker thread {} aborting acquisition".format(self.sensor_name)
        # self.send_message.emit(message)
        # print(message)
        self.__abort = True

if __name__ == "__main__":
    pass