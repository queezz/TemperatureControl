import pyqtgraph as pg
from PyQt5 import QtGui, QtCore, QtWidgets
from pyqtgraph.dockarea import Dock
from ..buttons.toggles import *


class PlotScaleDock(Dock):
    def __init__(self):
        super().__init__("Scales")
        self.widget = pg.LayoutWidget()

        self.autoscale = changeScale()
        self.temperature_plot_toggle = ToggleTemperaturePlot()
        self.pid_plot_toggle = TogglePIDPlot()
        [
            i.setChecked(True)
            for i in [self.temperature_plot_toggle, self.pid_plot_toggle]
        ]
        self.t_max = QtWidgets.QSpinBox()
        self.t_max.setMinimum(50)
        self.t_max.setMaximum(1000)
        self.t_max.setMinimumSize(QtCore.QSize(60, 60))
        self.t_max.setSingleStep(50)

        [
            i.setStyleSheet(
                "QSpinBox::up-button   { width: 30px; }\n"
                "QSpinBox::down-button { width: 30px;}\n"
                "QSpinBox {font: 20pt;}"
            )
            for i in [self.t_max]
        ]

        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.widget)
        self.widget.addWidget(self.t_max, 0, 0)
        self.widget.addWidget(self.temperature_plot_toggle, 0, 1)
        self.widget.addWidget(self.pid_plot_toggle, 0, 2)
        self.widget.addWidget(self.autoscale, 0, 3)

        self.verticalSpacer = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.widget.layout.setVerticalSpacing(5)
        self.widget.layout.addItem(self.verticalSpacer)


if __name__ == "__main__":
    pass
