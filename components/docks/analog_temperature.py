import pyqtgraph as pg
from PyQt5 import QtGui, QtCore, QtWidgets
from pyqtgraph.dockarea import Dock


from ..widgets.analoggauge import AnalogGaugeWidget
from readsettings import select_settings

config = select_settings(verbose=False)
MAXTEMP = config["Max Temperature"]


class AnalogTemperatureGauge(Dock):
    def __init__(self):
        super().__init__("Gauge")
        self.widget = pg.LayoutWidget()

        self.gaugeT = AnalogGaugeWidget()
        self.gaugeT.set_MinValue(0)
        self.gaugeT.set_MaxValue(MAXTEMP)
        self.gaugeT.set_total_scale_angle_size(180)
        self.gaugeT.set_start_scale_angle(180)
        self.gaugeT.set_enable_value_text(False)

        self.__setLayout()

    def __setLayout(self):
        self.addWidget(self.widget)
        self.widget.addWidget(self.gaugeT, 0, 0)
