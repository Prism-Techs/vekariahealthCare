import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, 
                           QVBoxLayout, QHBoxLayout, QPushButton, QListWidget)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QFont
import time
import RPi.GPIO as GPIO
from dataclasses import dataclass
from typing import List, Optional
from globalvar import globaladc

@dataclass
class CFFConfig:
    """Configuration constants for CFF testing"""
    SWITCH_PIN: int = 20
    INITIAL_FREQUENCY: float = 34.5
    FREQUENCY_DECREMENT: float = 0.5
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
        self._initial_freq = initial_freq
        self._frequency = initial_freq
        self._interval = interval
        self._running = True

    def run(self):
        while self._running:
            if self._frequency > CFFConfig.MINIMUM_FREQUENCY:
                self._frequency = round(self._frequency - CFFConfig.FREQUENCY_DECREMENT, 1)
                self.frequency_updated.emit(self._frequency)
                globaladc.put_cff_fovea_frq(self._frequency)
                time.sleep(self._interval)
            else:
                self._frequency = self._initial_freq
                self.frequency_updated.emit(self._frequency)
                globaladc.buzzer_3()
                self.trial_timeout.emit()
                break

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
        globaladc.get_print('patient_switch_enable')
        self._enabled = True

    def disable(self):
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

class TrialManager:
    """Manages the state and data for CFF trials"""
    def __init__(self):
        self.reset()

    def reset(self):
        self._current_trial = 0
        self._responses = [0.0] * CFFConfig.TRIALS_COUNT
        self._min_amplitude = 0.0
        self._max_amplitude = 0.0

    @property
    def current_trial(self) -> int:
        return self._current_trial

    @property
    def is_complete(self) -> bool:
        return self._current_trial >= CFFConfig.TRIALS_COUNT

    @property
    def min_amplitude(self) -> float:
        return self._min_amplitude

    @property
    def max_amplitude(self) -> float:
        return self._max_amplitude

    def record_response(self, frequency: float) -> bool:
        if self.is_complete:
            return True

        self._responses[self._current_trial] = frequency
        self._min_amplitude = globaladc.get_cff_f_min_cal(self._current_trial, frequency)
        self._current_trial += 1

        if self.is_complete:
            self._max_amplitude = globaladc.get_cff_f_max_cal()
            return True
        return False

class CFFWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Initialize all attributes first
        self._trial_manager = TrialManager()
        self._freq_thread = None
        self._gpio_thread = None
        self._current_frequency = CFFConfig.INITIAL_FREQUENCY
        self._skip_event = True  # Changed from _trial_in_progress to match original logic
        self._thread_created = False  # Added to match original code
        self._response_count = 0  # Added to track responses like original
        
        # Initialize UI elements that will be referenced elsewhere
        self.min_label = None
        self.max_label = None
        self.freq_label = None
        self.trial_list = None
        self.patient_action = None
        self.back_btn = None
        self.next_btn = None
        
        # Setup UI and threads
        self.setup_ui()
        self.setup_threads()

    def setup_ui(self):
        self.setWindowTitle("CFF Fovea Test")
        self.setFixedSize(1024, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Setup header
        header_layout = QHBoxLayout()
        self.setup_header(header_layout)
        main_layout.addLayout(header_layout)

        # Setup trial section
        self.setup_trial_section()
        main_layout.addWidget(self.patient_action, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.trial_list, alignment=Qt.AlignRight)

        # Setup navigation
        nav_layout = QHBoxLayout()
        self.setup_navigation(nav_layout)
        main_layout.addLayout(nav_layout)

    def setup_header(self, layout):
        header_label = QLabel("CFF FOVEA:", font=CFFConfig.DEFAULT_FONT)
        self.min_label = QLabel("    ", font=CFFConfig.DEFAULT_FONT)
        self.max_label = QLabel("    ", font=CFFConfig.DEFAULT_FONT)
        self.freq_label = QLabel("    ", font=CFFConfig.DEFAULT_FONT)
        self.freq_label.setStyleSheet("background-color: #F7F442;")
        
        for widget in (header_label, self.min_label, self.max_label, self.freq_label):
            layout.addWidget(widget)
        layout.addStretch()

    def setup_trial_section(self):
        self.trial_list = QListWidget()
        self.trial_list.setFont(CFFConfig.DEFAULT_FONT)
        self.trial_list.setMaximumWidth(100)
        
        self.patient_action = QLabel("Patient's side Button\nBegins Trial")
        self.patient_action.setFont(CFFConfig.DEFAULT_FONT)
        self.patient_action.setAlignment(Qt.AlignCenter)

    def setup_navigation(self, layout):
        self.back_btn = QPushButton("<<")
        self.next_btn = QPushButton(">>")
        
        for btn in (self.back_btn, self.next_btn):
            btn.setFont(CFFConfig.LARGE_FONT)
            btn.setStyleSheet("background-color: green;")
        
        self.back_btn.clicked.connect(self.on_back)
        self.next_btn.clicked.connect(self.on_next)
        
        layout.addWidget(self.back_btn)
        layout.addWidget(self.next_btn)

    def setup_threads(self):
        self._gpio_thread = GPIOMonitor(CFFConfig.SWITCH_PIN)
        self._gpio_thread.button_pressed.connect(self.handle_button_press)


    @pyqtSlot()
    def handle_button_press(self):
        globaladc.get_print('handle to be implemented')
        jmp = False
        
        if self._gpio_thread:
            self._gpio_thread.disable()
        time.sleep(0.15)

        if self._skip_event:
            # Starting new measurement
            self.patient_action.hide()
            self._thread_created = True

            # Set starting frequency based on trial count
            if self._response_count == 0:
                start_freq = CFFConfig.INITIAL_FREQUENCY
            else:
                start_freq = self._trial_manager.min_amplitude + CFFConfig.FREQUENCY_INCREMENT

            self._current_frequency = start_freq
            
            # Start the flicker
            globaladc.fliker_start_g()
            
            # Start frequency decrease thread
            if self._freq_thread is None:
                self._freq_thread = FrequencyWorker(start_freq, globaladc.get_cff_delay())
                self._freq_thread.frequency_updated.connect(self.update_frequency)
                self._freq_thread.trial_timeout.connect(self.handle_timeout)
                self._freq_thread.start()
            
            time.sleep(0.2)
            self._skip_event = False

        else:
            # Recording measurement
            self._skip_event = True
            time.sleep(0.5)

            if self._thread_created and self._freq_thread:
                # Stop frequency updates but don't destroy thread
                self._freq_thread.stop()
                self._freq_thread = None
                globaladc.fliker_stop_g()  # Add this to stop flickering

                # Record response
                self.trial_list.addItem(f"{self._current_frequency:.1f}")
                self._trial_manager.record_response(self._current_frequency)
                self.min_label.setText(f"{self._trial_manager.min_amplitude:.1f}")
                
                self._response_count += 1
                
                # Check if all trials are complete
                if self._response_count == 5:
                    self.max_label.setText(f"{self._trial_manager.max_amplitude:.1f}")
                    avg_val = globaladc.get_cff_f_avg_cal()
                    globaladc.get_print(f"CFF_F-{avg_val}")
                    time.sleep(1)
                    globaladc.buzzer_3()
                    if self._gpio_thread:
                        self._gpio_thread.disable()
                    self.hide()
                    jmp = True
                
                self.freq_label.setText(f"{self._current_frequency:.1f}")

        # Re-enable button if not jumping to next screen
        if not jmp:
            if self._skip_event:
                time.sleep(0.2)
                globaladc.buzzer_3()
            if self._gpio_thread:
                self._gpio_thread.enable()

    @pyqtSlot(float)
    def update_frequency(self, new_freq):
        self._current_frequency = new_freq
        self.freq_label.setText(f"{new_freq:.1f}")
        globaladc.put_cff_fovea_frq(new_freq)

    @pyqtSlot()
    def handle_timeout(self):
        self._trial_in_progress = False
        if self._freq_thread:
            self._freq_thread.stop()
            self._freq_thread = None
        
        self.freq_label.setText(f"{CFFConfig.INITIAL_FREQUENCY:.1f}")

    def complete_trials(self):
        self.max_label.setText(f"{self._trial_manager.max_amplitude:.1f}")
        avg_val = globaladc.get_cff_f_avg_cal()
        globaladc.get_print(f"CFF_F-{avg_val}")
        
        time.sleep(1)
        globaladc.buzzer_3()
        
        if self._gpio_thread:
            self._gpio_thread.disable()
        
        self.hide()

    def update_display(self):
        self.freq_label.setText(f"{self._current_frequency:.1f}")
        self.min_label.setText(f"{self._trial_manager.min_amplitude:.1f}")

    def reset(self):
        """Reset the window state for a new test"""
        self._trial_manager.reset()
        self._trial_in_progress = False
        self._current_frequency = CFFConfig.INITIAL_FREQUENCY
        
        self.min_label.setText("    ")
        self.max_label.setText("    ")
        self.freq_label.setText("    ")
        self.trial_list.clear()
        self.patient_action.show()

    def showEvent(self, event):
        super().showEvent(event)
        self.reset()
        globaladc.cff_Fovea_Prepair()
        if self._gpio_thread:
            self._gpio_thread.start()
        globaladc.blue_led_off()

    def hideEvent(self, event):
        super().hideEvent(event)
        if self._freq_thread:
            self._freq_thread.stop()
        if self._gpio_thread:
            self._gpio_thread.stop()

    def on_back(self):
        self.hide()
        # Add navigation logic here

    def on_next(self):
        self.hide()
        # Add navigation logic here

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CFFWindow()
    window.show()
    sys.exit(app.exec_())