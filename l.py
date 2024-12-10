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

class CFFWindow(QMainWindow):
    # ... other methods remain the same ...

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