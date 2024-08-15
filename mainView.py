import pyqtgraph as pg
from PyQt5 import QtGui, QtWidgets
from pyqtgraph.dockarea import DockArea, Dock

from components.docks.log import LogDock
from components.docks.plots import PlotScaleDock
from components.docks.control import ControlDock
from components.docks.tempcontrol import HeaterControl, CathodeBoxTemperature
from components.docks.analog_temperature import AnalogTemperatureGauge
from components.docks.pid_tuning import PidTuning
from components.docks.settings import SettingsDock
from components.widgets.graph import Graph


class UIWindow(object):
    def __init__(self):
        super().__init__()
        pg.setConfigOptions(imageAxisOrder="row-major")

        self.main_window = QtWidgets.QMainWindow()
        self.tab_widget = QtWidgets.QTabWidget()
        self.area = DockArea()
        self.plot_dock = Dock("Plots", size=(300, 400))
        self.control_dock = ControlDock()
        self.temperature_control_dock = HeaterControl()
        self.cathode_box_dock = CathodeBoxTemperature()
        self.pid_tuning_dock = PidTuning()
        self.temperature_gauge_dock = AnalogTemperatureGauge()
        self.log_dock = LogDock()
        [
            dock.setStretch(*(10, 20))
            for dock in [
                self.control_dock,
                self.log_dock,
                self.temperature_control_dock,
                self.cathode_box_dock,
                self.temperature_gauge_dock,
            ]
        ]
        self.control_dock.setStretch(*(10, 300))
        self.graph = Graph()
        self.scale_dock = PlotScaleDock()

        self.settings_area = DockArea()
        self.settings_dock = SettingsDock()
        self.log_dock.setStretch(*(200, 100))
        self.settings_dock.setStretch(*(80, 100))

        self.main_window.setGeometry(20, 50, 1000, 600)
        screen_geometry = QtWidgets.QDesktopWidget().screenGeometry(-1)
        # print(" Screen size : " + str(sizeObject.height()) + "x" + str(sizeObject.width()))
        if screen_geometry.height() < 1000:
            self.main_window.showMaximized()

        # self.MainWindow.showFullScreen()
        self.main_window.setObjectName("Monitor")
        self.main_window.setWindowTitle("Temperature Control")
        # self.MainWindow.statusBar().showMessage("")
        self.main_window.setAcceptDrops(True)

        self.set_layout()

    def set_layout(self):
        self.main_window.setCentralWidget(self.tab_widget)
        self.tab_widget.addTab(self.area, "Data")

        self.area.addDock(self.plot_dock, "top")
        self.area.addDock(self.control_dock, "left", self.plot_dock)
        self.area.addDock(self.scale_dock, "bottom", self.control_dock)
        self.area.addDock(self.temperature_control_dock, "bottom", self.control_dock)
        self.area.addDock(
            self.cathode_box_dock, "bottom", self.temperature_control_dock
        )
        self.area.addDock(self.pid_tuning_dock, "bottom", self.control_dock)

        self.plot_dock.addWidget(self.graph)

        self.tab_widget.addTab(self.settings_area, "Settings")
        self.settings_area.addDock(self.settings_dock)
        self.settings_area.addDock(self.log_dock, "right")

    def showMain(self):
        self.main_window.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("./icons/temperature.png"))
    ui = UIWindow()
    ui.showMain()
    sys.exit(app.exec_())
