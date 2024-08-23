import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from pyqtgraph.dockarea import Dock

from ...readsettings import select_settings

config = select_settings(verbose=False)
MAXTEMP = config["Max Temperature"]

DEGREE_SMB = "\N{DEGREE SIGN}"


class HeaterControl(Dock):
    def __init__(self):
        super().__init__("Membreane Heater")
        self.widget = pg.LayoutWidget()
        self.tempBw = QtWidgets.QTextBrowser()
        self.tempBw.setMinimumSize(QtCore.QSize(80, 60))
        self.tempBw.setMaximumHeight(60)
        self.temperatureSB = QtWidgets.QSpinBox()
        self.temperatureSB.setMinimum(0)
        self.temperatureSB.setMaximum(MAXTEMP)
        self.temperatureSB.setSuffix(f"{DEGREE_SMB} C")
        self.temperatureSB.setMinimumSize(QtCore.QSize(180, 80))
        self.temperatureSB.setSingleStep(10)
        self.temperatureSB.setStyleSheet(
            "QSpinBox::up-button   { width: 60px; }\n"
            "QSpinBox::down-button { width: 60px;}\n"
            "QSpinBox {font: 26pt;}"
        )
        self.set_button = QtWidgets.QPushButton("set")
        self.set_button.setMinimumSize(QtCore.QSize(80, 80))
        self.set_button.setStyleSheet("font: 26pt")
        self.set_layout()

    def set_layout(self):
        self.addWidget(self.widget)

        self.widget.addWidget(self.tempBw, 0, 0, 1, 2)
        self.widget.addWidget(self.temperatureSB, 1, 0)
        self.widget.addWidget(self.set_button, 1, 1)

        self.verticalSpacer = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        # self.widget.layout.setVerticalSpacing(0)
        self.widget.layout.addItem(self.verticalSpacer)

    def set_label_font(self, text: str, color: str):
        txt = "<font color={}><h4>{}</h4></font>".format(color, text)
        return txt

    def update_displayed_temperatures(self, temperature, temp_now):
        """set values into browser"""
        htmltag = '<font size=6 color="#d1451b">'
        htag1 = '<font size=6 color = "#4275f5">'
        cf = "</font>"
        self.tempBw.setText(
            f"{htmltag}{temperature} {DEGREE_SMB}C{cf}"
            f"&nbsp;&nbsp;&nbsp;{htag1}{temp_now} {DEGREE_SMB}C{cf}"
        )

    def set_heating_goal(self, temperature: int, temp_now):
        self.update_displayed_temperatures(temperature, temp_now)
        self.temperatureSB.setValue(temperature)


class CathodeBoxTemperature(Dock):
    def __init__(self):
        super().__init__("Box T")
        self.widget = pg.LayoutWidget()
        self.temperature_browser = QtWidgets.QTextBrowser()
        self.temperature_browser.setMinimumSize(QtCore.QSize(80, 60))
        self.temperature_browser.setMaximumHeight(60)
        self.set_layout()

    def set_layout(self):
        self.addWidget(self.widget)

        self.widget.addWidget(self.temperature_browser, 0, 0, 1, 2)

        self.verticalSpacer = QtWidgets.QSpacerItem(
            0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        # self.widget.layout.setVerticalSpacing(0)
        self.widget.layout.addItem(self.verticalSpacer)

    def set_label_font(self, text: str, color: str):
        txt = "<font color={}><h4>{}</h4></font>".format(color, text)
        return txt

    def update_displayed_temperatures(self, temp_now):
        """set values into browser"""
        htmltag = '<font size=6 color="#d1451b">'
        htag1 = '<font size=6 color = "#4275f5">'
        cf = "</font>"
        self.temperature_browser.setText(f"{htmltag}{temp_now} {DEGREE_SMB}C{cf}")


if __name__ == "__main__":
    pass
