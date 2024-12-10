import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, 
                           QVBoxLayout, QHBoxLayout, QPushButton, QListWidget)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
import time
import RPi.GPIO as GPIO
from dataclasses import dataclass
from typing import List, Tuple
from globalvar import globaladc

@dataclass
class CFFConfig:
    SWITCH_PIN: int = 20
    INITIAL_FREQUENCY: float = 34.5
    FREQUENCY_INCREMENT: float = 6.5
    MINIMUM_FREQUENCY: float = 5.0
    TRIALS_COUNT: int = 5
    DEBOUNCE_DELAY: float = 0.15
    DEFAULT_FONT = QFont("Arial", 15)
    LARGE_FONT = QFont("Arial", 20)

class FrequencyWorker(QThread):
    """Worker thread for frequency updates"""
    frequency_updated = pyqtSignal(float)
    trial_timeout = pyqtSignal()

    def __init__(self, initial_freq: float, interval: float):
        super().__init__()
        self.frequency = initial_freq
        self.interval = interval
        self.running = True

    def run(self):
        while self.running:
            if self.frequency > CFFConfig.MINIMUM_FREQUENCY:
                self.frequency = round(self.frequency - 0.5, 1)
                self.frequency_updated.emit(self.frequency)
                time.sleep(self.interval)
            else:
                self.trial_timeout.emit()
                break

    def stop(self):
        self.running = False

