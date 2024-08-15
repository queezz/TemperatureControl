import pyqtgraph as pg
from PyQt5 import QtGui, QtWidgets

DEGREE_SMB = "\N{DEGREE SIGN}"


class Graph(pg.GraphicsLayoutWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("graph")

        labelStyle = {"color": "#FFF", "font-size": "18pt"}
        font = QtGui.QFont("serif", 14)

        self.temperature_plot = self.addPlot(row=1, col=0)
        self.temperature_plot.setLabel(
            "left", "T", units=DEGREE_SMB + "C", **labelStyle
        )
        # Adjust the label offset
        self.temperature_plot.setLabel("bottom", "time", units="sec", **labelStyle)

        self.setBackground(background="#25272b")

        tickFont = QtGui.QFont("serif", 18)
        left_axis = self.temperature_plot.getAxis("left")
        left_axis.setWidth(80)
        left_axis.setPen("#ff7878")
        left_axis.setTickFont(tickFont)

        bottom_axis = self.temperature_plot.getAxis("bottom")
        bottom_axis.setPen("#ff7878")
        bottom_axis.setTickFont(tickFont)

        self.pid_plot = self.addPlot(row=0, col=0)
        self.pid_plot.setLabel("left", "p,i,d", **labelStyle)
        left_axis = self.pid_plot.getAxis("left")
        left_axis.setWidth(80)
        left_axis.setTickFont(tickFont)


if __name__ == "__main__":
    pass
