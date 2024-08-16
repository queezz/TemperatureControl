import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets, QtGui
from pyqtgraph.dockarea import Dock


class PidTuning(Dock):
    def __init__(self):
        super().__init__("PID")
        self.widget = pg.LayoutWidget()
        self.pid_state_browser = QtWidgets.QTextBrowser()
        self.pid_state_browser.setMinimumSize(QtCore.QSize(60, 50))
        self.pid_state_browser.setMaximumHeight(60)

        self.pid_spinboxes = {
            "p": self.create_spinbox_pair(suffix=" p"),
            "i": self.create_spinbox_pair(suffix=" i"),
            "d": self.create_spinbox_pair(suffix=" d"),
        }

        self.set_button = QtWidgets.QPushButton("set")
        self.set_button.setMinimumSize(QtCore.QSize(80, 50))
        self.set_button.setStyleSheet("font: 20pt")

        self.reset_button = QtWidgets.QPushButton("reset")
        self.reset_button.setMinimumSize(QtCore.QSize(80, 50))
        self.reset_button.setStyleSheet("font: 20pt")

        self.set_layout()

    def create_spinbox_pair(self, suffix=""):
        "create a pair of significant and epxonent spinboxes"
        significand_spinbox = QtWidgets.QSpinBox()
        exponent_spinbox = QtWidgets.QSpinBox()
        self.spin_box_style(significand_spinbox, type="significand", suffix=suffix)
        self.spin_box_style(exponent_spinbox, type="exponent")
        return {"significand": significand_spinbox, "exponent": exponent_spinbox}

    def spin_box_style(self, spin_box, type="significand", suffix=""):
        """style the spin box"""
        if type == "significand":
            spin_box.setMinimum(0)
            spin_box.setMaximum(9)
        if type == "exponent":
            spin_box.setMinimum(-10)
            spin_box.setMaximum(2)

        spin_box.setSuffix(suffix)
        spin_box.setMinimumSize(QtCore.QSize(80, 40))
        spin_box.setSingleStep(1)
        spin_box.setStyleSheet(
            "QSpinBox::up-button   { width: 35px; }\n"
            "QSpinBox::down-button { width: 35px;}\n"
            "QSpinBox {font: 16pt;}"
        )
        spin_box.setWrapping(True)

    def set_layout(self):
        self.addWidget(self.widget)

        self.widget.addWidget(self.pid_state_browser, 0, 0, 1, 4)

        # print(self.pid_spinboxes["p"]["exponent"])

        self.widget.addWidget(self.pid_spinboxes["p"]["significand"], 1, 0)
        self.widget.addWidget(self.pid_spinboxes["p"]["exponent"], 1, 1)
        self.widget.addWidget(self.pid_spinboxes["i"]["significand"], 1, 2)
        self.widget.addWidget(self.pid_spinboxes["i"]["exponent"], 1, 3)
        self.widget.addWidget(self.pid_spinboxes["d"]["significand"], 2, 0)
        self.widget.addWidget(self.pid_spinboxes["d"]["exponent"], 2, 1)
        self.widget.addWidget(self.set_button, 2, 2)
        self.widget.addWidget(self.reset_button, 2, 3)

        self.verticalSpacer = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.widget.layout.addItem(self.verticalSpacer)

    def set_label_font(self, text: str, color: str):
        txt = "<font color={}><h4>{}</h4></font>".format(color, text)
        return txt

    def update_display(self, p, i, d):
        """
        Update current PID coefficients
        Parameters
        ----------
        p: float
            proportional coefficient
        i: float
            integral coefficient
        d: float
            differential coeffitient
        """
        html_tag_1 = '<font size=6 color="#0ad157">'
        html_tag_2 = '<font size=6 color = "#d1b60a">'
        html_tag_3 = '<font size=6 color = "#d10a8f">'
        close_tag = "</font>"

        self.pid_state_browser.setText(
            f"{html_tag_1}p={p:.0e} {close_tag}"
            f"&nbsp;&nbsp;&nbsp;{html_tag_2}i={i:.0e} {close_tag}"
            f"&nbsp;&nbsp;&nbsp;{html_tag_3}d={d:.0e} {close_tag}"
        )


if __name__ == "__main__":
    pass
