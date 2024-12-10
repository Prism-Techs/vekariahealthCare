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
    """Worker thread for handling frequency updates"""
    frequency_updated = pyqtSignal(float)
    trial_timeout = pyqtSignal()

    def __init__(self, initial_freq: float, interval: float):
        super().__init__()
        self._frequency = initial_freq
        self._interval = interval
        self._running = True
        self._skip_event = False

    def run(self):
        while self._running:
            if not self._skip_event:
                # Decrease frequency
                self._frequency = round(self._frequency - 0.5, 1)
                self.frequency_updated.emit(self._frequency)
                
                # Check for minimum frequency
                if self._frequency < 5:
                    self._skip_event = True
                    self._frequency = self._initial_freq  # Reset to start frequency
                    self.frequency_updated.emit(self._frequency)
                    globaladc.buzzer_3()
                    self.trial_timeout.emit()
                
                globaladc.put_cff_fovea_frq(self._frequency)
            else:
                # When skipped, set default frequency
                globaladc.put_cff_fovea_frq(35)
                globaladc.get_print('CF')
            
            time.sleep(self._interval)

    def stop(self):
        self._running = False
        self.wait()
class GPIOMonitor(QThread):
    """Thread for monitoring GPIO button presses"""
    button_pressed = pyqtSignal()

    def __init__(self, pin: int):
        super().__init__()
        self._pin = pin
        self._running = True
        self._enabled = True

    def run(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
            while self._running:
                if self._enabled and GPIO.input(self._pin) == GPIO.HIGH:
                    self.button_pressed.emit()
                    time.sleep(CFFConfig.DEBOUNCE_DELAY)
                time.sleep(0.01)
        finally:
            self.cleanup()

    def enable(self):
        """Enable button detection"""
        globaladc.get_print('patient_switch_enable')
        self._enabled = True

    def disable(self):
        """Disable button detection"""
        globaladc.get_print('patient_switch_disable')
        self._enabled = False

    def stop(self):
        self._running = False
        self.cleanup()
        self.wait()

    def cleanup(self):
        try:
            GPIO.cleanup(self._pin)
        except:
            pass

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

        self.skip_event = True
        self.threadCreated = False
        self.response_count = 0
        self.freq_val_start = 34.5
        self.freq_val = self.freq_val_start
        self.min_apr = 0
        self.response_array = [0] * 5
        
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
        """Initialize threads for GPIO monitoring"""
        self._gpio_thread = GPIOMonitor(CFFConfig.SWITCH_PIN)
        self._gpio_thread.button_pressed.connect(self.handle_button_press)



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
        """Handles button press events, matching original logic"""
        globaladc.get_print('handle to be implemented')
        jmp = False
        
        # Disable button detection
        if self._gpio_thread:
            self._gpio_thread.disable()
        time.sleep(0.15)

        if self._trial_in_progress == False:  # equivalent to self.skip_event
            # Starting new measurement
            self.patient_action.hide()
            self._trial_in_progress = True

            # Set starting frequency based on trial count
            if self._trial_manager.current_trial == 0:
                start_freq = CFFConfig.INITIAL_FREQUENCY
            else:
                start_freq = self._trial_manager.min_amplitude + CFFConfig.FREQUENCY_INCREMENT

            self._current_frequency = start_freq
            
            # Start the flicker
            globaladc.fliker_start_g()
            
            # Start frequency decrease thread
            self._freq_thread = FrequencyWorker(start_freq, globaladc.get_cff_delay())
            self._freq_thread.frequency_updated.connect(self.update_frequency)
            self._freq_thread.trial_timeout.connect(self.handle_timeout)
            self._freq_thread.start()
            
            time.sleep(0.2)
            self._trial_in_progress = True

        else:
            # Recording measurement
            self._trial_in_progress = False
            time.sleep(0.5)

            if self._freq_thread:
                # Stop frequency updates
                self._freq_thread.stop()
                self._freq_thread = None

                # Record response
                self.trial_list.addItem(f"{self._current_frequency:.1f}")
                
                # Calculate and update minimum amplitude
                self._trial_manager.record_response(self._current_frequency)
                self.min_label.setText(f"{self._trial_manager.min_amplitude:.1f}")
                
                # Check if all trials are complete
                if self._trial_manager.is_complete:
                    self.complete_trials()
                    jmp = True
                
                self.freq_label.setText(f"{self._current_frequency:.1f}")

        # Re-enable button if not jumping to next screen
        if not jmp:
            if not self._trial_in_progress:  # equivalent to self.skip_event
                time.sleep(0.2)
                globaladc.buzzer_3()
            if self._gpio_thread:
                self._gpio_thread.enable()


    @pyqtSlot(float)
    def update_frequency(self, new_freq: float):
        """Handle frequency updates from worker thread"""
        self._current_frequency = new_freq
        self.freq_label.setText(f"{new_freq:.1f}")


    def complete_trials(self):
        """Handle completion of all trials"""
        # Update max amplitude display
        self.max_label.setText(f"{self._trial_manager.max_amplitude:.1f}")
        
        # Log the data
        globaladc.get_print(f'self.max_apr={self._trial_manager.max_amplitude}')
        
        # Calculate and log average
        avg_val = globaladc.get_cff_f_avg_cal()
        log_data = f"CFF_F-{avg_val}"
        # currentPatientInfo.log_update(log_data)  # Uncomment when currentPatientInfo is available
        
        # Cleanup and transition
        time.sleep(1)
        globaladc.buzzer_3()
        globaladc.get_print('done')
        
        # Stop GPIO monitoring
        if self._gpio_thread:
            self._gpio_thread.disable()
        
        # Hide current window
        self.hide()
        # Uncomment when pageDisctonary is available:
        # pageDisctonary['BrkFovea_1'].show()

    @pyqtSlot()
    def handle_timeout(self):
        """Handle trial timeout - when frequency goes below minimum"""
        self._trial_in_progress = False
        if self._freq_thread:
            self._freq_thread.stop()
            self._freq_thread = None
            
        # Reset to start frequency
        self._current_frequency = CFFConfig.INITIAL_FREQUENCY
        self.freq_label.setText(f"{self._current_frequency:.1f}")

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

    def complete_trial_sequence(self):
            """Handle completion of all trials"""
            # Calculate maximum amplitude
            self.max_apr = globaladc.get_cff_f_max_cal()
            self.max_label.setText(str(self.max_apr))
            
            # Log the data
            str_data = f'self.max_apr={self.max_apr}'
            globaladc.get_print(str_data)
            
            # Calculate and log average value
            avgval = globaladc.get_cff_f_avg_cal()
            log_data = f"CFF_F-{avgval}"
            # currentPatientInfo.log_update(log_data)
            
            # Final cleanup and transition
            time.sleep(1)
            globaladc.buzzer_3()
            globaladc.get_print('done')
            
            # Stop GPIO monitoring
            self.gpio_thread.stop()
            
            # Transition to next screen
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
        self.reset_test()
        globaladc.cff_Fovea_Prepair()
        if self._gpio_thread:
            self._gpio_thread.start()  # Start GPIO monitoring
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