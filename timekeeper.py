from datetime import datetime

class TimeKeeper():
    def __init__(self):
        pass

    def now(self):
        self.timenow = datetime.now()
        self.timedelta = (self.timenow - self.start_time).total_seconds()
        return self.timenow

    def start(self):
        self.start_time = datetime.now()

    def end(self):
        self.end_time = datetime.now()
        self.timedelta = (self.end_time - self.start_time).total_seconds()

if __name__ == '__main__':
    pass