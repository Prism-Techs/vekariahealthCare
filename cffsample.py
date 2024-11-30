import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QListWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import time
from globalvar import globaladc
import RPi.GPIO as GPIO

class PeriodicThread(QThread):
    update_signal = pyqtSignal()

    def __init__(self, interval, parent=None):
        super().__init__(parent)
        self.interval = interval
        self.isStarted = False

    def run(self):
        self.isStarted = True
        while self.isStarted:
            self.update_signal.emit()
            time.sleep(self.interval)

    def stop(self):
        self.isStarted = False

    def kill(self):
        self.stop()
        self.wait()

switch = 20
contt_fva = 34.5
FONT = QFont("Arial", 15)
FONT2 = QFont("Arial", 20)
intervel = globaladc.get_cff_delay()
select = 1
cffValue_frq_x = 820
cffValue_frq_y = 40

def hardware():
    CffFovea.handleuserButton()

class CffFovea(QWidget):
    def __init__(self):
        super().__init__()
        self.response_count = 0
        self.skip_event = True
        self.threadCreated = False
        self.worker_cff = PeriodicThread(intervel)
        self.worker_cff.update_signal.connect(self.periodic_event)
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.max_apr = 0
        self.response_array = [0, 0, 0, 0, 0]
        
        self.initUI()
        
    def initUI(self):
        self.setGeometry(0, 0, 1024, 600)
        
        # Create widgets
        self.trialList = QListWidget(self)
        self.trialList.setFont(FONT)
        self.trialList.setFixedWidth(100)
        
        self.actionLabel = QLabel('Side Button \n Begins Trial', self)
        self.actionLabel.setFont(FONT)
        self.actionLabel.setStyleSheet("background-color: white;")
        
        self.cffValue_min = QLabel('    ', self)
        self.cffValue_min.setFont(FONT)
        self.cffValue_min.setStyleSheet("background-color: white;")
        
        self.cffValue_max = QLabel('    ', self)
        self.cffValue_max.setFont(FONT)
        self.cffValue_max.setStyleSheet("background-color: white;")
        
        self.cffValue_frq = QLabel('    ', self)
        self.cffValue_frq.setFont(FONT)
        self.cffValue_frq.setStyleSheet("background-color: #F7F442;")
        
        cffLabel = QLabel('CFF FOVEA :', self)
        cffLabel.setFont(FONT)
        
        # Position widgets
        cffLabel.move(420, 10)
        self.cffValue_min.move(430, 40)
        self.cffValue_max.move(500, 40)
        self.cffValue_frq.move(810, 30)
        self.actionLabel.move(380, 100)
        self.trialList.move(800, 60)

    def handleuserButton(self, switch):
        globaladc.get_print('handle to be implemented')
        jmp = False
        self.patient_switch_disable()
        time.sleep(0.15)        
        
        if self.skip_event:
            self.actionLabel.hide()
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
                self.trialList.insertItem(self.response_count, str(self.response_array[self.response_count]))
                self.min_apr = globaladc.get_cff_f_min_cal(self.response_count, self.freq_val)  
                self.response_count = self.response_count + 1
                self.cffValue_min.setText(str(self.min_apr))
                
                if self.response_count == 5:
                    self.max_apr = globaladc.get_cff_f_max_cal()                        
                    self.cffValue_max.setText(str(self.max_apr))
                    str_data = 'self.max_apr=' + str(self.max_apr)
                    globaladc.get_print(str_data)            
                    self.stop_thread()
                    avgval = globaladc.get_cff_f_avg_cal()
                    time.sleep(1)
                    globaladc.buzzer_3()
                    globaladc.get_print('done')
                    self.patient_switch_disable()
                    jmp = True
                    
                self.cffValue_frq.setText(str(self.freq_val))
                
        if not jmp:
            if self.skip_event:
                time.sleep(0.2) 
                globaladc.buzzer_3()            
            self.patient_switch_enable()

    def patient_switch_enable(self):
        globaladc.get_print('patient_switch_enable')
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(switch, GPIO.RISING, callback=self.handleuserButton)
                
    def patient_switch_disable(self):
        globaladc.get_print('patient_switch_disable')
        GPIO.remove_event_detect(switch)

    def show_ui(self):
        self.cffValue_min.setText('     ')
        self.cffValue_max.setText('     ')
        self.cffValue_frq.setText('     ')
        self.trialList.clear()
        self.show()
        self.actionLabel.show()
        globaladc.cff_Fovea_Prepair()
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.response_array = [0, 0, 0, 0, 0]
        self.response_count = 0 
        self.min_apr = 0
        self.max_apr = 0 
        self.skip_event = True
        self.threadCreated = False
        self.run_thread()
        globaladc.blue_led_off()

    def hide_ui(self):
        self.stop_thread()
        self.hide()
        
    def run_thread(self):
        globaladc.get_print("worker_cff thread started")        
        self.worker_cff = PeriodicThread(intervel)
        self.worker_cff.update_signal.connect(self.periodic_event)
        if not self.worker_cff.isStarted:
            self.worker_cff.start()
            self.patient_switch_enable()
        
    def stop_thread(self):
        globaladc.get_print("worker_cff thread stopped")
        if self.worker_cff.isStarted:
            self.worker_cff.stop()  
            self.worker_cff.kill()
            self.patient_switch_disable()
            self.skip_event = True
            self.threadCreated = False

    def periodic_event(self):
        if not self.skip_event:
            self.freq_val = round((self.freq_val - 0.5), 1)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CffFovea()
    ex.show()
    sys.exit(app.exec_())