import sys
import time
import RPi.GPIO as GPIO
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton
from PyQt5.QtCore import QTimer
from globalvar import globaladc, currentPatientInfo

switch = 20
intervel = globaladc.get_cff_delay()
Font = "Arial"

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

        self.initUI()
        self.setupGPIO()

    def initUI(self):
        layout = QVBoxLayout()

        self.patentActionflabel = QLabel("Patient's side Button \n Begins Trial", self)
        self.cffValue_min = QLabel("    ", self)
        self.cffValue_max = QLabel("    ", self)
        self.cffValue_frq = QLabel("    ", self)
        self.trialList = QListWidget(self)

        layout.addWidget(QLabel("CFF FOVEA :", self))
        layout.addWidget(self.patentActionflabel)
        layout.addWidget(QLabel("Min Frequency:"))
        layout.addWidget(self.cffValue_min)
        layout.addWidget(QLabel("Max Frequency:"))
        layout.addWidget(self.cffValue_max)
        layout.addWidget(QLabel("Current Frequency:"))
        layout.addWidget(self.cffValue_frq)
        layout.addWidget(self.trialList)

        self.setLayout(layout)
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle("CFF FOVEA Test")

        # Buttons for navigation (if needed)
        fwButton = QPushButton(">>", self)
        fwButton.clicked.connect(self.onfw)
        layout.addWidget(fwButton)

        bwButton = QPushButton("<<", self)
        bwButton.clicked.connect(self.onbw)
        layout.addWidget(bwButton)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.periodic_event)
        self.run_thread()

    def setupGPIO(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        try:
            GPIO.add_event_detect(switch, GPIO.RISING, callback=self.gpio_callback)
        except RuntimeError:
            # Ignore if already detected
            pass

    def gpio_callback(self, channel):
        self.handle_user_button()

    def handle_user_button(self):
        jmp = False
        self.patient_switch_disable()
        time.sleep(0.15)  

        if self.skip_event:
            self.patentActionflabel.hide()
            self.threadCreated = True
            if self.response_count == 0:
                self.freq_val_start = self.freq_val_start
            else:
                self.freq_val_start = self.min_apr + 6.5
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
                self.cffValue_min.setText(str(self.min_apr))

                if self.response_count == 5:
                    self.max_apr = globaladc.get_cff_f_max_cal()
                    self.cffValue_max.setText(str(self.max_apr))
                    globaladc.get_print(f"Max Apr: {self.max_apr}")
                    avgval = globaladc.get_cff_f_avg_cal()
                    currentPatientInfo.log_update(f"CFF_F-{avgval}")
                    time.sleep(1)
                    globaladc.buzzer_3()
                    self.hide()
                    jmp = True

                self.cffValue_frq.setText(str(self.freq_val))

        if not jmp:
            if self.skip_event:
                time.sleep(0.2)
                globaladc.buzzer_3()
            self.patient_switch_enable()

    def patient_switch_enable(self):
        try:
            GPIO.add_event_detect(switch, GPIO.RISING, callback=self.gpio_callback)
        except RuntimeError:
            pass

    def patient_switch_disable(self):
        try:
            GPIO.remove_event_detect(switch)
        except RuntimeError:
            pass

    def periodic_event(self):
        if not self.skip_event:
            self.freq_val = round(self.freq_val - 0.5, 1)
            self.cffValue_frq.setText(str(self.freq_val))
            if self.freq_val < 5:
                self.skip_event = True
                self.threadCreated = False
                self.freq_val = self.freq_val_start
                self.cffValue_frq.setText(str(self.freq_val))
                globaladc.buzzer_3()
            globaladc.put_cff_fovea_frq(self.freq_val)
        else:
            globaladc.put_cff_fovea_frq(35)
            globaladc.get_print('CF')

    def onfw(self):
        globaladc.get_print("Forward button clicked")

    def onbw(self):
        globaladc.get_print("Backward button clicked")

    def run_thread(self):
        globaladc.get_print("Worker thread started")
        self.timer.start(intervel * 1000)

    def hide(self):
        self.timer.stop()
        self.patient_switch_disable()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CffFovea()
    window.show()

    # Clean up GPIO on exit
    import atexit
    @atexit.register
    def cleanup_gpio():
        GPIO.cleanup()

    sys.exit(app.exec_())
