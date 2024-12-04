import sys
import time
import RPi.GPIO as GPIO
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont

from globalvar import globaladc
# from globalvar import pageDisctonary
# from globalvar import currentPatientInfo

class CFFTest(QMainWindow):
    def __init__(self, frame=None):
        super().__init__()
        
        # Hardware and state variables
        self.switch = 20
        self.contt_fva = 34.5
        self.intervel = globaladc.get_cff_delay()
        
        # Test state variables
        self.response_count = 0
        self.skip_event = True
        self.threadCreated = False
        
        # Frequency and response tracking
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.max_apr = 0
        self.response_array = [0,0,0,0,0]
        
        # Fonts
        self.font_normal = QFont("Arial", 15)
        self.font_large = QFont("Arial", 20)
        
        self.setupUI()
        self.setupGPIO()
        
        # Timer for periodic events
        self.timer = QTimer()
        self.timer.timeout.connect(self.periodic_event)
        self.timer.start(int(self.intervel * 1000))  # Convert to milliseconds
        
    def setupUI(self):
        self.setWindowTitle('CFF Fovea Test')
        self.setGeometry(100, 100, 1024, 600)
        
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        layout = QGridLayout()
        
        # CFF Label
        cfflabel = QLabel('CFF FOVEA:', self)
        cfflabel.setFont(self.font_normal)
        
        # Minimum and Maximum Value Labels
        self.cffValue_min = QLabel('    ', self)
        self.cffValue_min.setFont(self.font_normal)
        self.cffValue_min.setStyleSheet("background-color: white")
        
        self.cffValue_max = QLabel('    ', self)
        self.cffValue_max.setFont(self.font_normal)
        self.cffValue_max.setStyleSheet("background-color: white")
        
        # Frequency Value Label
        self.cffValue_frq = QLabel('    ', self)
        self.cffValue_frq.setFont(self.font_normal)
        self.cffValue_frq.setStyleSheet("background-color: #F7F442")
        
        # Patient Action Label
        self.patentActionflabel = QLabel("Patient's side Button\nBegins Trial", self)
        self.patentActionflabel.setFont(self.font_normal)
        self.patentActionflabel.setStyleSheet("background-color: white")
        
        # Trial List
        self.trialList = QListWidget(self)
        self.trialList.setFont(self.font_normal)
        
        # Navigation Buttons
        self.fwButton = QPushButton(">>", self)
        self.fwButton.setFont(self.font_large)
        self.fwButton.setStyleSheet("background-color: green")
        self.fwButton.clicked.connect(self.onForward)
        
        self.bwButton = QPushButton("<<", self)
        self.bwButton.setFont(self.font_large)
        self.bwButton.setStyleSheet("background-color: green")
        self.bwButton.clicked.connect(self.onBackward)
        
        # Layout Positioning
        layout.addWidget(cfflabel, 0, 0)
        layout.addWidget(self.cffValue_min, 1, 0)
        layout.addWidget(self.cffValue_max, 1, 1)
        layout.addWidget(self.cffValue_frq, 1, 2)
        layout.addWidget(self.patentActionflabel, 2, 0, 1, 2)
        layout.addWidget(self.trialList, 1, 3, 3, 1)
        layout.addWidget(self.fwButton, 4, 2)
        layout.addWidget(self.bwButton, 4, 0)
        
        centralWidget.setLayout(layout)
        
    def setupGPIO(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.switch, GPIO.RISING, callback=self.handleUserButton)
        
    def handleUserButton(self, switch=None):
        globaladc.get_print('handle to be implemented')
        jmp = False
        self.patient_switch_desable()
        time.sleep(0.15)
        
        if self.skip_event:
            self.patentActionflabel.hide()
            self.threadCreated = True
            
            # Adjust frequency based on response count
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
                    
                    str_data = f'self.max_apr={self.max_apr}'
                    globaladc.get_print(str_data)
                    
                    avgval = globaladc.get_cff_f_avg_cal()
                    log_data = f"CFF_F-{avgval}"
                    # currentPatientInfo.log_update(log_data)
                    
                    time.sleep(1)
                    globaladc.buzzer_3()
                    globaladc.get_print('done')
                    
                    # Navigation logic (replace with your actual navigation)
                    self.hide()
                    # Uncomment and modify these lines according to your navigation setup
                    # pageDisctonary['CffFovea'].hide()
                    # pageDisctonary['BrkFovea_1'].show()
                    
                    self.patient_switch_desable()
                    jmp = True
                
                self.cffValue_frq.setText(str(self.freq_val))
        
        if not jmp:
            if self.skip_event:
                time.sleep(0.2)
                globaladc.buzzer_3()
            self.patient_switch_enable()
    
    def onForward(self):
        # Replace with your actual forward navigation
        self.hide()
        # pageDisctonary['CffFovea'].hide()
        # pageDisctonary['MainScreen'].show()
    
    def onBackward(self):
        # Replace with your actual backward navigation
        self.hide()
        # pageDisctonary['CffFovea'].hide()
        # pageDisctonary['BrkparaFovea'].show()
    
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
    
    def show(self):
        # Reset all values and prepare for a new test
        self.cffValue_min.setText('     ')
        self.cffValue_max.setText('     ')
        self.cffValue_frq.setText('     ')
        self.trialList.clear()
        
        # Reset test parameters
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.response_array = [0,0,0,0,0]
        self.response_count = 0
        self.min_apr = 0
        self.max_apr = 0
        self.skip_event = True
        self.threadCreated = False
        
        globaladc.cff_Fovea_Prepair()
        globaladc.blue_led_off()
        
        # Show the window
        super().show()
    
    def closeEvent(self, event):
        # Cleanup GPIO and resources
        GPIO.cleanup()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = CFFTest()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()