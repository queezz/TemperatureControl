import pyqtgraph as pg
from PyQt5 import QtGui, QtCore, QtWidgets
from pyqtgraph.dockarea import Dock

# from components.scaleButtons import ScaleButtons
from ..buttons.toggles import MySwitch, OnOffSwitch, QmsSwitch
from QLed import QLed


class ControlDock(Dock):
    def __init__(self):
        super().__init__("Control")
        self.widget = pg.LayoutWidget()

        self.quitBtn = QtWidgets.QPushButton("quit")
        self.quitBtn.setStyleSheet(
            "QPushButton {color:#f9ffd9; background:#ed2a0c;}"
            "QPushButton:disabled {color:#8f8f8f; background:#bfbfbf;}"
        )
        self.quitBtn.setFont(QtGui.QFont("serif", 16))

        self.scaleBtn = QtWidgets.QComboBox()
        self.scaleBtn.setFont(QtGui.QFont("serif", 18))
        items = [
            "20 s",
            "60 sec",
            "5 min",
            "15 min",
            "30 min",
            "1 hr",
            "1.5 hr",
            "2 hrs",
            "Full",
        ]
        sizes = [20, 60, 5 * 60, 15 * 60, 30 * 60, 60 * 60, 90 * 60, 120 * 60, -1]
        [self.scaleBtn.addItem(i) for i in items]
        self.sampling_windows = {i: j for i, j in zip(items, sizes)}

        self.fullscreen_toggle = MySwitch()
        self.on_off_toggle = OnOffSwitch()
        self.on_off_toggle.setFont(QtGui.QFont("serif", 16))

        self.explamp = QLed(self, onColour=QLed.Red, shape=QLed.Circle)
        self.explamp.setValue(False)

        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.widget)

        self.widget.addWidget(self.on_off_toggle, 0, 0)
        self.widget.addWidget(self.explamp, 0, 1)
        self.widget.addWidget(self.quitBtn, 0, 2)

        self.widget.addWidget(self.fullscreen_toggle, 1, 0)
        self.widget.addWidget(self.scaleBtn, 1, 1, 1, 2)

        self.verticalSpacer = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.widget.layout.setVerticalSpacing(3)
        self.widget.layout.addItem(self.verticalSpacer)


if __name__ == "__main__":
    pass
