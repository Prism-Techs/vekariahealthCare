import sys
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QListWidget, QVBoxLayout, QHBoxLayout, QGridLayout
)
from PyQt5.QtCore import QTimer
import RPi.GPIO as GPIO
from globalvar import globaladc

# Hardware Configuration
switch = 20
Font = ("Arial", 15)
intervel = globaladc.get_cff_delay()  # Retrieve delay from hardware

class CffFoveaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CFF Fovea Measurement")
        self.setGeometry(100, 100, 1024, 600)

        # Variables
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.max_apr = 0
        self.response_count = 0
        self.response_array = [0, 0, 0, 0, 0]
        self.skip_event = True

        # Timer for periodic events
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.periodic_event)

        # GUI Layout
        self.cff_label = QLabel("CFF Fovea Measurement", self)
        self.freq_label = QLabel(f"Frequency: {self.freq_val} Hz", self)
        self.min_label = QLabel("Min Frequency: -", self)
        self.max_label = QLabel("Max Frequency: -", self)

        self.trial_list = QListWidget(self)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_test)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_test)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.cff_label)
        layout.addWidget(self.freq_label)
        layout.addWidget(self.min_label)
        layout.addWidget(self.max_label)
        layout.addWidget(self.trial_list)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

        # GPIO Event Setup
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(switch, GPIO.RISING, callback=self.handle_user_button, bouncetime=200)

    def start_test(self):
        """Starts the CFF test."""
        globaladc.fliker_start_g()  # Start flicker
        self.response_count = 0
        self.response_array = [0, 0, 0, 0, 0]
        self.freq_val = self.freq_val_start
        self.freq_label.setText(f"Frequency: {self.freq_val} Hz")
        self.min_label.setText("Min Frequency: -")
        self.max_label.setText("Max Frequency: -")
        self.trial_list.clear()
        self.skip_event = False
        self.timer.start(intervel)  # Start periodic event timer

    def stop_test(self):
        """Stops the CFF test."""
        globaladc.get_print("Stopping Test")
        globaladc.fliker_stop()  # Stop flicker
        self.timer.stop()
        self.freq_val = self.freq_val_start
        self.freq_label.setText(f"Frequency: {self.freq_val} Hz")
        self.skip_event = True

    def handle_user_button(self, channel):
        """Handles the GPIO button press."""
        if not self.skip_event:
            globaladc.buzzer_1()  # Play a buzzer sound
            self.response_array[self.response_count] = self.freq_val
            self.trial_list.addItem(f"Trial {self.response_count + 1}: {self.freq_val} Hz")
            self.min_apr = globaladc.get_cff_f_min_cal(self.response_count, self.freq_val)
            self.min_label.setText(f"Min Frequency: {self.min_apr} Hz")
            self.response_count += 1

            if self.response_count == 5:
                self.max_apr = globaladc.get_cff_f_max_cal()
                self.max_label.setText(f"Max Frequency: {self.max_apr} Hz")
                avgval = globaladc.get_cff_f_avg_cal()
                globaladc.buzzer_3()  # Indicate test completion
                self.stop_test()  # Stop the test after 5 trials

    def periodic_event(self):
        """Periodic function to decrement the flicker frequency."""
        if not self.skip_event:
            self.freq_val = round((self.freq_val - 0.5), 1)
            self.freq_label.setText(f"Frequency: {self.freq_val} Hz")
            if self.freq_val < 5:
                self.stop_test()  # Stop if frequency goes below 5 Hz
            globaladc.put_cff_fovea_frq(self.freq_val)

    def closeEvent(self, event):
        """Clean up GPIO on application close."""
        GPIO.cleanup()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CffFoveaApp()
    window.show()
    sys.exit(app.exec_())
