import pyqtgraph as pg
from PyQt5 import QtGui, QtCore, QtWidgets
from pyqtgraph.dockarea import Dock
from ..buttons.toggles import *


class PlotScaleDock(Dock):
    def __init__(self):
        super().__init__("Scales")
        self.widget = pg.LayoutWidget()

        self.autoscale = changeScale()
        self.togT = ToggleTemperaturePlot()
        [i.setChecked(True) for i in [self.togT]]
        self.Tmax = QtWidgets.QSpinBox()
        self.Tmax.setMinimum(50)
        self.Tmax.setMaximum(1000)
        self.Tmax.setMinimumSize(QtCore.QSize(60, 60))
        self.Tmax.setSingleStep(50)

        [
            i.setStyleSheet(
                "QSpinBox::up-button   { width: 50px; }\n"
                "QSpinBox::down-button { width: 50px;}\n"
                "QSpinBox {font: 26pt;}"
            )
            for i in [self.Tmax]
        ]

        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.widget)
        self.widget.addWidget(self.Tmax, 0, 0)
        self.widget.addWidget(self.togT, 0, 1)
        self.widget.addWidget(self.autoscale, 0, 2)

        self.verticalSpacer = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.widget.layout.setVerticalSpacing(5)
        self.widget.layout.addItem(self.verticalSpacer)


if __name__ == "__main__":
    pass
