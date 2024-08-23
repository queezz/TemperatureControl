import pyqtgraph as pg
from PyQt5 import QtWidgets
from pyqtgraph.dockarea import Dock


class LogDock(Dock):
    def __init__(self):
        super().__init__("Log")
        self.widget = pg.LayoutWidget()

        self.log = QtWidgets.QTextEdit()
        self.log.setReadOnly(True)
        self.log.document().setDefaultStyleSheet("p { margin: 0; }")
        self.log.setStyleSheet("QTextEdit { background-color: #f2e9b8; }")

        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.widget)

        self.widget.addWidget(self.log, 0, 0, 1, 1)


if __name__ == "__main__":
    pass
