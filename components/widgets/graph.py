import pyqtgraph as pg
from PyQt5 import QtGui
import datetime

DEGREE_SMB = "\N{DEGREE SIGN}"


class Graph(pg.GraphicsLayoutWidget):

    pens = {
            "T": {"color": "#5999ff", "width": 1},
            "trigger": {"color": "#edbc34", "width": 1},
            "p": {"color": "#0ad157", "width": 1},
            "i": {"color": "#d1b60a", "width": 1},
            "d": {"color": "#d10a8f", "width": 1},
        }

    def __init__(self):
        super().__init__()
        pg.setConfigOptions(useOpenGL=True)
        self.setObjectName("graph")
        self.setBackground(background="#262629")

        self.labelStyle = {"color": "#FFF", "font-size": "16pt"}
        self.tickFont = QtGui.QFont("serif", 16)
        self.prep_temperature_plot()
        self.prep_pid_plot()

    def prep_temperature_plot(self):
        """
        set up plot for membrane temperature
        """
        self.temperature_plot = self.addPlot(row=1, col=0)
        self.temperature_plot.setLabel(
            "left", "T", units=DEGREE_SMB + "C", **self.labelStyle
        )
        # Adjust the label offset
        self.temperature_plot.setLabel("bottom", "time", units="sec", **self.labelStyle)

        
        left_axis = self.temperature_plot.getAxis("left")
        left_axis.setWidth(80)
        left_axis.setPen("#ff7878")
        left_axis.setTickFont(self.tickFont)
        left_axis.setTextPen("#ff7878")

        axis = pg.DateAxisItem()
        self.temperature_plot.setAxisItems({"bottom": axis})
        bottom_axis = self.temperature_plot.getAxis("bottom")
        bottom_axis.setPen("#ff7878")
        bottom_axis.setTickFont(QtGui.QFont("serif", 18))
        bottom_axis.setTextPen("#ff7878")
        self.temperature_curve = self.temperature_plot.plot(
            pen=self.pens["T"]
        )
        self.temperature_curve.setDownsampling(auto=True, method='mean')
        self.temperature_plot.setYRange(0, 320, 0)

    def prep_pid_plot(self):
        """
        set up plots for PID tuning
        """
        self.pid_plot = self.addPlot(row=0, col=0)
        self.pid_plot.setLabel("left", "PID", **self.labelStyle)
        self.pid_plot.setLabel("bottom", " ")
        left_axis = self.pid_plot.getAxis("left")
        left_axis.setWidth(80)
        left_axis.setTickFont(self.tickFont)

        axis = pg.DateAxisItem()
        self.pid_plot.setAxisItems({"bottom": axis})

        self.pid_curves = {
            component: self.pid_plot.plot(pen=self.pens[component])
            for component in ["p", "i", "d"]
        }

        self.pid_plot.setXLink(self.temperature_plot)


if __name__ == "__main__":
    pass
