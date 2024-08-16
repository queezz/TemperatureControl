"""
Main loop of the app
"""

import sys
import datetime
from datetime import timedelta
import os
import pandas as pd
from PyQt5 import QtGui, QtCore, QtWidgets

from mainView import UIWindow
from worker import Worker, NI9211

from ft232h import QmsSigSync

import readsettings
from striphtmltags import strip_tags


# must inherit QtCore.QObject in order to use 'connect'
class MainWidget(QtCore.QObject, UIWindow):
    """"""

    DEFAULT_TEMPERATURE = 0
    DEFALT_VOLTAGE = 0
    STEP = 3

    sigAbortWorkers = QtCore.pyqtSignal()

    # MARK: init
    def __init__(self, app: QtWidgets.QApplication):
        super(self.__class__, self).__init__()
        self.__app = app
        self.connections()
        self.temperature_control_dock.set_heating_goal(self.DEFAULT_TEMPERATURE, "---")
        self.cathode_box_dock.update_displayed_temperatures("---")

        QtCore.QThread.currentThread().setObjectName("main")

        self.__workers_done = 0
        self.threads = []
        self.temperature_setpoint = self.DEFAULT_TEMPERATURE

        self.trigData = None
        self.tData = None

        self.config = readsettings.init_configuration(verbose=True)
        self.datapath = self.config["Data Folder"]
        self.sampling = self.config["Sampling Time"]

        # Plot line colors
        # self.currentvalues = {"T": 0}
        self.currentvalues = {i: 0 for i in ["T", "Cathode Box T"]}
        self.baratronsignal1 = 0
        self.baratronsignal2 = 0
        self.pens = {
            "T": {"color": "#5999ff", "width": 2},
            "trigger": {"color": "#edbc34", "width": 2},
            "p": {"color": "#0ad157", "width": 2},
            "i": {"color": "#d1b60a", "width": 2},
            "d": {"color": "#d10a8f", "width": 2},
        }

        self.temperatuere_curve_data = self.graph.temperature_plot.plot(
            pen=self.pens["T"]
        )
        self.graph.temperature_plot.setYRange(0, 320, 0)

        self.pid_curves = {
            component: self.graph.pid_plot.plot(pen=self.pens[component])
            for component in ["p", "i", "d"]
        }

        self.graph.pid_plot.setXLink(self.graph.temperature_plot)

        self.temperature_worker = None

        self.qmssigreader = QmsSigSync()

        self.qmssig = False
        self.control_dock.explamp.setValue(self.qmssig)

        self.update_plot_timewindow()

        self.showMain()
        self.log_to_file(f"App started: {os.path.abspath(__file__)}")

    # MARK: connections
    def connections(self):
        """
        Defines GUI to logic connections
        """
        self.control_dock.scaleBtn.currentIndexChanged.connect(
            self.update_plot_timewindow
        )

        self.temperature_control_dock.set_button.clicked.connect(self.set_heater_goal)

        self.control_dock.fullscreen_toggle.clicked.connect(self.fulltonormal)
        self.control_dock.on_off_toggle.clicked.connect(self.__onoff)
        self.control_dock.quitBtn.clicked.connect(self.__quit)

        # Toggle plots for Current, Temperature, and Pressure
        self.scale_dock.temperature_plot_toggle.clicked.connect(self.toggle_plots)
        self.scale_dock.pid_plot_toggle.clicked.connect(self.toggle_plots)

        self.scale_dock.t_max.valueChanged.connect(self.__updateTScale)

        self.scale_dock.autoscale.clicked.connect(self.__auto_or_levels)
        self.settings_dock.sampling_button.clicked.connect(self.set_sampling)

        self.pid_tuning_dock.set_button.clicked.connect(self.set_pid_coefficients)

    # MARK: UI
    def __quit(self):
        """terminate app"""
        self.__app.quit()

    def __onoff(self):
        """
        Start and stop worker threads
        """
        if self.control_dock.on_off_toggle.isChecked():
            self.prep_threads()
            self.control_dock.quitBtn.setEnabled(False)
        else:
            quit_msg = "Are you sure you want to stop data acquisition?"
            reply = QtWidgets.QMessageBox.warning(
                self.main_window,
                "Message",
                quit_msg,
                QtWidgets.QMessageBox.Yes,
                QtWidgets.QMessageBox.No,
            )
            if reply == QtWidgets.QMessageBox.Yes:
                self.abort_all_threads()
                self.control_dock.quitBtn.setEnabled(True)
            else:
                self.control_dock.on_off_toggle.setChecked(True)

    def toggle_plots(self):
        """
        Toggle plots
        self.scaleDock.togIp
        self.graph.plaPl
        """

        def toggleplot(i, pl, row=0, col=0):
            if i.isChecked():
                try:
                    self.graph.addItem(pl, row=row, col=col)
                except:
                    pass
            else:
                try:
                    self.graph.removeItem(pl)  # remove plot
                except:
                    pass

        items = {
            "pid": [self.scale_dock.pid_plot_toggle, self.graph.pid_plot, 0, 0],
            "T": [
                self.scale_dock.temperature_plot_toggle,
                self.graph.temperature_plot,
                1,
                0,
            ],
        }

        [toggleplot(*items[jj]) for jj in ["T", "pid"]]

    @QtCore.pyqtSlot()
    def set_sampling(self):
        """Set sampling time for all threads"""
        if not len(self.threads):
            return
        txt = self.settings_dock.sampling_checkbox.currentText()
        value = float(txt.split(" ")[0])
        self.sampling = value
        self.update_plot_timewindow()
        if self.temperature_worker is not None:
            self.temperature_worker.setSampling(value)
            self.log_message(f"Temperature sampling set to {value}")

    # MARK: plotting
    def update_plot_timewindow(self):
        """
        adjust time window for data plots
        """
        # index = self.controlDock.scaleBtn.currentIndex()
        txt = self.control_dock.scaleBtn.currentText()
        val = self.control_dock.sampling_windows[txt]
        self.time_window = val
        # self.log_message(f"Timewindow = {val}")
        try:
            [self.update_plots(sensor_name) for sensor_name in self.sensor_names]
        except AttributeError:
            pass
            # print("can't update plots, no workers yet")

    def __updateTScale(self):
        """Updated plot limits for the Temperature viewgraph"""
        tmax = self.scale_dock.t_max.value()
        self.graph.temperature_plot.setYRange(0, tmax, 0)

    def __updateScales(self):
        """Update all scales according to spinboxes"""
        self.__updateTScale()

    def __autoscale(self):
        """Set all plots to autoscale"""
        # enableAutoRange
        plots = [self.graph.temperature_plot]

        # [i.autoRange() for i in plots]
        [i.enableAutoRange() for i in plots]

    def __auto_or_levels(self):
        """Change plot scales from full auto to Y axis from settings"""
        if self.scale_dock.autoscale.isChecked():
            self.__autoscale()
        else:
            self.__updateScales()

    def fulltonormal(self):
        """Change from full screen to normal view on click"""
        if self.control_dock.fullscreen_toggle.isChecked():
            self.main_window.showFullScreen()
            self.control_dock.setStretch(*(10, 300))  # minimize control dock width
        else:
            self.main_window.showNormal()
            self.control_dock.setStretch(*(10, 300))  # minimize control dock width

    # MARK: update plots
    def update_plots(self, sensor_name):
        """"""
        if sensor_name == "NI9211":
            df = self.select_data_to_plot(sensor_name)
            # time = df["time"].values.astype(float)
            utc_offset = 9
            time = (
                df["date"]
                .apply(lambda x: (x - timedelta(hours=utc_offset)).timestamp())
                .values
            )
            temperature = df["T"].values.astype(float)
            skip = self.calculate_skip_points(time.shape[0])
            self.temperatuere_curve_data.setData(time[::skip], temperature[::skip])

            for component, curve in self.pid_curves.items():
                values = df[component].values.astype(float)
                curve.setData(time[::skip], values[::skip])

    # MARK: prep threads
    def prep_threads(self):
        """
        Define Workers to run in separate threads.
        2020/03/05: two sensors: ADC and temperatures, hence
        2 threds to read a) temperature, and b) analog signals (P1,P2, Ip)
        """
        self.log_message(
            "<font color='#1cad47'>Starting</font> acquisition", htmltag="h2"
        )
        self.savepaths = {}
        self.datadict = {
            "NI9211": pd.DataFrame(columns=self.config["Temperature Columns"]),
        }
        self.newdata = {
            "NI9211": pd.DataFrame(columns=self.config["Temperature Columns"]),
        }

        self.__workers_done = 0

        for thread, worker in self.threads:
            thread.quit()
            thread.wait()

        self.threads = []

        now = datetime.datetime.now()
        threads = {}

        # NI9211_0 thermocouple sensor for Membrane temperature with PID
        sensor_name = "NI9211"
        threads[sensor_name] = QtCore.QThread()
        threads[sensor_name].setObjectName(f"{sensor_name}")
        self.temperature_worker = NI9211(sensor_name, self.__app, now, self.config)
        self.temperature_worker.set_temp_worker(self.temperature_setpoint)
        self.temperature_worker.qmssig = int(self.qmssigreader.get_sig())

        workers = {worker.sensor_name: worker for worker in [self.temperature_worker]}
        self.sensor_names = list(workers)

        [self.start_thread(workers[s], threads[s]) for s in self.sensor_names]

    # MARK: start thread
    def start_thread(self, worker: Worker, thread: QtCore.QThread):
        """
        Setup workers [Dataframe creation]
        - Creates instances of worker
        - Creates connections
        - Creates Pandas Dataframes for data logging
        - Saves empty dataframes to local csv. File name based on date and time
        - starts threads
        - sets initial values for all parameters (zeros)
        """

        self.threads.append((thread, worker))
        worker.moveToThread(thread)
        self.connect_worker_signals(worker)

        # if worker.sensor_name != "DAC8532" or worker.sensor_name != "MCP4725":
        if worker.sensor_name == "NI9211":
            self.create_file(worker.sensor_name)
            self.log_message(
                f"<font size=4 color='blue'>{worker.sensor_name}</font>"
                + f" savepath:<br> {self.savepaths[worker.sensor_name]}",
            )
            worker.signal_send_pid.connect(self.update_pid_components)
        thread.started.connect(worker.start)
        thread.start()

    def connect_worker_signals(self, worker):
        """
        Connects worker signals to the main thread
        """
        worker.send_step_data.connect(self.on_worker_step)
        worker.signal_done.connect(self.on_worker_done)
        worker.send_message.connect(self.log_message)
        self.sigAbortWorkers.connect(worker.abort)

    # MARK: file managment
    def create_file(self, sensor_name):
        """
        Create file for saving sensor data
        """
        # if sensor_name == "MAX6675":
        #     self.savepaths[sensor_name] = os.path.join(
        #         os.path.abspath(self.datapath),
        #         f"cu_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_temp.csv",
        #     )
        #     with open(self.savepaths[sensor_name], "w") as f:
        #         f.writelines(self.generate_header_temperature())
        if sensor_name == "NI9211":
            self.savepaths[sensor_name] = os.path.join(
                os.path.abspath(self.datapath),
                f"temp_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            )
            with open(self.savepaths[sensor_name], "w") as f:
                f.writelines(self.generate_header_temperature())

    def generate_header_temperature(self):
        """
        Generage Teperature header
        """
        return [
            "# Title , Control Unit Temperature Control signals\n",
            f"# Date, {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"# Columns , {', '.join(self.config['Temperature Columns'])}\n",
            f"# Heater Pin , {self.config['FT232H']['Heater Output']['Pin']}\n",
            f"# Qms sync Pin , {self.config['FT232H']['Sync Input']['Pin']}\n" "#\n",
            "# [Data]\n",
        ]

    # MARK: Process Data
    @QtCore.pyqtSlot(list)
    def on_worker_step(self, result):
        """
        Collect data from worker
        - Recives data from worker(s)
        - Updates text indicators in GUI
        - Appends recived data to dataframes (call to self.__setStepData)
        - Updates data in plots (skips points if data is too big)
        """

        sensor_name = result[-1]

        if sensor_name == "NI9211":
            # [self.data, self.sensor_name]
            self.newdata[sensor_name] = result[0]
            self.append_data(sensor_name)
            self.save_data(sensor_name)
            # here 3 is number of data points recieved from worker.
            # TODO: update to self.newdata[sensor_name]['T'].mean()
            self.currentvalues["T"] = self.datadict[sensor_name].iloc[-3:]["T"].mean()
            self.currentvalues["Cathode Box T"] = (
                self.datadict[sensor_name].iloc[-3:]["Cathode Box T"].mean()
            )
            self.update_plots(sensor_name)

        self.update_current_values(sensor_name)

    def update_current_values(self, sensor_name):
        """
        update current values when new signal comes
        """

        # TODO: updated dislpayed valuves from dataframes

        self.temperature_control_dock.update_displayed_temperatures(
            self.temperature_setpoint, f"{self.currentvalues['T']:.0f}"
        )
        self.cathode_box_dock.update_displayed_temperatures(
            f"{self.currentvalues['Cathode Box T']:.0f}"
        )
        self.temperature_gauge_dock.gaugeT.update_value(self.currentvalues["T"])

    def calculate_skip_points(self, l, noskip=5000):
        return 1 if l < noskip else l // noskip + 1

    def append_data(self, sensor_name):
        """
        Append new data to dataframe
        """
        self.datadict[sensor_name] = pd.concat(
            [self.datadict[sensor_name], self.newdata[sensor_name]], ignore_index=True
        )

    def select_data_to_plot(self, sensor_name):
        """
        Select data based on self.time_window
        """
        df = self.datadict[sensor_name]
        if self.time_window > 0:
            last_ts = df["date"].iloc[-1]
            timewindow = last_ts - pd.Timedelta(self.time_window, "seconds")
            df = df[df["date"] > timewindow]
        return df

    # MARK: Save Data
    def save_data(self, sensor_name):
        """
        Save sensor data
        """
        savepath = self.savepaths[sensor_name]
        data = self.newdata[sensor_name]
        data.to_csv(savepath, mode="a", header=False, index=False)

    # MARK: PID tune
    @QtCore.pyqtSlot()
    def set_pid_coefficients(self):
        """update p, i, and d"""
        tags = ["p", "i", "d"]

        def calculate_spinbox_value(tag):
            significand = self.pid_tuning_dock.pid_spinboxes[tag]["significand"].value()
            exponent = self.pid_tuning_dock.pid_spinboxes[tag]["exponent"].value()
            return significand * 10**exponent

        pid_coffecients = {tag: calculate_spinbox_value(tag) for tag in tags}

        if self.temperature_worker is not None:
            self.temperature_worker.update_pid_coefficients(
                list(pid_coffecients.values())
            )
            self.__app.processEvents()

    def update_pid_components(self, pid_components):
        """update pid components browser"""
        self.pid_tuning_dock.update_display(*pid_components)

    # MARK: Set Heater
    @QtCore.pyqtSlot()
    def set_heater_goal(self):
        value = self.temperature_control_dock.temperatureSB.value()
        self.temperature_setpoint = value
        temp_now = self.currentvalues["T"]
        self.temperature_control_dock.set_heating_goal(
            self.temperature_setpoint, f"{temp_now:.0f}"
        )
        if self.temperature_worker is not None:
            self.temperature_worker.set_preset_temp(self.temperature_setpoint)
            self.__app.processEvents()

    # MARK: Aborting
    @QtCore.pyqtSlot(str)
    def on_worker_done(self, sensor_name):
        self.log_message(
            f"Sensor thread <font size=4 color='blue'> {sensor_name}</font> <font size=4 color={'red'}>stopped</font>",
            htmltag="div",
        )
        self.__workers_done += 1
        self.reset_data(sensor_name)
        if self.__workers_done == 2:
            self.abort_all_threads()

    @QtCore.pyqtSlot()
    def abort_all_threads(self):
        self.sigAbortWorkers.emit()
        for thread, worker in self.threads:
            thread.quit()
            thread.wait()

        self.threads = []

    def reset_data(self, sensor_name):
        self.datadict[sensor_name] = self.datadict[sensor_name].iloc[0:0]
        self.newdata[sensor_name] = self.newdata[sensor_name].iloc[0:0]

    # MARK: logging
    def generate_time_stamp(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log_to_file(self, message):
        filepath = self.config["Log File Path"]
        time_stamp = self.generate_time_stamp()
        new_line = f"{time_stamp}, {message}\n"
        with open(filepath, "a") as f:
            f.write(new_line)

    def log_message(self, message, htmltag="p"):
        """
        Append a message to the log browser with a timestamp.
        """
        time_stamp = self.generate_time_stamp()
        self.log_to_file(strip_tags(message))
        new_line = f"<{htmltag}>{time_stamp}: {message}</{htmltag}>"
        if not self.log_dock.log.toPlainText():
            self.log_dock.log.setHtml(new_line)
        else:
            current_text = self.log_dock.log.toHtml()
            current_text += new_line
            self.log_dock.log.setHtml(current_text)

        self.log_dock.log.moveCursor(self.log_dock.log.textCursor().End)
        # self.logDock.log.append(f"<{htmltag}>{nowstamp}: {message}</{htmltag}>")


def main():
    """
    for command line script using entrypoint
    """
    app = QtWidgets.QApplication([])
    widget = MainWidget(app)
    sys.exit(app.exec_())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    app.setWindowIcon(QtGui.QIcon("./icons/temperature.png"))
    widget = MainWidget(app)
    sys.exit(app.exec_())