class GPIOMonitor(QThread):
    """Thread for monitoring GPIO button presses"""
    button_pressed = pyqtSignal()

    def __init__(self, pin: int):
        super().__init__()
        self.pin = pin
        self.running = True

    def run(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        while self.running:
            if GPIO.input(self.pin) == GPIO.HIGH:
                self.button_pressed.emit()
                time.sleep(CFFConfig.DEBOUNCE_DELAY)
            time.sleep(0.01)

    def stop(self):
        self.running = False
        GPIO.cleanup(self.pin)

class CFFTrial:
    def __init__(self):
        self.reset()

    def reset(self):
        self.current_trial = 0
        self.responses = [0.0] * CFFConfig.TRIALS_COUNT
        self.min_amplitude = 0.0
        self.max_amplitude = 0.0
        
    def record_response(self, frequency: float) -> bool:
        """Record trial response and return True if all trials complete"""
        if self.current_trial >= CFFConfig.TRIALS_COUNT:
            return True
            
        self.responses[self.current_trial] = frequency
        self.min_amplitude = globaladc.get_cff_f_min_cal(self.current_trial, frequency)
        self.current_trial += 1
        return self.current_trial >= CFFConfig.TRIALS_COUNT

class CFFWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.trial = CFFTrial()
        self.setup_ui()
        self.setup_threads()
        
    def setup_ui(self):
        self.setWindowTitle("CFF Fovea Test")
        self.setFixedSize(1024, 600)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Header
        header = QHBoxLayout()
        header_label = QLabel("CFF FOVEA:", font=CFFConfig.DEFAULT_FONT)
        self.min_label = QLabel("    ", font=CFFConfig.DEFAULT_FONT)
        self.max_label = QLabel("    ", font=CFFConfig.DEFAULT_FONT)
        self.freq_label = QLabel("    ", font=CFFConfig.DEFAULT_FONT)
        self.freq_label.setStyleSheet("background-color: #F7F442;")
        
        header.addWidget(header_label)
        header.addWidget(self.min_label)
        header.addWidget(self.max_label)
        header.addWidget(self.freq_label)
        header.addStretch()
        
        # Trial list
        self.trial_list = QListWidget()
        self.trial_list.setFont(CFFConfig.DEFAULT_FONT)
        self.trial_list.setMaximumWidth(100)
        
        # Patient action label
        self.patient_action = QLabel("Patient's side Button\nBegins Trial")
        self.patient_action.setFont(CFFConfig.DEFAULT_FONT)
        self.patient_action.setAlignment(Qt.AlignCenter)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.back_btn = QPushButton("<<")
        self.next_btn = QPushButton(">>")
        for btn in (self.back_btn, self.next_btn):
            btn.setFont(CFFConfig.LARGE_FONT)
            btn.setStyleSheet("background-color: green;")
        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.next_btn)

        # Add all elements to main layout
        layout.addLayout(header)
        layout.addWidget(self.patient_action, alignment=Qt.AlignCenter)
        layout.addWidget(self.trial_list, alignment=Qt.AlignRight)
        layout.addLayout(nav_layout)
        
        # Connect navigation buttons
        self.back_btn.clicked.connect(self.on_back)
        self.next_btn.clicked.connect(self.on_next)

    def setup_threads(self):
        # GPIO monitoring thread
        self.gpio_thread = GPIOMonitor(CFFConfig.SWITCH_PIN)
        self.gpio_thread.button_pressed.connect(self.handle_button_press)
        
        # Frequency update thread
        self.freq_thread = None
        
    def start_trial(self):
        """Start a new trial"""
        self.patient_action.hide()
        starting_freq = (CFFConfig.INITIAL_FREQUENCY if self.trial.current_trial == 0 
                        else self.trial.min_amplitude + CFFConfig.FREQUENCY_INCREMENT)
        
        # Start frequency decrease thread
        self.freq_thread = FrequencyWorker(starting_freq, globaladc.get_cff_delay())
        self.freq_thread.frequency_updated.connect(self.update_frequency)
        self.freq_thread.trial_timeout.connect(self.handle_timeout)
        self.freq_thread.start()
        
        globaladc.fliker_start_g()

    @pyqtSlot()
    def handle_button_press(self):
        """Handle patient button press"""
        if not self.freq_thread or not self.freq_thread.isRunning():
            self.start_trial()
        else:
            self.record_response()

    @pyqtSlot(float)
    def update_frequency(self, freq: float):
        """Update frequency display"""
        self.freq_label.setText(f"{freq:.1f}")
        globaladc.put_cff_fovea_frq(freq)

    @pyqtSlot()
    def handle_timeout(self):
        """Handle trial timeout"""
        self.freq_thread.stop()
        self.freq_thread = None
        globaladc.buzzer_3()
        self.reset_trial()

    def record_response(self):
        """Record current trial response"""
        if self.freq_thread:
            current_freq = float(self.freq_label.text())
            self.freq_thread.stop()
            self.freq_thread = None
            
            if self.trial.record_response(current_freq):
                self.complete_trials()
            else:
                self.trial_list.addItem(f"{current_freq:.1f}")
                self.min_label.setText(f"{self.trial.min_amplitude:.1f}")
                globaladc.buzzer_3()

    def complete_trials(self):
        """Handle completion of all trials"""
        self.trial.max_amplitude = globaladc.get_cff_f_max_cal()
        self.max_label.setText(f"{self.trial.max_amplitude:.1f}")
        
        avg_value = globaladc.get_cff_f_avg_cal()
        # currentPatientInfo.log_update(f"CFF_F-{avg_value}")
        
        time.sleep(1)
        globaladc.buzzer_3()
        self.hide()
        # pageDisctonary['BrkFovea_1'].show()

    def reset_trial(self):
        """Reset for new trial"""
        self.trial.reset()
        self.min_label.setText("    ")
        self.max_label.setText("    ")
        self.freq_label.setText("    ")
        self.trial_list.clear()
        self.patient_action.show()

    def showEvent(self, event):
        """Handle window show event"""
        super().showEvent(event)
        self.reset_trial()
        globaladc.cff_Fovea_Prepair()
        self.gpio_thread.start()
        globaladc.blue_led_off()

    def hideEvent(self, event):
        """Handle window hide event"""
        super().hideEvent(event)
        if self.freq_thread:
            self.freq_thread.stop()
        self.gpio_thread.stop()

    def on_back(self):
        """Handle back button press"""
        self.hide()
        # pageDisctonary['BrkparaFovea'].show()

    def on_next(self):
        """Handle next button press"""
        self.hide()
        # pageDisctonary['MainScreen'].show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CFFWindow()
    window.show()
    sys.exit(app.exec_())