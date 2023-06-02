import serial

class Signal():
    def __init__(self):
        self.port = "COM4"
        self.baudrate = 9600

        self.open_port()

    def output_signal(self, signal):
        if type(signal) != str:
            signal = str(signal)
        self.ser.write(bytes(signal,'utf-8'))


    def open_port(self):
        self.ser = serial.Serial(self.port,self.baudrate,timeout=1)

    def close_port(self):
        self.ser.close()

if __name__ == "__main__":
    pass
