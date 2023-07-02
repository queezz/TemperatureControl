from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

class LampWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(30, 30)
        self.setAlignment(Qt.AlignCenter)
        self.update_color(False)  # デフォルトは消灯色

    def set_state(self, is_on):
        self.update_color(is_on)

    def update_color(self, is_on):
        color = QColor("green" if is_on else "red")
        self.setStyleSheet(f"background-color: {color.name()}")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.lamp = LampWidget()
        layout.addWidget(self.lamp)
        self.setLayout(layout)

        # ボタンをクリックするとランプの状態が切り替わる例
        self.is_lamp_on = False
        self.lamp.set_state(self.is_lamp_on)

    def toggle_lamp_state(self):
        self.is_lamp_on = not self.is_lamp_on
        self.lamp.set_state(self.is_lamp_on)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
