import nidaqmx
import matplotlib.pyplot as plt
import time
import pandas as pd
import datetime

# plt.ion()

### Write down fundamental program to communicate with NI-DAQ (NI-9211)


class Thermocouple():
    def __init__(self):
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

        self.measurement_flag = True
        self.measuring_flag = False


    def measure_temperature(self):
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_thrmcpl_chan("cDAQ1Mod1/ai0",thermocouple_type = nidaqmx.constants.ThermocoupleType(self.tc_type))
            task.timing.cfg_samp_clk_timing(rate=1000)
            while self.measurement_flag:
                self.temperature = task.read(number_of_samples_per_channel=1)
                self.measuring_flag = True

        
if __name__ == '__main__':
    Thermocouple()