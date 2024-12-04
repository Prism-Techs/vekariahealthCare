from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
import sys
import RPi.GPIO as GPIO
import time
from globalvar import globaladc



class CFFTest(QMainWindow):
    def __init__(self, frame=None):
        super().__init__()
        self.switch = 20
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.response_count = 0
        self.skip_event = True
        self.threadCreated = False
        self.response_array = [0,0,0,0,0]
        self.min_apr = 0
        self.max_apr = 0
        self.flicker_bool = True
        
        globaladc.flicker_Prepair()
        self.globaladc = globaladc
        self.globaladc.fliker_start_g()
        
        self.setupUI()
        self.setupGPIO()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.periodic_event)
        self.timer.start(1000)

    def setupUI(self):
        self.setWindowTitle('CFF Test')
        self.setGeometry(100, 100, 1024, 600)
        
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QGridLayout()
        
        self.cff_label = QLabel('CFF FOVEA:', self)
        self.cff_label.setStyleSheet("font: 15pt Arial")
        
        self.min_label = QLabel('', self)
        self.min_label.setStyleSheet("font: 15pt Arial; background-color: white")
        
        self.max_label = QLabel('', self)
        self.max_label.setStyleSheet("font: 15pt Arial; background-color: white")
        
        self.freq_label = QLabel('', self)
        self.freq_label.setStyleSheet("font: 15pt Arial; background-color: #F7F442")
        
        self.action_label = QLabel("Patient's side Button\nBegins Trial", self)
        self.action_label.setStyleSheet("font: 15pt Arial; background-color: white")
        
        self.trial_list = QListWidget()
        self.trial_list.setStyleSheet("font: 15pt Arial")
        self.trial_list.setMaximumWidth(100)
        
        layout.addWidget(self.cff_label, 0, 1)
        layout.addWidget(self.min_label, 1, 1)
        layout.addWidget(self.max_label, 1, 2)
        layout.addWidget(self.freq_label, 1, 3)
        layout.addWidget(self.action_label, 2, 1, 1, 2)
        layout.addWidget(self.trial_list, 1, 4, 3, 1)
        
        centralWidget.setLayout(layout)

    def setupGPIO(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.switch, GPIO.RISING, callback=self.handleUserButton)

    def handleUserButton(self, channel):
        globaladc.get_print('handle to be implemented')
        jmp = False
        self.patient_switch_desable()
        time.sleep(0.15)

        if self.skip_event:
            self.action_label.hide()
            self.threadCreated = True
            
            # Adjust starting frequency based on response count
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
                self.trial_list.addItem(str(self.response_array[self.response_count]))
                
                self.min_apr = globaladc.get_cff_f_min_cal(self.response_count, self.freq_val)
                self.response_count += 1
                
                self.min_label.setText(str(self.min_apr))
                
                if self.response_count == 5:
                    self.max_apr = globaladc.get_cff_f_max_cal()
                    self.max_label.setText(str(self.max_apr))
                    
                    str_data = 'self.max_apr=' + str(self.max_apr)
                    globaladc.get_print(str_data)
                    
                    avgval = globaladc.get_cff_f_avg_cal()
                    globaladc.get_print(f"CFF_F-{avgval}")
                    
                    time.sleep(1)
                    globaladc.buzzer_3()
                    globaladc.get_print('done')
                    
                    # Close the application or add your navigation logic here
                    self.close()
                    
                    self.patient_switch_desable()
                    jmp = True
                
                self.freq_label.setText(str(self.freq_val))

        if not jmp:
            if self.skip_event:
                time.sleep(0.2)
                globaladc.buzzer_3()
            self.patient_switch_enable()

    def patient_switch_enable(self):
        globaladc.get_print('patient_switch_enable')
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.switch, GPIO.RISING, callback=self.handleUserButton)

    def patient_switch_desable(self):
        globaladc.get_print('patient_switch_desable')
        GPIO.remove_event_detect(self.switch)

    def periodic_event(self):
        if not self.skip_event:
            self.freq_val = round(self.freq_val - 1.0, 1)
            self.freq_label.setText(str(self.freq_val))
            self.globaladc.put_cff_fovea_frq(self.freq_val)
            
            self.globaladc.fliker(1 if self.flicker_bool else 0)
            self.flicker_bool = not self.flicker_bool
            
            if self.freq_val < 5:
                self.skip_event = True
                self.freq_val = self.freq_val_start
                self.freq_label.setText(str(self.freq_val))
                self.globaladc.buzzer_3()

    def closeEvent(self, event):
        self.globaladc.fliker(0)
        GPIO.cleanup()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CFFTest()
    window.show()
    sys.exit(app.exec_())