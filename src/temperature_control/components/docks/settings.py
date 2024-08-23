import pyqtgraph as pg
from PyQt5 import QtWidgets
from pyqtgraph.dockarea import Dock


class SettingsDock(Dock):
    def __init__(self):
        super().__init__("Settings")
        self.widget = pg.LayoutWidget()
        self.sampling_checkbox = QtWidgets.QComboBox()
        items = [f"{i} s" for i in [10, 1, 0.1, 0.01]]
        [self.sampling_checkbox.addItem(i) for i in items]
        self.sampling_checkbox.setCurrentIndex(2)
        self.sampling_checkbox.setMaximumWidth(120)
        self.sampling_checkbox.setToolTip("sampling time")
        self.sampling_button = QtWidgets.QPushButton("set")

        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.widget)

        self.widget.addWidget(self.sampling_checkbox, 0, 0)
        self.widget.addWidget(self.sampling_button, 0, 1)

        self.verticalSpacer = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.widget.layout.setVerticalSpacing(5)
        self.widget.layout.addItem(self.verticalSpacer)


if __name__ == "__main__":
    pass
