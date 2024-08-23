"""
Dummy for tests if the boards are not connected
and no board or digitalio are installed
"""

import random


# MARK: FT232h
class board:
    """Board dummy class"""

    C0, C1, C2, C3, C4, C5, C6, C7, D4, D5, D6, D7 = ["pin_board_dummy"] * 12


class DigitalInOut:
    """Dummy class for digitalio.DigitalInOut"""

    def __init__(self, pin):
        self.pin = pin
        self.value = False  # Dummy value for pin state
        self.direction = None

    def set_high(self):
        self.value = True

    def set_low(self):
        self.value = False


class Direction:
    """Dummy class for digitalio.Direction"""

    OUTPUT = "output"
    INPUT = "input"


class digitalio:
    """DigitalIO dummy class"""

    Direction = Direction
    DigitalInOut = DigitalInOut

    C0, C1, C2, C3, C4, C5, C6, C7, D4, D5, D6, D7 = [None] * 12


# MARK: NI
class nidaqmx:

    class Task:
        def __init__(self):
            self.ai_channels = self.AIChannels()
            self.timing = self.Timing()

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass

        def read(self, number_of_samples_per_channel=1):
            # Simulate temperature readings
            return [[random.uniform(50.0, 70.0)], [random.uniform(20.0, 40.0)]]

        class AIChannels:
            def add_ai_thrmcpl_chan(self, channel, thermocouple_type, cjc_source):
                pass

        class Timing:
            def cfg_samp_clk_timing(self, rate):
                pass

    class constants:
        class ThermocoupleType:
            def __init__(self, tc_type):
                pass

        class CJCSource:
            def __init__(self, value):
                self.value = value

            def __call__(self, *args, **kwargs):
                return self.value
