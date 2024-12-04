import sys
import time
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QListWidget,
    QVBoxLayout,
    QPushButton,
)
from PyQt5.QtCore import QTimer
import RPi.GPIO as GPIO
from globalvar import globaladc

switch = 20
intervel = globaladc.get_cff_delay()


class CffFovea(QWidget):
    def __init__(self):
        super().__init__()

        self.response_count = 0
        self.skip_event = True
        self.threadCreated = False
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.max_apr = 0
        self.response_array = [0, 0, 0, 0, 0]

        # GUI Elements
        self.setWindowTitle("CFF Fovea Test")
        self.resize(1024, 600)

        layout = QVBoxLayout()

        self.cff_label = QLabel("CFF FOVEA:", self)
        layout.addWidget(self.cff_label)

        self.cffValue_min = QLabel("Min APR:    ", self)
        layout.addWidget(self.cffValue_min)

        self.cffValue_max = QLabel("Max APR:    ", self)
        layout.addWidget(self.cffValue_max)

        self.cffValue_frq = QLabel("Frequency:    ", self)
        layout.addWidget(self.cffValue_frq)

        self.patentActionLabel = QLabel(
            "Patient's side Button \n Begins Trial", self
        )
        layout.addWidget(self.patentActionLabel)

        self.trialList = QListWidget(self)
        layout.addWidget(self.trialList)

        # Set layout
        self.setLayout(layout)

        # GPIO Setup
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.patient_switch_enable()

    def handleuserButton(self):
        globaladc.get_print("handle to be implemented")
        jmp = False
        self.patient_switch_desable()
        time.sleep(0.15)

        if self.skip_event:
            self.patentActionLabel.hide()
            self.threadCreated = True
            self.freq_val = self.freq_val_start
            globaladc.fliker_start_g()
            time.sleep(0.2)
            self.skip_event = False
        else:
            self.skip_event = True
            time.sleep(0.5)
            if self.threadCreated:
                self.response_array[self.response_count] = self.freq_val
                self.trialList.addItem(str(self.response_array[self.response_count]))
                self.min_apr = globaladc.get_cff_f_min_cal(self.response_count, self.freq_val)
                self.response_count += 1
                self.cffValue_min.setText(f"Min APR: {self.min_apr}")

                if self.response_count == 5:
                    self.max_apr = globaladc.get_cff_f_max_cal()
                    self.cffValue_max.setText(f"Max APR: {self.max_apr}")
                    avgval = globaladc.get_cff_f_avg_cal()
                    globaladc.buzzer_3()
                    globaladc.get_print("done")
                    jmp = True

                self.cffValue_frq.setText(f"Frequency: {self.freq_val}")

        if not jmp:
            self.patient_switch_enable()

    def patient_switch_enable(self):
        globaladc.get_print("patient_switch_enable")
        GPIO.add_event_detect(switch, GPIO.RISING, callback=self.gpio_callback)

    def patient_switch_desable(self):
        globaladc.get_print("patient_switch_desable")
        GPIO.remove_event_detect(switch)

    def gpio_callback(self, channel):
        # This method is called by GPIO when the switch is pressed
        self.handleuserButton()

    def show(self):
        self.response_count = 0
        self.skip_event = True
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.max_apr = 0
        self.response_array = [0, 0, 0, 0, 0]

        self.cffValue_min.setText("Min APR:    ")
        self.cffValue_max.setText("Max APR:    ")
        self.cffValue_frq.setText("Frequency:    ")
        self.trialList.clear()
        self.patentActionLabel.show()
        self.patient_switch_enable()

    def hide(self):
        self.patient_switch_desable()


# Run Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CffFovea()
    window.show()
    sys.exit(app.exec_())
