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
    BUTTON_STYLE = "background-color: green;"
    FREQ_LABEL_STYLE = "background-color: #F7F442;"

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
        self._skip_event = True

    def run(self):
        while self._running:
            if not self._skip_event:
                self._frequency = round(self._frequency - CFFConfig.FREQUENCY_DECREMENT, 1)
                self.frequency_updated.emit(self._frequency)
                
                if self._frequency <= CFFConfig.MINIMUM_FREQUENCY:
                    self._skip_event = True
                    self._frequency = self._initial_freq
                    self.frequency_updated.emit(self._frequency)
                    globaladc.buzzer_3()
                    self.trial_timeout.emit()
                
                globaladc.put_cff_fovea_frq(self._frequency)
            else:
                globaladc.put_cff_fovea_frq(CFFConfig.INITIAL_FREQUENCY)
            
            time.sleep(self._interval)

    def set_skip_event(self, skip: bool):
        self._skip_event = skip

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
        self._setup_gpio()

    def _setup_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        while self._running:
            if self._enabled and GPIO.input(self._pin) == GPIO.HIGH:
                self.button_pressed.emit()
                time.sleep(CFFConfig.DEBOUNCE_DELAY)
            time.sleep(0.01)

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def stop(self):
        self._running = False
        GPIO.cleanup(self._pin)
        self.wait()

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

    @property
    def min_amplitude(self) -> float:
        return self._min_amplitude

    @property
    def max_amplitude(self) -> float:
        return self._max_amplitude

class CFFWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._initialize_attributes()
        self._initialize_hardware()
        self.setup_ui()
        self.setup_threads()

    def _initialize_attributes(self):
        """Initialize all class attributes"""
        self._trial_manager = TrialManager()
        self._freq_thread = None
        self._gpio_thread = None
        self._current_frequency = CFFConfig.INITIAL_FREQUENCY
        self._skip_event = True
        self._thread_created = False
        self._response_count = 0
        self.min_label = None
        self.max_label = None
        self.freq_label = None
        self.trial_list = None
        self.patient_action = None
        self.back_btn = None
        self.next_btn = None

    def _initialize_hardware(self):
        """Initialize hardware state"""
        globaladc.on_time = 1
        globaladc.cff_Fovea_Prepair()
        time.sleep(0.1)
        self._ensure_flicker_state()

    def _ensure_flicker_state(self):
        """Ensure proper flicker LED state"""
        globaladc.fliker_stop()
        time.sleep(0.1)
        globaladc.green_volt_control(20)
        globaladc.green_freq_control(0)
        globaladc.fliker_start_g()

    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("CFF Fovea Test")
        self.setFixedSize(1024, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        self._setup_header(layout)
        self._setup_trial_section(layout)
        self._setup_navigation(layout)

    def _setup_header(self, parent_layout):
        """Setup header section with labels"""
        header_layout = QHBoxLayout()
        
        header_label = QLabel("CFF FOVEA:", font=CFFConfig.DEFAULT_FONT)
        self.min_label = QLabel("    ", font=CFFConfig.DEFAULT_FONT)
        self.max_label = QLabel("    ", font=CFFConfig.DEFAULT_FONT)
        self.freq_label = QLabel("    ", font=CFFConfig.DEFAULT_FONT)
        self.freq_label.setStyleSheet(CFFConfig.FREQ_LABEL_STYLE)
        
        for widget in (header_label, self.min_label, self.max_label, self.freq_label):
            header_layout.addWidget(widget)
        
        header_layout.addStretch()
        parent_layout.addLayout(header_layout)

    def _setup_trial_section(self, parent_layout):
        """Setup trial list and patient action sections"""
        self.trial_list = QListWidget()
        self.trial_list.setFont(CFFConfig.DEFAULT_FONT)
        self.trial_list.setMaximumWidth(100)

        self.patient_action = QLabel("Patient's side Button\nBegins Trial")
        self.patient_action.setFont(CFFConfig.DEFAULT_FONT)
        self.patient_action.setAlignment(Qt.AlignCenter)

        parent_layout.addWidget(self.patient_action, alignment=Qt.AlignCenter)
        parent_layout.addWidget(self.trial_list, alignment=Qt.AlignRight)

    def _setup_navigation(self, parent_layout):
        """Setup navigation buttons"""
        nav_layout = QHBoxLayout()

        self.back_btn = QPushButton("<<")
        self.next_btn = QPushButton(">>")

        for btn in (self.back_btn, self.next_btn):
            btn.setFont(CFFConfig.LARGE_FONT)
            btn.setStyleSheet(CFFConfig.BUTTON_STYLE)

        self.back_btn.clicked.connect(self.on_back)
        self.next_btn.clicked.connect(self.on_next)

        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.next_btn)
        parent_layout.addLayout(nav_layout)

    def setup_threads(self):
        """Initialize and setup monitoring threads"""
        self._gpio_thread = GPIOMonitor(CFFConfig.SWITCH_PIN)
        self._gpio_thread.button_pressed.connect(self.handle_button_press)

    @pyqtSlot()
    def handle_button_press(self):
        """Handle patient button press events"""
        if self._gpio_thread:
            self._gpio_thread.disable()
        
        time.sleep(0.15)

        if self._skip_event:
            self._handle_trial_start()
        else:
            self._handle_trial_response()

        # Re-enable button if not completed all trials
        if self._response_count < CFFConfig.TRIALS_COUNT:
            if self._skip_event:
                time.sleep(0.2)
                globaladc.buzzer_3()
            if self._gpio_thread:
                self._gpio_thread.enable()

    def _handle_trial_start(self):
        """Handle the start of a new trial"""
        self.patient_action.hide()
        self._thread_created = True
        
        start_freq = (CFFConfig.INITIAL_FREQUENCY if self._response_count == 0 
                     else self._trial_manager.min_amplitude + CFFConfig.FREQUENCY_INCREMENT)
        
        self._current_frequency = start_freq
        self._ensure_flicker_state()
        
        if self._freq_thread is None:
            self._setup_frequency_thread(start_freq)
        
        self._freq_thread.set_skip_event(False)
        self._skip_event = False
        time.sleep(0.2)

    def _handle_trial_response(self):
        """Handle the patient's response during a trial"""
        self._skip_event = True
        time.sleep(0.5)

        if self._thread_created and self._freq_thread:
            self._freq_thread.set_skip_event(True)
            self._record_trial_result()

    def _setup_frequency_thread(self, start_freq):
        """Setup the frequency update thread"""
        self._freq_thread = FrequencyWorker(start_freq, globaladc.get_cff_delay())
        self._freq_thread.frequency_updated.connect(self.update_frequency)
        self._freq_thread.trial_timeout.connect(self.handle_timeout)
        self._freq_thread.start()

    def _record_trial_result(self):
        """Record and process trial results"""
        self.trial_list.addItem(f"{self._current_frequency:.1f}")
        self._trial_manager.record_response(self._current_frequency)
        self.min_label.setText(f"{self._trial_manager.min_amplitude:.1f}")
        
        self._response_count += 1
        
        if self._response_count == CFFConfig.TRIALS_COUNT:
            self._complete_trial_set()
        
        self.freq_label.setText(f"{self._current_frequency:.1f}")

    def _complete_trial_set(self):
        """Handle completion of all trials"""
        self.max_label.setText(f"{self._trial_manager.max_amplitude:.1f}")
        avg_val = globaladc.get_cff_f_avg_cal()
        
        if self._freq_thread:
            self._freq_thread.stop()
            self._freq_thread = None
        
        time.sleep(1)
        globaladc.buzzer_3()
        
        if self._gpio_thread:
            self._gpio_thread.disable()
        
        self.hide()

    @pyqtSlot(float)
    def update_frequency(self, new_freq):
        """Update displayed frequency and hardware state"""
        self._current_frequency = new_freq
        self.freq_label.setText(f"{new_freq:.1f}")
        globaladc.put_cff_fovea_frq(new_freq)

    @pyqtSlot()
    def handle_timeout(self):
        """Handle trial timeout"""
        if self._freq_thread:
            self._freq_thread.stop()
            self._freq_thread = None
        self.freq_label.setText(f"{CFFConfig.INITIAL_FREQUENCY:.1f}")

    def reset(self):
        """Reset window state for new test"""
        self._trial_manager.reset()
        self._current_frequency = CFFConfig.INITIAL_FREQUENCY
        self._response_count = 0
        self._skip_event = True
        self._thread_created = False
        
        self.min_label.setText("    ")
        self.max_label.setText("    ")
        self.freq_label.setText("    ")
        self.trial_list.clear()
        self.patient_action.show()

    def showEvent(self, event):
        """Handle window show event"""
        super().showEvent(event)
        self.reset()
        self._initialize_hardware()
        if self._gpio_thread:
            self._gpio_thread.start()

    def hideEvent(self, event):
        """Handle window hide event"""
        super().hideEvent(event)
        if self._freq_thread:
            self._freq_thread.stop()
            self._freq_thread = None
        if self._gpio_thread:
            self._gpio_thread.stop()

    def on_back(self):
        """Handle back button press"""
        self.hide()

    def on_next(self):
        """Handle next button press"""
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CFFWindow()
    window.show()
    sys.exit(app.exec_())