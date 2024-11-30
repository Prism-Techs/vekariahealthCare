import sys
import time
import RPi.GPIO as GPIO
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QListWidget, 
                             QPushButton, QVBoxLayout, QHBoxLayout, QFrame)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

# Import your custom modules (assuming they exist in your project)
import PerodicThread 
from globalvar import globaladc

# Global variable to store the CffFovea widget instance
current_cff_fovea_instance = None

def hardware():
    global current_cff_fovea_instance
    if current_cff_fovea_instance:
        current_cff_fovea_instance.handleuserButton()

class CffFoveaWidget(QWidget):
    def __init__(self, on_forward_callback=None, on_backward_callback=None):
        super().__init__()
        global current_cff_fovea_instance
        current_cff_fovea_instance = self

        self.switch = 20
        self.contt_fva = 34.5
        self.intervel = globaladc.get_cff_delay()
        
        # Store navigation callbacks
        self.on_forward_callback = on_forward_callback
        self.on_backward_callback = on_backward_callback
        
        self.init_ui()
        self.init_variables()

    def init_variables(self):
        self.response_count = 0
        self.skip_event = True
        self.threadCreated = False
        self.worker_cff = PerodicThread.PeriodicThread(self.intervel, self)
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.max_apr = 0
        self.response_array = [0, 0, 0, 0, 0]

    def init_ui(self):
        self.setWindowTitle('CFF Fovea')
        self.setGeometry(100, 100, 1024, 600)

        # Main Layout
        main_layout = QVBoxLayout()

        # Top Section
        top_section = QHBoxLayout()
        self.cff_label = QLabel('CFF FOVEA:')
        self.cff_label.setFont(QFont('Arial', 15))
        
        self.cffValue_min = QLabel('    ')
        self.cffValue_min.setFont(QFont('Arial', 15))
        
        self.cffValue_max = QLabel('    ')
        self.cffValue_max.setFont(QFont('Arial', 15))
        
        self.cffValue_frq = QLabel('    ')
        self.cffValue_frq.setFont(QFont('Arial', 15))
        self.cffValue_frq.setStyleSheet('background-color: #F7F442;')

        top_section.addWidget(self.cff_label)
        top_section.addWidget(self.cffValue_min)
        top_section.addWidget(self.cffValue_max)
        top_section.addWidget(self.cffValue_frq)
        main_layout.addLayout(top_section)

        # Middle Section
        middle_section = QHBoxLayout()
        self.patient_action_label = QLabel('Patient\'s side Button\nBegins Trial')
        self.patient_action_label.setFont(QFont('Arial', 15))
        
        self.trial_list = QListWidget()
        self.trial_list.setFont(QFont('Arial', 15))
        self.trial_list.setFixedWidth(100)

        middle_section.addWidget(self.patient_action_label)
        middle_section.addWidget(self.trial_list)
        main_layout.addLayout(middle_section)

        # Bottom Section
        bottom_section = QHBoxLayout()
        self.bw_button = QPushButton('<<')
        self.bw_button.setFont(QFont('Arial', 20))
        self.bw_button.setStyleSheet('background-color: green; color: white;')
        self.bw_button.clicked.connect(self.on_bw)

        self.fw_button = QPushButton('>>')
        self.fw_button.setFont(QFont('Arial', 20))
        self.fw_button.setStyleSheet('background-color: green; color: white;')
        self.fw_button.clicked.connect(self.on_fw)

        bottom_section.addWidget(self.bw_button)
        bottom_section.addWidget(self.fw_button)
        main_layout.addLayout(bottom_section)

        self.setLayout(main_layout)

        # Timer for periodic events
        self.periodic_timer = QTimer(self)
        self.periodic_timer.timeout.connect(self.periodic_event)

    def handleuserButton(self, switch=None):
        globaladc.get_print('handle to be implemented')
        jmp = False
        self.patient_switch_disable()
        time.sleep(0.15)

        if self.skip_event:
            self.patient_action_label.hide()
            self.threadCreated = True

            # Frequency adjustment logic similar to Tkinter version
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
                self.trial_list.insertItem(self.response_count, str(self.response_array[self.response_count]))
                
                self.min_apr = globaladc.get_cff_f_min_cal(self.response_count, self.freq_val)
                self.response_count += 1
                
                self.cffValue_min.setText(str(self.min_apr))

                if self.response_count == 5:
                    self.max_apr = globaladc.get_cff_f_max_cal()
                    self.cffValue_max.setText(str(self.max_apr))
                    
                    globaladc.get_print(f'self.max_apr={self.max_apr}')
                    
                    avgval = globaladc.get_cff_f_avg_cal()
                    log_data = f"CFF_F-{avgval}"
                    
                    time.sleep(1)
                    globaladc.buzzer_3()
                    globaladc.get_print('done')
                    
                    # Replaced page navigation with callback
                    if self.on_forward_callback:
                        self.on_forward_callback()
                    
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
        GPIO.setup(self.switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.switch, GPIO.RISING, callback=self.handleuserButton)

    def patient_switch_disable(self):
        globaladc.get_print('patient_switch_disable')
        GPIO.remove_event_detect(self.switch)

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

    def on_fw(self):
        # Replaced direct page navigation with callback
        if self.on_forward_callback:
            self.on_forward_callback()

    def on_bw(self):
        # Replaced direct page navigation with callback
        if self.on_backward_callback:
            self.on_backward_callback()

    def show_widget(self):
        self.reset_ui()
        self.show()
        globaladc.cff_Fovea_Prepair()
        globaladc.blue_led_off()
        self.start_thread()

    def reset_ui(self):
        self.cffValue_min.setText('     ')
        self.cffValue_max.setText('     ')
        self.cffValue_frq.setText('     ')
        self.trial_list.clear()
        
        self.init_variables()
        self.patient_action_label.show()

    def start_thread(self):
        globaladc.get_print("worker_cff thread started")
        self.periodic_timer.start(self.intervel)  # Start periodic timer
        self.patient_switch_enable()

    def stop_thread(self):
        globaladc.get_print("worker_cff thread stopped")
        self.periodic_timer.stop()
        self.patient_switch_disable()
        self.skip_event = True
        self.threadCreated = False

    @classmethod
    def get_current_instance(cls):
        return current_cff_fovea_instance

def main():
    app = QApplication(sys.argv)
    
    # Example of how to use with navigation callbacks
    def forward_callback():
        print("Navigate forward")
        # Add your forward navigation logic here
    
    def backward_callback():
        print("Navigate backward")
        # Add your backward navigation logic here
    
    cff_fovea = CffFoveaWidget(
        on_forward_callback=forward_callback, 
        on_backward_callback=backward_callback
    )
    cff_fovea.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()