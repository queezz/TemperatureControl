import pyqtgraph as pg
from PyQt5 import QtGui
import datetime

DEGREE_SMB = "\N{DEGREE SIGN}"


class Graph(pg.GraphicsLayoutWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("graph")

        labelStyle = {"color": "#FFF", "font-size": "16pt"}

        self.temperature_plot = self.addPlot(row=1, col=0)
        self.temperature_plot.setLabel(
            "left", "T", units=DEGREE_SMB + "C", **labelStyle
        )
        # Adjust the label offset
        self.temperature_plot.setLabel("bottom", "time", units="sec", **labelStyle)

        self.setBackground(background="#25272b")

        tickFont = QtGui.QFont("serif", 16)
        left_axis = self.temperature_plot.getAxis("left")
        left_axis.setWidth(80)
        left_axis.setPen("#ff7878")
        left_axis.setTickFont(tickFont)

        axis = pg.DateAxisItem()
        self.temperature_plot.setAxisItems({"bottom": axis})
        bottom_axis = self.temperature_plot.getAxis("bottom")
        bottom_axis.setPen("#ff7878")
        bottom_axis.setTickFont(QtGui.QFont("serif", 18))

        self.pid_plot = self.addPlot(row=0, col=0)
        self.pid_plot.setLabel("left", "PID", **labelStyle)
        self.pid_plot.setLabel("bottom", " ")
        left_axis = self.pid_plot.getAxis("left")
        left_axis.setWidth(80)
        left_axis.setTickFont(tickFont)

        axis = pg.DateAxisItem()
        self.pid_plot.setAxisItems({"bottom": axis})


if __name__ == "__main__":
    pass
