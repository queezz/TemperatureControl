import serial
import time

 

class HeaterControl():
    def __init__(self):
        self.duty = 0
        self.measurement_flag = True

    def start_control_arduino(self):
        port = "COM4"
        baudrate = 9600
        with serial.Serial(port, baudrate, timeout=1) as ser:
            while self.measurement_flag:
                while self.duty == 1 & self.measurement_flag:
                    ser.write(b'1')
                    time.sleep(0.01)
                while self.duty == 0 & self.measurement_flag:
                    ser.write(b'0')
                    time.sleep(0.01)
                ser.write(b'1')
                time.sleep(0.01 * self.duty)
                ser.write(b'0')
                time.sleep(0.01 * (1-self.duty))
            ser.write(b'0')
            ser.close()

    def start_control_ft232h(self):
        import os
        os.environ['BLINKA_FT232H'] = '1' #Setting Environmental Variable

        import board
        import time
        import digitalio

        #GPIO Setting : C0 will be output port.
        pin = digitalio.DigitalInOut(board.C0)
        pin.direction = digitalio.Direction.OUTPUT

        while self.measurement_flag:
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
